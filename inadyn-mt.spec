Summary:	Dynamic DNS Client
Name:		inadyn-mt
Version:	2.24.36
Release:	1
License:	GPL v3
Group:		Daemons
Source0:	http://downloads.sourceforge.net/inadyn-mt/%{name}.v.0%{version}.tar.gz
# Source0-md5:	14c044a2754417b344be364eeccc6779
Source1:	%{name}.conf
Source2:	inadyn.service
Source3:	inadyn-nm-dispatcher
Patch1:		sig11.patch
URL:		http://inadyn-mt.sourceforge.net/
BuildRequires:	libao-devel
BuildRequires:	rpmbuild(macros) >= 1.647
Requires:	systemd-units >= 38
Obsoletes:	inadyn < 2.24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
INADYN-MT is a dynamic DNS client. It maintains the IP address of a
host name. It periodically checks wheather the IP address stored by
the DSN server is the real current address of the machine that is
running INADYN-MT.

Before using inadyn-mt for the first time you must use the DynDNS
provider's web interface to create the entry for the hostname. You
should then fill in /etc/inadyn.conf with the appropriate detail

%prep
%setup -q -n %{name}.v.0%{version}
%patch1 -p1
%{__rm} -r bin

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},%{_mandir}/man{5,8}}

install -p src/inadyn-mt $RPM_BUILD_ROOT%{_sbindir}/inadyn
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}

cp -p man/inadyn.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -p man/inadyn.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5

install -d $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/lang
cp -p lang/* $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/lang

install -d $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/extra
cp -a extra/* $RPM_BUILD_ROOT%{_datadir}/inadyn-mt/extra

install -d $RPM_BUILD_ROOT%{systemdunitdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher/30-inadyn

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post inadyn.service

%preun
%systemd_preun inadyn.service

%postun
%systemd_reload

%files
%defattr(644,root,root,755)
%doc readme.html
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%attr(755,root,root) %{_sysconfdir}/NetworkManager/dispatcher/30-inadyn
%attr(755,root,root) %{_sbindir}/inadyn
%{systemdunitdir}/inadyn.service
%{_mandir}/man5/inadyn.conf.5*
%{_mandir}/man8/inadyn.8*
%dir %{_datadir}/%{name}
%dir %{_datadir}/inadyn-mt/lang
%{_datadir}/inadyn-mt/lang/en.lng
%{_datadir}/%{name}/extra
