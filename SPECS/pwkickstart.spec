%global gittag 1.0.2
%global debug_package %{nil}

Name: pwkickstart
Version: 1.0.2
Release: 1%{?dist}
Summary: Helps to generate kickstart passwords
License: MIT
URL: https://github.com/lzap/pwkickstart
Source0: https://github.com/lzap/%{name}/archive/%{gittag}.tar.gz

Requires:	python3
Requires:	txt2man

%description
Helps to generate kickstart passwords, similarly to grub-crypt tool.

%prep
%autosetup -n %{name}-%{gittag}

%build
txt2man -t %{name} -r %{version} -s 1 README > %{name}.1

%install
install -m 755 -D %{name} %{buildroot}/%{_bindir}/%{name}
install -m 644 -D %{name}.1 %{buildroot}/%{_mandir}/man1/%{name}.1

%files
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%license LICENSE

%changelog
* Mon Feb 12 2018 Lukas Zapletal <lzap+rpm@redhat.com> 1.0.2-1
- Rebased to new upstream version
- Changed to python3 explicit dependency

* Mon Feb 12 2018 Lukas Zapletal <lzap+rpm@redhat.com> 1.0.1-1
- Initial version
