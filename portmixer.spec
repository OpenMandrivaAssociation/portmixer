%define		major 0
%define		libname	%mklibname portmixer %{major}
%define		devname %mklibname portmixer -d

Summary:	Shared PortMixer library
Name:		portmixer
Version:	18.1
Release:	10
License:	BSD
Url:		https://www.portaudio.com/
Group:	Sound
# No more available at $URL: use stored sources
Source0:	%{name}_v18_1.tar.bz2
Patch0:	portmixer_v18_1-mdk.diff
BuildRequires:	file
BuildRequires:	pkgconfig(portaudio-2.0)

%description
This library is intended to work side-by-side with PortAudio, the Portable
Real-Time Audio Library by Ross Bencina and Phil Burk.

#-----------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Shared PortMixer library
Group:	System/Libraries

%description -n	%{libname}
This library is intended to work side-by-side with PortAudio, the Portable
Real-Time Audio Library by Ross Bencina and Phil Burk.
This package contains the main library.

%files -n %{libname}
%license LICENSE.txt
%{_libdir}/libportmixer.so.*

#-----------------------------------------------------------------------------

%package -n	%{devname}
Summary:		Development files for the PortMixer library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel  = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig(portaudio-2.0)
%rename	%{libname}-devel

%description -n	%{devname}
This library is intended to work side-by-side with PortAudio, the Portable
Real-Time Audio Library by Ross Bencina and Phil Burk.
This package contains the development library and the API Header File.

%files -n %{devname}
%doc px_tests/Makefile px_tests/px_test.c
%{_includedir}/%{name}.h
%{_libdir}/libportmixer.so
%{_libdir}/libportmixer.a

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}

# Fix perms
find . -type d | xargs chmod 755
find . -type f | xargs chmod 644

# Strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'


%build
%make_build CFLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT -D_GNU_SOURCE -Ipx_common -fno-lto"


%install
install -d %{buildroot}/%{_includedir}
install -d %{buildroot}/%{_libdir}

install -m0755 libportmixer.so.%{major}.%{version} %{buildroot}/%{_libdir}/
ln -snf libportmixer.so.%{major}.%{version} %{buildroot}%{_libdir}/libportmixer.so.%{major}
ln -snf libportmixer.so.%{major}.%{version} %{buildroot}%{_libdir}/libportmixer.so
install -m0644 libportmixer.a %{buildroot}%{_libdir}/
install -m0644 px_common/%{name}.h %{buildroot}%{_includedir}/
