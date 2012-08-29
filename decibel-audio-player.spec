Summary:	Music player for GNOME
Name:		decibel-audio-player
Version:	1.08
Release:	5%{?dist}
License:	GPLv2+
Group:		Applications/Multimedia
URL:		http://decibel.silent-blade.org/
Source0:	http://decibel.silent-blade.org/uploads/Main/%{name}-%{version}.tar.gz

Requires:	dbus-python
Requires:	gnome-python2-gnome
Requires:	gnome-python2-gnomekeyring
Requires:	gstreamer-python
Requires:	hicolor-icon-theme
Requires:	notify-python
Requires:	python-imaging
Requires:	python-CDDB
Requires:	python-mutagen

BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildArch:	noarch

%description
Decibel is an audio player that aims at being very straightforward to use by
means of a very clean and user friendly interface. It is especially targeted
at GNOME and will follow, as closely as possible, the GNOME HIG. It makes use
of the GStreamer library to read audio files.

%prep
%setup -q

# Suppress rpmlint error.
sed --in-place --expression '1d' ./src/%{name}.py

%build

%install
for S in 16 24 32 48 64 128; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${S}x${S}/apps
done

make install prefix=%{_prefix} INSTALL="install -p" \
  DESTDIR=$RPM_BUILD_ROOT

# workaround for https://bugs.launchpad.net/decibel-audio-player/+bug/910644
cat start.sh | sed -e "s!prefix!%{_prefix}!g" > $RPM_BUILD_ROOT%{_bindir}/%{name}
cat start-remote.sh | sed -e "s!prefix!%{_prefix}!g" > $RPM_BUILD_ROOT%{_bindir}/%{name}-remote

%find_lang %{name}

# icon
for S in 16 24 32 64 128; do
  install -p -m644 $RPM_BUILD_ROOT%{_datadir}/%{name}/pix/%{name}-$S.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${S}x${S}/apps/%{name}.png
done
install -p -m644 $RPM_BUILD_ROOT%{_datadir}/%{name}/pix/%{name}.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

desktop-file-install --delete-original \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :

if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc doc/ChangeLog
%doc doc/LICENCE
%{_bindir}/%{name}
%{_bindir}/%{name}-remote
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-remote.1*

%{_datadir}/%{name}

%changelog
* Fri Apr 18 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.08-5
- changing name of the desktop file according to guidelines
- making macros consistent

* Tue Apr 15 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.08-4
- correcting BR

* Thu Apr 10 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.08-3
- changelog fixed, install macro no longer used
- removed "sed" from BR

* Thu Apr 10 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.08-2
- defattr dropped, variables fixed
- using loop for some tasks in the spec
- man pages marked as doco

* Sun Jan 01 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 1.08-1
- Version bump to 1.08

* Wed Aug 11 2010 Debarshi Ray <rishi@fedoraproject.org> - 1.05-1
- Version bump to 1.05. (Red Hat Bugzilla #608398)

* Sun May 23 2010 Debarshi Ray <rishi@fedoraproject.org> - 1.04-1
- Version bump to 1.04. (Red Hat Bugzilla #521476)
- Updated the desktop database and icon cache scriptlet snippets according to
  Fedora packaging guidelines.

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 1.00-3
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 1.00-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 1.00-1
- Version bump to 1.00. (Red Hat Bugzilla #477262)
  * http://decibel.silent-blade.org/index.php?n=Main.ReleaseNotes
- Added 'Requires: notify-python'.

* Fri Nov 14 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.11-1
- Version bump to 0.11. (Red Hat Bugzilla #464479)
  * http://decibel.silent-blade.org/index.php?n=Main.ReleaseNotes
- Replaced 'Requires: gnome-python2' with 'Requires: gnome-python2-gnome' on
  all distributions starting from Fedora 10. (Red Hat Bugzilla #460027)
- Added 'Requires: python-CDDB'.

* Thu Jul 24 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.10-2
- Added 'Requires: gnome-python2-gnomekeyring'. Closes Red Hat Bugzilla bug
  #455780.

* Thu May 22 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.10-1
- Version bump to 0.10.
  * http://decibel.silent-blade.org/index.php?n=Main.ReleaseNotes

* Sun Feb 03 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.09-1
- Initial build.
  * http://decibel.silent-blade.org/index.php?n=Main.ReleaseNotes
- Fixed wrong MimeType.
- Removed Application from Categories.
- Removed Encoding from Desktop Entry for all distributions, except Fedora 7.
