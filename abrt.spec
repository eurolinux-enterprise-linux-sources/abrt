%{!?python_site: %global python_site %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
# platform-dependent
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%bcond_with systemd

%if 0%{?rhel} >= 6
%define desktopvendor redhat
%else
%define desktopvendor fedora
%endif

# CAUTION:
# On RHEL-6.8 and later, please consider removing the migration script from
# %%post which removes the old dump directories (#1212868)

Summary: Automatic bug detection and reporting tool
Name: abrt
Version: 2.0.8
Release: 26.sl6.1
License: GPLv2+
Group: Applications/System
URL: https://fedorahosted.org/abrt/
Source: https://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.gz
Source1: abrt.init
Source2: abrt-ccpp.init
Source3: abrt-oops.init
Source4: abrt1_to_abrt2
Source5:	abrt.ini
Patch0: 0001-correct-check-for-enabled-abrtd-service.patch
Patch1: 0005-dump-oops-fix-removing-jiffies-time-stamp.patch
Patch2: 0006-use-the-suided-helper-for-installing-vmcore-debuginf.patch
Patch3: 0009-Spelling-fixes-in-doc.patch
Patch4: 0011-man-page-for-a-a-generate-core-backtrace.patch
Patch5: 0012-analyze-oops-fix-double-free.patch
Patch6: 0022-analyze-vmcore-added-d-option-to-specify-problem_dir.patch
Patch7: 0023-added-man-page-for-a-a-analyze-vmcore.patch
Patch8: 0024-doc-fixed-a-a-a-vmcore-man-pages.patch
Patch9: 0025-koops-unit-test-test-refactorization.patch
Patch10: 0026-minor-fixes-to-a-a-a-vmcore.patch
Patch11: 0027-vmcore-fixed-exception-in-error-path.patch
Patch12: 0029-koops-unit-test-rhbz-789526-write-unit-test-for-impr.patch
Patch13: 0030-koops-unit-test-bundle-test-koops-into-tarball.patch
Patch14: 0031-koops-unit-test-test-for-stripping-jiffies-from-kern.patch
Patch15: 0033-koops-unit-test-add-jiffies-test-file.patch
Patch16: 0057-updated-po-files.patch
Patch17: 0058-handle-event-fix-blaming-dump-dir-its-self-as-duplic.patch
Patch18: 0059-Fix-uploaded-crash-directory-being-marked-as-duplica.patch
Patch19: 0060-abrtd-fix-indetations.patch
Patch20: 0061-a-dump-oops-add-spaces-for-multiline-static-string-c.patch
Patch21: 0062-Don-t-download-debuginfo-for-pkgs-without-build-ids.patch
Patch22: 0063-koops-unit-test-add-test-for-short-oops.patch
Patch23: 0064-enable-dedup-client.patch
Patch24: 0067-mark-some-strings-in-the-event-xml-as-translatable-r.patch
Patch25: 0068-fixed-typo-in-previous-commit.patch
Patch26: 0070-oops-don-t-create-oops-dir-in-reverse-rhbz-814594.patch
Patch27: 0071-abrt-dump-oops-fix-SEGV-off-by-one-access-to-list-rh.patch
Patch28: 0073-Save-cgroup-information-for-crashing-process.patch
Patch29: 0074-a-a-analyze-core-check-the-len-if-the-line-array-bef.patch
Patch30: 0075-abrt-action-install-debuginfo-fix-a-problem-with-cle.patch
Patch31: 0077-trac-523-use-a-vmcore-from-the-current-directory-onl.patch
Patch32: 0078-minor-fix-to-install-ccpp-man-page.patch
Patch33: 0079-pyhook-add-timetout-to-sockets-rhbz-808562-rhbz-8373.patch
Patch34: 0080-applet-reverse-list-to-not-be-surprise-during-debugg.patch
Patch35: 0081-trac-527-add-check-for-locale.h-in-order-to-define-H.patch
Patch36: 0082-abrt-hook-ccpp-save-chrooted-etc-system-release-too-.patch
Patch37: 0085-use-rhel-gpg-keys.patch
Patch38: 0087-Make-abrt-ccpp-status-tell-user-whether-hook-is-curr.patch
Patch39: 0089-For-RHEL-commenting-out-all-reporter-events-for-all-.patch
Patch40: 0090-rhbz-839285-do-not-delete-an-uploaded-archive-by-def.patch
Patch41: 0091-blacklist-more-usual-suspects-which-are-usually-not-.patch
Patch42: 0092-disable-core-backtrace.patch
Patch43: 0093-disable-debuginfo-install.patch
Patch44: 0094-Make-ccpp_event.conf-comments-more-readable.-No-actu.patch
Patch45: 0095-automatically-send-email-when-a-new-crash-is-detecte.patch
Patch46: 0097-enable-sos-report-auto-collecting.patch
Patch47: 0099-use-rhel6-deployment-url-in-help.patch
Patch48: 0100-updated-translations.patch
Patch49: 0101-remove-report-problem-with-ABRT-button.patch
Patch50: 0102-remove-retrace-client.patch
Patch51: 0104-remove-smolt.patch
Patch52: 0107-abrt-harvest-vmcore-add-CopyVMcore-config-option-to-.patch
Patch53: 0109-applet-fix-a-SEGV-caused-by-notify_init-not-being-ca.patch
Patch54: 0110-abrt-install-ccpp-hook-fix-the-check-for-e-presense..patch
Patch55: 0111-minor-fix-to-pkg-config-file.patch
Patch56: 0112-hopefully-fixed-ugly-applet-icon-rhbz-797078.patch
Patch57: 0113-don-t-print-error-msg-if-dbus-send-is-missing-rhbz-8.patch
Patch58: 0114-added-relro-and-fpie-flags-for-a-a-install-debuginfo.patch
Patch59: 0116-updated-translation-rhbz-864023.patch
Patch60: 0117-abrtd-set-inotify-fd-to-non-blocking-mode-ignore-0-s.patch
Patch61: 0118-abrtd-don-t-mark-problems-having-count-1-as-duplicat.patch
Patch62: 0119-rhbz-852760-fix-loop-condition-in-generation-of-oops.patch
Patch63: 0120-abrt-action-analyze-oops-fail-if-we-end-up-hashing-e.patch
Patch64: 0121-Teach-kernel-oops-hash-to-ignore-IRQ-EOI-prefixes.-C.patch
Patch65: 0122-fixed-the-make-check-related-to-rhbz-864023.patch
Patch66: 0123-fixed-the-relro-flags-rhbz-812284.patch
Patch67: 0124-libabrt-link-with-libreport-rhbz-892658.patch
Patch68: 0125-abrt-action-install-debuginfo-to-abrt-cache-clear-en.patch
Patch69: 0126-abrt-server-do-not-save-the-repeating-crash-in-the-s.patch
Patch70: 0127-abrtd-allow-parallel-runs-of-post-create-events.patch
Patch71: 0128-abrtd-preparatory-patch.-Only-moves-blocks-of-code-a.patch
Patch72: 0129-abrtd-fix-a-problem-when-we-eat-post-create-exit-cod.patch
Patch73: 0130-abrtd-do-not-run-post-create-event-concurrently.patch
Patch74: 0131-multilib-fixes.patch
Patch75: 0132-abrtd-disable-glib-s-buffering-on-inotify-reads.-Clo.patch
Patch76: 0133-move-abrt.pth-to-arch-specific-location-rhbz-912672.patch
Patch77: 0135-abrt-harvest-vmcore-don-t-copy-dir-from-var-crash-if.patch
Patch78: 0136-Improve-log-messages-in-cccpp-hook-and-save-package-.patch
Patch79: 0137-abrtd-Remove-Corrupted-or-bad-directory-words-from-t.patch
Patch80: 0139-abrtd-prohibit-DumpLocation-WatchCrashdumpArchiveDir.patch
Patch81: 0140-abrt-gui-fix-broken-help-URL.-Closes-rhbz-903195.patch
Patch82: 0141-analyze-ccpp-don-t-suid-to-abrt-when-run-as-root-rel.patch
Patch83: 0143-added-option-to-bypass-di-install-closes-618.patch
Patch84: 0144-added-options-to-disable-bugzilla-and-bodhi-related-.patch
Patch85: 0145-disable-again-bugzilla-and-bodhi-related-to-rhbz-828.patch
Patch86: 0150-build-abrtd-and-setuided-executables-with-full-relro.patch
Patch87: 0152-created-problem_api-part-of-rhbz-961231.patch
Patch88: 0153-implemented-status-command-to-abrt-cli-rhbz-961231.patch
Patch89: 0154-added-a-console-notification-script-to-profile.d-rhb.patch
Patch90: 0156-abrtd-update-last-occurrence-dump-dir-file.patch
Patch91: 0157-abrt-python-initial.patch
Patch92: 0158-abrt-python-fix-each-test-to-run-standalone.patch
Patch93: 0159-abrt-python-rename-to-abrt-python.patch
Patch94: 0161-abrt-python-add-python-problem-tests-to-POTFILES.ski.patch
Patch95: 0162-abrt-python-cover-python-problem-by-autotools.patch
Patch96: 0164-abrt-python-add-python-nose-to-buildrequires.patch
Patch97: 0165-abrt-python-fix-tests-not-cleaning-after-themselves.patch
Patch98: 0166-abrt-python-add-test-executable.patch
Patch99: 0167-abrt-python-force-string-for-dbus-set-item.patch
Patch100: 0168-abrt-python-add-support-for-dump-dir-access.patch
Patch101: 0169-abrt-python-DeleteProblem-takes-list-of-problems.patch
Patch102: 0170-abrt-python-add-debugging-message-for-dbus-calls.patch
Patch103: 0171-abrt-python-add-new-problem-notification-support.patch
Patch104: 0172-abrt-python-add-missing-watch-examples.patch
Patch105: 0173-abrt-python-minor-test-updates.patch
Patch106: 0174-abrt-python-skip-non-accessible-directories.patch
Patch107: 0175-abrt-python-use-var-tmp-abrt-by-default.patch
Patch108: 0176-abrt-python-use-filesystem-proxy-as-a-fallback.patch
Patch109: 0177-abrt-python-fix-list_all-to-return-meaningful-result.patch
Patch110: 0178-abrt-python-add-DEFAULT_DUMP_LOCATION-to-config.patch
Patch111: 0179-abrt-python-add-missing-file.patch
Patch112: 0180-abrt-python-import-dbus-lazily.patch
Patch113: 0181-abrt-python-fix-makefiles.patch
Patch114: 0182-abrt-python-pep8-cleanup.patch
Patch115: 0183-abrt-python-fix-bug-in-problem.get.patch
Patch116: 0184-abrt-python-fix-deprecation-warnings.patch
Patch117: 0185-abrt-python-pass-DD_OPEN_READONLY-only-if-available.patch
Patch118: 0186-abrt-python-fix-tests-compatibility-with-python-2.6.patch
Patch119: 0187-abrt-python-check-if-gid-equals-current-users-gid.patch
Patch120: 0188-abrt-python-fix-dbus-compatibility-on-RHEL6.patch
Patch121: 0189-abrt-python-don-t-build-man-page-for-python-api.patch
Patch122: 0190-abrt-python-whole-python-API-path-in-POTFILES.skip.patch
Patch123: 0191-abrt-python-fix-DEFAULT_DUMP_LOCATION.patch
Patch124: 0192-fix-problem-occurrence-counter-updating-algorithm.patch
Patch125: 0193-use-last_occurrence-with-since.patch
Patch126: 0194-console-notification-shouldn-t-ask-confirmation-clos.patch
Patch127: 0197-abrt-python-open-dirs-read-only-if-possible.patch
Patch128: 0198-abrt-dump-oops-limit-amount-of-created-dirs-add-cool.patch
Patch129: 0201-updated-translation-rhbz-993564.patch
Patch130: 0202-updated-translation-rhbz-993564.patch
Patch131: 0203-abrt-dump-oops-add-Machine-Check-Exception-to-the-li.patch
Patch132: 0203-doc-update-OpenGPGCheck-in-a-a-save-package-data-rhb.patch
Patch133: 0205-fail-quietly-when-there-is-no-uid-file.patch
Patch134: 0206-abrt_event-fix-post-create-reporter-uploader-example.patch
Patch135: 0207-Fix-RPMdiff-warnings-about-abrtd-and-abrt-action-ins.patch
Patch136: 0208-add-man-page-for-abrt-harvest-vmcore.patch
Patch137: 0210-abrt_event-fix-post-create-reporter-uploader-example.patch
Patch138: 0211-koops-provide-general-hints-and-tips-for-useless-bac.patch
Patch139: 0213-koops-fix-a-use-after-free-bug-uncoverd-by-coverity.patch
# $ git format-patch 2.0.8-26.el6 -N --start-number 214 --topo-order
Patch140: 0214-a-a-save-package-data-turn-off-reading-data-from-roo.patch
Patch141: 0215-ccpp-fix-symlink-race-conditions.patch
Patch142: 0216-ccpp-do-not-read-data-from-root-directories.patch
Patch143: 0217-ccpp-open-file-for-dump_fd_info-with-O_EXCL.patch
Patch144: 0218-ccpp-postpone-changing-ownership-of-new-dump-directo.patch
Patch145: 0219-ccpp-create-dump-directory-without-parents.patch
Patch146: 0220-ccpp-do-not-override-existing-files-by-compat-cores.patch
Patch147: 0221-ccpp-do-not-use-value-of-proc-PID-cwd-for-chdir.patch
Patch148: 0222-ccpp-harden-dealing-with-UID-GID.patch
Patch149: 0223-ccpp-check-for-overflow-in-abrt-coredump-path-creati.patch
Patch150: 0224-ccpp-emulate-selinux-for-creation-of-compat-cores.patch
Patch151: 0225-make-the-dump-directories-owned-by-root-by-default.patch
Patch152: 0226-ccpp-avoid-overriding-system-files-by-coredump.patch
#Patch153: 0227-spec-add-libselinux-devel-to-BRs.patch
Patch154: 0228-lib-add-functions-validating-dump-dir.patch
Patch155: 0229-a-a-i-d-t-a-cache-sanitize-arguments.patch
Patch156: 0230-a-a-i-d-t-a-cache-sanitize-umask.patch
Patch157: 0231-ccpp-revert-the-UID-GID-changes-if-user-core-fails.patch
Patch158: 0232-upload-validate-and-sanitize-uploaded-dump-directori.patch
Patch159: 0233-lib-don-t-setuid-setgid-when-running-eu-unstrip.patch
Patch160: 0234-lib-avoid-race-conditions-while-going-trough-all-dum.patch
Patch161: 0235-daemon-harden-against-race-conditions-in-DELETE.patch
Patch162: 0236-daemon-dbus-allow-only-root-to-create-CCpp-Koops-vmc.patch
Patch163: 0237-cli-adapt-to-PrivateReports.patch
Patch164: 0238-gui-adapt-to-PrivateReports.patch
#Patch165: 0239-spec-add-abrt-consolehelper-applications.patch
#Patch166: 0240-spec-add-usermode-and-pam-to-Requires.patch
Patch167: 0241-ccpp-do-not-unlink-failed-and-big-user-cores.patch
Patch168: 0242-abrtd-do-not-log-new-client-connected.patch
Patch169:	abrt-add-sl-gpg-keys.patch

BuildRequires: dbus-devel
BuildRequires: gtk2-devel
BuildRequires: rpm-devel >= 4.6
BuildRequires: desktop-file-utils
BuildRequires: libnotify-devel
#why? BuildRequires: file-devel
BuildRequires: python-devel
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: nss-devel
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: libreport-devel >= 2.0.9-21.el6_6.1
BuildRequires: btparser-devel
BuildRequires: elfutils-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: binutils-devel
BuildRequires: libselinux-devel

Requires: libreport >= 2.0.9-21.el6_6.1

%if %{with systemd}
Requires: systemd-units
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{name}-libs = %{version}-%{release}
Requires: libreport-plugin-mailx
Requires(pre): shadow-utils
Obsoletes: abrt-plugin-sqlite3 > 0.0.1
# required for transition from 1.1.13, can be removed after some time
Obsoletes: abrt-plugin-runapp > 0.0.1
Obsoletes: abrt-plugin-filetransfer > 0.0.1
Obsoletes: abrt-plugin-sosreport > 0.0.1

%description
%{name} is a tool to help users to detect defects in applications and
to create a bug report with all informations needed by maintainer to fix it.
It uses plugin system to extend its functionality.

%package libs
Summary: Libraries for %{name}
Group: System Environment/Libraries

%description libs
Libraries for %{name}.

%package devel
Summary: Development libraries for %{name}
Group: Development/Libraries
Requires: abrt-libs = %{version}-%{release}

%description devel
Development libraries and headers for %{name}.

%package gui
Summary: %{name}'s gui
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}
Requires: pam
Requires: usermode-gtk
BuildRequires: libreport-gtk-devel
# we used to have abrt-applet, now abrt-gui includes it:
Provides: abrt-applet = %{version}-%{release}
Obsoletes: abrt-applet < 0.0.5
Conflicts: abrt-applet < 0.0.5

