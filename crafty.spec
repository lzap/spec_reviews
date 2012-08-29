%global         debug_package %{nil}

Name:           crafty
Version:        23.3
Release:        1%{?dist}
Summary:        Advanced shortcut bar written in Mono

Group:          Amusements/Games
License:        GPL????
URL:            http://www.craftychess.com/
Source0:        ftp://ftp.cis.uab.edu/pub/hyatt/source/crafty-%{version}.zip

#Patch0:         %{name}-%{version}-nozoom.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


Requires:       gnome-sharp gtk-sharp2 gnome-desktop-sharp
Requires:       gnome-keyring-sharp gtk-sharp2-gapi mono-addins
Requires:       mono ndesk-dbus ndesk-dbus-glib
Requires:       notify-sharp gio-sharp
Requires:       glib2 gtk2

BuildRequires:  autoconf automake libtool
# sharp deps
BuildRequires:  gnome-sharp-devel gtk-sharp2-devel gnome-desktop-sharp-devel
BuildRequires:  gnome-keyring-sharp-devel gtk-sharp2-gapi mono-addins-devel
BuildRequires:  mono-devel ndesk-dbus-devel ndesk-dbus-glib-devel
BuildRequires:  notify-sharp-devel gio-sharp-devel
# native deps
BuildRequires:  python2-devel
BuildRequires:  glib2-devel gtk2-devel
BuildRequires:  gettext
BuildRequires:  perl-XML-Parser
BuildRequires:  intltool
BuildRequires:  desktop-file-utils



%description
Docky is an advanced shortcut bar that sits at the bottom, top, and/or sides 
of your screen. It provides easy access to some of the files, folders, 
and applications on your computer, displays which applications are 
currently running, holds windows in their minimized state, and more.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files
for developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .nozoom


%build
%configure
make %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
make install DESTDIR=$RPM_BUILD_ROOT
desktop-file-install    \
        --dir $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart       \
        --add-only-show-in=GNOME                                \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
desktop-file-install --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%find_lang %{name}


%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT
%{_bindir}/%{name}/
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/*/apps/gmail.png
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/applications/*.desktop
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{name}.desktop
%{python_sitelib}/%{name}


%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/docky.cairohelper.pc
%{_libdir}/pkgconfig/docky.services.pc
%{_libdir}/pkgconfig/docky.widgets.pc
%{_libdir}/pkgconfig/docky.items.pc
%{_libdir}/pkgconfig/docky.windowing.pc


%changelog
* Mon Sep 06 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.6-1
- Initial package
