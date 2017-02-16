%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%global is_rhel5 %(%{__grep} -c "release 5" /etc/redhat-release)
%global rhel5_minor %(%{__grep} -o "5.[0-9]*" /etc/redhat-release |%{__sed} -s 's/5.//')

%if 0%{?is_rhel5} > 0
# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}
%else
# Fedora and RHEL 6+
# we don't want to provide private python extension libs
%define __provides_exclude_from %{python_sitearch}/.*\.so$
%endif

%if (0%{?fedora} >= 16 || 0%{?rhel} >= 7)
    %global use_systemd 1
%endif

%if (0%{?use_systemd} == 1)
    %global with_initscript --with-initscript=systemd --with-systemdunitdir=%{_unitdir}
%else
    %global with_initscript --with-initscript=sysv
%endif

%global enable_experimental 1

%if (0%{?enable_experimental} == 1)
    %global experimental --enable-all-experimental-features
%endif

# Determine the location of the LDB modules directory
%global ldb_modulesdir %(pkg-config --variable=modulesdir ldb)

%if (0%{?fedora} > 15 || 0%{?rhel} >= 7)
%define _hardened_build 1
%endif

Name: sssd
Version: 1.11.7
Release: 0%{?dist}
Group: Applications/System
Summary: System Security Services Daemon
License: GPLv3+
URL: http://fedorahosted.org/sssd/
Source0: %{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

### Patches ###

### Dependencies ###

Requires: sssd-common = %{version}-%{release}
Requires: sssd-ldap = %{version}-%{release}
Requires: sssd-krb5 = %{version}-%{release}
Requires: sssd-ipa = %{version}-%{release}
Requires: sssd-common-pac = %{version}-%{release}
Requires: sssd-ad = %{version}-%{release}
Requires: sssd-proxy = %{version}-%{release}
Requires: python-sssdconfig = %{version}-%{release}

%global servicename sssd
%global sssdstatedir %{_localstatedir}/lib/sss
%global dbpath %{sssdstatedir}/db
%global pipepath %{sssdstatedir}/pipes
%global mcpath %{sssdstatedir}/mc
%global pubconfpath %{sssdstatedir}/pubconf

### Build Dependencies ###

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: m4
%{?fedora:BuildRequires: popt-devel}
%if 0%{?is_rhel5} > 0
BuildRequires: popt
%endif
%if 0%{?rhel} >= 6
BuildRequires: popt-devel
%endif
BuildRequires: libtalloc-devel
BuildRequires: libtevent-devel
BuildRequires: libtdb-devel
BuildRequires: libldb-devel
BuildRequires: libdhash-devel >= 0.4.2
BuildRequires: libcollection-devel
BuildRequires: libini_config-devel
BuildRequires: dbus-devel
BuildRequires: dbus-libs
%if 0%{?rhel5_minor} >= 7
BuildRequires: openldap24-libs-devel
%else
BuildRequires: openldap-devel
%endif
BuildRequires: pam-devel
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: pcre-devel
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: docbook-style-xsl
BuildRequires: krb5-devel
BuildRequires: c-ares-devel
BuildRequires: python-devel
BuildRequires: check-devel
BuildRequires: doxygen
BuildRequires: libselinux-devel
BuildRequires: libsemanage-devel
BuildRequires: bind-utils
BuildRequires: keyutils-libs-devel
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: findutils
BuildRequires: glib2-devel
BuildRequires: selinux-policy-targeted
%if (0%{?fedora} >= 18)
BuildRequires: libcmocka-devel
BuildRequires: libnl3-devel
%else
BuildRequires: libnl-devel
%endif

# RHEL 5 is too old to support samba4 and the PAC responder
%if !0%{?is_rhel5}
BuildRequires: samba4-devel
%endif

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a pluggable backend system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

The sssd subpackage is a meta-package that contains the deamon as well as all
the existing back ends.

%package common
Summary: Common files for the SSSD
Group: Applications/System
License: GPLv3+
Requires: libldb >= 0.9.3
Requires: libtdb >= 1.1.3
Requires: sssd-client%{?_isa} = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
Conflicts: sssd < %{version}-%{release}
%if (0%{?use_systemd} == 1)
Requires(post): systemd-units systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
%else
Requires(post): initscripts chkconfig
Requires(preun):  initscripts chkconfig
Requires(postun): initscripts chkconfig
%endif

### Provides ###
Provides: libsss_sudo = %{version}-%{release}
Obsoletes: libsss_sudo <= 1.9.93
Provides: libsss_sudo-devel = %{version}-%{release}
Obsoletes: libsss_sudo-devel <= 1.9.93
Provides: libsss_autofs = %{version}-%{release}
Obsoletes: libsss_autofs <= 1.9.93

%description common
Common files for the SSSD. The common package includes all the files needed
to run a particular back end, however, the back ends are packaged in separate
subpackages such as sssd-ldap.

%package client
Summary: SSSD Client libraries for NSS and PAM
Group: Applications/System
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description client
Provides the libraries needed by the PAM and NSS stacks to connect to the SSSD
service.

%package tools
Summary: Userspace tools for use with the SSSD
Group: Applications/System
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description tools
Provides userspace tools for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides several other administrative tools:
    * sss_debuglevel to change the debug level on the fly
    * sss_seed which pre-creates a user entry for use in kickstarts
    * sss_obfuscate for generating an obfuscated LDAP password

%package -n python-sssdconfig
Summary: SSSD and IPA configuration file manipulation classes and functions
Group: Applications/System
License: GPLv3+
BuildArch: noarch

%description -n python-sssdconfig
Provides python files for manipulation SSSD and IPA configuration files.

%package ldap
Summary: The LDAP back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < %{version}-%{release}
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}