%description gui
GTK+ wizard for convenient bug reporting.

%package addon-ccpp
Summary: %{name}'s C/C++ addon
Group: System Environment/Libraries
Requires: elfutils, elfutils-libelf, elfutils-libs, cpio
# we don't install debuginfos on rhel, so requiring gdb is pointless
#Requires: gdb >= 7.0-3
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}

%description addon-ccpp
This package contains hook for C/C++ crashed programs and %{name}'s C/C++
analyzer plugin.

%package addon-vmcore
Summary: %{name}'s vmcore addon
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops

%description addon-vmcore
This package contains plugin for collecting kernel crash information from vmcore files.

%package addon-kerneloops
Summary: %{name}'s kerneloops addon
Group: System Environment/Libraries
Requires: curl
Requires: %{name} = %{version}-%{release}
Requires: abrt-libs = %{version}-%{release}
Requires: libreport-plugin-kerneloops
Obsoletes: kerneloops > 0.0.1
Obsoletes: abrt-plugin-kerneloops > 0.0.1
Obsoletes: abrt-plugin-kerneloopsreporter > 0.0.1

%description addon-kerneloops
This package contains plugin for collecting kernel crash information.

%package addon-python
Summary: %{name}'s addon for catching and analyzing Python exceptions
Group: System Environment/Libraries
Requires: python
Requires: %{name} = %{version}-%{release}
Obsoletes: gnome-python2-bugbuddy > 0.0.1
Provides: gnome-python2-bugbuddy

%description addon-python
This package contains python hook and python analyzer plugin for handling
uncaught exception in python programs.

%package tui
Summary: %{name}'s command line interface
Group: User Interface/Desktops
Requires: abrt-libs = %{version}-%{release}
Requires: pam
Requires: usermode

%description tui
This package contains simple command line client for processing abrt reports in
command line environment

%package cli
Summary: Virtual package to install all necessary packages for usage from command line environment
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: abrt-tui
Requires: libreport-cli
Requires: abrt-addon-kerneloops
Requires: abrt-addon-ccpp, abrt-addon-python
Requires: libreport-plugin-logger, libreport-plugin-rhtsupport, libreport-plugin-mailx
Requires: sos

%description cli
Virtual package to make easy default installation on non-graphical environments.

%package desktop
Summary: Virtual package to install all necessary packages for usage from desktop environment
Group: User Interface/Desktops
# This package gets installed when anything requests bug-buddy -
# happens when users upgrade Fn to Fn+1;
# or if user just wants "typical desktop installation".
# Installing abrt-desktop should result in the abrt which works without
# any tweaking in abrt.conf (IOW: all plugins mentioned there must be installed)
Requires: %{name} = %{version}-%{release}
Requires: abrt-addon-kerneloops
Requires: abrt-addon-ccpp, abrt-addon-python
# Default config of addon-ccpp requires gdb
Requires: gdb >= 7.0-3
Requires: abrt-gui
Requires: libreport-plugin-logger, libreport-plugin-rhtsupport, libreport-plugin-mailx
Requires: sos
#Requires: abrt-plugin-firefox
%if 0%{?fedora}
Requires: libreport-plugin-bodhi
%endif
Obsoletes: bug-buddy > 0.0.1
Provides: bug-buddy

%description desktop
Virtual package to make easy default installation on desktop environments.

%package console-notification
Summary: ABRT console notification script
Group: Applications/System
Requires: %{name} = %{version}-%{release}
Requires: %{name}-cli = %{version}-%{release}

%description console-notification
A small script which prints a count of detected problems when someone logs in
to the shell

%package python
Summary: ABRT Python API
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pygobject2
BuildRequires: python-sphinx
BuildRequires: python-nose
BuildArch: noarch

%description python
High-level API for querying, creating and manipulating
problems handled by ABRT in Python.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch93 -p1
%patch94 -p1
%patch95 -p1
%patch96 -p1
%patch97 -p1
%patch98 -p1
%patch99 -p1
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1
%patch137 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch145 -p1
%patch146 -p1
%patch147 -p1
%patch148 -p1
%patch149 -p1
%patch150 -p1
%patch151 -p1
%patch152 -p1
#Patch153: 0227-spec-add-libselinux-devel-to-BRs.patch
%patch154 -p1
%patch155 -p1
%patch156 -p1
%patch157 -p1
%patch158 -p1
%patch159 -p1
%patch160 -p1
%patch161 -p1
%patch162 -p1
%patch163 -p1
%patch164 -p1
#Patch165: 0239-spec-add-abrt-consolehelper-applications.patch
#Patch166: 0240-spec-add-usermode-and-pam-to-Requires.patch
%patch167 -p1
%patch168 -p1
%patch169 -p1


