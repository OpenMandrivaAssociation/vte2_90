%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define api	2_90
%define nicever 2.90
%define major	9
%define libname	%mklibname vte %{api} %{major}
%define girname	%mklibname vte-gir %{api}
%define devname	%mklibname -d %{name}

Name:		vte%{api}
Version:	0.34.2
Release:	5
Summary:	A terminal emulator widget
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/vte/%{url_ver}/vte-%{version}.tar.xz
# See https://bugzilla.gnome.org/show_bug.cgi?id=663779
Patch0:		vte-0.31.0-gtk32-meta-map.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pkgconfig(cairo-xlib)
BuildRequires:	pkgconfig(glib-2.0) >= 2.26.0
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
%configure2_5x \
	--enable-shared \
	--disable-static \
	--libexecdir=%{_libdir}/%{name} \
	--enable-gtk-doc \
	--enable-introspection

%make LIBS='-lm -lncurses -lutil -lgmodule-2.0'

%install
%makeinstall_std
find %{buildroot} -name "*.la" -delete
%find_lang vte-%{nicever}

%files -f vte-%{nicever}.lang
%doc COPYING HACKING NEWS README
%{_bindir}/vte%{api}
%dir %{_libdir}/%{name}
%{_sysconfdir}/profile.d/vte.sh
%attr(2711,root,utmp) %{_libdir}/%{name}/gnome-pty-helper

%files -n %{libname}
%{_libdir}/libvte%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Vte-%{nicever}.typelib

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/vte-%{nicever}
%{_includedir}/vte-%{nicever}
%{_libdir}/libvte%{api}.so
%{_libdir}/pkgconfig/vte-%{nicever}.pc
%{_datadir}/gir-1.0/Vte-%{nicever}.gir
