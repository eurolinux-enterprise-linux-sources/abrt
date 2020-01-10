/*
    Copyright (C) 2010  Red Hat, Inc.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/
#include <syslog.h>
#include "https-utils.h"

#define MAX_FORMATS 16
#define MAX_RELEASES 32

enum
{
    TASK_RETRACE,
    TASK_DEBUG,
    TASK_VMCORE,
};

struct retrace_settings
{
    int running_tasks;
    int max_running_tasks;
    long long max_packed_size;
    long long max_unpacked_size;
    char *supported_formats[MAX_FORMATS];
    char *supported_releases[MAX_RELEASES];
};

static const char *dump_dir_name = NULL;
static const char *coredump = NULL;
static const char *required_retrace[] = { FILENAME_COREDUMP,
                                          FILENAME_EXECUTABLE,
                                          FILENAME_PACKAGE,
                                          FILENAME_OS_RELEASE,
                                          NULL };
static const char *required_vmcore[] = { FILENAME_VMCORE,
                                         NULL };
static unsigned delay = 0;
static int task_type = TASK_RETRACE;
static bool http_show_headers;

static struct https_cfg cfg =
{
    .url = "retrace.fedoraproject.org",
    .port = 443,
    .ssl_allow_insecure = false,
};

static void alert_crash_too_large()
{
    alert(_("Retrace server can not be used, because the crash "
            "is too large. Try local retracing."));
}

/* Add an entry name to the args array if the entry name exists in a
 * problem directory. The entry is added to argindex offset to the array,
 * and the argindex is then increased.
 */
static void args_add_if_exists(const char *args[],
                               struct dump_dir *dd,
                               const char *name,
                               int *argindex)
{
    if (dd_exist(dd, name))
    {
        args[*argindex] = name;
        *argindex += 1;
    }
}

/* Create an archive with files required for retrace server and return
 * a file descriptor. Returns -1 if it fails.
 */
static int create_archive(bool unlink_temp)
{
    struct dump_dir *dd = dd_opendir(dump_dir_name, /*flags:*/ 0);
    if (!dd)
        return -1;

    /* Open a temporary file. */
    char *filename = xstrdup("/tmp/abrt-retrace-client-archive-XXXXXX.tar.xz");
    int tempfd = mkstemps(filename, /*suffixlen:*/7);
    if (tempfd == -1)
        perror_msg_and_die(_("Cannot open temporary file"));
    if (unlink_temp)
        xunlink(filename);
    free(filename);

    /* Run xz:
     * - xz reads input from a pipe
     * - xz writes output to the temporary file.
     */
    const char *xz_args[4];
    xz_args[0] = "xz";
    xz_args[1] = "-2";
    xz_args[2] = "-";
    xz_args[3] = NULL;

    int tar_xz_pipe[2];
    xpipe(tar_xz_pipe);
    pid_t xz_child = vfork();
    if (xz_child == -1)
        perror_msg_and_die("vfork");
    if (xz_child == 0)
    {
        close(tar_xz_pipe[1]);
        xmove_fd(tar_xz_pipe[0], STDIN_FILENO);
        xdup2(tempfd, STDOUT_FILENO);
        execvp(xz_args[0], (char * const*)xz_args);
        perror_msg_and_die(_("Can't execute '%s'"), xz_args[0]);
    }

    close(tar_xz_pipe[0]);

    /* Run tar, and set output to a pipe with xz waiting on the other
     * end.
     */
    const char *tar_args[10];
    tar_args[0] = "tar";
    tar_args[1] = "cO";
    tar_args[2] = xasprintf("--directory=%s", dump_dir_name);

    const char **required_files = task_type == TASK_VMCORE ? required_vmcore : required_retrace;
    int index = 3;
    while (required_files[index - 3])
        args_add_if_exists(tar_args, dd, required_files[index - 3], &index);

    tar_args[index] = NULL;
    dd_close(dd);

    pid_t tar_child = vfork();
    if (tar_child == -1)
        perror_msg_and_die("vfork");
    if (tar_child == 0)
    {
        xmove_fd(xopen("/dev/null", O_RDWR), STDIN_FILENO);
        xmove_fd(tar_xz_pipe[1], STDOUT_FILENO);
        execvp(tar_args[0], (char * const*)tar_args);
        perror_msg_and_die(_("Can't execute '%s'"), tar_args[0]);
    }

    free((void*)tar_args[2]);
    close(tar_xz_pipe[1]);

    /* Wait for tar and xz to finish */
    VERB1 log_msg("Waiting for tar...");
    safe_waitpid(tar_child, NULL, 0);
    VERB1 log_msg("Waiting for xz...");
    safe_waitpid(xz_child, NULL, 0);
//FIXME: need to check that both exited with 0! Think about out-of-disk-space situation...
    VERB1 log_msg("Done...");
    xlseek(tempfd, 0, SEEK_SET);
    return tempfd;
}

