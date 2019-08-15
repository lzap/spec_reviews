Name: HdrHistogram_c
Version: 0.9.11
Release: 1%{?dist}
Summary: C port of the HdrHistogram 
License: BSD 2 and Public Domain
URL: https://github.com/HdrHistogram/%{name}
Source0: https://github.com/HdrHistogram/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake

%description
C port of High Dynamic Range (HDR) Histogram.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}


%build
%cmake .
%make_build


%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE.txt
%doc README.md
%exclude %{_bindir}/hiccup
%exclude %{_bindir}/hdr_decoder
%exclude %{_bindir}/perftest
%exclude %{_bindir}/hdr_histogram_log_test
%exclude %{_bindir}/hdr_histogram_test
%{_libdir}/libhdr_histogram.so.3.1.2
%{_libdir}/libhdr_histogram.so.3

%files devel
%{_includedir}/hdr/hdr_thread.h
%{_includedir}/hdr/hdr_interval_recorder.h
%{_includedir}/hdr/hdr_writer_reader_phaser.h
%{_includedir}/hdr/hdr_time.h
%{_includedir}/hdr/hdr_histogram_log.h
%{_includedir}/hdr/hdr_histogram.h
%{_libdir}/libhdr_histogram.so

%changelog
* Wed Aug 14 2019 Lukáš Zapletal 0.9.11-1
- Initial package version
