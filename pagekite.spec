%if 0%{?rhel} && 0%{?rhel} <= 5
  %{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
  %{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:       pagekite
Version:    0.5.5a
Release:    1
Summary:    PageKite makes localhost servers visible to the world

Group:      Development/Libraries
License:    AGPLv3+
Url:        http://pagekite.org/
Source0:    http://pagekite.net/pk/src/%{name}-%{version}.tar.gz

%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

BuildArch:  noarch

Requires:   python-SocksipyChain
Requires(postun): initscripts

BuildRequires:  python-devel

%description
PageKite is a system for running publicly visible servers (generally
web servers) on machines without a direct connection to the Internet,
such as mobile devices or computers behind restrictive firewalls.
PageKite works around NAT, firewalls and IP-address limitations by
using a combination of  tunnels and reverse proxies.

Natively supported protocols: HTTP, HTTPS
Partially supported protocols: IRC, Finger

Any other TCP-based service, including SSH and VNC, may be exposed
as well to clients supporting HTTP Proxies.


%prep
%setup -q

%build

%install
%if 0%{?rhel} && 0%{?rhel} <= 5
  %{__rm} -rf $RPM_BUILD_ROOT
%endif

install -d $RPM_BUILD_ROOT%{python_sitelib}/%{name}
install -d $RPM_BUILD_ROOT%{python_sitelib}/%{name}/proto
install -d $RPM_BUILD_ROOT%{python_sitelib}/%{name}/ui
install -pm 0644 %{name}/*py $RPM_BUILD_ROOT%{python_sitelib}/%{name}/
install -pm 0644 %{name}/proto/*py $RPM_BUILD_ROOT%{python_sitelib}/%{name}/proto/
install -pm 0644 %{name}/ui/*py $RPM_BUILD_ROOT%{python_sitelib}/%{name}/ui/

install -Dpm 0755 scripts/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}
install -Dpm 0755 scripts/lapcat $RPM_BUILD_ROOT%{_bindir}/lapcat

install -Dpm 0644 etc/sysconfig/%{name}.fedora $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -Dpm 0644 etc/sysconfig/%{name}.fedora $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/%{name}
install -Dpm 0755 etc/init.d/%{name}.fedora $RPM_BUILD_ROOT%{_initrddir}/%{name}
install -Dpm 0644 etc/logrotate.d/%{name}.fedora $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/pagekite.d/default/
install -Dpm 0644 etc/pagekite.d/* $RPM_BUILD_ROOT%{_sysconfdir}/pagekite.d/default/
install -Dpm 0600 etc/pagekite.d/10_account.rc $RPM_BUILD_ROOT%{_sysconfdir}/pagekite.d/default/

install -Dpm 0644 doc/%{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1
install -Dpm 0644 doc/lapcat.1 $RPM_BUILD_ROOT%{_mandir}/man1/lapcat.1

install -d -m 0755 $RPM_BUILD_ROOT/%{_localstatedir}/log/pagekite


%if 0%{?rhel} && 0%{?rhel} <= 5
%clean
%{__rm} -rf $RPM_BUILD_ROOT
%endif


%post
/sbin/chkconfig --add %{name}


%preun
if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi


%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING README.md TODO.md
%{python_sitelib}/%{name}/
%{_bindir}/%{name}
%{_bindir}/lapcat
%{_sysconfdir}/sysconfig/%{name}
%{_initrddir}/%{name}
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/pagekite.d/default/*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/lapcat.1*
%{_localstatedir}/log/pagekite


%changelog
* Fri Feb 08 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.5.5a-1
- Initial version.