struct retrace_settings *get_settings()
{
    struct retrace_settings *settings = xzalloc(sizeof(struct retrace_settings));

    PRFileDesc *tcp_sock, *ssl_sock;
    ssl_connect(&cfg, &tcp_sock, &ssl_sock);
    struct strbuf *http_request = strbuf_new();
    strbuf_append_strf(http_request,
                       "GET /settings HTTP/1.1\r\n"
                       "Host: %s\r\n"
                       "Content-Length: 0\r\n"
                       "Connection: close\r\n"
                       "\r\n", cfg.url);
    PRInt32 written = PR_Send(tcp_sock, http_request->buf, http_request->len,
                              /*flags:*/0, PR_INTERVAL_NO_TIMEOUT);
    if (written == -1)
    {
        PR_Close(ssl_sock);
        alert_connection_error();
        error_msg_and_die(_("Failed to send HTTP header of length %d: NSS error %d."),
                          http_request->len, PR_GetError());
    }
    strbuf_free(http_request);

    char *http_response = tcp_read_response(tcp_sock);
    if (http_show_headers)
        http_print_headers(stderr, http_response);
    int response_code = http_get_response_code(http_response);
    if (response_code != 200)
    {
        alert_server_error();
        error_msg_and_die(_("Unexpected HTTP response from server: %d\n%s"),
                          response_code, http_response);
    }

    char *headers_end = strstr(http_response, "\r\n\r\n");
    char *c, *row, *value;
    if (!headers_end)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing HTTP message body."));
    }
    row = headers_end + strlen("\r\n\r\n");

    do
    {
        /* split rows */
        c = strchr(row, '\n');
        if (c)
            *c = '\0';

        /* split key and values */
        value = strchr(row, ' ');
        if (!value)
        {
            row = c + 1;
            continue;
        }

        *value = '\0';
        ++value;

        if (0 == strcasecmp("running_tasks", row))
            settings->running_tasks = atoi(value);
        else if (0 == strcasecmp("max_running_tasks", row))
            settings->max_running_tasks = atoi(value);
        else if (0 == strcasecmp("max_packed_size", row))
            settings->max_packed_size = atoi(value) * 1024 * 1024;
        else if (0 == strcasecmp("max_unpacked_size", row))
            settings->max_unpacked_size = atoi(value) * 1024 * 1024;
        else if (0 == strcasecmp("supported_formats", row))
        {
            char *space;
            int i;
            for (i = 0; i < MAX_FORMATS - 1 && (space = strchr(value, ' ')); ++i)
            {
                *space = '\0';
                settings->supported_formats[i] = xstrdup(value);
                value = space + 1;
            }

            /* last element */
            settings->supported_formats[i] = xstrdup(value);
        }
        else if (0 == strcasecmp("supported_releases", row))
        {
            char *space;
            int i;
            for (i = 0; i < MAX_RELEASES - 1 && (space = strchr(value, ' ')); ++i)
            {
                *space = '\0';
                settings->supported_releases[i] = xstrdup(value);
                value = space + 1;
            }

            /* last element */
            settings->supported_releases[i] = xstrdup(value);
        }

        /* the beginning of the next row */
        row = c + 1;
    } while (c);

    free(http_response);
    ssl_disconnect(ssl_sock);

    return settings;
}

