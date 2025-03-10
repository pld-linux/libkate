# TODO
# - katedj package (KateDJ script + kdj python modules)?
#
# Conditional build:
%bcond_without	tests	# unit tests
#
Summary:	Libraries to handle the Kate bitstream format
Summary(pl.UTF-8):	Biblioteki do obsługi strumienia bitowego Kate
Name:		libkate
Version:	0.4.3
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://downloads.xiph.org/releases/kate/%{name}-%{version}.tar.gz
# Source0-md5:	6bdd4315a2ebe49effa4b6e76e383d4f
URL:		https://wiki.xiph.org/OggKate
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	libogg-devel >= 2:1.0
# oggz binary
BuildRequires:	liboggz
BuildRequires:	libpng-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3
BuildRequires:	python3-modules >= 1:3
# kdj import check
BuildRequires:	python3-wxPython
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	util-linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%description
This is libkate, the reference implementation of a codec for the Kate
bitstream format. Kate is a karaoke and text codec meant for
encapsulation in an Ogg container. It can carry text, images, and
animate them.

Kate is meant to be used for karaoke alongside audio/video streams
(typically Vorbis and Theora), movie subtitles, song lyrics, and
anything that needs text data at arbitrary time intervals.

%description -l pl.UTF-8
Ten pakiet zawiera libkate - referencyjną implementację kodeka do
formatu strumienia bitowego Kate. Kate to kodek tekstowy i karaoke
przeznaczony do opakowania w kontener Ogg. Może zawierać tekst,
obrazki i animować je.

Kate może być używany do karaoke dla strumieni audio/video (zwykle
Vorbis i Theora), napisów do filmów, tekstów piosenek oraz
czegokolwiek innego wymagającego tekstu w określonych chwilach.

%package devel
Summary:	Header files for Kate libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Kate
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libogg-devel >= 2:1.0

%description devel
This package contains the header files for developing applications
that use Kate libraries.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących biblioteki Kate.

%package static
Summary:	Static Kate libraries
Summary(pl.UTF-8):	Statyczne biblioteki Kate
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Kate libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Kate.

%package utils
Summary:	Encoder/Decoder utilities for Kate bitstreams
Summary(pl.UTF-8):	Kodery i dekodery do strumieni bitowych Kate
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
# oggz binary (for KateDJ only)
Requires:	liboggz

%description utils
This package contains the katedec/kateenc binaries for Kate streams.

%description utils -l pl.UTF-8
Ten pakiet zawiera narzędzie katedec i kateenc do strumieni Kate.

%package docs
Summary:	Documentation for Kate libraries
Summary(pl.UTF-8):	Dokumentacja do bibliotek Kate
Group:		Documentation

%description docs
This package contains the documentation for Kate libraries.

%description docs -l pl.UTF-8
Ten pakiet zawiera dokumentację do bibliotek Kate.

%prep
%setup -q

# We regenerate these files at built step
%{__rm} tools/kate_parser.{c,h}
%{__rm} tools/kate_lexer.c

%{__sed} -i -e '1s,/usr/bin/env python3$,%{__python3},' tools/KateDJ/KateDJ

%build
cp -f /usr/share/automake/config.sub misc/autotools
%configure \
	--docdir=%{_docdir}/%{name}-%{version}

%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="install -p"

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*kate.la

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# Fix for header timestramps
touch -r $RPM_BUILD_ROOT%{_includedir}/kate/kate_config.h $RPM_BUILD_ROOT%{_includedir}/kate/kate.h

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{_docdir}/libkate-%{version}
%exclude %{_docdir}/libkate-%{version}/html
%attr(755,root,root) %{_libdir}/libkate.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libkate.so.1
%attr(755,root,root) %{_libdir}/liboggkate.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liboggkate.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libkate.so
%attr(755,root,root) %{_libdir}/liboggkate.so
%{_includedir}/kate
%{_pkgconfigdir}/kate.pc
%{_pkgconfigdir}/oggkate.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libkate.a
%{_libdir}/liboggkate.a

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/KateDJ
%attr(755,root,root) %{_bindir}/katalyzer
%attr(755,root,root) %{_bindir}/katedec
%attr(755,root,root) %{_bindir}/kateenc
%{py3_sitescriptdir}/kdj
%{_mandir}/man1/KateDJ.1*
%{_mandir}/man1/katalyzer.1*
%{_mandir}/man1/katedec.1*
%{_mandir}/man1/kateenc.1*

%files docs
%defattr(644,root,root,755)
%doc %{_docdir}/libkate-%{version}/html
