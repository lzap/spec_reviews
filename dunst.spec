%global githubuser knopwob
%global gitlast g63ceed3
%global gitdir c4b2274

Name:     dunst
Version:  0.3.1
Release:  3%{?dist}
Summary:  Simple and configurable notification-daemon
Group:    User Interface/X
License:  BSD and MIT
URL:      http://github.com/knopwob/dunst
Source0:  http://github.com/knopwob/dunst/tarball/v%{version}/%{githubuser}-%{name}-v%{version}-0-%{gitlast}.tar.gz
Patch0:   %{name}-fedoraflags.patch

Requires: dbus

BuildRequires: libX11-devel
BuildRequires: libXinerama-devel
BuildRequires: libXft-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libxdg-basedir-devel
BuildRequires: dbus-devel

%description
Dunst is a highly configurable and lightweight notification daemon with the
similar look and feel to dmenu.


%prep
%setup -q -n %{githubuser}-%{name}-%{gitdir}

# until EXTRACFLAGS is added upstream, see https://github.com/knopwob/dunst/issues/56
%patch0 -p1


%build
make %{?_smp_mflags} VERSION=%{version} PREFIX=%{_prefix} EXTRACFLAGS="%{optflags}"


%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}


%files
%doc AUTHORS CHANGELOG LICENSE README.pod
%{_bindir}/%{name}
%{_datadir}/dbus-1/services/org.%{githubuser}.%{name}.service
%{_datadir}/%{name}
%{_datadir}/man/man1/%{name}.1.gz

%changelog
* Mon Sep 03 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.3.1-3
- package review

* Wed Aug 29 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.3.1-2
- package review

* Mon Aug 27 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.3.1-1
- initial version
