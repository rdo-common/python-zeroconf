%global pypi_name zeroconf

Name:           python-%{pypi_name}
Version:        0.17.6
Release:        1%{?dist}
Summary:        Pure Python Multicast DNS Service Discovery Library

License:        LGPLv2
URL:            https://github.com/jstasiak/%{name}
Source0:        %{url}/archive/%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-netifaces
BuildRequires:  python3-six

# Integration tests work in mock but fail in Koji with PermissionError
%bcond_with integration

%description
A pure Python implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%package -n     python3-%{pypi_name}
Summary:        Pure Python Multicast DNS Service Discovery Library
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-netifaces
Requires:       python3-six

%description -n python3-%{pypi_name}
A pure Python implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%prep
%autosetup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info


%build
%py3_build


%install
%py3_install


%check
%{__python3} -m pytest \
%if %{with integartion}

%else
  -k "not integration"
%endif


%files -n python3-%{pypi_name}
%license COPYING
%doc README.rst
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%changelog
* Sun Dec 04 2016 Miro Hrončok <mhroncok@redhat.com> - 0.17.6-1
- Initial package
