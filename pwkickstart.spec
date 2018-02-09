%global gittag 1.0.0
%global commit efaa360b7c4d4fe8ef9f673ebcf2295e066c523e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global debug_package %{nil}

Name: pwkickstart
Version: 1.0.0
Release: 1%{?dist}
Summary: Helps to generate kickstart passwords
License: MIT
URL: https://github.com/lzap/pwkickstart
Source0: https://github.com/lzap/%{name}/archive/%{gittag}.tar.gz

Requires:	python

%description
Helps to generate kickstart passwords, similarly to grub-crypt tool.

%prep
%autosetup -n %{name}-%{gittag}

%build
# blank

%install
install -m 755 -D %{name} %{buildroot}/%{_bindir}/%{name}

%files
%{_bindir}/%{name}
%license LICENSE

%changelog

