#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.0
%define		qtver		5.15.2
%define		kfname		breeze-icons

Summary:	breeze icons
Name:		kf6-%{kfname}
Version:	6.0.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	795661e00d90c350bfc57665060a0ebf
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
Requires:	%{name}-data = %{version}-%{release}
Obsoletes:	breeze-icon-theme
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6
%define		_enable_debug_packages	0

%description
Breeze-icons is a freedesktop.org compatible icon theme.

%package data
Summary:	Data files for %{kfname}
Summary(pl.UTF-8):	Dane dla %{kfname}
Group:		X11/Applications
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

%files
%defattr(644,root,root,755)

%files data
%defattr(644,root,root,755)
%{_iconsdir}/breeze
%{_iconsdir}/breeze-dark

%files devel
%defattr(644,root,root,755)
%dir %{_libdir}/cmake/KF6BreezeIcons
%{_libdir}/cmake/KF6BreezeIcons/KF6BreezeIconsConfig.cmake
%{_libdir}/cmake/KF6BreezeIcons/KF6BreezeIconsConfigVersion.cmake