static void free_settings(struct retrace_settings *settings)
{
    if (!settings)
        return;

    int i;
    for (i = 0; i < MAX_FORMATS; ++i)
        free(settings->supported_formats[i]);

    for (i = 0; i < MAX_RELEASES; ++i)
        free(settings->supported_releases[i]);

    free(settings);
}

/* returns release identifier as dist-ver-arch */
/* or NULL if unknown */
static char *get_release(const char *dump_dir_name)
{
    char *filename;
    FILE *f;

    filename = concat_path_file(dump_dir_name, FILENAME_ARCHITECTURE);
    f = fopen(filename, "r");
    free(filename);
    if (!f)
        perror_msg_and_die("fopen");

    char *arch = xmalloc_fgetline(f);
    fclose(f);

    if (strcmp("i686", arch) == 0 || strcmp("i586", arch) == 0)
    {
        free(arch);
        arch = xstrdup("i386");
    }

    filename = concat_path_file(dump_dir_name, FILENAME_OS_RELEASE);
    f = fopen(filename, "r");
    free(filename);
    if (!f)
        perror_msg_and_die("fopen");

    char *line = xmalloc_fgetline(f);
    fclose(f);

    char *release = NULL, *version = NULL, *result = NULL;
    parse_release_for_rhts(line, &release, &version);

    if (strcmp("Fedora", release) == 0)
        result = xasprintf("fedora-%s-%s", version, arch);
    else if (strcmp("Red Hat Enterprise Linux", release) == 0)
        result = xasprintf("rhel-%s-%s", version, arch);

    free(release);
    free(version);
    free(line);
    free(arch);
    return result;
}

