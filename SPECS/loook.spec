Name:       loook
Version:    0.6.7
Release:    4%{?dist}
Summary:    OpenOffice.org document search tool

Group:      Applications/Text
License:    GPLv2+
URL:        http://www.danielnaber.de/loook/
Source0:    http://www.danielnaber.de/loook/%{name}-%{version}.zip
Source1:    %{name}.desktop

Patch0:     %{name}-python3-env.patch
Patch1:     %{name}-manpage.patch

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:  noarch

Requires:   python3-tkinter
Requires:   hicolor-icon-theme

BuildRequires:  python3-devel


%description
Loook is a simple Python tool that searches for text strings in OpenOffice.org
(and StarOffice 6.0 or later) files. It works under Linux, Windows and
Macintosh. AND, OR and phrase searches are supported. It doesn't create an
index, but searching should be fast enough unless you have really many files.


%prep
%setup -q -c
%patch0 -p1
%patch1 -p1


%build


%install
%{__rm} -rf $RPM_BUILD_ROOT
install -Dpm 0755 %{name}.py $RPM_BUILD_ROOT%{python3_sitelib}/%{name}/%{name}.py
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -s %{python3_sitelib}/%{name}/%{name}.py $RPM_BUILD_ROOT%{_bindir}/%{name}
install -Dpm 0644 %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING
%{python3_sitelib}/%{name}/
%{_mandir}/man1/%{name}.1*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop


%changelog
* Thu Nov 11 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 0.6.7-4
- Fixing issues reported by Hans de Goede
- Desktop icon properly added
* Thu Nov 11 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 0.6.7-3
- Fixing issues reported by Thomas Spura
* Thu Nov 04 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 0.6.7-2
- Fixing issues reported by Thomas Spura
* Thu Nov 04 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 0.6.7-1
- Initial package
