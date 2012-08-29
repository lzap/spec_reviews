%define githubuser knopwob
%define gitlast g63ceed3
%define gitdir c4b2274

Name:     dunst
Version:  0.3.1 
Release:  1%{?dist}
Summary:  Dmenu-ish lightweight notification-daemon
Group:    User Interface/X
License:  BSD
URL:      http://github.com/knopwob/dunst
Source0:  http://github.com/knopwob/dunst/tarball/v%{version}/%{githubuser}-%{name}-v%{version}-0-%{gitlast}.tar.gz

Requires: dbus

BuildRequires: libX11-devel
BuildRequires: libXinerama-devel
BuildRequires: libXft-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libxdg-basedir-devel
BuildRequires: dbus-devel

%description
Dunst is a lightweight notification-daemon for the libnotify. It displays
messages received via dbus or as command line argument in a fashion similar
to dmenu.


%prep
%setup -q -n %{githubuser}-%{name}-%{gitdir}


%build
make %{?_smp_mflags} VERSION=%{version} PREFIX=%{_prefix}


%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}


%files
%doc AUTHORS CHANGELOG LICENSE README.pod
%{_bindir}/%{name}
%{_datadir}/dbus-1/services/org.%{githubuser}.%{name}.service
%{_datadir}/%{name}/dunstrc
%{_datadir}/man/man1/%{name}.1.gz

%changelog
* Mon Aug 27 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.3.1-1
- initial version
