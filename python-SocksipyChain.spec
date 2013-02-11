%if 0%{?rhel} && 0%{?rhel} <= 5
  %{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
  %{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%define canonicalname SocksipyChain

Name:       python-%{canonicalname}
Version:    2.0.12
Release:    1
Summary:    A Python SOCKS/HTTP Proxy module

Group:      Development/Libraries
License:    BSD
Url:        http://github.com/pagekite/Py%{canonicalname}
Source0:    http://pagekite.net/pk/src/%{canonicalname}-%{version}.tar.gz

%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

BuildArch:  noarch

BuildRequires:  python-devel


%description
This Python module allows you to create TCP connections through a chain
of SOCKS or HTTP proxies without any special effort. It also supports
TLS/SSL encryption if the OpenSSL modules are installed.


%prep
%setup -q -n %{canonicalname}-%{version}


%build


%install
install -Dpm 0755 sockschain/__init__.py $RPM_BUILD_ROOT%{python_sitelib}/sockschain/__init__.py


%if 0%{?rhel} && 0%{?rhel} <= 5
%clean
%{__rm} -rf $RPM_BUILD_ROOT
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE README.md BUGS
%{python_sitelib}/sockschain

%changelog
* Fri Feb 08 2013 Lukas Zapletal <lzap+rpm[@]redhat.com> - 2.0.12-1
- Initial version.
