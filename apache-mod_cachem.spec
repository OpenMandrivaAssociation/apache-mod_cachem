#Module-Specific definitions
%define mod_name mod_cachem
%define mod_conf A21_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	A shared memory support module
Name:		apache-%{mod_name}
Version:	0.2
Release:	%mkrel 10
Group:		System/Servers
License:	GPL
URL:		https://cachem.sourceforge.net/
Source0:	apache2-%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	apr-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
A shared memory support module.

%package	devel
Summary:	Development files for %{name}
Group:		Development/C

%description	devel
Development files for %{name}

%prep

%setup -q -n apache2-%{mod_name}-%{version}

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

cp %{SOURCE1} %{mod_conf}

%build
%{_sbindir}/apxs -c %{mod_name}.c

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_includedir}

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}
install -m0644 %{mod_name}.h %{buildroot}%{_includedir}/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

%files devel
%defattr(-,root,root,-)
%{_includedir}/*

