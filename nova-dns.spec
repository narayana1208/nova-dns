%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%define mod_name nova_dns

Name:             nova-dns
Version:          0.0.1
Release:          1
Summary:          REST API for DNS configuration and service to add records for fixed ips
License:          GNU LGPL v2.1
Vendor:           Grid Dynamics International, Inc.
URL:              http://www.griddynamics.com/openstack
Group:            Development/Languages/Python

Source0:          %{name}-%{version}.tar.gz
BuildRoot:        %{_tmppath}/%{name}-%{version}-build
BuildRequires:    python-devel python-setuptools make
BuildArch:        noarch
Requires:         python-nova
Requires:         start-stop-daemon

%description
Nova is a cloud computing fabric controller (the main part of an IaaS system)
built to match the popular AWS EC2 and S3 APIs. It is written in Python, using
the Tornado and Twisted frameworks, and relies on the standard AMQP messaging
protocol, and the Redis KVS.

TODO
This package contains the service to add dns records for instances with 
attached floating ip.


%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
BuildRequires:  python-sphinx make

%description doc
Documentation and examples for %{name}.


%prep
%setup -q -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%__rm -rf %{buildroot}

%{__python} setup.py install -O1 --skip-build --prefix=%{_prefix} --root=%{buildroot}
export PYTHONPATH=%{buildroot}%{python_sitelib}
make -C doc html
install -p -D -m 755 redhat/nova-dns.init %{buildroot}%{_initrddir}/%{name}

%clean
%__rm -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -eq 1 ] ; then
    /sbin/service %{name} condrestart
fi

%files
%defattr(-,root,root,-)
%doc README
%{_initrddir}/*
%{python_sitelib}/%{mod_name}*
%{_usr}/bin/*

%files doc
%defattr(-,root,root,-)
%doc doc/build/html

%changelog
