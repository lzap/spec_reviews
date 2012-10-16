Name:     inih-devel
Version:  r26
Release:  1%{?dist}
Summary:  Simple INI file parser

Group:    Development/Libraries
License:  BSD
URL:      http://inih.googlecode.com/
Source0:  http://inih.googlecode.com/files/inih_%{version}.zip
Provides: inih-static = %{version}-%{release}

%description
The inih package provides simple INI file parser which is only a couple of
pages of code, and it was designed to be small and simple, so it's good for
embedded systems.


%prep
%setup -q -c inih


%build
pushd extra
make -f Makefile.static %{?_smp_mflags} EXTRACFLAGS="%{optflags}"
popd


%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install -m 644 ini.h %{buildroot}%{_includedir}/ini.h
install -m 644 extra/libinih.a %{buildroot}%{_libdir}/libinih.a


%files
%doc LICENSE.txt README.txt
%{_includedir}/ini.h
%{_libdir}/libinih.a


%changelog
* Wed Oct 10 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - r26-1
- initial version