%description ldap
Provides the LDAP back end that the SSSD can utilize to fetch identity data
from and authenticate against an LDAP server.

%package krb5-common
Summary: SSSD helpers needed for Kerberos and GSSAPI authentication
Group: Applications/System
License: GPLv3+
Conflicts: sssd < %{version}-%{release}
Requires: cyrus-sasl-gssapi
Requires: sssd-common = %{version}-%{release}

%description krb5-common
Provides helper processes that the LDAP and Kerberos back ends can use for
Kerberos user or host authentication.

%package krb5
Summary: The Kerberos authentication back end for the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < %{version}-%{release}
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}

%description krb5
Provides the Kerberos back end that the SSSD can utilize authenticate
against a Kerberos server.

# RHEL 5 is too old to support the PAC responder
%if !0%{?is_rhel5}
%package common-pac
Summary: Common files needed for supporting PAC processing
Group: Applications/System
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description common-pac
Provides common files needed by SSSD providers such as IPA and Active Directory
for handling Kerberos PACs.
%endif #is_rhel5

%package ipa
Summary: The IPA back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < %{version}-%{release}
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: libipa_hbac = %{version}-%{release}
Requires: bind-utils
# RHEL 5 is too old to support the PAC responder
%if !0%{?is_rhel5}
Requires: sssd-common-pac = %{version}-%{release}
%endif

%description ipa
Provides the IPA back end that the SSSD can utilize to fetch identity data
from and authenticate against an IPA server.

%package ad
Summary: The AD back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < %{version}-%{release}
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: bind-utils
# RHEL 5 is too old to support the PAC responder
%if !0%{?is_rhel5}
Requires: sssd-common-pac = %{version}-%{release}
%endif

%description ad
Provides the Active Directory back end that the SSSD can utilize to fetch
identity data from and authenticate against an Active Directory server.

%package proxy
Summary: The proxy back end of the SSSD
Group: Applications/System
License: GPLv3+
Conflicts: sssd < %{version}-%{release}
Requires: sssd-common = %{version}-%{release}

%description proxy
Provides the proxy back end which can be used to wrap an existing NSS and/or
PAM modules to leverage SSSD caching.

%package -n libsss_idmap
Summary: FreeIPA Idmap library
Group: Development/Libraries
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libsss_idmap
Utility library to convert SIDs to Unix uids and gids

%package -n libsss_idmap-devel
Summary: FreeIPA Idmap library
Group: Development/Libraries
License: LGPLv3+
Requires: libsss_idmap = %{version}-%{release}

%description -n libsss_idmap-devel
Utility library to SIDs to Unix uids and gids

%package -n libipa_hbac
Summary: FreeIPA HBAC Evaluator library
Group: Development/Libraries
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libipa_hbac
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n libipa_hbac-devel
Summary: FreeIPA HBAC Evaluator library
Group: Development/Libraries
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-devel
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n libipa_hbac-python
Summary: Python bindings for the FreeIPA HBAC Evaluator library
Group: Development/Libraries
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-python
The libipa_hbac-python contains the bindings so that libipa_hbac can be
used by Python applications.