static int create(bool delete_temp_archive,
                  char **task_id,
                  char **task_password)
{
    struct language lang;
    get_language(&lang);

    if (delay)
    {
        puts(_("Querying server settings"));
        fflush(stdout);
    }

    struct retrace_settings *settings = get_settings();

    if (settings->running_tasks >= settings->max_running_tasks)
    {
        alert(_("The server is fully occupied. Try again later."));
        error_msg_and_die(_("The server denied your request."));
    }

    long long unpacked_size = 0;
    struct stat file_stat;

    /* get raw size */
    if (coredump)
    {
        if (stat(coredump, &file_stat) == -1)
            error_msg_and_die(_("Unable to stat file '%s'."), coredump);

        unpacked_size = (long long)file_stat.st_size;
    }
    else if (dump_dir_name != NULL)
    {
        struct dump_dir *dd = dd_opendir(dump_dir_name, /*flags*/ 0);
        if (!dd)
            error_msg_and_die(_("Unable to open dump directory '%s'."), dump_dir_name);

        if (dd_exist(dd, FILENAME_VMCORE))
            task_type = TASK_VMCORE;

        dd_close(dd);

        char *path;
        int i = 0;
        const char **required_files = task_type == TASK_VMCORE ? required_vmcore : required_retrace;
        while (required_files[i])
        {
            path = concat_path_file(dump_dir_name, required_files[i]);
            if (stat(path, &file_stat) == -1)
            {
                error_msg(_("Unable to stat file '%s'."), path);
                free(path);
                xfunc_die();
            }

            unpacked_size += (long long)file_stat.st_size;
            free(path);

            ++i;
        }
    }

    if (unpacked_size > settings->max_unpacked_size)
    {
        alert_crash_too_large();
        error_msg_and_die(_("The size of your crash is %lld bytes, "
                            "but the retrace server only accepts "
                            "crashes smaller or equal to %lld bytes."),
                          unpacked_size, settings->max_unpacked_size);
    }

    if (settings->supported_formats)
    {
        int i;
        bool supported = false;
        for (i = 0; i < MAX_FORMATS && settings->supported_formats[i]; ++i)
            if (strcmp("application/x-xz-compressed-tar", settings->supported_formats[i]) == 0)
            {
                supported = true;
                break;
            }

        if (!supported)
        {
            alert_server_error();
            error_msg_and_die(_("The server does not support "
                                "xz-compressed tarballs."));
        }
    }

    /* we need dump dir to parse release file */
    /* not needed for TASK_VMCORE - the information is kept in the vmcore itself */
    if (task_type != TASK_VMCORE && dump_dir_name && settings->supported_releases)
    {
        char *release = get_release(dump_dir_name);
        if (!release)
            error_msg_and_die("Unable to parse release.");
        int i;
        bool supported = false;
        for (i = 0; i < MAX_RELEASES && settings->supported_releases[i]; ++i)
            if (strcmp(release, settings->supported_releases[i]) == 0)
            {
                supported = true;
                break;
            }

        if (!supported)
        {
            char *msg = xasprintf(_("The release '%s' is not supported by the"
                                    " Retrace server."), release);
            alert(msg);
            free(msg);
            error_msg_and_die(_("The server is not able to"
                                " handle your request."));
        }

        free(release);
    }

    if (delay)
    {
        puts(_("Preparing an archive to upload"));
        fflush(stdout);
    }

    int tempfd = create_archive(delete_temp_archive);
    if (-1 == tempfd)
        return 1;

    /* Get the file size. */
    fstat(tempfd, &file_stat);
    if ((long long)file_stat.st_size > settings->max_packed_size)
    {
        alert_crash_too_large();
        error_msg_and_die(_("The size of your archive is %lld bytes, "
                            "but the retrace server only accepts "
                            "archives smaller or equal %lld bytes."),
                          (long long)file_stat.st_size,
                          settings->max_packed_size);
    }

    free_settings(settings);

    int size_mb = file_stat.st_size / (1024 * 1024);

    if (size_mb > 8) /* 8 MB - should be configurable */
    {
        char *question = xasprintf(_("You are going to upload %d megabytes."
                                     "Continue?"), size_mb);

        int response = ask_yes_no(question);
        free(question);

        if (!response)
            error_msg_and_die(_("Cancelled by user"));
    }

    PRFileDesc *tcp_sock, *ssl_sock;
    ssl_connect(&cfg, &tcp_sock, &ssl_sock);
    /* Upload the archive. */
    struct strbuf *http_request = strbuf_new();
    strbuf_append_strf(http_request,
                       "POST /create HTTP/1.1\r\n"
                       "Host: %s\r\n"
                       "Content-Type: application/x-xz-compressed-tar\r\n"
                       "Content-Length: %lld\r\n"
                       "Connection: close\r\n"
                       "X-Task-Type: %d\r\n",
                       cfg.url, (long long)file_stat.st_size, task_type);

    if (lang.encoding)
        strbuf_append_strf(http_request,
                           "Accept-Charset: %s\r\n",
                           lang.encoding);
    if (lang.locale)
    {
        strbuf_append_strf(http_request,
                           "Accept-Language: %s\r\n",
                           lang.locale);
        free(lang.locale);
    }

    strbuf_append_str(http_request, "\r\n");

    PRInt32 written = PR_Send(tcp_sock, http_request->buf, http_request->len,
                              /*flags:*/0, PR_INTERVAL_NO_TIMEOUT);
    if (written == -1)
    {
        PR_Close(ssl_sock);
        alert_connection_error();
        error_msg_and_die(_("Failed to send HTTP header of length %d: NSS error %d."),
                          http_request->len, PR_GetError());
    }

    if (delay)
    {
        if (size_mb > 1)
            printf(_("Uploading %d megabytes\n"), size_mb);
        else
            printf(_("Uploading %lld bytes\n"), (long long)file_stat.st_size);
        fflush(stdout);
    }

    strbuf_free(http_request);
    int result = 0;
    int i;
    char buf[32768];

    time_t start, now;
    time(&start);

    for (i = 0;; ++i)
    {
        if (delay)
        {
            time(&now);
            if (now - start >= delay)
            {
                time(&start);
                int progress = 100 * i * sizeof(buf) / file_stat.st_size;
                if (progress > 100)
                    continue;

                printf(_("Uploading %d%%\n"), progress);
                fflush(stdout);
            }
        }

        int r = read(tempfd, buf, sizeof(buf));
        if (r <= 0)
        {
            if (r == -1)
            {
                if (EINTR == errno || EAGAIN == errno || EWOULDBLOCK == errno)
                    continue;
                perror_msg_and_die(_("Failed to read from a pipe"));
            }
            break;
        }
        written = PR_Send(tcp_sock, buf, r,
                          /*flags:*/0, PR_INTERVAL_NO_TIMEOUT);
        if (written == -1)
        {
            /* Print error message, but do not exit.  We need to check
               if the server send some explanation regarding the
               error. */
            result = 1;
            alert_connection_error();
            error_msg(_("Failed to send data: NSS error %d (%s): %s"),
                      PR_GetError(),
                      PR_ErrorToName(PR_GetError()),
                      PR_ErrorToString(PR_GetError(), PR_LANGUAGE_I_DEFAULT));
            break;
        }
    }
    close(tempfd);

    if (delay)
    {
        puts(_("Upload successful"));
        fflush(stdout);
    }

    /* Read the HTTP header of the response from server. */
    char *http_response = tcp_read_response(tcp_sock);
    char *http_body = http_get_body(http_response);
    if (!http_body)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing HTTP message body."));
    }
    if (http_show_headers)
        http_print_headers(stderr, http_response);
    int response_code = http_get_response_code(http_response);
    if (response_code == 500 || response_code == 507)
    {
        alert_server_error();
        error_msg_and_die(http_body);
    }
    else if (response_code == 403)
    {
        alert(_("Your problem directory is corrupted and can not "
                "be processed by the Retrace server."));
        error_msg_and_die(_("The archive contains malicious files (such as symlinks) "
                            "and thus can not be processed."));
    }
    else if (response_code != 201)
    {
        alert_server_error();
        error_msg_and_die(_("Unexpected HTTP response from server: %d\n%s"), response_code, http_body);
    }
    free(http_body);
    *task_id = http_get_header_value(http_response, "X-Task-Id");
    if (!*task_id)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing X-Task-Id."));
    }
    *task_password = http_get_header_value(http_response, "X-Task-Password");
    if (!*task_password)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing X-Task-Password."));
    }
    free(http_response);
    ssl_disconnect(ssl_sock);

    if (delay)
    {
        puts(_("Retrace job started"));
        fflush(stdout);
    }

    return result;
}