%build
rm -f src/plugins/*.1
mkdir -p m4
#rm libtool
rm ltmain.sh
test -r m4/aclocal.m4 || touch m4/aclocal.m4
aclocal
libtoolize
autoconf
automake --add-missing --force --copy
#autoreconf
%configure --with-systemdsystemunitdir=""
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
CFLAGS="-fno-strict-aliasing"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
%find_lang %{name}

# remove all .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f
mkdir -p ${RPM_BUILD_ROOT}/%{_initrddir}
%if ! %{with systemd}
install -m 755 %SOURCE1 ${RPM_BUILD_ROOT}/%{_initrddir}/abrtd
install -m 755 %SOURCE2 ${RPM_BUILD_ROOT}/%{_initrddir}/abrt-ccpp
install -m 755 %SOURCE3 ${RPM_BUILD_ROOT}/%{_initrddir}/abrt-oops
%endif
install -m 755 %SOURCE4 ${RPM_BUILD_ROOT}/%{_libexecdir}/abrt1-to-abrt2
mkdir -p $RPM_BUILD_ROOT/var/cache/abrt-di
mkdir -p $RPM_BUILD_ROOT/var/run/abrt
mkdir -p $RPM_BUILD_ROOT/var/spool/abrt
mkdir -p $RPM_BUILD_ROOT/var/spool/abrt-upload

desktop-file-install \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
        --vendor %{desktopvendor} \
        --delete-original \
        ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

desktop-file-install \
        --dir ${RPM_BUILD_ROOT}%{_sysconfdir}/xdg/autostart \
        src/applet/abrt-applet.desktop

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%check
#make check

%pre
#uidgid pair 173:173 reserved in setup rhbz#670231
%define abrt_gid_uid 173
getent group abrt >/dev/null || groupadd -f -g %{abrt_gid_uid} --system abrt
getent passwd abrt >/dev/null || useradd --system -g abrt -u %{abrt_gid_uid} -d /etc/abrt -s /sbin/nologin abrt
exit 0

%post
# $1 == 1 if install; 2 if upgrade
if [ $1 -eq 1 ]; then
%if %{with systemd}
    # Enable (but don't start) the units by default
    /bin/systemctl enable abrtd.service >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add abrtd
%endif
fi

# Remove old dump directories because of #1212868
#
# * ignore commented lines and non absolute paths
# * allow any number of white spaces anywhere
# * use the last valid line.
# * if not configured, use the default path
DUMP_LOCATION="$(sed -n 's/^\s*DumpLocation\s*=\s*\(\/.*[^\s]\)\s*$/\1/p' /etc/abrt/abrt.conf | tail -1)"
if [ -z "$DUMP_LOCATION" ]; then
    DUMP_LOCATION="/var/spool/abrt"
fi
# $1 == 1 if install; 2 if upgrade
if [ "$1" -eq 2 ]
then
    test -d "$DUMP_LOCATION" || exit 0

    # remove old dump directories
    for DD in `find "$DUMP_LOCATION" -maxdepth 1 -type d`
    do
        # in order to not remove user stuff remove only directories containing 'time' file
        if [ -f "$DD/time" ]; then
            rm -rf $DD
        fi
    done
fi

%post addon-ccpp
if [ $1 -eq 1 ]; then # Is this a clean install (as opposed to upgrade?)
%if %{with systemd}
    # Enable (but don't start) the units by default
    /bin/systemctl enable abrt-ccpp.service >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add abrt-ccpp
%endif
fi

%post addon-kerneloops
if [ $1 -eq 1 ]; then # Is this a clean install (as opposed to upgrade?)
%if %{with systemd}
    # Enable (but don't start) the units by default
    /bin/systemctl enable abrt-oops.service >/dev/null 2>&1 || :
%else
    if /sbin/chkconfig abrtd >/dev/null 2>&1; then
        /sbin/chkconfig --add abrt-oops
    fi
%endif
fi

%post addon-vmcore
if [ $1 -eq 1 ]; then
    # (see explanation in addon-ccpp section)
%if %{with systemd}
    if [ "`/bin/systemctl is-enabled abrtd.service`" = "enabled" ]; then
        # Enable (but don't start) the units by default
        /bin/systemctl enable abrt-vmcore.service >/dev/null 2>&1 || :
    fi
%else
    if /sbin/chkconfig abrtd >/dev/null 2>&1; then
        /sbin/chkconfig --add abrt-vmcore
    fi
%endif
fi

%preun addon-vmcore
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload abrt-vmcore.service >/dev/null 2>&1 || :
    /bin/systemctl stop abrt-vmcore.service >/dev/null 2>&1 || :
%else
    service abrt-vmcore stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-vmcore
%endif
fi

%preun
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload disable abrtd.service > /dev/null 2>&1 || :
    /bin/systemctl stop abrtd.service >/dev/null 2>&1 || :
%else
    service abrtd stop >/dev/null 2>&1
    /sbin/chkconfig --del abrtd
%endif
fi

%preun addon-ccpp
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload disable abrt-ccpp.service >/dev/null 2>&1 || :
    /bin/systemctl stop abrt-ccpp.service >/dev/null 2>&1 || :
%else
    service abrt-ccpp stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-ccpp
%endif
fi

%preun addon-kerneloops
if [ "$1" -eq "0" ] ; then
%if %{with systemd}
    /bin/systemctl --no-reload abrt-oops.service >/dev/null 2>&1 || :
    /bin/systemctl stop abrt-oops.service >/dev/null 2>&1 || :
%else
    service abrt-oops stop >/dev/null 2>&1
    /sbin/chkconfig --del abrt-oops
%endif
fi

%if %{with systemd}
%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun addon-kerneloops
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun addon-vmcore
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun addon-ccpp
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%endif

%post gui
# update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%postun gui
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
service abrtd condrestart >/dev/null 2>&1 || :

%posttrans addon-ccpp
service abrt-ccpp condrestart >/dev/null 2>&1 || :

%posttrans addon-kerneloops
service abrt-oops condrestart >/dev/null 2>&1 || :

%posttrans addon-vmcore
service abrt-vmcore condrestart >/dev/null 2>&1 || :

%posttrans gui
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%if %{with systemd}
/lib/systemd/system/abrtd.service
%else
%{_initrddir}/abrtd
%endif
%{_sbindir}/abrtd
%{_sbindir}/abrt-dbus
%{_sbindir}/abrt-server
%{_libexecdir}/abrt-handle-event
%{_bindir}/abrt-handle-upload
%{_bindir}/abrt-action-save-package-data
%config(noreplace) %{_sysconfdir}/%{name}/abrt.conf
%config(noreplace) %{_sysconfdir}/%{name}/abrt-action-save-package-data.conf
%config(noreplace) %{_sysconfdir}/%{name}/gpg_keys
%config(noreplace) %{_sysconfdir}/libreport/events.d/abrt_event.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/dbus-abrt.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/smart_event.conf
%dir %attr(0755, abrt, abrt) %{_localstatedir}/spool/%{name}
%dir %attr(0700, abrt, abrt) %{_localstatedir}/spool/%{name}-upload
%dir %attr(0775, abrt, abrt) %{_localstatedir}/run/%{name}
# abrtd runs as root
%dir %attr(0755, root, root) %{_localstatedir}/run/%{name}
%ghost %attr(0666, -, -) %{_localstatedir}/run/%{name}/abrt.socket
%ghost %attr(0644, -, -) %{_localstatedir}/run/abrtd.pid

%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/plugins
%{_mandir}/man1/abrt-handle-upload.1.gz
%{_mandir}/man1/abrt-server.1.gz
%{_mandir}/man1/abrt-action-save-package-data.1.gz
%{_mandir}/man8/abrtd.8.gz
%{_mandir}/man8/abrt-dbus.8.gz
%{_mandir}/man5/abrt.conf.5.gz
%{_mandir}/man5/abrt-action-save-package-data.conf.5.gz
# {_mandir}/man5/pyhook.conf.5.gz
%{_datadir}/dbus-1/system-services/com.redhat.abrt.service
%{_libexecdir}/abrt1-to-abrt2

%files libs
%defattr(-,root,root,-)
%{_libdir}/libabrt*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/abrt/*
%{_libdir}/libabrt*.so
#FIXME: this should go to libreportgtk-devel package
%{_libdir}/pkgconfig/*

%files gui
%defattr(-,root,root,-)
%{_bindir}/abrt-gui
%{_bindir}/abrt-gui-root
%dir %{_datadir}/%{name}
# all glade, gtkbuilder and py files for gui
%{_datadir}/applications/%{desktopvendor}-%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/status/*
%{_datadir}/%{name}/icons/hicolor/*/status/*
%{_bindir}/abrt-applet
%config(noreplace) %{_sysconfdir}/xdg/autostart/abrt-applet.desktop
%config(noreplace) %{_sysconfdir}/pam.d/abrt-gui-root
%config(noreplace) %{_sysconfdir}/security/console.apps/abrt-gui-root

%files addon-ccpp
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/CCpp.conf
%dir %attr(0775, abrt, abrt) %{_localstatedir}/cache/abrt-di
%if %{with systemd}
/lib/systemd/system/abrt-ccpp.service
%else
%{_initrddir}/abrt-ccpp
%endif
%{_libexecdir}/abrt-hook-ccpp
%attr(4755, abrt, abrt) %{_libexecdir}/abrt-action-install-debuginfo-to-abrt-cache
%{_bindir}/abrt-action-analyze-c
%{_bindir}/abrt-action-trim-files
%{_bindir}/abrt-action-analyze-core
%{_bindir}/abrt-action-install-debuginfo
%{_bindir}/abrt-action-generate-backtrace
%{_bindir}/abrt-action-generate-core-backtrace
%{_bindir}/abrt-action-analyze-backtrace
%{_bindir}/abrt-action-list-dsos
%{_bindir}/abrt-dedup-client
%{_bindir}/abrt-action-analyze-ccpp-local
%{_sbindir}/abrt-install-ccpp-hook
%config(noreplace) %{_sysconfdir}/libreport/events.d/ccpp_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/gconf_event.conf
%config(noreplace) %{_sysconfdir}/libreport/events.d/vimrc_event.conf
%config %{_sysconfdir}/libreport/events/analyze_LocalGDB.xml
%config %{_sysconfdir}/libreport/events/collect_xsession_errors.xml
%config %{_sysconfdir}/libreport/events/collect_GConf.xml
%config %{_sysconfdir}/libreport/events/collect_vimrc_user.xml
%config %{_sysconfdir}/libreport/events/collect_vimrc_system.xml
%{_mandir}/man*/abrt-action-analyze-c.*
%{_mandir}/man*/abrt-action-trim-files.*
%{_mandir}/man*/abrt-action-generate-backtrace.*
%{_mandir}/man*/abrt-action-generate-core-backtrace.*
%{_mandir}/man*/abrt-action-analyze-backtrace.*
%{_mandir}/man*/abrt-action-list-dsos.*
%{_mandir}/man1/abrt-install-ccpp-hook.1.gz

%files addon-kerneloops
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/koops_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/plugins/oops.conf
%if %{with systemd}
/lib/systemd/system/abrt-oops.service
%else
%{_initrddir}/abrt-oops
%endif
%{_bindir}/abrt-dump-oops
%{_bindir}/abrt-action-analyze-oops
%{_mandir}/man1/abrt-action-analyze-oops.1*
%{_mandir}/man5/abrt-oops.conf.5*

%files addon-vmcore
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/libreport/events.d/vmcore_event.conf
%config(noreplace) %{_sysconfdir}/%{name}/abrt-harvest-vmcore.conf
%config %{_sysconfdir}/libreport/events/analyze_VMcore.xml
%if %{with systemd}
/lib/systemd/system/abrt-vmcore.service
%else
%{_initrddir}/abrt-vmcore
%endif
%{_sbindir}/abrt-harvest-vmcore
%{_bindir}/abrt-action-analyze-vmcore
%{_mandir}/man1/abrt-action-analyze-vmcore.1*
%{_mandir}/man1/abrt-harvest-vmcore.1*

%files addon-python
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/%{name}/plugins/python.conf
%config %{_sysconfdir}/libreport/events.d/python_event.conf
%{_bindir}/abrt-action-analyze-python
%{_mandir}/man1/abrt-action-analyze-python.1*
%{python_sitearch}/abrt*.py*
%{python_sitearch}/abrt.pth

%files cli
%defattr(-,root,root,-)

%files tui
%defattr(-,root,root,-)
%{_bindir}/abrt-cli
%{_bindir}/abrt-cli-root
%{_mandir}/man1/abrt-cli.1.gz
%config(noreplace) %{_sysconfdir}/pam.d/abrt-cli-root
%config(noreplace) %{_sysconfdir}/security/console.apps/abrt-cli-root

%files desktop
%defattr(-,root,root,-)

%files python
%{python_sitelib}/problem/
%{_defaultdocdir}/%{name}-python-%{version}/examples/

%files console-notification
%config(noreplace) %{_sysconfdir}/profile.d/abrt-console-notification.sh

%changelog
* Tue Jul 07 2015 Scientific Linux Auto Patch Process <SCIENTIFIC-LINUX-DEVEL@LISTSERV.FNAL.GOV>
- Added Source: abrt.ini
-->  Config file for automated patch script
- Added Patch: abrt-add-sl-gpg-keys.patch
-->  Add the Scientific Linux keys to the recognized list
- Ran Regex: (Release: .*)%{\?dist}(.*) => \1.sl6\2
-->  Modify release string to note changes

