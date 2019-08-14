%{?systemd_requires}

Name:     unifi-controller
Version:  5.5.24
Release:  1%{?dist}
Summary:  Ubiquity UniFi controller web application
Group:    Applications/System
License:  EULA
URL:      https://www.ubnt.com/download/unifi/
Source0:  http://dl.ubnt.com/unifi/%{version}/UniFi.unix.zip

Requires: mongodb-server
Requires: java-1.8.0-openjdk
Requires(pre): shadow-utils
BuildRequires: unzip
BuildRequires: wget
BuildRequires: systemd

%description
Ubiquity UniFi controller proprietary web application.

%prep

%build

%install
mkdir -p %{buildroot}/opt
unzip -q %{SOURCE0} -d %{buildroot}/opt
mkdir -p %{buildroot}/%{_unitdir}
cat >%{buildroot}/%{_unitdir}/%{name}.service <<SYSD
[Unit]
Description=UniFi AP Web Controller
After=syslog.target network.target

[Service]
Type=simple
User=ubnt
WorkingDirectory=/opt/UniFi
ExecStart=/usr/bin/java -Xmx1024M -jar /opt/UniFi/lib/ace.jar start
ExecStop=/usr/bin/java -jar /opt/UniFi/lib/ace.jar stop
SuccessExitStatus=143

[Install]
WantedBy=multi-user.target
SYSD

%files
%defattr(-,root,root,-)
%{_unitdir}/%{name}.service
%defattr(-,ubnt,ubnt,-)
/opt/UniFi

%pre
getent group ubnt >/dev/null || groupadd -r ubnt
getent passwd ubnt >/dev/null || \
    useradd -r -g ubnt -d /opt/UniFi -s /sbin/nologin \
    -c "Ubiquiti UniFi controller system user" ubnt
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%changelog
