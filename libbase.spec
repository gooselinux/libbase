# Use rpmbuild --without gcj to disable native bits
%define with_gcj %{!?_without_gcj:1}%{?_without_gcj:0}

Name: libbase
Version: 1.0.0
Release: 3.OOo31.1%{?dist}
Summary: JFree Base Services
License: LGPLv2+
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/jfreereport/%{name}-%{version}-OOo31.zip
URL: http://reporting.pentaho.org/
BuildRequires: ant, java-devel, jpackage-utils, jakarta-commons-logging
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: java, jpackage-utils, jakarta-commons-logging
%if %{with_gcj}
BuildRequires: java-gcj-compat-devel >= 1.0.31
Requires(post): java-gcj-compat >= 1.0.31
Requires(postun): java-gcj-compat >= 1.0.31
%else
BuildArch: noarch
%endif

%description
LibBase is a library developed to provide base services like logging,
configuration and initialization to other libraries and applications. The
library is the root library for all Pentaho-Reporting projects.

%package javadoc
Summary: Javadoc for %{name}
Group: Development/Documentation
Requires: %{name} = %{version}-%{release}
Requires: jpackage-utils
%if %{with_gcj}
BuildArch: noarch
%endif

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -c
mkdir -p lib
find . -name "*.jar" -exec rm -f {} \;
build-jar-repository -s -p lib commons-logging-api

%build
ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/api $RPM_BUILD_ROOT%{_javadocdir}/%{name}
%if %{with_gcj}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{with_gcj}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc ChangeLog.txt licence-LGPL.txt README.txt
%{_javadir}/%{name}.jar
%if %{with_gcj}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.0.0-3.OOo31.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Caolan McNamara <caolanm@redhat.com> 1.0.0-3.OOo31
- make javadoc no-arch when building as arch-dependant aot

* Mon Mar 16 2009 Caolan McNamara <caolanm@redhat.com> 1.0.0-2.OOo31
- Post released tuned for OpenOffice.org reportbuilder

* Wed Dec 03 2008 Caolan McNamara <caolanm@redhat.com> 1.0.0-1
- initial fedora import