static int run_create(bool delete_temp_archive)
{
    char *task_id, *task_password;
    int result = create(delete_temp_archive, &task_id, &task_password);
    if (0 != result)
        return result;
    printf(_("Task Id: %s\nTask Password: %s\n"), task_id, task_password);
    free(task_id);
    free(task_password);
    return 0;
}

/* Caller must free task_status and status_message */
static void status(const char *task_id,
                   const char *task_password,
                   char **task_status,
                   char **status_message)
{
    struct language lang;
    get_language(&lang);

    PRFileDesc *tcp_sock, *ssl_sock;
    ssl_connect(&cfg, &tcp_sock, &ssl_sock);
    struct strbuf *http_request = strbuf_new();
    strbuf_append_strf(http_request,
                       "GET /%s HTTP/1.1\r\n"
                       "Host: %s\r\n"
                       "X-Task-Password: %s\r\n"
                       "Content-Length: 0\r\n"
                       "Connection: close\r\n",
                       task_id, cfg.url, task_password);

    if (lang.encoding)
        strbuf_append_strf(http_request,
                           "Accept-Charset: %s\r\n",
                           lang.encoding);
    if (lang.locale)
    {
        strbuf_append_strf(http_request,
                           "Accept-Language: %s\r\n",
                           lang.locale);
        free(lang.locale);
    }

    strbuf_append_str(http_request, "\r\n");

    PRInt32 written = PR_Send(tcp_sock, http_request->buf, http_request->len,
                              /*flags:*/0, PR_INTERVAL_NO_TIMEOUT);
    if (written == -1)
    {
        PR_Close(ssl_sock);
        alert_connection_error();
        error_msg_and_die(_("Failed to send HTTP header of length %d: NSS error %d"),
                          http_request->len, PR_GetError());
    }
    strbuf_free(http_request);
    char *http_response = tcp_read_response(tcp_sock);
    char *http_body = http_get_body(http_response);
    if (!*http_body)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing HTTP message body."));
    }
    if (http_show_headers)
        http_print_headers(stderr, http_response);
    int response_code = http_get_response_code(http_response);
    if (response_code != 200)
    {
        alert_server_error();
        error_msg_and_die(_("Unexpected HTTP response from server: %d\n%s"),
                          response_code, http_body);
    }
    *task_status = http_get_header_value(http_response, "X-Task-Status");
    if (!*task_status)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing X-Task-Status."));
    }
    *status_message = http_body;
    free(http_response);
    ssl_disconnect(ssl_sock);
}