%package -n libsss_nss_idmap
Summary: Library for SID based lookups
Group: Development/Libraries
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libsss_nss_idmap
Utility library for SID based lookups

%package -n libsss_nss_idmap-devel
Summary: Library for SID based lookups
Group: Development/Libraries
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}

%description -n libsss_nss_idmap-devel
Utility library for SID based lookups

%package -n libsss_nss_idmap-python
Summary: Python bindings for libsss_nss_idmap
Group: Development/Libraries
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}

%description -n libsss_nss_idmap-python
The libsss_nss_idmap-python contains the bindings so that libsss_nss_idmap can
be used by Python applications.

%package dbus
Summary: The D-Bus responder of the SSSD
Group: Applications/System
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description dbus
Provides the D-Bus responder of the SSSD, called the InfoPipe, that allows
the information from the SSSD to be transmitted over the system bus.

%prep
%setup -q -n %{name}-%{version}

%build

# RHEL 5 uses an old libtool, so we need to force it to reconfigure
# This is safe to do on newer packages too, as it will just
# gather the appropriate m4 files from the libtool package
for i in libtool.m4  lt~obsolete.m4  ltoptions.m4  ltsugar.m4  ltversion.m4
do
    find . -name $i -exec rm -f {} \;
done

autoreconf -ivf

%configure \
    --with-test-dir=/dev/shm \
    --with-db-path=%{dbpath} \
    --with-mcache-path=%{mcpath} \
    --with-pipe-path=%{pipepath} \
    --with-pubconf-path=%{pubconfpath} \
    --with-init-dir=%{_initrddir} \
    --with-krb5-rcache-dir=%{_localstatedir}/cache/krb5rcache \
    --enable-nsslibdir=/%{_lib} \
    --enable-pammoddir=/%{_lib}/security \
    --disable-static \
    --disable-rpath \
    %{?with_ccache} \
    %{with_initscript} \
    %{?experimental}

make %{?_smp_mflags} all


# Only build docs on recent distros
%if 0%{?fedora}
make %{?_smp_mflags} docs
%endif

%if 0%{?rhel} >= 6
make %{?_smp_mflags} docs
%endif


%check
export CK_TIMEOUT_MULTIPLIER=10
make %{?_smp_mflags} check
unset CK_TIMEOUT_MULTIPLIER

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Prepare language files
/usr/lib/rpm/find-lang.sh $RPM_BUILD_ROOT sssd

# Prepare empty config file (needed for RHEL 5)
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sssd
touch $RPM_BUILD_ROOT/%{_sysconfdir}/sssd/sssd.conf

# Copy default logrotate file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
install -m644 src/examples/logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rwtab.d
install -m644 src/examples/rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/sssd

# Remove .la files created by libtool
find $RPM_BUILD_ROOT -name "*.la" -exec rm -f {} \;

# Suppress developer-only documentation
rm -Rf ${RPM_BUILD_ROOT}/%{_docdir}/%{name}

# Older versions of rpmbuild can only handle one -f option
# So we need to append to the sssd*.lang file
for file in `ls $RPM_BUILD_ROOT/%{python_sitelib}/*.egg-info 2> /dev/null`
do
    echo %{python_sitelib}/`basename $file` >> python_sssdconfig.lang
done

touch sssd.lang
touch sssd_tools.lang
touch sssd_client.lang
for provider in ldap krb5 ipa ad proxy
do
    touch sssd_$provider.lang
done

for man in `find $RPM_BUILD_ROOT/%{_mandir}/??/man?/ -type f | sed -e "s#$RPM_BUILD_ROOT/%{_mandir}/##"`
do
    lang=`echo $man | cut -c 1-2`
    case `basename $man` in
        sss_cache*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
        sss_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
            ;;
        sssd_krb5_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        pam_sss*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        sssd-ldap*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ldap.lang
            ;;
        sssd-krb5*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_krb5.lang
            ;;
        sssd-ipa*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ipa.lang
            ;;
        sssd-ad*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ad.lang
            ;;
        sssd-proxy*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_proxy.lang
            ;;
        *)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
    esac
done

