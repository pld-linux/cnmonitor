
%define		_subver	3
Summary:	Directory Server Monitoring application
Name:		cnmonitor
Version:	1.3
Release:	0.%{_subver}.1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/project/cnmonitor/CN%3DMonitor/%{version}/%{name}-%{version}-%{_subver}.tgz
# Source0-md5:	e8db79806c5a02d000b2dbf553c4e0b4
URL:		http://cnmonitor.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires(triggerpostun):	sed >= 4.0
Requires:	webserver(php)
Requires:	php-cli
Requires:	php-gd
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Directory Server Monitoring application. The idea is to monitor entire
small to large scaled deployed directory server environments.

%prep
%setup -q -n %{name}

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a {bin,conf,sql,www} $RPM_BUILD_ROOT%{_appdir}
cp -a config $RPM_BUILD_ROOT%{_sysconfdir}
cp -a conf/httpd/cnmonitor.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a conf/httpd/cnmonitor.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
ln -s %{_sysconfdir}/config $RPM_BUILD_ROOT%{_appdir}/config

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.pdf
%dir %attr(750,root,http) %{_sysconfdir}
%dir %attr(750,root,http) %{_sysconfdir}/config
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config/*.php
%{_appdir}
