%if 0%{?rhel} && 0%{?rhel} == 5
  %{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
  %{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:       pagekite
Version:    0.5.5a
Release:    3%{?dist}
Summary:    Makes localhost servers visible to the world

Group:      Development/Libraries
License:    AGPLv3+
Url:        http://pagekite.org/
Source0:    http://pagekite.net/pk/src/%{name}-%{version}.tar.gz
Source1:    %{name}.service

%if 0%{?rhel} && 0%{?rhel} == 5
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

BuildArch:  noarch

Requires:   python-SocksipyChain
Requires:   setup
Requires(postun): initscripts

BuildRequires: python2-devel

%if 0%{?fedora} >= 18
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

BuildRequires: systemd
%endif

%description
System for running publicly visible servers (generally web servers) on machines
without a direct connection to the Internet, such as mobile devices or
computers behind restrictive firewalls. It works around NAT, firewalls and
IP-address limitations by using a combination of  tunnels and reverse proxies.

Natively supported protocols: HTTP, HTTPS
Partially supported protocols: IRC, Finger

Any other TCP-based service, including SSH and VNC, may be exposed as well to
clients supporting HTTP Proxies.


%prep
%setup -q

%build

%install
%if 0%{?rhel} && 0%{?rhel} == 5
  %{__rm} -rf $RPM_BUILD_ROOT
%endif

install -d $RPM_BUILD_ROOT%{python_sitelib}/%{name}
install -d $RPM_BUILD_ROOT%{python_sitelib}/%{name}/proto
install -d $RPM_BUILD_ROOT%{python_sitelib}/%{name}/ui
install -pm 0644 %{name}/*py $RPM_BUILD_ROOT%{python_sitelib}/%{name}/
install -pm 0644 %{name}/proto/*py $RPM_BUILD_ROOT%{python_sitelib}/%{name}/proto/
install -pm 0644 %{name}/ui/*py $RPM_BUILD_ROOT%{python_sitelib}/%{name}/ui/

install -Dpm 0755 scripts/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

install -Dpm 0644 etc/sysconfig/%{name}.fedora $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -Dpm 0644 etc/sysconfig/%{name}.fedora $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -Dpm 0644 etc/logrotate.d/%{name}.fedora $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}
%if 0%{?rhel} && 0%{?rhel} <= 6
  install -Dpm 0755 etc/init.d/%{name}.fedora $RPM_BUILD_ROOT%{_initrddir}/%{name}
%else
  install -Dpm 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
%endif

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/
install -Dpm 0644 etc/%{name}.d/* $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/
install -Dpm 0600 etc/%{name}.d/10_account.rc $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.d/

install -Dpm 0644 doc/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

install -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/log/%{name}

# remove shebangs from library files
for lib in $RPM_BUILD_ROOT%{python_sitelib}/%{name}/*.py \
    $RPM_BUILD_ROOT%{python_sitelib}/%{name}/proto/*.py \
    $RPM_BUILD_ROOT%{python_sitelib}/%{name}/ui/*.py ; do
  sed '1{\@^#!/usr/bin/python.*@d}' $lib > $lib.new &&
  touch -r $lib $lib.new &&
  mv $lib.new $lib
done

%if 0%{?rhel} && 0%{?rhel} == 5
%clean
%{__rm} -rf $RPM_BUILD_ROOT
%endif


%post
%if 0%{?rhel} && 0%{?rhel} <= 6
  /sbin/chkconfig --add %{name}
%else
  %systemd_post %{name}.service
%endif


%preun
%if 0%{?rhel} && 0%{?rhel} <= 6
  if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
  fi
%else
  %systemd_preun %{name}.service
%endif


%postun
%if 0%{?rhel} && 0%{?rhel} <= 6
  if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
  fi
%else
  %systemd_postun_with_restart %{name}.service
%endif


%files
%defattr(-,root,root,-)
%doc COPYING README.md TODO.md
%{python_sitelib}/%{name}/
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%if 0%{?rhel} && 0%{?rhel} <= 6
  %{_initrddir}/%{name}
%else
  %{_unitdir}/%{name}.service
%endif
%{_sysconfdir}/logrotate.d/%{name}
%attr(660,root,root) %config(noreplace) %{_sysconfdir}/%{name}.d/*
%{_mandir}/man1/%{name}.1*
%{_localstatedir}/log/%{name}


%changelog
* Tue Mar 19 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.5.5a-3
- package review items

* Wed Feb 20 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.5.5a-2
- Initial review
- Removed lapcat from the distribution

* Fri Feb 08 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.5.5a-1
- Initial version.