# Old versions of rpmbuild require ghost files to be present in the buildroot
mkdir -p $RPM_BUILD_ROOT/%{mcpath}
touch $RPM_BUILD_ROOT/%{mcpath}/passwd
touch $RPM_BUILD_ROOT/%{mcpath}/group

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING

%files common -f sssd.lang
%defattr(-,root,root,-)
%doc COPYING
%doc src/examples/sssd-example.conf
%{_sbindir}/sssd
%if (0%{?use_systemd} == 1)
%{_unitdir}/sssd.service
%else
%{_initrddir}/%{name}
%endif

%dir %{_libexecdir}/%{servicename}
%{_libexecdir}/%{servicename}/sssd_be
%{_libexecdir}/%{servicename}/sssd_nss
%{_libexecdir}/%{servicename}/sssd_pam

%{_libexecdir}/%{servicename}/sssd_autofs
%{_libexecdir}/%{servicename}/sssd_ssh
%{_libexecdir}/%{servicename}/sssd_sudo

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libsss_simple.so

#Internal shared libraries
%{_libdir}/%{name}/libsss_child.so
%{_libdir}/%{name}/libsss_crypt.so
%{_libdir}/%{name}/libsss_debug.so
%{_libdir}/%{name}/libsss_ldap_common.so
%{_libdir}/%{name}/libsss_util.so

# 3rd party application libraries
%{_libdir}/sssd/modules/libsss_autofs.so
%{_libdir}/libsss_sudo.so

%{ldb_modulesdir}/memberof.so
%{_bindir}/sss_ssh_authorizedkeys
%{_bindir}/sss_ssh_knownhostsproxy
%{_sbindir}/sss_cache
%{_libexecdir}/%{servicename}/sss_signal

