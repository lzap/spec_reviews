Name: chan
Version: 0.0.4
Release: 1%{?dist}
Summary: Pure C implementation of Go channels
License: ASL 2.0
URL: https://github.com/tylertreat/%{name}
Source0: https://github.com/tylertreat/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: autoconf automake libtool
#Requires:       

%description
Pure C implementation of Go channels. Unbuffered, buffered
and closing channels are available.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}


%build
./autogen.sh
%configure --disable-static
%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%doc README.md
%{_libdir}/lib%{name}.so.0.0.0
%{_libdir}/lib%{name}.so.0

%files devel
%{_includedir}/%{name}/queue.h
%{_includedir}/%{name}/%{name}.h
%{_libdir}/lib%{name}.so


%changelog
* Wed Aug 14 2019 Lukáš Zapletal 0.0.4-1
- Initial package version
