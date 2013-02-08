%define name pagekite
%define version 0.5.5a
%define unmangled_version 0.5.5a
%define unmangled_version 0.5.5a
%define release 0pagekite_fc14fc15fc16

Summary: PageKite makes localhost servers visible to the world.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: AGPLv3+
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: PageKite Packaging Team <packages@pagekite.net>
Requires: python-SocksipyChain
Url: http://pagekite.org/

%description
PageKite is a system for running publicly visible servers (generally
web servers) on machines without a direct connection to the Internet,
such as mobile devices or computers behind restrictive firewalls.
PageKite works around NAT, firewalls and IP-address limitations by
using a combination of  tunnels and reverse proxies.

Natively supported protocols: HTTP, HTTPS
Partially supported protocols: IRC, Finger

Any other TCP-based service, including SSH and VNC, may be exposed
as well to clients supporting HTTP Proxies.


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
# This is a replacement for the default disttools RPM build method
# which gets the file lists right, including the byte-compiled files.
#
# We also process our man-pages here.

python setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT

for manpage in $(cd doc && echo *.1); do
  mkdir -m 755 -p $RPM_BUILD_ROOT/usr/share/man/man1/
  install -v -m 644 doc/$manpage $RPM_BUILD_ROOT/usr/share/man/man1/
  gzip --verbose $RPM_BUILD_ROOT/usr/share/man/man1/$manpage
done

mkdir -m 755 -p $RPM_BUILD_ROOT/etc/pagekite.d/default
for rcfile in etc/pagekite.d/*; do
  install -v -m 644 $rcfile $RPM_BUILD_ROOT/etc/pagekite.d/default/
done
chmod 600 $RPM_BUILD_ROOT/etc/pagekite.d/default/*account*

find $RPM_BUILD_ROOT -type f \
  |sed -e "s|^$RPM_BUILD_ROOT/*|/|" \
       -e 's|/[^/]*$||' \
  |uniq >INSTALLED_FILES

mkdir -m 755 -p $RPM_BUILD_ROOT/var/log/pagekite
echo /var/log/pagekite >>INSTALLED_FILES

for where in init.d logrotate.d sysconfig; do
  if [ -e etc/$where/pagekite.fedora ]; then
    mkdir -m 755 -p $RPM_BUILD_ROOT/etc/$where
    install -v -m 755 etc/$where/pagekite.fedora $RPM_BUILD_ROOT/etc/$where/pagekite
    echo /etc/$where/pagekite >>INSTALLED_FILES
  fi
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
# HACK: Enable default config files, without overwriting.
cd /etc/pagekite.d/default
for conffile in *; do
  [ -e ../$conffile ] || cp -a $conffile ..
done

# Make sure PageKite is restarted if necessary
chkconfig --add pagekite || true
service pagekite status && service pagekite restart



%preun

(service pagekite status >/dev/null \
  && service pagekite stop \
  || true)

(chkconfig --del pagekite || true)

# HACK: uninstall config files that have not changed.
cd /etc/pagekite.d/default
for conffile in *; do
  if [ -f "../$conffile" ]; then
    md5org=$(md5sum "$conffile" |awk '{print $1}')
    md5act=$(md5sum "../$conffile" |awk '{print $1}')
    [ "$md5org" = "$md5act" ] && rm -f "../$conffile"
  fi
done


%files -f INSTALLED_FILES
%defattr(-,root,root)
