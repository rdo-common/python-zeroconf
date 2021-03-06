%if 0%{?fedora} || 0%{?rhel} > 7
%global with_python3 1
%endif

%global pypi_name zeroconf

Name:           python-%{pypi_name}
Version:        0.19.1
Release:        3%{?dist}
Summary:        Pure Python Multicast DNS Service Discovery Library

License:        LGPLv2
URL:            https://github.com/jstasiak/%{name}
Source0:        %{url}/archive/%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pytest
BuildRequires:  python2-mock
BuildRequires:  python-enum34
BuildRequires:  python-netifaces
BuildRequires:  python2-six

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-mock
BuildRequires:  python3-netifaces
BuildRequires:  python3-six
%endif

# Integration tests work in mock but fail in Koji with PermissionError
%bcond_with integration

%description
A pure Python implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%package -n     python2-%{pypi_name}
Summary:        Pure Python 2 Multicast DNS Service Discovery Library
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-enum34
Requires:       python-netifaces
Requires:       python2-six

%description -n python2-%{pypi_name}
A pure Python 2 implementation of multicast DNS service discovery
supporting Bonjour/Avahi.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Pure Python 3 Multicast DNS Service Discovery Library
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3-netifaces
Requires:       python3-six

%description -n python3-%{pypi_name}
A pure Python 3 implementation of multicast DNS service discovery
supporting Bonjour/Avahi.
%endif

%prep
%autosetup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove enum-compat from install_requires
# See https://bugzilla.redhat.com/show_bug.cgi?id=1432165
sed -i '/enum-compat/d' setup.py

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} -m pytest \
%if %{with integartion}

%else
  -k "not integration"
%endif

%if 0%{?with_python3}
%{__python3} -m pytest \
%if %{with integartion}

%else
  -k "not integration"
%endif
%endif


%files -n python2-%{pypi_name}
%license COPYING
%doc README.rst
%{python2_sitelib}/%{pypi_name}.py*
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license COPYING
%doc README.rst
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif


%changelog
* Fri Dec 08 2017 Iryna Shcherbina <ishcherb@redhat.com> - 0.19.1-3
- Fix ambiguous Python 2 dependency declarations
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Miro Hrončok <mhroncok@redhat.com> - 0.19.1-1
- New version 0.19.1 (#1461043)
- Updated (B)Rs to use python2- where possible

* Tue Mar 14 2017 Miro Hrončok <mhroncok@redhat.com> - 0.18.0-2
- Remove enum-compat from install_requires (#1432165)

* Sat Feb 18 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.18.0-1
- Update to 0.18.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Miro Hrončok <mhroncok@redhat.com> - 0.17.6-3
- Rebuild for Python 3.6

* Wed Dec 21 2016 Miro Hrončok <mhroncok@redhat.com> - 0.17.6-2
- Add Python 2 subpackage

* Sun Dec 04 2016 Miro Hrončok <mhroncok@redhat.com> - 0.17.6-1
- Initial package
