%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"] ')}
%{!?ruby_sitearch: %global ruby_sitearch %(ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}
%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname virt
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: Simple to use ruby interface to libvirt
Name: rubygem-%{gemname}
Version: 0.1.0
Release: 2%{?dist}
Group: Development/Languages
License: GPLv3
URL: https://github.com/ohadlevy/virt
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

Requires: rubygems
Requires: ruby-libvirt
BuildRequires: rubygems

Provides: rubygem(%{gemname}) = %{version}

%description
Simplified interface to use ruby the libvirt ruby library.


%prep


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
gem install --local --install-dir %{buildroot}%{gemdir} \
            --force --rdoc %{SOURCE0}

# there is a .document hidden file being distributed
find %{buildroot}/ -name .document -print0 | xargs -0 /bin/rm -f


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%{geminstdir}
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/LICENSE.txt
%doc %{geminstdir}/README.rdoc
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec


%changelog
* Thu Oct 06 2011 Lukas Zapletal <lzap+rpm[@]redhat.com> - 0.1.0-2
- Fixed spec

* Mon Jan 31 2011 Lukáš Zapletal <lzap+spam@redhat.com> - 0.1.0-1
- Initial package