static void run_status(const char *task_id, const char *task_password)
{
    char *task_status;
    char *status_message;
    status(task_id, task_password, &task_status, &status_message);
    printf(_("Task Status: %s\n%s\n"), task_status, status_message);
    free(task_status);
    free(status_message);
}

/* Caller must free backtrace */
static void backtrace(const char *task_id, const char *task_password,
                      char **backtrace)
{
    struct language lang;
    get_language(&lang);

    PRFileDesc *tcp_sock, *ssl_sock;
    ssl_connect(&cfg, &tcp_sock, &ssl_sock);
    struct strbuf *http_request = strbuf_new();
    strbuf_append_strf(http_request,
                       "GET /%s/backtrace HTTP/1.1\r\n"
                       "Host: %s\r\n"
                       "X-Task-Password: %s\r\n"
                       "Content-Length: 0\r\n"
                       "Connection: close\r\n",
                       task_id, cfg.url, task_password);

    if (lang.encoding)
        strbuf_append_strf(http_request,
                           "Accept-Charset: %s\r\n",
                           lang.encoding);
    if (lang.locale)
    {
        strbuf_append_strf(http_request,
                           "Accept-Language: %s\r\n",
                           lang.locale);
        free(lang.locale);
    }

    strbuf_append_str(http_request, "\r\n");

    PRInt32 written = PR_Send(tcp_sock, http_request->buf, http_request->len,
                              /*flags:*/0, PR_INTERVAL_NO_TIMEOUT);
    if (written == -1)
    {
        PR_Close(ssl_sock);
        alert_connection_error();
        error_msg_and_die(_("Failed to send HTTP header of length %d: NSS error %d."),
                          http_request->len, PR_GetError());
    }
    strbuf_free(http_request);
    char *http_response = tcp_read_response(tcp_sock);
    char *http_body = http_get_body(http_response);
    if (!http_body)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing HTTP message body."));
    }
    if (http_show_headers)
        http_print_headers(stderr, http_response);
    int response_code = http_get_response_code(http_response);
    if (response_code != 200)
    {
        alert_server_error();
        error_msg_and_die(_("Unexpected HTTP response from server: %d\n%s"),
                          response_code, http_body);
    }
    *backtrace = http_body;
    free(http_response);
    ssl_disconnect(ssl_sock);
}

static void run_backtrace(const char *task_id, const char *task_password)
{
    char *backtrace_text;
    backtrace(task_id, task_password, &backtrace_text);
    printf("%s", backtrace_text);
    free(backtrace_text);
}