%dir %{sssdstatedir}
%dir %{_localstatedir}/cache/krb5rcache
%attr(700,root,root) %dir %{dbpath}
%attr(755,root,root) %dir %{mcpath}
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %{mcpath}/passwd
%ghost %attr(0644,root,root) %verify(not md5 size mtime) %{mcpath}/group
%attr(755,root,root) %dir %{pipepath}
%attr(755,root,root) %dir %{pubconfpath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(711,root,root) %dir %{_sysconfdir}/sssd
%ghost %attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sssd/sssd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/sssd
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%dir %{_datadir}/sssd
%{_datadir}/sssd/sssd.api.conf
%{_datadir}/sssd/sssd.api.d
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man5/sssd-sudo.5*
%{_mandir}/man8/sssd.8*
%{_mandir}/man8/sss_cache.8*
%{_mandir}/man1/sss_ssh_authorizedkeys.1*
%{_mandir}/man1/sss_ssh_knownhostsproxy.1*
%{python_sitearch}/pysss.so
%{python_sitearch}/pysss_murmur.so

%files ldap -f sssd_ldap.lang
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_ldap.so
%{_mandir}/man5/sssd-ldap.5*

%files krb5-common
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_krb5_common.so
%{_libexecdir}/%{servicename}/ldap_child
%{_libexecdir}/%{servicename}/krb5_child

%files krb5 -f sssd_krb5.lang
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_krb5.so
%{_mandir}/man5/sssd-krb5.5*

# RHEL 5 is too old to support the PAC responder
%if !0%{?is_rhel5}
%files common-pac
%defattr(-,root,root,-)
%doc COPYING
%{_libexecdir}/%{servicename}/sssd_pac
%endif


%files ipa -f sssd_ipa.lang
%defattr(-,root,root,-)
%doc COPYING
%attr(755,root,root) %dir %{pubconfpath}/krb5.include.d
%{_libdir}/%{name}/libsss_ipa.so
%{_mandir}/man5/sssd-ipa.5*

%files ad -f sssd_ad.lang
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/%{name}/libsss_ad.so
%{_mandir}/man5/sssd-ad.5*

%files proxy
%defattr(-,root,root,-)
%doc COPYING
%{_libexecdir}/%{servicename}/proxy_child
%{_libdir}/%{name}/libsss_proxy.so

%files dbus
%defattr(-,root,root,-)
%doc COPYING
%{_libexecdir}/%{servicename}/sssd_ifp
%{_mandir}/man5/sssd-ifp.5*
# InfoPipe DBus plumbing
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.sssd.infopipe.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.sssd.infopipe.service

%files client -f sssd_client.lang
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
/%{_lib}/libnss_sss.so.2
/%{_lib}/security/pam_sss.so
%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%if !0%{?is_rhel5}
%{_libdir}/krb5/plugins/authdata/sssd_pac_plugin.so
%endif
%{_mandir}/man8/pam_sss.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*

%files tools -f sssd_tools.lang
%defattr(-,root,root,-)
%doc COPYING
%{_sbindir}/sss_useradd
%{_sbindir}/sss_userdel
%{_sbindir}/sss_usermod
%{_sbindir}/sss_groupadd
%{_sbindir}/sss_groupdel
%{_sbindir}/sss_groupmod
%{_sbindir}/sss_groupshow
%{_sbindir}/sss_obfuscate
%{_sbindir}/sss_debuglevel
%{_sbindir}/sss_seed
%{_mandir}/man8/sss_groupadd.8*
%{_mandir}/man8/sss_groupdel.8*
%{_mandir}/man8/sss_groupmod.8*
%{_mandir}/man8/sss_groupshow.8*
%{_mandir}/man8/sss_useradd.8*
%{_mandir}/man8/sss_userdel.8*
%{_mandir}/man8/sss_usermod.8*
%{_mandir}/man8/sss_obfuscate.8*
%{_mandir}/man8/sss_debuglevel.8*
%{_mandir}/man8/sss_seed.8*

%files -n python-sssdconfig -f python_sssdconfig.lang
%defattr(-,root,root,-)
%dir %{python_sitelib}/SSSDConfig
%{python_sitelib}/SSSDConfig/*.py*

%files -n libsss_idmap
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_idmap.so.*

%files -n libsss_idmap-devel
%defattr(-,root,root,-)
%if 0%{?fedora}
%doc idmap_doc/html
%endif
%if 0%{?rhel} >= 6
%doc idmap_doc/html
%endif
%{_includedir}/sss_idmap.h
%{_libdir}/libsss_idmap.so
%{_libdir}/pkgconfig/sss_idmap.pc

%files -n libipa_hbac
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libipa_hbac.so.*

%files -n libipa_hbac-devel
%defattr(-,root,root,-)
%if 0%{?fedora}
%doc hbac_doc/html
%endif
%if 0%{?rhel} >= 6
%doc hbac_doc/html
%endif
%{_includedir}/ipa_hbac.h
%{_libdir}/libipa_hbac.so
%{_libdir}/pkgconfig/ipa_hbac.pc

%files -n libsss_nss_idmap
%defattr(-,root,root,-)
%doc src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_nss_idmap.so.*

%files -n libsss_nss_idmap-devel
%defattr(-,root,root,-)
%if 0%{?fedora}
%doc nss_idmap_doc/html
%endif
%if 0%{?rhel} >= 6
%doc nss_idmap_doc/html
%endif
%{_includedir}/sss_nss_idmap.h
%{_libdir}/libsss_nss_idmap.so
%{_libdir}/pkgconfig/sss_nss_idmap.pc

%files -n libsss_nss_idmap-python
%defattr(-,root,root,-)
%{python_sitearch}/pysss_nss_idmap.so

%files -n libipa_hbac-python
%defattr(-,root,root,-)
%{python_sitearch}/pyhbac.so

%if (0%{?use_systemd} == 1)
# systemd
%post common
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun common
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable sssd.service > /dev/null 2>&1 || :
    /bin/systemctl stop sssd.service > /dev/null 2>&1 || :
fi

%postun common
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart sssd.service >/dev/null 2>&1 || :
fi

%else
# sysv
%post common
/sbin/chkconfig --add %{servicename}

%posttrans
/sbin/service %{servicename} condrestart 2>&1 > /dev/null

%preun common
if [ $1 = 0 ]; then
    /sbin/service %{servicename} stop 2>&1 > /dev/null
    /sbin/chkconfig --del %{servicename}
fi
%endif

%post client -p /sbin/ldconfig

%postun client -p /sbin/ldconfig

%post -n libipa_hbac -p /sbin/ldconfig

%postun -n libipa_hbac -p /sbin/ldconfig

%post -n libsss_idmap -p /sbin/ldconfig

%postun -n libsss_idmap -p /sbin/ldconfig

%post -n libsss_nss_idmap -p /sbin/ldconfig

%postun -n libsss_nss_idmap -p /sbin/ldconfig

%changelog
* Mon Mar 15 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.11.7-0
- Automated build of the SSSD
