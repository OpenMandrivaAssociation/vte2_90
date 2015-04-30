%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api	2.91
%define major	0
%define libname	%mklibname vte %{api} %{major}
%define girname	%mklibname vte-gir %{api}
%define devname	%mklibname -d %{name}

Name:		vte%{api}
Version:	0.40.0
Release:	1
Summary:	A terminal emulator widget
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/vte/%{url_ver}/vte-%{version}.tar.xz
Patch0:		0001-widget-Only-show-the-cursor-on-motion-if-moved.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(cairo-xlib)
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.1.9
BuildRequires:	pkgconfig(pango) >= 1.22.0
BuildRequires:	pkgconfig(x11)

%description
VTE is a terminal emulator widget for use with GTK+ 3.0.

%package -n %{libname}
Summary:	A terminal emulator widget
Group:		System/Libraries

%description -n %{libname}
VTE is a terminal emulator widget for use with GTK+ 3.0.

%package -n %{girname}
Summary:	GObject Introspection interface description for vte with GTK+ 3.0
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}

%description -n %{girname}
GObject Introspection interface description for vte with GTK+ 3.0.

%package -n %{devname}
Summary:	Files needed for developing applications which use VTE
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires: 	%{libname} = %{version}-%{release}
Requires: 	%{girname} = %{version}-%{release}

%description -n %{devname}
VTE is a terminal emulator widget for use with GTK+ 3.0.  This
package contains the files needed for building applications using VTE.

%prep
%setup -qn vte-%{version}
%apply_patches

%build
%configure \
	--enable-shared \
	--disable-static \
	--libexecdir=%{_libdir}/%{name} \
	--enable-gnome-pty-helper \
	--enable-gtk-doc \
	--enable-introspection

%make
#LIBS='-lm -lncurses -lutil -lgmodule-2.0'

%install
%makeinstall_std
find %{buildroot} -name "*.la" -delete
%find_lang vte-%{api}

%files -f vte-%{api}.lang
%doc COPYING HACKING NEWS README
%{_bindir}/vte-%{api}
%dir %{_libdir}/%{name}
%{_sysconfdir}/profile.d/vte.sh
%attr(2711,root,utmp) %{_libdir}/%{name}/gnome-pty-helper

%files -n %{libname}
%{_libdir}/libvte-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Vte-%{api}.typelib

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/vte-%{api}
%{_includedir}/vte-%{api}
%{_libdir}/libvte-%{api}.so
%{_libdir}/pkgconfig/vte-%{api}.pc
%{_datadir}/gir-1.0/Vte-%{api}.gir
%{_datadir}/vala/vapi/*
