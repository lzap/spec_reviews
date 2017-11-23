Name:     dunst
Version:  1.2.0
Release:  1%{?dist}
Summary:  Simple and configurable notification-daemon
Group:    User Interface/X
License:  BSD and MIT
URL:      https://dunst-project.org
Source0:  %{name}-%{version}.tar.gz

Requires: dbus

BuildRequires: libX11-devel
BuildRequires: libXinerama-devel
BuildRequires: libXft-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libxdg-basedir-devel
BuildRequires: pango-devel
BuildRequires: gtk2-devel
BuildRequires: dbus-devel
BuildRequires: /usr/bin/pod2man
BuildRequires: systemd

%description
Dunst is a highly configurable and lightweight notification daemon with the
similar look and feel to dmenu.


%prep
%setup -q


%build
make %{?_smp_mflags} VERSION=%{version} PREFIX=%{_prefix} EXTRACFLAGS="%{optflags}"


%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}


%files
%doc AUTHORS CHANGELOG.md LICENSE README.md RELEASE_NOTES
%{_bindir}/%{name}
%{_datadir}/dbus-1/services/org.knopwob.%{name}.service
%{_userunitdir}/%{name}.service
%{_datadir}/%{name}
%{_datadir}/man/man1/%{name}.1.gz

%changelog
* Mon Jan 28 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.5.0-1
- version bump
- inih library is no longer required

* Mon Sep 03 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.3.1-3
- package review

* Wed Aug 29 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.3.1-2
- package review

* Mon Aug 27 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.3.1-1
- initial version
