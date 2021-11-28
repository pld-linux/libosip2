#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	The GNU oSIP library
Summary(pl.UTF-8):	Biblioteka GNU oSIP
Name:		libosip2
Version:	5.3.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://ftp.gnu.org/gnu/osip/%{name}-%{version}.tar.gz
# Source0-md5:	81381372bf1b16089f326bb7f7f305e8
Patch0:		%{name}-nolibs.patch
Patch1:		%{name}-link.patch
URL:		http://www.gnu.org/software/osip/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	libtool >= 2:2
Provides:	libosip
Obsoletes:	libosip < 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is "the GNU oSIP library" (for Omnibus SIP). It has been designed
to provide the Internet Community a simple way to support the Session
Initiation Protocol. SIP is described in the RFC2543 which is
available at http://www.ietf.org/rfc/rfc2543.txt.

%description -l pl.UTF-8
To jest biblioteka GNU oSIP (Omnibus SIP). Została zaprojektowana, aby
dostarczyć Społeczności Internetowej prostą obsługę protokołu SIP.
Protokół SIP (Session Initiation Protocol) jest opisany w RFC2543.

%package devel
Summary:	The GNU oSIP library - development files
Summary(pl.UTF-8):	Pliki dla programistów używających GNU oSIP
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	libosip-devel
Obsoletes:	libosip-devel < 1.0

%description devel
Development files for the GNU oSIP library.

%description devel -l pl.UTF-8
Pliki dla programistów używających biblioteki GNU oSIP.

%package static
Summary:	The GNU oSIP library - static version
Summary(pl.UTF-8):	Statyczna biblioteka GNU oSIP
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	libosip-static
Obsoletes:	libosip-static < 1.0

%description static
Static version of the GNU oSIP library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki GNU oSIP.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I scripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-debug%{!?debug:=no} \
	--enable-pthread \
	--enable-semaphore \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libosip*.la

%{__mv} $RPM_BUILD_ROOT%{_mandir}/man{1,3}
%{__mv} $RPM_BUILD_ROOT%{_mandir}/man3/osip.{1,3}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog FEATURES HISTORY NEWS README TODO
%attr(755,root,root) %{_libdir}/libosip2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosip2.so.15
%attr(755,root,root) %{_libdir}/libosipparser2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libosipparser2.so.15

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libosip2.so
%attr(755,root,root) %{_libdir}/libosipparser2.so
%{_includedir}/osip2
%{_includedir}/osipparser2
%{_pkgconfigdir}/libosip2.pc
%{_mandir}/man3/osip.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libosip2.a
%{_libdir}/libosipparser2.a
%endif