static void run_log(const char *task_id, const char *task_password)
{
    struct language lang;
    get_language(&lang);

    PRFileDesc *tcp_sock, *ssl_sock;
    ssl_connect(&cfg, &tcp_sock, &ssl_sock);
    struct strbuf *http_request = strbuf_new();
    strbuf_append_strf(http_request,
                       "GET /%s/log HTTP/1.1\r\n"
                       "Host: %s\r\n"
                       "X-Task-Password: %s\r\n"
                       "Content-Length: 0\r\n"
                       "Connection: close\r\n",
                       task_id, cfg.url, task_password);

    if (lang.encoding)
        strbuf_append_strf(http_request,
                           "Accept-Charset: %s\r\n",
                           lang.encoding);
    if (lang.locale)
    {
        strbuf_append_strf(http_request,
                           "Accept-Language: %s\r\n",
                           lang.locale);
        free(lang.locale);
    }

    strbuf_append_str(http_request, "\r\n");

    PRInt32 written = PR_Send(tcp_sock, http_request->buf, http_request->len,
                              /*flags:*/0, PR_INTERVAL_NO_TIMEOUT);
    if (written == -1)
    {
        PR_Close(ssl_sock);
        alert_connection_error();
        error_msg_and_die(_("Failed to send HTTP header of length %d: NSS error %d."),
                          http_request->len, PR_GetError());
    }
    strbuf_free(http_request);
    char *http_response = tcp_read_response(tcp_sock);
    char *http_body = http_get_body(http_response);
    if (!http_body)
    {
        alert_server_error();
        error_msg_and_die(_("Invalid response from server: missing HTTP message body."));
    }
    if (http_show_headers)
        http_print_headers(stderr, http_response);
    int response_code = http_get_response_code(http_response);
    if (response_code != 200)
    {
        alert_server_error();
        error_msg_and_die(_("Unexpected HTTP response from server: %d\n%s"),
                          response_code, http_body);
    }
    puts(http_body);
    free(http_body);
    free(http_response);
    ssl_disconnect(ssl_sock);
}

static int run_batch(bool delete_temp_archive)
{
    char *task_id, *task_password;
    int retcode = create(delete_temp_archive, &task_id, &task_password);
    if (0 != retcode)
        return retcode;
    char *task_status = xstrdup("");
    char *status_message = xstrdup("");
    int status_delay = delay ? delay : 10;
    while (0 != strncmp(task_status, "FINISHED", strlen("finished")))
    {
        free(task_status);
        free(status_message);
        sleep(status_delay);
        status(task_id, task_password, &task_status, &status_message);
        puts(status_message);
        fflush(stdout);
    }
    if (0 == strcmp(task_status, "FINISHED_SUCCESS"))
    {
        char *backtrace_text;
        backtrace(task_id, task_password, &backtrace_text);
        if (dump_dir_name)
        {
            /* the result of TASK_VMCORE is not backtrace, but kernel log */
            char *backtrace_path = xasprintf("%s/%s", dump_dir_name,
                                             task_type == TASK_VMCORE ? FILENAME_KERNEL_LOG : FILENAME_BACKTRACE);
            int backtrace_fd = xopen3(backtrace_path, O_WRONLY | O_CREAT | O_TRUNC, 0640);
            xwrite(backtrace_fd, backtrace_text, strlen(backtrace_text));
            close(backtrace_fd);
            free(backtrace_path);
        }
        else
            printf("%s", backtrace_text);
        free(backtrace_text);
    }
    else
    {
        alert(_("Retrace failed. Try again later and if the problem persists "
                "report this issue please."));
        run_log(task_id, task_password);
        retcode = 1;
    }
    free(task_status);
    free(status_message);
    free(task_id);
    free(task_password);
    return retcode;
}

