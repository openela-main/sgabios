%if 0%{?fedora}
%define cross 1
%endif

%global hash cbaee52
%global date 20170427


Name:           sgabios
Epoch:          1
Version:        0.%{date}git
Release:        3%{?dist}
Summary:        Serial graphics BIOS option rom

Group:          Applications/Emulators
License:        ASL 2.0
URL:            https://github.com/qemu/sgabios
# There are no upstream releases.  This archive is prepared as follows:
#
# git clone https://github.com/qemu/sgabios
# cd sgabios
# hash=`git log -1 --format='%h'`
# date=`git log -1 --format='%cd' --date=short | tr -d -`
# git archive --prefix sgabios-${date}-git${hash}/ ${hash} | xz -7e > ../openbios-${date}-git${hash}.tar.xz
Source0:        sgabios-%{date}-git%{hash}.tar.xz
Patch0:         sgabios-hostcc.patch

%if 0%{?cross}
BuildRequires:  binutils-x86_64-linux-gnu gcc-x86_64-linux-gnu
Buildarch: noarch
%else
ExclusiveArch: %{ix86} x86_64
%endif

Requires: %{name}-bin = %{epoch}:%{version}-%{release}

# Sgabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

%description
SGABIOS is designed to be inserted into a BIOS as an option rom to provide over
a serial port the display and input capabilities normally handled by a VGA
adapter and a keyboard, and additionally provide hooks for logging displayed
characters for later collection after an operating system boots.


%package bin
Summary: Sgabios for x86
Buildarch: noarch

%description bin
SGABIOS is designed to be inserted into a BIOS as an option rom to provide over
a serial port the display and input capabilities normally handled by a VGA
adapter and a keyboard, and additionally provide hooks for logging displayed
characters for later collection after an operating system boots.


%prep
%setup -q -n sgabios-%{date}-git%{hash}
%autopatch


%build
unset MAKEFLAGS
make \
        HOSTCC=gcc \
%if 0%{?cross}
        CC=x86_64-linux-gnu-gcc \
        AS=x86_64-linux-gnu-as \
        LD=x86_64-linux-gnu-ld \
        OBJCOPY=x86_64-linux-gnu-objcopy \
        OBJDUMP=x86_64-linux-gnu-objdump
%endif


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sgabios
install -m 0644 sgabios.bin $RPM_BUILD_ROOT%{_datadir}/sgabios


%files
%doc COPYING design.txt


%files bin
%dir %{_datadir}/sgabios/
%{_datadir}/sgabios/sgabios.bin


%changelog
* Fri Jun 28 2019 Danilo de Paula <ddepaula@redhat.com> - 1:0.20170427git-3
- Rebuild all virt packages to fix RHEL's upgrade path
- Resolves: rhbz#1695587
  (Ensure modular RPM upgrade path)

* Wed Jun 27 2018 Danilo de Paula <ddepaula@redhat.com> - 1:0.20170427git-2
- Trigger a new sgabios build

* Sun Mar 25 2018 Cole Robinson <crobinso@redhat.com> - 1:0.20170427git-1
- Switch to qemu sgabios repo, which has an extra bugfix

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Paolo Bonzini <pbonzini@redhat.com> - 1:0.20110622svn-12
- Allow disabling cross-compilation

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110622svn-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110622svn-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1:0.20110622svn-3
- Root sgabios package is noarch too because it only contains docs

* Thu Oct 25 2012 Paolo Bonzini <pbonzini@redhat.com> - 1:0.20110622svn-2
- Cross compile (fixes bug #869876).

* Wed Oct 17 2012 Cole Robinson <crobinso@redhat.com> - 1:0.20110622svn-2
- Fix deps with epoch bump

* Mon Oct 15 2012 Paolo Bonzini <pbonzini@redhat.com> - 1:0.20110622svn-1
- Move date from release to version (requires epoch bump).

* Sun Aug 12 2012 Richard W.M. Jones <rjones@redhat.com> - 0-1.1.20110622svn
- Fix date in release string.
  NB: To make this version > than the previous, I had to use 1.1.20110622
  instead of 0.1.20110622, since the old second field was 20110623.
- Unset MAKEFLAGS, since parallel make breaks the build.
- Bring the spec file up to modern standards.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.20110623SVN
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.20110622SVN
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Justin M. Forbes <jforbes@redhat.com> 0.0-0.20110621SVN
- Updates per review.

* Tue Jun 21 2011 Justin M. Forbes <jforbes@redhat.com> 0.1-0.20110621SVN
- Created initial package
