%define modname pinba
%define dirname %{modname}
%define soname %{modname}.so
%define inifile B11_%{modname}.ini

Summary:	PHP extension for Pinba
Name:		php-%{modname}
Version:	0.0.6
Release:	%mkrel 2
Group:		Development/PHP
License:	PHP License
URL:		http://pinba.org/
Source0:	http://pinba.org/files/pinba_extension-%{version}.tgz
Source1:	B11_pinba.ini
BuildRequires:	protobuf-devel
BuildRequires:	php-devel >= 3:5.2.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Pinba is a statistics server for PHP using MySQL as a read-only interface.

%prep

%setup -q -n pinba_extension-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

cp %{SOURCE1} %{inifile}

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" config.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}
%make
mv modules/*.so .

%install
rm -rf %{buildroot} 

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/
install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc NEWS README package*.xml
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}

