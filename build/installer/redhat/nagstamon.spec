%define python_sitelib %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib()')
%define python_sitearch %(%{__python} -c 'from distutils import sysconfig; print sysconfig.get_python_lib(1)')

Summary: Nagios status monitor for your desktop
Name: nagstamon
Version: 0.9.12
Release: 1.mizu%{?dist}
License: GPL
Group: Applications/Utilities
URL: http://nagstamon.ifw-dresden.de/

Source: http://downloads.sourceforge.net/project/nagstamon/nagstamon/nagstamon%20%{version}/nagstamon_%{version}.tar.gz
Source1: nagstamon.desktop
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Buildarch: noarch
BuildRequires: desktop-file-utils
BuildRequires: Distutils
#BuildRequires: gnome-python2-libegg
#BuildRequires: pygtk2-devel
#BuildRequires: python-devel
#BuildRequires: rpm-macros-rpmforge
Requires: gnome-icon-theme
Requires: gnome-python2-libegg
Requires: openssh
Requires: pygtk2
Requires: python >= 2.5
Requires: python-setuptools
Requires: rdesktop
Requires: sox
Requires: vnc

%description
Nagstamon is a Nagios status monitor for the desktop. It connects to multiple
Nagios, Icinga, Opsview, Centreon, Op5 Monitor/Ninja and Check_MK Multisite
monitoring servers and resides in systray or as a floating statusbar at the
desktop showing a brief summary of critical, warning, unknown, unreachable and
down hosts and services and pops up a detailed status overview when moving the
mouse pointer over it. Connecting to displayed hosts and services is easily
established by context menu via SSH, RDP and VNC. Users can be notified by
sound. Hosts and services can be filtered by category and regular expressions.

%prep
%setup -n Nagstamon

%build
cd ../
%{__python} setup.py build

%install
cd ../
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root="%{buildroot}" --prefix="%{_prefix}"

%{__chmod} +x %{buildroot}%{python_sitelib}/Nagstamon/Server/Multisite.py

# install the desktop file
%{__install} -m755 -d %{buildroot}%{_desktopdir}
%{__install} -m755 -d %{buildroot}%{_datadir}/pixmaps
%{__install} -m644 Nagstamon/resources/nagstamon.svg %{buildroot}%{_datadir}/pixmaps/nagstamon.svg
%{__install} -m644 %{SOURCE1} %{buildroot}%{_desktopdir}/nagstamon.desktop

desktop-file-install --dir %{buildroot}%{_desktopdir} \
    --vendor OBS \
    --delete-original \
    %{buildroot}%{_desktopdir}/nagstamon.desktop


# fix for stupid strip issue
#%{__chmod} -R u+w %{buildroot}/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
#%doc COPYRIGHT ChangeLog LICENSE
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_datadir}/pixmaps/*
#%{_desktopdir}/OBS-nagstamon.desktop
%{python_sitelib}/Nagstamon
%{python_sitelib}/nagstamon-*-py*.egg-info

%changelog
* Sun Mar 03 2014 Vorontsov Igor <mizunokazumi@mail.ru> - 0.9.12-1.mizu
- Initial package.

