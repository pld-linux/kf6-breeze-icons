#
# Conditional build:
%bcond_with	tests		# automatic tests

%define		kdeframever	6.16
%define		kf_ver		%{version}
%define		qt_ver		6.7.0
%define		kfname		breeze-icons

Summary:	Breeze icons theme
Summary(pl.UTF-8):	Motyw ikon Breeze
Name:		kf6-%{kfname}
Version:	6.16.0
Release:	1
License:	LGPL v2.1+ (library), LGPL v3+ (icons)
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	6cf6f9e5da0330827d0b50c48a581686
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
%{?with_tests:BuildRequires:	Qt6Test-devel >= %{qt_ver}}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-lxml
BuildRequires:	qt6-linguist >= %{qt_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	%{name}-data = %{version}-%{release}
Requires:	kf6-dirs
Obsoletes:	breeze-icon-theme < 6.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Breeze-icons is a freedesktop.org compatible icon theme.

%description -l pl.UTF-8
Breeze-icons to motyw ikon zgodny z freedesktop.org.

%package data
Summary:	Data files for %{kfname}
Summary(pl.UTF-8):	Dane dla %{kfname}
License:	LGPL v3+
Group:		X11/Applications
Provides:	kf5-breeze-icons-data = %{version}-%{release}
Obsoletes:	kf5-breeze-icons-data < 5.240
BuildArch:	noarch

%description data
Data files for %{kfname}.

%description data -l pl.UTF-8
Dane dla %{kfname}.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
License:	LGPL v2.1+
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
%attr(755,root,root) %{_libdir}/libKF6BreezeIcons.so.*.*.*
%ghost %{_libdir}/libKF6BreezeIcons.so.6

%files data
%defattr(644,root,root,755)
%doc COPYING-ICONS README.md
%{_iconsdir}/breeze
%{_iconsdir}/breeze-dark

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/BreezeIcons
%{_libdir}/cmake/KF6BreezeIcons
%{_libdir}/libKF6BreezeIcons.so