* Mon Jun 01 2015 Jakub Filak <jfilak@redhat.com> - 2.0.8-26%{?dist}.1
- remove old dump directories in upgrade
- remove outdated rmp scriptlets
- daemon: allow only root to submit CCpp, Koops, VMCore and Xorg problems
- abrt-action-install-debuginfo-to-abrt-cache: sanitize arguments and umask
- make the problem directories owned by abrt and the group root
- validate uploaded problem directories in abrt-handle-upload
- don't override nor remove files with user core dump files
- fix symbolic link and race condition flaws
- Resolves: #1211966

* Fri Aug 1 2014 Jakub Filak <jfilak@redhat.com> - 2.0.8-26
- koops: fix a use-after-free bug uncoverd by coverity
- Related: #1084467

* Fri Aug 1 2014 Jakub Filak <jfilak@redhat.com> - 2.0.8-25
- inform users about uselessness of Kernel oopses
- Resolves: #1084467

* Tue Jul 22 2014 Jakub Filak <jfilak@redhat.com> - 2.0.8-24
- fix post-create reporter-uploader examples
- Resolves: #888282

* Thu Jun 26 2014 Jakub Filak <jfilak@redhat.com> - 2.0.8-23
- doc: update OpenGPGCheck in a-a-save-package-data rhbz#997922
- Resolves: #997922

* Thu Jun 19 2014 Jakub Filak <jfilak@redhat.com> - 2.0.8-22
- desktop file is named redhat-abrt.desktop rhbz#905822
- dependency missing for abrt-addon-vmcore
- removed unnecessary debug message "Can't open file '/*/uid': No such file or directory"
- fix post-create reporter-uploader examples
- add abrt-harvest-vmcore manual page
- Resolves: #812284, #888282, #905822, #984065, #1022160

* Tue Aug 13 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-21
- updated translation (ko, po) #952773
- added support for MCE errors rhbz#812537
- Resolves: #812537, #952773

* Wed Aug  7 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-20
- rebuild because of failed rpmdiff
- Related: #952773

* Tue Aug  6 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-19
- fixed problem with wrong kernel oops duplicates - rhbz#953813
- updated translation rhbz#993564
- Resolves: #953813

* Fri Jul 26 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-18
- limit the oops detection rate rhbz#952773
- Resolves: #952773

* Fri Jun  7 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-17
- ABRT won't install debuginfos from rhn repository rhbz#759443
- Brewtap reports MacroSurprise or SetuidMissingRELRO rhbz#812284
- abrt missing dependency: libreport-plugin-bugzilla rhbz#828673
- Same values for variables  'DumpLocation' & 'WatchCrashdumpArchiveDir'  stops mailx plugin rhbz#854668
- abrt-vmcore repeats processing old vmcores on the service (re)start rhbz#885044
- abrt-gui help menu item points to generic RHEL documentation rhbz#903195
- Desktop file is named redhat-abrt.desktop rhbz#905822
- 'post-create' on 'xxx' exited with 1 Corrupted or bad directory xxx, deleting rhbz#909617
- abrt.pth prevents python virtualenv creation rhbz#912672
- [RFE] add the console notification to RHEL6 rhbz#961231
- provide the python API for abrt rhbz#952704
- abrtd marks problems having count > 1 as duplicates rhbz#886631
- Resolves: #886631, #905429, #961231, #961231, #961231, #961231, #812284, #828673, #828673, #759443, #759443, #903195, #854668, #905822, #909617, #885044, #912672, #912672, #952704, #875260

* Mon Jan 28 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-16
- disable buffering on gio channels
- Related: 873815

* Wed Jan 23 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-15
- more multilib fixes
- Related: #826924

* Wed Jan 23 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-14
- rebuild because of broken brew builder
- Related: #826924

* Wed Jan 23 2013 Denys Vlasenko <dvlasenk@redhat.com> 2.0.8-13
- Prevent daemon from being stuck (unresponsive to socket connects)
  while post-create even runs
- Prevent infinite loop of crashes
- Resolves: #826924

* Fri Jan 11 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-12
- don't follow symlinks
- Related: #895443

* Fri Jan 11 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-11
- fixed possible deadlock in abrt daemon
- Resolves: #873815

* Mon Jan  7 2013 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-10
- fixed relro flags
- fixed the undefined weak symbols
- Resolves: #812284, #892658

* Thu Oct 18 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-9
- updated translation rhbz#864023
- Resolves: #864023

* Wed Aug 22 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-8
- hopefully fixed ugly applet icon rhbz#797078
- abrt-install-ccpp-hook: fix the check for %e presense rhbz#851097
- abrt-harvest-vmcore: add CopyVMcore config option to copy vmcores. Closes rhbz#847227
- fixed problems discovered by brewtap rhbz#812284
- don't try to run dbus-send if it's not installed rhbz#811901
- Resolves: #797078, #851097, #847227, #812284, #811901

* Thu Aug 09 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-7
- [abrt] abrt-addon-ccpp-2.0.7-4.fc17: abrt-action-analyze-core:106:extract_info_from_core:IndexError: list index out of range rhbz#804309
- abrt-addon-python: The process might hang forever if no one collects the dump it sends rhbz#808562
- Reporting may fail with: "abrt-bodhi: command not found" rhbz#810309
- too strict check for tainted kernel rhbz#814594
- "abrt-ccpp status" returned no status messages rhbz#820475
- abrt missing dependency: libreport-plugin-bugzilla rhbz#828673
- abrt-addon-python: The process might hang forever if no one collects the dump it sends rhbz#837333
- don't remove new problems from abrt-upload directory rhbz#839285
- Resolves: #839285, #828673, #810309, #820475, #828673, #808562, #837333, #804309, #814594, #814594

* Wed May 16 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-6
- enable plugin services after install rhbz#820515
- Resolves: #820515

* Thu Apr 05 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-5
- removed the "report problem with ABRT btn" rhbz#809587
- fixed double free
- fixed ccpp-install man page
- Resolves: #809587, #796216, #799027

* Fri Mar 16 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-4
- don't mark reports reported in post-create by mailx as reported
- Resolves: #803618

* Mon Mar 12 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-3
- fixed remote crash handling rhbz#800828
- Resolves: #800828

* Tue Mar 06 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-2
- updated translation
- added man page for a-a-analyze-vmcore
- minor fixes in kernel oops parser
- Related: #759375

* Thu Feb 16 2012 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.8-1
- rebase to the latest upstream
- partly fixed probles with suided cores
- fixed confusing message about "moved copy"
- properly enable daemons on update from previous version
- added default config file for mailx
- cli doesn't depend on python plugin
- properly init i18n all plugins
- added missing man page to abrt-cli
- added warning when user tries to report already reported problem again
- added vmcores plugin
- Resolves: #759375, #783450, #773242, #771597, #770357, #751068, #749100, #747624, #727494

* Wed Oct 26 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-14
- updated translation rhbz#731947
- Resolves: #731947

* Fri Oct 21 2011 Nikola Pajkovsky <npajkovs@redaht.com>
- Excessive writing to /var/log/messages
- Resolves: #726121

* Thu Oct 13 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-13
- fixed typo in ccpp_event.conf rhbz#744784
- fixed return codes in abrt-cli rhbz#742474
- Resolves: #744784, #742474

* Tue Oct 11 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-12
- fixed help url rhbz#744783
- Resolves: #744783

* Mon Sep 19 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-11
- abrt-cli run gui and prints help even for correct cmdline option
- Resolves: #739562

* Fri Sep 16 2011 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.4-10
- abrtd daemon need "messagebus" daemon, please update "Required-Start" section of /etc/init.d/abrtd
- move abrt-action-install-debuginfo-to-abrt-cache to libexec  rhbz#736068
- fix possible NULL dereference  rhbz#735942
  Resolves: #735942, #736068, #733975

* Fri Aug 26 2011 Karel Klíč <kklic@redhat.com> - 2.0.4-9
- Update translations
  Resolves: #731947

* Thu Aug 25 2011 Miroslav Lichvar <mlichvar@redhat.com> - 2.0.4-8
- read DBPath from SQLite3.conf in abrt1-to-abrt2  rhbz#726122
  Resolves: #726122
- update man pages
  Resolves: #727569

* Thu Aug 25 2011 Karel Klíč <kklic@redhat.com> - 2.0.4-7
- Fixed bug in #732535 solution
  Related: #732535

* Tue Aug 23 2011 Karel Klíč <kklic@redhat.com> - 2.0.4-6
- Removed unconditioned `service abrt-ccpp restart` and `service
  abrt-oops restart` from %%post sections, because services cannot be
  automatically started after package install. We start new daemons
  another way: if abrtd is running on the system being updated, run
  abrt-{oops,ccpp} services as well, because what was a part of abrtd
  service became a separate service.
  Resolves: #732535
- Added proper fix for rhbz#729686 make check fails
  Related: #729686
