Summary:	Shepherd service manager
Summary(pl.UTF-8):	Zarządca usług Shepherd
Name:		shepherd
Version:	0.10.2
Release:	0.1
License:	GPL v3+ (daemon), FDL v1.3+ (documentation)
Group:		Daemons
Source0:	https://ftp.gnu.org/gnu/shepherd/%{name}-%{version}.tar.gz
# Source0-md5:	6afe8676a82ce5ede5c86e8d55e5dc33
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/shepherd/
BuildRequires:	gettext-tools >= 0.19
BuildRequires:	guile-devel >= 5:2.2
BuildRequires:	guile-fibers >= 1.3.0
BuildRequires:	help2man
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	texinfo
Requires:	guile >= 5:2.2
Requires:	guile-fibers >= 1.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautostrip	.*\.go

%description
The GNU Daemon Shepherd, or GNU Shepherd is a service manager written
in Guile that looks after the herd of system services, providing a
replacement for the service-managing capabilities of SysV-init (or any
other init) with a dependency-based system with a convenient
interface. It is intended for use on GNU/Linux and GNU/Hurd, but it is
supposed to work on every POSIX-like system where Guile is available.

In a previous life, the GNU Shepherd was known as GNU dmd, the
daemon-managing daemon.

%description -l pl.UTF-8
GNU Daemon Shepherd lub GNU Shepherd (pasterz) to napisany w języku
Guile zarządca usług, pilnujący stada usług systemowych. Dostarcza
zamiennik funkcjonalności zarządzania usługami z SysV-init (lub
dowolnego innego inita) z systemem opartym na zależnościach i wygodnym
interfejsem. Głównym zastosowaniem są systemy GNU/Linux lub GNU/Hurd,
ale powinien działać na dowolnym systemie zgodnym z POSIX, gdzie
dostępny jest Guile.

W poprzednim życiu GNU Shepherd był znany jako GNU dmd -
daemon-managing daemon (demon zarządzający demonami).

%package init
Summary:	SysV init replacement tools
Summary(pl.UTF-8):	Zamiennik narzędzi z SysV init
Group:		Daemons
Requires:	%{name} = %{version}-%{release}

%description init
SysV init replacement tools.

%description init -l pl.UTF-8
Zamiennik narzędzi z SysV init.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--disable-silent-rules \
	--with-bash-completion-dir=%{bash_compdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cat >$RPM_BUILD_ROOT%{systemdtmpfilesdir}/shepherd.conf <<EOF
d /var/run/shepherd 0700 root root -
EOF

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog* NEWS README THANKS TODO
%attr(755,root,root) %{_bindir}/herd
%attr(755,root,root) %{_bindir}/shepherd
%dir %{_libdir}/shepherd
%attr(755,root,root) %{_libdir}/shepherd/crash-handler.so
%{_libdir}/guile/*.*/site-ccache/shepherd.go
%{_libdir}/guile/*.*/site-ccache/shepherd
%dir %{_libdir}/guile/*.*/site-ccache
%{_datadir}/guile/site/*.*/shepherd.scm
%{_datadir}/guile/site/*.*/shepherd
%dir /var/run/shepherd
%{systemdtmpfilesdir}/shepherd.conf
%{bash_compdir}/herd
%{_infodir}/shepherd.info*
%{_mandir}/man1/herd.1*
%{_mandir}/man1/shepherd.1*

%files init
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/halt
%attr(755,root,root) %{_sbindir}/reboot
%attr(755,root,root) %{_sbindir}/shutdown
%{_mandir}/man8/halt.8*
%{_mandir}/man8/reboot.8*
