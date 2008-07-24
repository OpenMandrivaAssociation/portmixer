%define	major 0
%define libname	%mklibname portmixer %{major}

Summary:	Shared PortMixer library
Name:		portmixer
Version:	18.1
Release:	%mkrel 6
License:	BSD
Group:		System/Libraries
URL:		http://www.portaudio.com/
Source0:	%{name}_v18_1.tar.bz2
Patch0:		portmixer_v18_1-mdk.diff
BuildRequires:	file
BuildRequires:	libportaudio-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
PortMixer is intended to work side-by-side with PortAudio,
the Portable Real-Time Audio Library by Ross Bencina and
Phil Burk.

%package -n	%{libname}
Summary:	Shared PortMixer library
Group:          System/Libraries

%description -n	%{libname}
PortMixer is intended to work side-by-side with PortAudio,
the Portable Real-Time Audio Library by Ross Bencina and
Phil Burk.

%package -n	%{libname}-devel
Summary:	Static library and header files for the PortMixer library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Provides:	lib%{name}-devel  = %{version}
Requires:	%{libname} = %{version}
Requires:	libportaudio-devel

%description -n	%{libname}-devel
PortMixer is intended to work side-by-side with PortAudio,
the Portable Real-Time Audio Library by Ross Bencina and
Phil Burk.

This package contains the static PortMixer development library and
the PortMixer API Header File.

%prep

%setup -q -n %{name}
%patch0 -p1

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build

%make CC="gcc" \
    CFLAGS="%{optflags} -fPIC -DPIC -D_REENTRANT -D_GNU_SOURCE -Ipx_common"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}/%{_includedir}
install -d %{buildroot}/%{_libdir}

install -m0755 libportmixer.so.%{major}.%{version} %{buildroot}/%{_libdir}/
ln -snf libportmixer.so.%{major}.%{version} %{buildroot}%{_libdir}/libportmixer.so.%{major}
ln -snf libportmixer.so.%{major}.%{version} %{buildroot}%{_libdir}/libportmixer.so
install -m0644 libportmixer.a %{buildroot}%{_libdir}/
install -m0644 px_common/portmixer.h %{buildroot}%{_includedir}/

cat > README.MDK << EOF
P O R T M I X E R
-----------------

This (old) code was taken from the iaxclient codebase, I was not able
to find a tarball nor a version, so I used the same versioning as in 
portaudio. It seems Audacity uses a bundled version of this code, and
there could be other softwares doing that as well.

Regards // Oden Eriksson
EOF


%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE.txt README.MDK
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc px_tests/Makefile px_tests/px_test.c
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a

