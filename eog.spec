Summary:	The Eye of GNOME image viewer
Name:		eog
Version:	3.6.2
Release:	2
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/eog/3.6/%{name}-%{version}.tar.xz
# Source0-md5:	da1c7011ba3c86f3fb9d6aca36048a45
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	exempi-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-desktop-devel
BuildRequires:	libpeas-gtk-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	lcms-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	librsvg-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	shared-mime-info
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Eye of GNOME is a tool for viewing/cataloging images.

%package devel
Summary:	Development files
Group:		Development/Libraries

%description devel
Eye of the GNOME Development files.

%package apidocs
Summary:	Eye of the GNOME API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
Eye of the GNOME API documentation.

%prep
%setup -q

# kill gnome common deps
sed -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__gtkdocize}
%{__gnome_doc_prepare}
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,en@shaw}
rm -f $RPM_BUILD_ROOT%{_libdir}/eog/plugins/*.la

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_desktop_database_postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/eog

%dir %{_libdir}/eog
%dir %{_libdir}/eog/plugins
%attr(755,root,root) %{_libdir}/eog/plugins/*.so
%{_libdir}/eog/plugins/*.plugin

%dir %{_libdir}/eog/girepository-1.0
%{_libdir}/eog/girepository-1.0/Eog-3.0.typelib

%{_datadir}/eog
%{_datadir}/glib-2.0/schemas/*.xml

%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/eog.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/eog-3.0
%{_pkgconfigdir}/*.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/eog

