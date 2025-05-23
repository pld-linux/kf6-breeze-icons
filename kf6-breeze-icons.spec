#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.14
%define		qtver		5.15.2
%define		kfname		breeze-icons

Summary:	Breeze icons theme
Summary(pl.UTF-8):	Motyw ikon Breeze
Name:		kf6-%{kfname}
Version:	6.14.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	b132c475a7e389e6f7d36323279a7f3d
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpm-build(macros) >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
Requires:	kf6-dirs
Obsoletes:	breeze-icon-theme < 6.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

%description
Breeze-icons is a freedesktop.org compatible icon theme.

%description -l pl.UTF-8
Breeze-icons to motyw ikon zgodny z freedesktop.org.

%package data
Summary:	Data files for %{kfname}
Summary(pl.UTF-8):	Dane dla %{kfname}
Group:		X11/Applications
Obsoletes:	kf5-breeze-icons-data < 5.240
BuildArch:	noarch

%description data
Data files for %{kfname}.

%description data -l pl.UTF-8
Dane dla %{kfname}.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%ghost %{_libdir}/libKF6BreezeIcons.so.?
%attr(755,root,root) %{_libdir}/libKF6BreezeIcons.so.6.*

%files data
%defattr(644,root,root,755)
%{_iconsdir}/breeze
%{_iconsdir}/breeze-dark

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/BreezeIcons
%{_libdir}/cmake/KF6BreezeIcons
%{_libdir}/libKF6BreezeIcons.so