int main(int argc, char **argv)
{
    setlocale(LC_ALL, "");
#if ENABLE_NLS
    bindtextdomain(PACKAGE, LOCALEDIR);
    textdomain(PACKAGE);
#endif

    abrt_init(argv);

    const char *task_id = NULL;
    const char *task_password = NULL;

    enum {
        OPT_verbose   = 1 << 0,
        OPT_syslog    = 1 << 1,
        OPT_insecure  = 1 << 2,
        OPT_url       = 1 << 3,
        OPT_port      = 1 << 4,
        OPT_headers   = 1 << 5,
        OPT_group_1   = 1 << 6,
        OPT_dir       = 1 << 7,
        OPT_core      = 1 << 8,
        OPT_delay     = 1 << 9,
        OPT_no_unlink = 1 << 10,
        OPT_group_2   = 1 << 11,
        OPT_task      = 1 << 12,
        OPT_password  = 1 << 13
    };

    /* Keep enum above and order of options below in sync! */
    struct options options[] = {
        OPT__VERBOSE(&g_verbose),
        OPT_BOOL('s', "syslog", NULL, _("log to syslog")),
        OPT_BOOL('k', "insecure", NULL,
                 _("allow insecure connection to retrace server")),
        OPT_STRING(0, "url", &(cfg.url), "URL",
                   _("retrace server URL")),
        OPT_INTEGER(0, "port", &(cfg.port),
                    _("retrace server port")),
        OPT_BOOL(0, "headers", NULL,
                 _("(debug) show received HTTP headers")),
        OPT_GROUP(_("For create and batch operations")),
        OPT_STRING('d', "dir", &dump_dir_name, "DIR",
                   _("read data from ABRT problem directory")),
        OPT_STRING('c', "core", &coredump, "COREDUMP",
                   _("read data from coredump")),
        OPT_INTEGER('l', "status-delay", &delay,
                    _("Delay for polling operations")),
        OPT_BOOL(0, "no-unlink", NULL,
                 _("(debug) do not delete temporary archive created"
                   " from dump dir in /tmp")),
        OPT_GROUP(_("For status, backtrace, and log operations")),
        OPT_STRING('t', "task", &task_id, "ID",
                   _("id of your task on server")),
        OPT_STRING('p', "password", &task_password, "PWD",
                   _("password of your task on server")),
        OPT_END()
    };

    const char *usage = _("abrt-retrace-client <operation> [options]\n"
        "Operations: create/status/backtrace/log/batch");

    char *env_url = getenv("RETRACE_SERVER_URL");
    if (env_url)
        cfg.url = env_url;

    char *env_port = getenv("RETRACE_SERVER_PORT");
    if (env_port)
        cfg.port = xatou(env_port);

    char *env_delay = getenv("ABRT_STATUS_DELAY");
    if (env_delay)
        delay = xatou(env_delay);

    char *env_insecure = getenv("RETRACE_SERVER_INSECURE");
    if (env_insecure)
        cfg.ssl_allow_insecure = strncmp(env_insecure, "insecure", strlen("insecure")) == 0;

    unsigned opts = parse_opts(argc, argv, options, usage);
    if (opts & OPT_syslog)
    {
        openlog(msg_prefix, 0, LOG_DAEMON);
        logmode = LOGMODE_SYSLOG;
    }
    const char *operation = NULL;
    if (optind < argc)
        operation = argv[optind];
    else
        show_usage_and_die(usage, options);

    if (!cfg.ssl_allow_insecure)
        cfg.ssl_allow_insecure = opts & OPT_insecure;
    http_show_headers = opts & OPT_headers;

    /* Initialize NSS */
    SECMODModule *mod;
    PK11GenericObject *cert;
    nss_init(&mod, &cert);

    /* Run the desired operation. */
    int result = 0;
    if (0 == strcasecmp(operation, "create"))
    {
        if (!dump_dir_name && !coredump)
            error_msg_and_die(_("Either problem directory or coredump is needed."));
        result = run_create(0 == (opts & OPT_no_unlink));
    }
    else if (0 == strcasecmp(operation, "batch"))
    {
        if (!dump_dir_name && !coredump)
            error_msg_and_die(_("Either problem directory or coredump is needed."));
        result = run_batch(0 == (opts & OPT_no_unlink));
    }
    else if (0 == strcasecmp(operation, "status"))
    {
        if (!task_id)
            error_msg_and_die(_("Task id is needed."));
        if (!task_password)
            error_msg_and_die(_("Task password is needed."));
        run_status(task_id, task_password);
    }
    else if (0 == strcasecmp(operation, "backtrace"))
    {
        if (!task_id)
            error_msg_and_die(_("Task id is needed."));
        if (!task_password)
            error_msg_and_die(_("Task password is needed."));
        run_backtrace(task_id, task_password);
    }
    else if (0 == strcasecmp(operation, "log"))
    {
        if (!task_id)
            error_msg_and_die(_("Task id is needed."));
        if (!task_password)
            error_msg_and_die(_("Task password is needed."));
        run_log(task_id, task_password);
    }
    else
        error_msg_and_die(_("Unknown operation: %s."), operation);

    /* Shutdown NSS. */
    nss_close(mod, cert);

    return result;
}
