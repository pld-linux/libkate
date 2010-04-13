Summary:	Libraries to handle the Kate bitstream format
Name:		libkate
Version:	0.3.7
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://libkate.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	e5c287b4f40498e5bde48c0a52225292
Patch0:		%{name}-libpng.patch
URL:		http://code.google.com/p/libkate/
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	flex
BuildRequires:	libogg-devel
BuildRequires:	liboggz
BuildRequires:	libpng-devel
BuildRequires:	python-devel
BuildRequires:	valgrind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is libkate, the reference implementation of a codec for the Kate
bitstream format. Kate is a karaoke and text codec meant for
encapsulation in an Ogg container. It can carry text, images, and
animate them.

Kate is meant to be used for karaoke alongside audio/video streams
(typically Vorbis and Theora), movie subtitles, song lyrics, and
anything that needs text data at arbitrary time intervals.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libogg-devel

%description devel
This package contains libraries and header files for developing
applications that use %{name}.

%package utils
Summary:	Encoder/Decoder utilities for %{name}
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	liboggz

%description utils
This package contains the katedec/kateenc binaries for %{name}.

%package docs
Summary:	Documentation for %{name}
Group:		Documentation

%description docs
This package contains the docs for %{name}.

%prep
%setup -q
%patch0 -p1

# We regenerate theses files at built step
rm tools/kate_parser.{c,h}
rm tools/kate_lexer.c

%build
%configure \
	--docdir=%{_docdir}/%{name}-%{version}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="install -p"

# Fix for header timestramps
touch -r $RPM_BUILD_ROOT%{_includedir}/kate/kate_config.h $RPM_BUILD_ROOT%{_includedir}/kate/kate.h

%check
make check

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%exclude %{_docdir}/libkate-%{version}/html
%doc %{_docdir}/libkate-%{version}
# XXX files fix
%attr(755,root,root) %{_libdir}/*.so.*

%files devel
%defattr(644,root,root,755)
%doc examples
%{_includedir}/kate
# XXX files fix
%attr(755,root,root) %{_libdir}/*.so
%{_pkgconfigdir}/*.pc

%files utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/KateDJ
%attr(755,root,root) %{_bindir}/katalyzer
%attr(755,root,root) %{_bindir}/katedec
%attr(755,root,root) %{_bindir}/kateenc
# XXX files fix
%{py_sitescriptdir}/kdj
%{_mandir}/man1/KateDJ.1*
%{_mandir}/man1/katalyzer.1*
%{_mandir}/man1/katedec.1*
%{_mandir}/man1/kateenc.1*

%files docs
%defattr(644,root,root,755)
%doc %{_docdir}/libkate-%{version}/html