- Updated potfiles_in.patch with better solution (Making check in po:
  *** No rule to make target
  `../src/plugins/abrt-action-kerneloops.c', needed by `abrt.pot')
  Related: #729686
- Added %%check section to the spec file; it runs make check during
  compilation, to test that it finishes successfully
  Related: #729686
- Updated helper_for_executing_shell_code.patch with better solution
  Related: #705768


* Wed Aug 17 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-5
- start new daemons (ccpp, oops) after install
- fixes problem with missing abrt-db rhbz#730696
- fixed potfiles.in rhbz#729686
- Resolves: #729686 #730696

* Sun Aug 14 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-4
- fixed vendor rhbz#725770
- Resolves: #725770

* Wed Aug 03 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-3
- fixed desktop file rhbz#725770
- removed retrace-client (moved to epel) rhbz#727457
- added helper for executing post-create events rhbz#705768
- removed stalled deps on gnome-keyring-devel
- Resolves: #725770 #727457 #705768

* Fri Jul 22 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-2
- fixed spec file to enable oops and ccpp services on update from abrt-1.x
- fixed auto reporting using reporter-upload in abrt_event.conf
- fixed sorting in main gui
- Related: #697494

* Tue Jul 19 2011 Jiri Moskovcak <jmoskovc@redhat.com> 2.0.4-1
- update to the latest upstream
- Resolves: #697494

* Thu Apr 07 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.16-3
- improved support for GSS customer portal
  - fixed the hash generating: use component name instead of package NVR
  - added a user-agent header to rhtsupport requests for easier hash algorithm
    matching
- Resolves: #694410

* Fri Mar 11 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.16-2
- enabled mailx as a crash notify
- Resolves: #678724

* Fri Feb 04 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.16-1
- added list of attachments to comment rhbz#668875
- stop consuming non-standard header rhbz#670492
- Resolves: #670492, #668875

* Tue Jan 18 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.15-2
- add a gui/uid to useradd/groupadd command (reserved in setup rhbz#670231)
- Resolves: #650975

* Mon Jan 10 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.15-1
- removed unused files (jmoskovc@redhat.com)
- update po files (jmoskovc@redhat.com)
- removed some unused files (jmoskovc@redhat.com)
- pass old pattern to ccpp hook and use it (dvlasenk@redhat.com)
- GUI: added warning when gnome-keyring can't be accessed rhbz#576866 (jmoskovc@redhat.com)
- 666893 - Unable to make sense of XML-RPC response from server (npajkovs@redhat.com)
- PyHook: ignore SystemExit exception rhbz#636913 (jmoskovc@redhat.com)
- 665405 - ABRT's usage of sos does not grab /var/log/messages (npajkovs@redhat.com)
- add a note in report if kernel is tainted (npajkovs@redhat.com)
- KerneloopsScanner.cpp: make a room for NULL byte (npajkovs@redhat.com)
- fix multicharacter warring (npajkovs@redhat.com)
- open help page instead of about rhbz#666267
- Resolves: #665405, #576866, #649309, #623142, #614486, #650975, #666267

* Mon Jan 10 2011 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.14-1
- updated po files (jmoskovc@redhat.com)
- GUI: make how to mandatory (jmoskovc@redhat.com)
- silent rules (npajkovs@redhat.com)
- fixed segv in abrt-hook-ccpp rhbz#652338 (jmoskovc@redhat.com)
- rhbz 623142 (npajkovs@redhat.com)
- GUI: make the "install debuginfo" hint selectable rhbz#644343 (jmoskovc@redhat.com)
- GUI: wrap howto and comments rhbz#625237 (jmoskovc@redhat.com)
- GUI: show horizontal scrollbar when needed (jmoskovc@redhat.com)
- GUI: wrap lines in the backtrace window rhbz#625232 (jmoskovc@redhat.com)
- GUI: changed '*' to '•' rhbz#625236 (jmoskovc@redhat.com)
- rm abrt_test.py (jmoskovc@redhat.com)
- added utf-8 coding tag into .py files (jmoskovc@redhat.com)
- GUI: show the scrollbar in summary only when needed (jmoskovc@redhat.com)
- GUI: added accelerator key "Delete" to the delete button rrakus@redhat.com (jmoskovc@redhat.com)
- backtrace rating check in abrt-cli (mtoman@redhat.com)
- Localization of [y/n] response in abrt-cli (kklic@redhat.com)
- abrt-cli --info: Make coredump and rating fields optional (kklic@redhat.com)
- GUI: increase dbus timeout in Report() call (vda.linux@googlemail.com)
- GUI: make the bt viewer not-editable rhbz#621871 (jmoskovc@redhat.com)
- increased version to 1.1.14 (jmoskovc@redhat.com)
- new bt parser (kklic) (jmoskovc@redhat.com)
- disable polkit (jmoskovc@redhat.com)
- add example of tainted kernel module (npajkovs@redhat.com)

* Thu Aug 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.13-4
- fixed typo kenel->kernel rhbz#627580
- Resovles: #627580

* Wed Aug 25 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.13-3
- fixed problem with redirection (http response 30x) rhbz#613164
- Resolves: #613164

* Wed Aug 18 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.13-2
- increased timeout in gui to prevent timeouts when uploading large files
- added update messages during upload
- Resolves: #625012

* Mon Aug 09 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.13-1
- updated translations rhbz#619340
- removed dependency on libzip
- added libxml-2.0 into configure (npajkovs@redhat.com)
- fixed typo in man page rhbz#610748 (jmoskovc@redhat.com)
- RHTSupport: GUI's SSLVerify checkbox had one missing bit of code (vda.linux@googlemail.com)
- Resolves: rhbz#619340

* Wed Jul 28 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.12-2
- minor fix to rhtsupport plugin
- Resolves: rhbz#612548

* Wed Jul 28 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.12-1
- updated translations
- made some more strings translatable rhbz#574693
- fixed SIGABRT in dumpoops rhbz#612548 (dvlasenk@redhat.com)
- moved abrtd.lock and abrt.socket to /var/run/abrt
- disabled debuginfo install
- Resolves: #612548, #574693

* Tue Jul 27 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.10-3
- blacklisted mono-core and /usr/bin/nspluginviewer

* Wed Jul 21 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.10-2
- enabled GPG check rhbz#609404
- made RHTSupport the default reporter instead of bugzilla rhbz#603056
- Resolves: #603056, #609404

* Wed Jul 14 2010 Karel Klic <kklic@redhat.com> 1.1.10-1
- a bugfix release
- die with an error message if the database plugin is not accessible when needed (kklic@redhat.com)
- change RHTSupport URL protocol from HTTP to HTTPS (dvlasenk@redhat.com)
- the Logger plugin returns a message as the result of Report() call instead of a file URL (kklic@redhat.com)
- Cut off prelink suffixes from executable name if any (mtoman@redhat.com)
- CCpp: abrt-debuginfo-install output lines can be long, accomodate them (dvlasenk@redhat.com)
- do not pop up message on crash if the same crash is the same (dvlasenk@redhat.com)
- Resolves: #612997, #612838, #611145

* Tue Jul 13 2010 Karel Klic <kklic@redhat.com> 1.1.9-1
- a bugfix release
- fedora bugs do not depend on rhel bugs (npajkovs@redhat.com)
- GUI: fixed problem with no gkeyring and just one reporter enabled rhbz#612457 (jmoskovc@redhat.com)
- added a document about interpreted language integration (kklic@redhat.com)
- moved devel header files to inc/ and included them in -devel package (jmoskovc@redhat.com, npajkovs@redhat.com)
- renamed abrt-utils.pc to abrt.pc (jmoskovc@redhat.com)
- string updates based on a UI text review (kklic@redhat.com)
- rhtsupport obsoletes the old rh plugins (jmoskovc@redhat.com)
- list allowed items in RHTSupport.conf (kklic@redhat.com)
- GUI: fixed package name in warning message when the packge is kernel rhbz#612191 (jmoskovc@redhat.com)
- remove rating for python crashes (jmoskovc@redhat.com)
- CCpp: give zero rating to an empty backtrace (jmoskovc@redhat.com)
- GUI: allow sending crashes without rating (jmoskovc@redhat.com)
- RHTSupport: set default URL to api.access.redhat.com/rs (dvlasenk@redhat.com)
- abort initialization on abrt.conf parsing errors (dvlasenk@redhat.com)
- changing NoSSLVerify to SSLVerify in bugzilla plugin (mtoman@redhat.com)
- Resolves: #612874, #612191, #612186, #612404, #568747

* Wed Jun 30 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.8-2
- added rating to python crashes
- Resolves: #607684

* Wed Jun 30 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.8-1
- show hostname in cli (kklic@redhat.com)
- disable the GPG check until GA
- updated po files (jmoskovc@redhat.com)
- added support for package specific actions rhbz#606917 (jmoskovc@redhat.com)
- renamed TicketUploader to ReportUploader (jmoskovc@redhat.com)
- bad hostnames on remote crashes (npajkovs@redhat.com)
- unlimited MaxCrashReportsSize (npajkovs@redhat.com)
- abrt_rh_support: improve error messages rhbz#608698 (vda.linux@googlemail.com)
- Added BacktraceRemotes option. (kklic@redhat.com)
- Allow remote crashes to not to belong to a package. Skip GPG check on remote crashes. (kklic@redhat.com)
- remove obsolete Catcut and rhfastcheck reporters (vda.linux@googlemail.com)
- make rhel bug point to correct place rhbz#578397 (npajkovs@redhat.com)
- Show comment and how to reproduce fields when reporing crashes in abrt-cli (kklic@redhat.com)
- Bash completion update (kklic@redhat.com)
- Rename --get-list to --list (kklic@redhat.com)
- Update man page (kklic@redhat.com)
- Options overhaul (kklic@redhat.com)
- Resolves: #607684, #608693, #608698, #578397

* Wed Jun 23 2010 Denys Vlasenko <dvlasenk@redhat.com> 1.1.7-2
- abrt should not point to Fedora bugs but create new RHEL bug instead (npajkovs@redhat.com)
- Resolves: #578397

* Wed Jun 23 2010 Denys Vlasenko <dvlasenk@redhat.com> 1.1.7-1
- Don't show global uuid in report (npajkovs@redhat.com)
- GUI: don't try to use action plugins as reporters (jmoskovc@redhat.com)
- Added WatchCrashdumpArchiveDir directive to abrt.conf and related code (vda.linux@googlemail.com)
- GUI: don't show the placehondler icon rhbz#605693 (jmoskovc@redhat.com)
- Make "Loaded foo.conf" message less confusing (vda.linux@googlemail.com)
- Fixed a flaw in strbuf_prepend_str (kklic@redhat.com)
- TicketUploader: do not add '\n' to text files in crashdump (vda.linux@googlemail.com)
- Resolves: #604706, #604088, #590698

* Wed Jun 16 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.6-1
- updated translation
- GUI: skip the plugin selection, if it's not needed (jmoskovc@redhat.com)
- Check conf file for syntax errors (kklic@redhat.com)
- move misplaced sanity checks in cron parser (vda.linux@googlemail.com)
- GUI: don't require the rating for all reporters (jmoskovc@redhat.com)
- GUI: fixed exception when there is no configure dialog for plugin rhbz#603745 (jmoskovc@redhat.com)
- Add a GUI config dialog for RHTSupport plugin (vda.linux@googlemail.com)
- abrt_curl: fix a problem with incorrect content-length on 32-bit arches (vda.linux@googlemail.com)
- sosreport: save the dump directly to crashdump directory (vda.linux@googlemail.com)
- plugin rename: rhticket -> RHTSupport (vda.linux@googlemail.com)
- Daemon socket for reporting crashes (karel@localhost.localdomain)
- GUI: fixed few typos (jmoskovc@redhat.com)
- Resolves: #604085, #568747

* Wed Jun 09 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.5-1
- GUI: polished the reporter assistant (jmoskovc@redhat.com)
- Logger reporter: do not store useless info (vda.linux@googlemail.com)
- ccpp hook: add SaveBinaryImage option which saves of the crashed binary (vda.linux@googlemail.com)
- SPEC: added CFLAGS="-fno-strict-aliasing" to fix the rpmdiff warnings rhbz#599364 (jmoskovc@redhat.com)
- GUI: don't remove user comments when re-reporting the bug rhbz#601779 (jmoskovc@redhat.com)
- remove "(deleted)" from executable path rhbz#593037 (jmoskovc@redhat.com)
- CCpp analyzer: add 60 sec cap on gdb run time. (vda.linux@googlemail.com)
- add new file *hostname* into debugdump directory (npajkovs@redhat.com)
- rhticket: upload real tarball, not a bogus file (vda.linux@googlemail.com)
- abrt-hook-ccpp: eliminate race between process exit and compat coredump creation rhbz#584554 (vda.linux@googlemail.com)
- rhticket: actually do create ticket, using Gavin's lib code (vda.linux@googlemail.com)
- properly obsolete gnome-python2-bugbuddy rhbz#579748 (jmoskovc@redhat.com)
- GUI: remember comment and howto on backtrace refresh rhbz#545690 (jmoskovc@redhat.com)
- use header case in button label rhbz#565812 (jmoskovc@redhat.com)
- make log window resizable (vda.linux@googlemail.com)
- rename a few remaining /var/cache/abrt -> /var/spool/abrt (vda.linux@googlemail.com)
- suppress misleading "crash 'XXXXXXXX' is not in database" messages rhbz#591843
- fixed race in creating user coredump rhbz#584554
- fixed few grammar errors rhbz#601785
- Resolves: rhbz#591843, rhbz#584554

* Fri Jun 04 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.4-2
- added CFLAGS="-fno-strict-aliasing"
- Resolves: rhbz#599364

* Wed May 26 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.4-1
- added reporting wizard partialy fixes rhbz#572379 (jmoskovc@redhat.com)
- fixed few leaked fds - selinux is happy now (vda.linux@googlemail.com)
- fixed kerneloops --- cut here --- problem rhbz#592152 (vda.linux@googlemail.com)
- updated translations
- Resolves: #572379

* Mon May 24 2010 Denys Vlasenko <dvlasenk@redhat.com> 1.1.3-1
- More fixes for /var/cache/abrt -> /var/spool/abrt conversion
- Resolves: #594688

* Thu May 20 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.2-3
- updated init script rhbz#594412

* Thu May 20 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.2-2
- added /var/spool to spec rhbz#593906
- Resolves: #574693

* Wed May 19 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.2-1
- updated translation rhbz#574693
- obsolete gnome-python2-bugbuddy rhbz#579748 (jmoskovc@redhat.com)
- Report "INFO: possible recursive locking detected rhbz#582378 (vda.linux@googlemail.com)
- kill yumdownloader if abrt-debuginfo-install is terminated mid-flight (vda.linux@googlemail.com)
- do not create Python dumps if argv[0] is not absolute (vda.linux@googlemail.com)
- improve kerneloops hash (vda.linux@googlemail.com)
- Move /var/cache/abrt to /var/spool/abrt. rhbz#568101. (vda.linux@googlemail.com)
- bugzilla: better summary and decription messages (npajkovs@redhat.com)
- renamed daemon pid and lock file rhbz#588315 (jmoskovc@redhat.com)
- Move hooklib from src/Hooks to lib/Utils (kklic@redhat.com)

* Wed May 12 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.1-1
- updated translations
- removed avant-window-navigator from blacklist (jmoskovc@redhat.com)
- Abort debuginfo download if low on disk space (partially addresses #564451) (vda.linux@googlemail.com)
- fix bug 588945 - sparse core files performance hit (vda.linux@googlemail.com)
- Add BlackListedPaths option to abrt.conf. Fixes #582421 (vda.linux@googlemail.com)
- Do not die when /var/cache/abrt/*/uid does not contain a number (rhbz#580899) (kklic@redhat.com)
- rid of rewriting config in /etc/abrt/abrt.conf (npajkovs@redhat.com)
- fix bug 571411: backtrace attachment of the form /var/cache/abrt/foo-12345-67890/backtrace (vda.linux@googlemail.com)
- Do not echo password to terminal in abrt-cli (kklic@redhat.com)
- Resolves: #591504

* Wed May 05 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.1.0-1
- updated translations
- fixed backtrace attaching rhbz#571411 (vda.linux@googlemail.com)
- fixed abrt-debuginfo-install rhbz#579038 (vda.linux@googlemail.com)
- don't echo password in cli rhbz#587283 (kklic@redhat.com)
- updated icons rhbz#587698 (jmoskovc@redhat.com)
- Show error message when abrtd service is run as non-root. rhbz#584352 (kklic@redhat.com)
- Crash function is now detected even for threads without an abort frame (kklic@redhat.com)
- do not catch perl/python crashes when the script is not of known package origin (kklic@redhat.com)
- comment can be private (npajkovs@redhat.com)
- kerneloop is more informative when failed (npajkovs@redhat.com)
- add function name into summary(if it's found) (npajkovs@redhat.com)
- Change kerneloops message when it fails to send the report (npajkovs@redhat.com)
- Resolves: #579038

* Wed Apr 28 2010 Jiri Moskovcak <jmoskovc@redhat.com> 1.0.9-1
- update to the latest stable upstream
- fixed problem with localized yum messages rhbz#581804
- better bugzilla summary (napjkovs@redhat.com)
- ignore interpreter (py,perl) crashes caused by unpackaged scripts (kklic@redhat.com)
- hooklib: fix excessive rounding down in free space calculation (bz#575644) (vda.linux@googlemail.com)
- gui: fix 551989 "crash detected in abrt-gui-1.0.0-1.fc12" and such (vda.linux@googlemail.com)
- trivial: fix 566806 "abrt-gui sometimes can't be closed" (vda.linux@googlemail.com)
- gui: fix the last case where gnome-keyring's find_items_sync() may throw DeniedError (vda.linux@googlemail.com)
- updated translation
- minor fix to sosreport to make it work with latest sos rhbz#576861 (jmoskovc@redhat.com)
- GUI: total rewrite based on design from Mairin Duffy (jmoskovc@redhat.com)
- trivial: better HTTP/curl error reporting (vda.linux@googlemail.com)
- Use backtrace parser from abrtutils, new backtrace rating algorithm, store crash function if it's known (kklic@redhat.com)
- PYHOOK: don't use sitecustomize.py rhbz#539497 (jmoskovc@redhat.com)
- rhfastcheck: a new reporter plugin based on Gavin's work (vda.linux@googlemail.com)
- rhticket: new reporter plugin (vda.linux@googlemail.com)
- Kerneloops: use 1st line of oops as REASON. Closes rhbz#574196. (vda.linux@googlemail.com)
- Kerneloops: fix a case when we file an oops w/o backtrace (vda.linux@googlemail.com)
- minor fix in abrt-debuginfo-install to make it work with yum >= 3.2.26 (jmoskovc@redhat.com)
- GUI: added action to applet to directly report last crash (jmoskovc@redhat.com)
- Never flag backtrace as binary file (fixes problem observed in bz#571411) (vda.linux@googlemail.com)
- improve syslog file detection. closes bz#565983 (vda.linux@googlemail.com)
- add arch, package and release in comment (npajkovs@redhat.com)
- add ProcessUnpackaged option to abrt.conf (vda.linux@googlemail.com)
- abrt-debuginfo-install: use -debuginfo repos which match enabled "usual" repos (vda.linux@googlemail.com)
- fix format security error (fcrozat@mandriva.com)
- icons repackaging (jmoskovc@redhat.com)
- partial fix for bz#565983 (vda.linux@googlemail.com)
- SPEC: Updated source URL (jmoskovc@redhat.com)
- removed unneeded patches
- Resolves: 572641, 572237, 576861

* Tue Apr  6 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.7-5
- removed sos-1.9 support as it's not in the trees yet
- removed hardcoded repository name "rhel-debuginfo" in debuginfo install
- and enabled the debuginfo install by default
- Resolves: #579038

* Wed Mar 31 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.7-4
- fixed problem with running sosreport
- Resolves: #576861

* Thu Feb 25 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.7-3
- fixed translation rhbz#574693 (jmoskovc@redhat.com)
- improved kerneloops summary in bugzilla rhbz#574196 (dvlasenk@reshat.com)
- fixed bug in initscript which prevents abrtd from restarting after update (npajkovs@redhat.com)
- fixed abrt-debuginfo-install to work with rhel dbeuginfo repos
- Resolves: #574196, #574693

* Thu Feb 25 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.7-2
- fixed problem with bz plugin
- Resolves: #564366

* Fri Feb 12 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.7-1
- Load plugin settings also from ~/.abrt/*.conf (kklic@redhat.com)
- fix bz#541088 "abrt should not catch python excp EPIPE" (vda.linux@googlemail.com)
- fix bz#554242 "Cannot tab between input areas in report dialog" (vda.linux@googlemail.com)
- fix bz#563484 "abrt uses unnecessary disk space when getting debug info" (vda.linux@googlemail.com)
- Don't show empty 'Not loaded plugins' section - fix#2 rhbz#560971 (jmoskovc@redhat.com)
- fix big-endian build problem (vda.linux@googlemail.com)
- Fixes, displays package owners (kklic@redhat.com)
- GUI: fixed exception in plugin settings dialog rhbz#560851 (jmoskovc@redhat.com)
- GUI: respect system settings for toolbars rhbz#552161 (jmoskovc@redhat.com)
- python hook: move UUID generation to abrtd; generate REASON, add it to bz title (vda.linux@googlemail.com)
- make "reason" field less verbose; bz reporter: include it in "summary" (vda.linux@googlemail.com)
- added avant-window-navigator to blacklist per maintainer request (jmoskovc@redhat.com)
- CCpp analyzer: fix rhbz#552435 (bt rating misinterpreting # chars) (vda.linux@googlemail.com)
- Ask for login and password if missing from reporter plugin. (kklic@redhat.com)
- abrtd: fix handling of dupes (weren't deleting dup's directory); better logging (vda.linux@googlemail.com)
- abrtd: handle "perl -w /usr/bin/script" too (vda.linux@googlemail.com)
- Component-wise duplicates (kklic@redhat.com)
- abrtd: fix rhbz#560642 - don't die on bad plugin names (vda.linux@googlemail.com)
- Fixed parsing backtrace from rhbz#549293 (kklic@redhat.com)
- GUI: fixed scrolling in reporter dialog rhbz#559687 (jmoskovc@redhat.com)
- fixed button order in plugins windows rhbz#560961 (jmoskovc@redhat.com)
- GUI: fixed windows icons and titles rhbz#537240, rhbz#560964 (jmoskovc@redhat.com)
- Fix to successfully parse a backtrace from rhbz#550642 (kklic@redhat.com)
- cli: fix the problem of not showing oops text in editor (vda.linux@googlemail.com)
- GUI: fix rhbz#560971 "Don't show empty 'Not loaded plugins' section" (vda.linux@googlemail.com)

* Tue Feb  2 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.6-1
- print __glib_assert_msg (rhbz#549735);
- SPEC: added some requires to abrt-cli to make it work out-of-the-box (jmoskovc@redhat.com)
- abrt-hook-ccpp: fix rhbz#560612 "limit '18446744073709551615' is bogus" rhbz#560612(vda.linux@googlemail.com)
- APPLET: don't show the icon when abrtd is not running rhbz#557866 (jmoskovc@redhat.com)
- GUI: made report message labels wrap (jmoskovc@redhat.com)
- GUI: don't die if daemon doesn't send the gpg keys (jmoskovc@redhat.com)
- disabled the autoreporting of kerneloopses (jmoskovc@redhat.com)
- Kerneloops: fix BZ reporting of oopses (vda.linux@googlemail.com)
- GUI: wider report message dialog (jmoskovc@redhat.com)
- moved the gpg key list from abrt.conf to gpg_keys file (jmoskovc@redhat.com)
- Logger: create log file with mode 0600 (vda.linux@googlemail.com)
- GUI: fixed the rating logic, to prevent sending BT with rating < 3 (jmoskovc@redhat.com)
- Report GUI: made more fields copyable - closed rhbz#526209; tweaked wording (vda.linux@googlemail.com)
- GUI: fixed bug caused by failed gk-authorization (jmoskovc@redhat.com)

* Fri Jan 29 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.5-1
- moved the gpg key list from abrt.conf to gpg_keys file (jmoskovc@redhat.com)
- Logger: create log file with mode 0600 rhbz#559545 (vda.linux@googlemail.com)
- GUI: fixed the rating logic, to prevent sending BT with rating < 3 (jmoskovc@redhat.com)
- Report GUI: made more fields copyable - closed rhbz#526209; tweaked wording (vda.linux@googlemail.com)
- GUI: fixed bug caused by failed gk-authorization (jmoskovc@redhat.com)
- fix bug 559881 (kerneloops not shown in "new" GUI) (vda.linux@googlemail.com)
- GUI ReporterDialog: hide log button (vda.linux@googlemail.com)
- added valgrind and strace to blacklist (jmoskovc@redhat.com)
- SOSreport: do not leave stray files in /tmp (vda.linux@googlemail.com)
- Save the core where it belongs if ulimit -c is > 0 (jmoskovc@redhat.com)
- reenabled gpg check (jmoskovc@redhat.com)
- SOSreport: run it niced (vda.linux@googlemail.com)
- report GUI: rename buttons: Log -> Show log, Send -> Send report (vda.linux@googlemail.com)
- applet: reduce blinking timeout to 3 sec (vda.linux@googlemail.com)
- fix dbus autostart (vda.linux@googlemail.com)
- abrtd: set "Reported" status only if at least one reporter succeeded (vda.linux@googlemail.com)
- SQLite3: disable newline escaping, SQLite does not handle it (vda.linux@googlemail.com)
- SOSreport: make it avoid double runs; add forced regeneration; upd PLUGINS-HOWTO (vda.linux@googlemail.com)
- attribute SEGVs in perl to script's package, like we already do for python (vda.linux@googlemail.com)

* Wed Jan 20 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.4-1
- enabled sosreport
- fixes in ticketuploader
- GUI: redesign of reporter dialog (jmoskovc@redhat.com)
- Set the prgname to "Automatic Bug Reporting Tool" fixes rhbz#550357 (jmoskovc@redhat.com)
- CCpp analyzer: display __abort_msg in backtrace. closes rhbz#549735 (vda.linux@googlemail.com)
- s/os.exit/sys.exit - closes rhbz#556313 (vda.linux@googlemail.com)
- use repr() to print variable values in python hook rhbz#545070 (jmoskovc@redhat.com)
- gui: add logging infrastructure (vda.linux@googlemail.com)
- Added "Enabled = yes" to all plugin's config files (jmoskovc@redhat.com)
- *: disable plugin loading/unloading through GUI. Document keyring a bit (vda.linux@googlemail.com)
- fix memory leaks in catcut plugin (npajkovs@redhat.com)
- fix memory leaks in bugzilla (npajkovs@redhat.com)
- abrt-hook-python: sanitize input more; log to syslog (vda.linux@googlemail.com)
- Fixed /var/cache/abrt/ permissions (kklic@redhat.com)
- Kerneloops: we require commandline for every crash, save dummy one for oopses (vda.linux@googlemail.com)
- *: remove nss dependencies (vda.linux@googlemail.com)
- CCpp: use our own sha1 implementation (less pain with nss libs) (vda.linux@googlemail.com)
- DebugDump: more consistent logic in setting mode and uid:gid on dump dir (vda.linux@googlemail.com)
- fixes based on security review (vda.linux@googlemail.com)
- SOSreport/TicketUploader: use more restrictive file modes (vda.linux@googlemail.com)
- abrt-hook-python: add input sanitization and directory size guard (vda.linux@googlemail.com)
- RunApp: safer chdir. Overhauled "sparn a child and get its output" in general (vda.linux@googlemail.com)
- DebugDump: use more restrictive modes (vda.linux@googlemail.com)
- SQLite3: check for SQL injection (vda.linux@googlemail.com)
- replace plugin enabling via EnabledPlugins by par-plugin Enabled = yes/no (vda.linux@googlemail.com)
- abrt.spec: move "requires: gdb" to abrt-desktop (vda.linux@googlemail.com)
- ccpp: add a possibility to disable backtrace generation (vda.linux@googlemail.com)
- abrtd: limit the number of frames in backtrace to 3000 (vda.linux@googlemail.com)

* Tue Jan  5 2010  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.3-1
- speed optimalization of abrt-debuginfo-install (jmoskovc@redhat.com)
- updated credits (jmoskovc@redhat.com)
- GUI: fixed crash when abrt-gui is run without X server rhbz#552039 (jmoskovc@redhat.com)
- abrt-backtrace manpage installed (kklic@redhat.com)
- cmdline and daemon checking is done by abrt-python-hook (kklic@redhat.com)
- moved get_cmdline() and daemon_is_ok() to abrtlib (kklic@redhat.com)
- large file support for whole abrt (kklic@redhat.com)
- made s_signal_caught volatile (vda.linux@googlemail.com)
- abrt-debuginfo-install: fixes for runs w/o cachedir (vda.linux@googlemail.com)
- remove unsafe log() from signal handler (vda.linux@googlemail.com)
- src/Hooks/CCpp.cpp: use and honour 'c' (core limit size). (vda.linux@googlemail.com)
- lib/Plugins/CCpp.cpp: save gdb error messages too (vda.linux@googlemail.com)
- prevent destructors from throwing exceptions; check curl_easy_init errors (vda.linux@googlemail.com)
- don't blame python for every crash in /usr/bin/python rhbz#533521 trac#109 (jmoskovc@redhat.com)
- GUI: autoscroll log window (jmoskovc@redhat.com)
- Kerneloops.conf: better comments (vda.linux@googlemail.com)
- applet: reduce blinking time to 30 seconds (vda.linux@googlemail.com)
- add paranoia checks on setuid/setgid (vda.linux@googlemail.com)
- more "obviously correct" code for secure opening of /dev/null (vda.linux@googlemail.com)
- get rid of ugly sleep call inside while() (vda.linux@googlemail.com)

* Mon Dec 14 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.2-1
- disabled GPG check again (jmoskovc@redhat.com)
- abrt-pyhook-helper rename (vda.linux@googlemail.com)
- abrt-cli: report success/failure of reporting. closes bug 71 (vda.linux@googlemail.com)
- less logging (vda.linux@googlemail.com)
- mkde abrt-gui --help and --version behave as expected. closes bug 85 (vda.linux@googlemail.com)
- dbus lib: fix parsing of 0-element arrays. Fixes bug 95 (vda.linux@googlemail.com)
- make "abrt-cli --delete randomuuid" report that deletion failed. closes bug 59 (vda.linux@googlemail.com)
- applet: make animation stop after 1 minute. (closes bug 108) (vda.linux@googlemail.com)
- show comment and how to reproduce fields, when BT rating > 3 (jmoskovc@redhat.com)
- Gui: make report status window's text wrap. Fixes bug 82 (vda.linux@googlemail.com)
- CCpp analyzer: added "info sharedlib" (https://fedorahosted.org/abrt/ticket/90) (vda.linux@googlemail.com)
- added link to bugzilla new account page to Bugzilla config dialog (jmoskovc@redhat.com)
- GUI: added log window (jmoskovc@redhat.com)

* Tue Dec  8 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.1-1
- PyHook: better logic for checking if abrtd is running rhbz#539987 (jmoskovc@redhat.com)
- re-enabled gpg sign checking (jmoskovc@redhat.com)
- PyHook: use repr() for displaying variables rhbz#545070 (jmoskovc@redhat.com)
- kerneloops: fix the linux kernel version identification (aarapov@redhat.com)
- gui review (rrakus@redhat.com)
- when we trim the dir, we must delete it from DB too rhbz#541854 (vda.linux@googlemail.com)
- improved dupe checking (kklic@redhat.com)
- GUI: handle cases when gui fails to start daemon on demand rhbz#543725 (jmoskovc@redhat.com)
- Add abrt group only if it is missing; fixes rhbz#543250 (kklic@redhat.com)
- GUI: more string fixes rhbz#543266 (jmoskovc@redhat.com)
- abrt.spec: straighten out relations between abrt-desktop and abrt-gui (vda.linux@googlemail.com)
- refuse to start if some required plugins are missing rhbz#518422 (vda.linux@googlemail.com)
- GUI: survive gnome-keyring access denial rhbz#543200 (jmoskovc@redhat.com)
- typo fixes rhbz#543266 (jmoskovc@redhat.com)
- abrt-debuginfo-install: better fix for incorrect passing double quotes (vda.linux@googlemail.com)
- APPLET: stop animation when it's not needed rhbz#542157 (jmoskovc@redhat.com)
- ccpp hook: reanme it, and add "crash storm protection" (see rhbz#542003) (vda.linux@googlemail.com)
- Hooks/CCpp.cpp: add MakeCompatCore = yes/no directive. Fixes rhbz#541707 (vda.linux@googlemail.com)
- SPEC: removed sqlite3 package, fixed some update problems (jmoskovc@redhat.com)
- Kerneloops are reported automaticky now when AutoReportUIDs = root is in Kerneloops.conf (npajkovs@redhat.com)
- remove word 'detected' from description rhbz#541459 (vda.linux@googlemail.com)
- src/Hooks/CCpp.cpp: do save abrtd's own coredumps, but carefully... (vda.linux@googlemail.com)
- CCpp.cpp: quote parameters if needed rhbz#540164 (vda.linux@googlemail.com)

* Fri Nov 20 2009  Jiri Moskovcak <jmoskovc@redhat.com> 1.0.0-1
- new version
- comment input wraps words rhbz#531276
- fixed hiding password dialog rhbz#529583
- easier kerneloops reporting rhbz#528395
- made menu entry translatable rhbz#536878 (jmoskovc@redhat.com)
- GUI: don't read the g-k every time we want to use the setting (jmoskovc@redhat.com)
- GUI: survive if g-k access is denied rhbz#534171 (jmoskovc@redhat.com)
- include more info into oops (we were losing the stack dump) (vda.linux@googlemail.com)
- make BZ insert small text attachments inline; move text file detection code (vda.linux@googlemail.com)
- GUI: fixed text wrapping in comment field rhbz#531276 (jmoskovc@redhat.com)
- GUI: added cancel to send dialog rhbz#537238 (jmoskovc@redhat.com)
- include abrt version in bug descriptions (vda.linux@googlemail.com)
- ccpp hook: implemented ReadonlyLocalDebugInfoDirs directive (vda.linux@googlemail.com)
- GUI: added window icon rhbz#537240 (jmoskovc@redhat.com)
- add support for \" escaping in config file (vda.linux@googlemail.com)
- add experimental saving of /var/log/Xorg*.log for X crashes (vda.linux@googlemail.com)
- APPLET: changed icon from default gtk-warning to abrt specific, add animation (jmoskovc@redhat.com)
- don't show icon on abrtd start/stop rhbz#537630 (jmoskovc@redhat.com)
- /var/cache/abrt permissions 1775 -> 0775 in spec file (kklic@redhat.com)
- Daemon properly checks /var/cache/abrt attributes (kklic@redhat.com)
- abrt user group; used by abrt-pyhook-helper (kklic@redhat.com)
- pyhook-helper: uid taken from system instead of command line (kklic@redhat.com)
- KerneloopsSysLog: fix breakage in code which detects abrt marker (vda.linux@googlemail.com)
- GUI: added support for backtrace rating (jmoskovc@redhat.com)
- InformAllUsers support. enabled by default for Kerneloops. Tested wuth CCpp. (vda.linux@googlemail.com)
- abrtd: call res_init() if /etc/resolv.conf or friends were changed rhbz#533589 (vda.linux@googlemail.com)
- supress errors in python hook to not colide with the running script (jmoskovc@redhat.com)

* Tue Nov 10 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.11-2
- spec file fixes

* Mon Nov  2 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.11-1
- re-enabled kerneloops
- abrt-debuginfo-install: download packages one-by-one - better logging (vda.linux@googlemail.com)
- do not report empty fields (vda.linux@googlemail.com)
- Added abrt.png, fixed rhbz#531181 (jmoskovc@redhat.com)
- added option DebugInfoCacheMB to limit size of unpacked debuginfos (vda.linux@googlemail.com)
- fixed the problem with overwriting the default plugin settings (jmoskovc@redhat.com)
- disabled kerneloops in config file (jmoskovc@redhat.com)
- added dependency to gdb >= 7.0 (jmoskovc@redhat.com)
- better format of report text (vda.linux@googlemail.com)
- Python backtrace size limited to 1 MB (kklic@redhat.com)
- lib/Plugins/Bugzilla: better message at login failure (vda.linux@googlemail.com)
- build fixes, added plugin-logger to abrt-desktop (jmoskovc@redhat.com)
- blacklisted nspluginwrapper, because it causes too many useless reports (jmoskovc@redhat.com)
- GUI: Wrong settings window is not shown behind the reporter dialog rhbz#531119 (jmoskovc@redhat.com)
- Normal user can see kerneloops and report it Bugzilla memory leaks fix (npajkovs@redhat.com)
- dumpoops: add -s option to dump results to stdout (vda.linux@googlemail.com)
- removed kerneloops from abrt-desktop rhbz#528395 (jmoskovc@redhat.com)
- GUI: fixed exception when enabling plugin rhbz#530495 (jmoskovc@redhat.com)
- Improved abrt-cli (kklic@redhat.com)
- Added backtrace rating to CCpp analyzer (dnovotny@redhat.com)
- GUI improvements (jmoskovc@redhat.com)
- Added abrt-pyhook-helper (kklic@redhat.com)

* Thu Oct 15 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.10-1
- new version
- added more logging (vda.linux@googlemail.com)
- made polkit policy to be more permissive when installing debuginfo (jmoskovc@redhat.com)
- lib/Plugins/CCpp.cpp: add build-ids to backtrace (vda.linux@googlemail.com)
- lib/Plugins/CCpp.cpp: do not use temp file for gdb commands - use -ex CMD instead (vda.linux@googlemail.com)
- GUI: added refresh button, added sanity check to plugin settings (jmoskovc@redhat.com)
- Initial man page for abrt-cli (kklic@redhat.com)
- Added --version, -V, --help, -? options. Fixed crash caused by unknown option. (kklic@redhat.com)
- Date/time honors current system locale (kklic@redhat.com)
- fixed saving/reading user config (jmoskovc@redhat.com)
- SPEC: added gnome-python2-gnomekeyring to requirements (jmoskovc@redhat.com)
- GUI: call Report() with the latest pluginsettings (jmoskovc@redhat.com)
- Fix Bug 526220 -  [abrt] crash detected in abrt-gui-0.0.9-2.fc12 (vda.linux@googlemail.com)
- removed unsecure reading/writting from ~HOME directory rhbz#522878 (jmoskovc@redhat.com)
- error checking added to archive creation (danny@rawhide.localdomain)
- try using pk-debuginfo-install before falling back to debuginfo-install (vda.linux@googlemail.com)
- abrt-gui: make "report" toolbar button work even if abrtd is not running (vda.linux@googlemail.com)
- set LIMIT_MESSAGE to 16k, typo fix and daemon now reads config information from dbus (npajkovs@redhat.com)
- add support for abrtd autostart (vda.linux@googlemail.com)
- GUI: reversed the dumplist, so the latest crashes are at the top (jmoskovc@redhat.com)
- rewrite FileTransfer to use library calls instead of commandline calls for compression (dnovotny@redhat.com)
- and many minor fixes ..

* Wed Sep 23 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.9-2
- added bug-buddy to provides rhbz#524934

* Tue Sep 22 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.9-1
- new version
- comments and how to reproduce are stored now (npajkovs@redhat.com)
- reduce verbosity a bit (vda.linux@googlemail.com)
- GUI: fixed word wrap in Comment field rhbz#524349 (jmoskovc@redhat.com)
- remove last vestives of dbus-c++ from build system (vda.linux@googlemail.com)
- GUI: added popup menu, fixed behaviour when run with root privs (jmoskovc@redhat.com)
- add dbus signalization when quota exceeded (npajkovs@redhat.com)
- Added cleaning of attachment variable, so there should not be mixed attachmetn anymore. (zprikryl@redhat.com)
- fixed closing of debug dump in case of existing backtrace (zprikryl@redhat.com)
- remove C++ dbus glue in src/CLI; fix a bug in --report (vda.linux@googlemail.com)
- new polkit action for installing debuginfo, default "yes" (danny@rawhide.localdomain)
- Polkit moved to Utils (can be used both in daemon and plugins) (danny@rawhide.localdomain)
- oops... remove stray trailing '\' (vda.linux@googlemail.com)
- GUI: added missing tooltips (jmoskovc@redhat.com)
- PYHOOK: ignore KeyboardInterrupt exception (jmoskovc@redhat.com)
- added ticket uploader plugin (gavin@redhat.com) (zprikryl@redhat.com)
- GUI: added UI for global settings (just preview, not usable!) (jmoskovc@redhat.com)
- Add checker if bugzilla login and password are filled in. (npajkovs@redhat.com)
- Add new config option InstallDebuginfo into CCpp.conf (npajkovs@redhat.com)
- translation updates
- many other fixes

* Fri Sep  4 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.8.5-1
- new version
- APPLET: added about dialog, removed popup, if icon is not visible, fixed (trac#43) (jmoskovc@redhat.com)
- renamed abrt to abrtd, few minor spec file fixes (jmoskovc@redhat.com)
- Made abrt service start by deafult (jmoskovc@redhat.com)
- add gettext support for all plugins (npajkovs@redhat.com)
- APPLET: removed the warning bubble about not running abrt service (walters)
- APPLET: changed tooltip rhbz#520293 (jmoskovc@redhat.com)
- CommLayerServerDBus: rewrote to use dbus, not dbus-c++ (vda.linux@googlemail.com)
- fixed timeout on boot causing [ FAILED ] message (vda.linux@googlemail.com)
- and many other fixes

* Wed Sep 02 2009  Colin Walters <watlers@verbum.org> 0.0.8-2
- Change Conflicts: kerneloops to be an Obsoletes so we do the right thing
  on upgrades.  Also add an Obsoletes: bug-buddy.

* Wed Aug 26 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.8-1
- new version
- resolved: Bug 518420 -  ordinary user's abrt-applet shows up for root owned crashes (npajkovs)
- GUI: added support for gettext (+part of czech translation) (jmoskovc)
- added support for saving settings (zprikryl)
- fixed conf: comment in the middle of the line isn't supported anymore (zprikryl)
- BZ#518413 PATCH ... furious kerneloops reporting (aarapov)
- GUI: added first part of support for gettext (jmoskovc)
- add new parameter to FileTransfer plugin (dnovotny)
- added support for updating abrt's table (zprikryl)
- added check for cc-list and reporter. +1 is created iff reporter is somebody else and current user isn't in cc list. (zprikryl)
- GUI: few improvements, to be more userfriendly (jmoskovc)
- LOGGER: return valid uri of the log file on succes (jmoskovc)
- GUI: bring the GUI up to front instead of just blinking in taskbar (trac#60, rhbz#512390) (jmoskovc)
- Try to execute $bindir/abrt-gui, then fall back to $PATH search. Closes bug 65 (vda.linux)
- APPLET: added popup menu (trac#37, rhbz#518386) (jmoskovc)
- Improved report results (zprikryl)
- Fixed sigsegv (#rhbz 518609) (zprikryl)
- GUI: removed dependency on libsexy if gtk2 >= 2.17 (jmoskovc)
- fixed signature check (zprikryl)
- KerneloopsSysLog: check line length to be >= 4 before looking for "Abrt" (vda.linux)
- Comment cannot start in the middle of the line. Comment has to start by Char # (first char in the line) (zprikryl)
- command mailx isn't run under root anymore. (zprikryl)
- GUI: added horizontal scrolling to report window (jmoskovc)
- GUI: added clickable link to "after report" status window (jmoskovc)
- added default values for abrt daemon (zprikryl)
- Plugins/CCpp: remove trailing \n from debuginfo-install's output (vda.linux)
- explain EnableGPGCheck option better (vda.linux)
- mailx: correct English (vda.linux)
- Bugzilla.conf: correct English (vda.linux)
- GUI: nicer after report message (jmoskovc)
- BZ plugin: removed /xmlrpc.cgi from config, made the report message more user friendly (jmoskovc)
- CCpp plugin: do not abort if debuginfos aren't found (vda.linux)
- abrt.spec: bump version to 0.0.7-2 (vda.linux)
- mailx removed dangerous parameter option (zprikryl)
- minimum timeout is 1 second (zprikryl)
- in case of plugin error, don't delete debug dumps (zprikryl)
- abrt-gui: fix crash when run by root (vda.linux)
- and lot more in git log ...

* Thu Aug 20 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.7.2-1
- new version
- fixed some bugs found during test day

* Wed Aug 19 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.7.1-1
- fixes to bugzilla plugin and gui to make the report message more user-friendly

* Tue Aug 18 2009  Denys Vlasenko <dvlasenk@redhat.com> 0.0.7-2
- removed dangerous parameter option
- minimum plugin activation period is 1 second
- in case of plugin error, don't delete debug dumps
- abrt-gui: fix crash when run by root
- simplify parsing of debuginfo-install output

* Tue Aug 18 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.7-1
- new version
- added status window to show user some info after reporting a bug

* Mon Aug 17 2009  Denys Vlasenko <dvlasenk@redhat.com> 0.0.6-1
- new version
- many fixes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.4-3
- fixed dependencies in spec file

* Tue Jun 16 2009 Daniel Novotny <dnovotny@redhat.com> 0.0.4-2
- added manual pages (also for plugins)

* Mon Jun 15 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.4-1
- new version
- added cli (only supports sockets)
- added python hook
- many fixes

* Fri Apr 10 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.3-1
- new version
- added bz plugin
- minor fix in reporter gui
- Configurable max size of debugdump storage rhbz#490889
- Wrap lines in report to keep the window sane sized
- Fixed gui for new daemon API
- removed unneeded code
- removed dependency on args
- new guuid hash creating
- fixed local UUID
- fixed debuginfo-install checks
- renamed MW library
- Added notification thru libnotify
- fixed parsing settings of action plugins
- added support for action plugins
- kerneloops - plugin: fail gracefully.
- Added commlayer to make dbus optional
- a lot of kerneloops fixes
- new approach for getting debuginfos and backtraces
- fixed unlocking of a debugdump
- replaced language and application plugins by analyzer plugin
- more excetpion handling
- conf file isn't needed
- Plugin's configuration file is optional
- Add curl dependency
- Added column 'user' to the gui
- Gui: set the newest entry as active (ticket#23)
- Delete and Report button are no longer active if no entry is selected (ticket#41)
- Gui refreshes silently (ticket#36)
- Added error reporting over dbus to daemon, error handling in gui, about dialog

* Wed Mar 11 2009  Jiri Moskovcak <jmoskovc@redhat.com> 0.0.2-1
- added kerneloops addon to rpm (aarapov)
- added kerneloops addon and plugin (aarapov)
- Made Crash() private
- Applet requires gui, removed dbus-glib deps
- Closing stdout in daemon rhbz#489622
- Changed applet behaviour according to rhbz#489624
- Changed gui according to rhbz#489624, fixed dbus timeouts
- Increased timeout for async dbus calls to 60sec
- deps cleanup, signal AnalyzeComplete has the crashreport as an argument.
- Fixed empty package Description.
- Fixed problem with applet tooltip on x86_64

* Wed Mar  4 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-13
- More renaming issues fixed..
- Changed BR from gtkmm24 to gtk2
- Fixed saving of user comment
- Added a progress bar, new Comment entry for user comments..
- FILENAME_CMDLINE and FILENAME_RELEASE are optional
- new default path to DB
- Rename to abrt

* Tue Mar  3 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-12
- initial fedora release
- changed SOURCE url
- added desktop-file-utils to BR
- changed crash-catcher to %%{name}

* Mon Mar  2 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-11
- more spec file fixes according to review
- async dbus method calls, added exception handler
- avoid deadlocks (zprikryl)
- root is god (zprikryl)
- create bt only once (zprikryl)

* Sat Feb 28 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-10
- New gui
- Added new method DeleteDebugDump to daemon
- Removed gcc warnings from applet
- Rewritten CCpp hook and removed dealock in DebugDumps lib (zprikryl)
- fixed few gcc warnings
- DBusBackend improvements

* Fri Feb 27 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-9
- fixed few gcc warnings
- added scrolled window for long reports

* Thu Feb 26 2009 Adam Williamson <awilliam@redhat.com> 0.0.1-8
- fixes for all issues identified in review

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-7
- Fixed cancel button behaviour in reporter
- disabled core file sending
- removed some debug messages

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-6
- fixed DB path
- added new signals to handler
- gui should survive the dbus timeout

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-5
- fixed catching debuinfo install exceptions
- some gui fixes
- added check for GPGP public key

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-4
- changed from full bt to simple bt

* Thu Feb 26 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-3
- spec file cleanups
- changed default paths to crash DB and log DB
- fixed some memory leaks

* Tue Feb 24 2009 Jiri Moskovcak <jmoskovc@redhat.com> 0.0.1-2
- spec cleanup
- added new subpackage gui

* Wed Feb 18 2009 Zdenek Prikryl <zprikryl@redhat.com> 0.0.1-1
- initial packing
