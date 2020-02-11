# Build conditionals (with - OFF, without - ON)...
%bcond_with rlottie
%bcond_with gtk3
%bcond_with clang
%bcond_without spellcheck
%bcond_without fonts
%bcond_without ipo
%bcond_without mindbg

# Telegram Desktop's constants...
%global appname tdesktop
%global launcher telegramdesktop
%global tarsuffix -full

# Telegram API tokens...
%global apiid 208164
%global apihash dfbe1bc42dc9d20507e17d1814cc2f0a

# Applying workaround to RHBZ#1559007...
%if %{with clang}
%global optflags %(echo %{optflags} | sed -e 's/-mcet//g' -e 's/-fcf-protection//g' -e 's/-fstack-clash-protection//g' -e 's/$/-Qunused-arguments -Wno-unknown-warning-option/')
%endif

# Decrease debuginfo verbosity to reduce memory consumption...
%if %{with mindbg}
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

Name: telegram-desktop
Version: 1.9.10
Release: 1%{?dist}

# Application and 3rd-party modules licensing:
# * Telegram Desktop - GPLv3+ with OpenSSL exception -- main tarball;
# * rlottie - LGPLv2+ -- static dependency;
# * qt_functions.cpp - LGPLv3 -- build-time dependency.
License: GPLv3+ and LGPLv2+ and LGPLv3
URL: https://github.com/telegramdesktop/%{appname}
Summary: Telegram Desktop official messaging app
ExclusiveArch: x86_64

# Source files...
Source0: %{url}/releases/download/v%{version}/%{appname}-%{version}%{tarsuffix}.tar.gz

# Permanent downstream patches...
Patch10: cmake_helpers-system-qrcode.patch

# Telegram Desktop require exact version of Qt due to Qt private API usage.
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Requires: qt5-qtimageformats%{?_isa}
Requires: hicolor-icon-theme

# Telegram Desktop require patched version of rlottie since 1.8.0.
# Pull Request pending: https://github.com/Samsung/rlottie/pull/252
%if %{with rlottie}
BuildRequires: rlottie-devel
%else
Provides: bundled(rlottie) = 0~git
%endif

# Telegram Desktop require patched version of lxqt-qtplugin.
# Pull Request pending: https://github.com/lxqt/lxqt-qtplugin/pull/52
Provides: bundled(lxqt-qtplugin) = 0.14.0~git

# Compilers and tools...
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: gcc

# Development packages for Telegram Desktop...
BuildRequires: guidelines-support-library-devel >= 1.0.0
BuildRequires: mapbox-variant-devel >= 0.3.6
BuildRequires: qt5-qtbase-private-devel
BuildRequires: libtgvoip-devel >= 2.4.4
BuildRequires: range-v3-devel >= 0.10.0
BuildRequires: libqrcodegencpp-devel
BuildRequires: minizip-compat-devel
BuildRequires: ffmpeg-devel >= 3.1
BuildRequires: dbusmenu-qt5-devel
BuildRequires: openal-soft-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: libstdc++-devel
BuildRequires: expected-devel
BuildRequires: openssl-devel
BuildRequires: xxhash-devel
BuildRequires: json11-devel
BuildRequires: ninja-build
BuildRequires: opus-devel
BuildRequires: lz4-devel
BuildRequires: xz-devel
BuildRequires: python3

%if %{with gtk3}
BuildRequires: libappindicator-gtk3-devel
BuildRequires: glib2-devel
BuildRequires: gtk3-devel
Recommends: libappindicator-gtk3%{?_isa}
Requires: gtk3%{?_isa}
%endif

%if %{with spellcheck}
BuildRequires: enchant2-devel
BuildRequires: glib2-devel
Requires: enchant2%{?_isa}
Requires: hunspell%{?_isa}
%endif

%if %{with clang}
BuildRequires: compiler-rt
BuildRequires: clang
BuildRequires: llvm
%endif

%if %{with fonts}
Requires: open-sans-fonts
%endif

%description
Telegram is a messaging app with a focus on speed and security, it’s super
fast, simple and free. You can use Telegram on all your devices at the same
time — your messages sync seamlessly across any number of your phones,
tablets or computers.

With Telegram, you can send messages, photos, videos and files of any type
(doc, zip, mp3, etc), as well as create groups for up to 50,000 people or
channels for broadcasting to unlimited audiences. You can write to your
phone contacts and find people by their usernames. As a result, Telegram is
like SMS and email combined — and can take care of all your personal or
business messaging needs.

%prep
# Unpacking Telegram Desktop source archive...
%autosetup -n %{appname}-%{version}%{tarsuffix} -p1
mkdir -p %{_target_platform}

# Unbundling libraries...
rm -rf Telegram/ThirdParty/{Catch,GSL,QR,SPMediaKeyTap,expected,libdbusmenu-qt,libtgvoip,lz4,minizip,variant,xxHash}

# Patching default desktop file...
desktop-file-edit --set-key=Exec --set-value="%{_bindir}/%{name} -- %u" --copy-name-to-generic-name lib/xdg/telegramdesktop.desktop

%build
# Building Telegram Desktop using cmake...
pushd %{_target_platform}
    %cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
%if %{without gtk3}
    -DTDESKTOP_DISABLE_GTK_INTEGRATION:BOOL=ON \
%endif
%if %{without spellcheck}
    -DDESKTOP_APP_DISABLE_SPELLCHECK:BOOL=ON \
%endif
%if %{without fonts}
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=OFF \
%endif
%if %{with ipo} && %{with mindbg} && %{without clang}
    -DDESKTOP_APP_ENABLE_IPO_OPTIMIZATIONS:BOOL=ON \
%endif
%if %{with rlottie}
    -DDESKTOP_APP_USE_PACKAGED_RLOTTIE:BOOL=ON \
%else
    -DDESKTOP_APP_USE_PACKAGED_RLOTTIE:BOOL=OFF \
%endif
%if %{with clang}
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_AR=%{_bindir}/llvm-ar \
    -DCMAKE_RANLIB=%{_bindir}/llvm-ranlib \
    -DCMAKE_LINKER=%{_bindir}/llvm-ld \
    -DCMAKE_OBJDUMP=%{_bindir}/llvm-objdump \
    -DCMAKE_NM=%{_bindir}/llvm-nm \
%else
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
%endif
    -DTDESKTOP_API_ID=%{apiid} \
    -DTDESKTOP_API_HASH=%{apihash} \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_EXPECTED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_VARIANT:BOOL=ON \
    -DDESKTOP_APP_USE_GLIBC_WRAPS:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
    -DTDESKTOP_USE_PACKAGED_TGVOIP:BOOL=ON \
    -DTDESKTOP_DISABLE_REGISTER_CUSTOM_SCHEME:BOOL=ON \
    -DTDESKTOP_DISABLE_DESKTOP_FILE_GENERATION:BOOL=ON \
    -DTDESKTOP_LAUNCHER_BASENAME=%{launcher} \
    ..
popd
%ninja_build -C %{_target_platform}

%install
%ninja_install -C %{_target_platform}

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{launcher}.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/%{launcher}.desktop

%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/%{name}
%{_datadir}/applications/%{launcher}.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_metainfodir}/%{launcher}.appdata.xml

%changelog
* Thu Feb 06 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.10-1
- Updated to version 1.9.10 (beta).

* Wed Jan 29 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.9-1
- Updated to version 1.9.9.
- Enabled LTO for all supported releases.

* Fri Jan 24 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.8-1
- Updated to version 1.9.8.
