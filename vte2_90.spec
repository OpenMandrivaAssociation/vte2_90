%define url_ver	%(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define api	2.91
%define major	0
%define libname	%mklibname vte %{api} %{major}
%define girname	%mklibname vte-gir %{api}
%define devname	%mklibname -d %{name}

Name:		vte%{api}
Version:	0.52.2
Release:	2
Summary:	A terminal emulator widget
License:	LGPLv2+
Group:		System/Libraries
URL:		https://www.gnome.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/vte/%{url_ver}/vte-%{version}.tar.xz
Patch0:		vte-0.52-pthread-linkage.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	vala-devel
BuildRequires:	pkgconfig(cairo-xlib)
BuildRequires:	pkgconfig(glib-2.0) >= 2.40.0
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(gnutls) >= 3.2.7
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.8.0
BuildRequires:	pkgconfig(pango) >= 1.22.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpcre2-8)

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
%autopatch -p1
./autogen.sh

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
%{_sysconfdir}/profile.d/vte.sh

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
