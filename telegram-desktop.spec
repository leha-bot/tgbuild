# Build conditionals...
%bcond_with gtk3
%bcond_with clang
%bcond_with spellcheck

# Telegram Desktop's constants...
%global appname tdesktop
%global apiid 208164
%global apihash dfbe1bc42dc9d20507e17d1814cc2f0a

# Git revision of cmake_helpers...
%global commit1 652bbaf002546ae1822fff4474ffe95091bfc2e4
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

# Git revision of patched rlottie...
%global commit2 c490c7a098b9b3cbc3195b00e90d6fc3989e2ba2
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})

# Git revision of lib_crl...
%global commit3 5a740bf0b7fe8f1f9a7f3e0878d5238f56502da1
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})

# Git revision of lib_base...
%global commit4 baae6cdd9ba5216732222e7dec9a76b9ea3a7c83
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})

# Git revision of lib_lottie...
%global commit5 a0a0269ffa44d1e23f0911eaeb286004a075b089
%global shortcommit5 %(c=%{commit5}; echo ${c:0:7})

# Git revision of lib_qr...
%global commit6 9877397dbf97b7198d539a3994bf0e9619cf653c
%global shortcommit6 %(c=%{commit6}; echo ${c:0:7})

# Git revision of lib_rpl...
%global commit7 2888aabf28bf9ca89f3d6d67a523bc5f2ce802ce
%global shortcommit7 %(c=%{commit7}; echo ${c:0:7})

# Git revision of lib_spellcheck...
%global commit8 d305de6d67ca4f3891bad96a0e49e40f5c904189
%global shortcommit8 %(c=%{commit8}; echo ${c:0:7})

# Git revision of lib_storage...
%global commit9 cb56ad46ca1bee22570a7f3f64d21531283ad84d
%global shortcommit9 %(c=%{commit9}; echo ${c:0:7})

# Git revision of lib_tl...
%global commit10 b0388a1a02b3f035f1486a6b66a01522c290b198
%global shortcommit10 %(c=%{commit10}; echo ${c:0:7})

# Git revision of lib_ui...
%global commit11 4ec9e32f8f5f6b8192fd60d73ae0b575e82c1c60
%global shortcommit11 %(c=%{commit11}; echo ${c:0:7})

# Decrease debuginfo verbosity to reduce memory consumption...
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

# Applying workaround to RHBZ#1559007...
%if %{with clang}
%global optflags %(echo %{optflags} | sed -e 's/-mcet//g' -e 's/-fcf-protection//g' -e 's/-fstack-clash-protection//g' -e 's/$/-Qunused-arguments -Wno-unknown-warning-option/')
%endif

Summary: Telegram Desktop official messaging app
Name: telegram-desktop
Version: 1.9.3
Release: 1%{?dist}

# Application and 3rd-party modules licensing:
# * S0 (Telegram Desktop) - GPLv3+ with OpenSSL exception -- main source;
# * S1 (crl) - GPLv3+ -- build-time dependency;
# * S2 (rlottie) - LGPLv2+ -- static dependency;
# * P0 (qt_functions.cpp) - LGPLv3 -- build-time dependency.
License: GPLv3+ and LGPLv3
URL: %{upstreambase}/%{appname}

%if 0%{?fedora} && 0%{?fedora} < 31
ExclusiveArch: i686 x86_64
%else
ExclusiveArch: x86_64
%endif

# Source files...
Source0: %{url}/archive/v%{version}/%{appname}-%{version}.tar.gz
Source1: https://github.com/desktop-app/cmake_helpers/archive/%{commit1}/cmake_helpers-%{shortcommit1}.tar.gz
Source2: https://github.com/desktop-app/rlottie/archive/%{commit2}/rlottie-%{shortcommit2}.tar.gz
Source3: https://github.com/desktop-app/lib_crl/archive/%{commit3}/lib_crl-%{shortcommit3}.tar.gz
Source4: https://github.com/desktop-app/lib_base/archive/%{commit4}/lib_base-%{shortcommit4}.tar.gz
Source5: https://github.com/desktop-app/lib_lottie/archive/%{commit5}/lib_lottie-%{shortcommit5}.tar.gz
Source6: https://github.com/desktop-app/lib_qr/archive/%{commit6}/lib_qr-%{shortcommit6}.tar.gz
Source7: https://github.com/desktop-app/lib_rpl/archive/%{commit7}/lib_rpl-%{shortcommit7}.tar.gz
Source8: https://github.com/desktop-app/lib_spellcheck/archive/%{commit8}/lib_spellcheck-%{shortcommit8}.tar.gz
Source9: https://github.com/desktop-app/lib_storage/archive/%{commit9}/lib_storage-%{shortcommit9}.tar.gz
Source10: https://github.com/desktop-app/lib_tl/archive/%{commit10}/lib_storage-%{shortcommit10}.tar.gz
Source11: https://github.com/desktop-app/lib_ui/archive/%{commit11}/lib_ui-%{shortcommit11}.tar.gz

%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Requires: qt5-qtimageformats%{?_isa}
Requires: hicolor-icon-theme
Requires: open-sans-fonts

# Telegram Desktop require patched version of rlottie since 1.8.0.
# Pull Request pending: https://github.com/Samsung/rlottie/pull/252
Provides: bundled(rlottie) = 0~git%{shortcommit2}

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
BuildRequires: range-v3-devel >= 0.9.1
BuildRequires: ffmpeg-devel >= 3.1
BuildRequires: openal-soft-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: libstdc++-devel
BuildRequires: openssl-devel
BuildRequires: xxhash-devel
BuildRequires: json11-devel
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
%endif

%if %{with clang}
BuildRequires: compiler-rt
BuildRequires: clang
BuildRequires: llvm
%endif

%if 0%{?fedora} && 0%{?fedora} >= 30
BuildRequires: minizip-compat-devel
%else
BuildRequires: minizip-devel
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
%setup -q -n %{appname}-%{version}

# Unpacking cmake_helpers...
rm -rf cmake
tar -xf %{SOURCE1}
mv cmake_helpers-%{commit1} cmake

# Unpacking patched rlottie...
pushd Telegram/ThirdParty
    rm -rf rlottie
    tar -xf %{SOURCE2}
    mv rlottie-%{commit2} rlottie
popd

# Unpacking lib_crl...
pushd Telegram
    rm -rf lib_crl
    tar -xf %{SOURCE3}
    mv lib_crl-%{commit3} lib_crl
popd

# Unpacking lib_base...
pushd Telegram
    rm -rf lib_base
    tar -xf %{SOURCE4}
    mv lib_base-%{commit4} lib_base
popd

# Unpacking lib_lottie...
pushd Telegram
    rm -rf lib_lottie
    tar -xf %{SOURCE5}
    mv lib_lottie-%{commit5} lib_lottie
popd

# Unpacking lib_qr...
pushd Telegram
    rm -rf lib_qr
    tar -xf %{SOURCE6}
    mv lib_qr-%{commit6} lib_qr
popd

# Unpacking lib_rpl...
pushd Telegram
    rm -rf lib_rpl
    tar -xf %{SOURCE7}
    mv lib_rpl-%{commit7} lib_rpl
popd

# Unpacking lib_spellcheck...
pushd Telegram
    rm -rf lib_spellcheck
    tar -xf %{SOURCE8}
    mv lib_spellcheck-%{commit8} lib_spellcheck
popd

# Unpacking lib_storage...
pushd Telegram
    rm -rf lib_storage
    tar -xf %{SOURCE9}
    mv lib_storage-%{commit9} lib_storage
popd

# Unpacking lib_tl...
pushd Telegram
    rm -rf lib_tl
    tar -xf %{SOURCE10}
    mv lib_tl-%{commit10} lib_tl
popd

# Unpacking lib_ui...
pushd Telegram
    rm -rf lib_ui
    tar -xf %{SOURCE11}
    mv lib_ui-%{commit11} lib_ui
popd

%build
# Setting build definitions...
%if %{without gtk3}
TDESKTOP_BUILD_DEFINES+='TDESKTOP_DISABLE_GTK_INTEGRATION,'
%endif
%if 0%{?fedora} && 0%{?fedora} < 30
TDESKTOP_BUILD_DEFINES+='TDESKTOP_DISABLE_OPENAL_EFFECTS,'
%endif
TDESKTOP_BUILD_DEFINES+='TDESKTOP_DISABLE_AUTOUPDATE,'
TDESKTOP_BUILD_DEFINES+='TDESKTOP_DISABLE_REGISTER_CUSTOM_SCHEME,'
TDESKTOP_BUILD_DEFINES+='TDESKTOP_DISABLE_DESKTOP_FILE_GENERATION,'
TDESKTOP_BUILD_DEFINES+='TDESKTOP_DISABLE_CRASH_REPORTS,'
TDESKTOP_BUILD_DEFINES+='TDESKTOP_LAUNCHER_FILENAME=%{name}.desktop,'

# Generating cmake script using GYP...
pushd Telegram/gyp
    gyp --depth=. --generator-output=../.. -Goutput_dir=out -Dapi_id=%{apiid} -Dapi_hash=%{apihash} -Dbuild_defines=$TDESKTOP_BUILD_DEFINES Telegram.gyp --format=cmake
popd

# Patching generated cmake script...
sed -i "$(($(wc -l < out/Release/CMakeLists.txt) - 2)) r Telegram/gyp/CMakeLists.inj" out/Release/CMakeLists.txt

# Building Telegram Desktop using cmake...
pushd out/Release
    %cmake \
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
    .
    %make_build
popd

%install
# Installing executables...
mkdir -p %{buildroot}%{_bindir}
install -m 0755 -p out/Release/Telegram %{buildroot}%{_bindir}/%{name}

# Installing desktop shortcut...
mv lib/xdg/telegramdesktop.desktop lib/xdg/%{name}.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications lib/xdg/%{name}.desktop

# Installing icons...
for size in 16 32 48 64 128 256 512; do
    dir=%{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps
    install -d $dir
    install -m 0644 -p Telegram/Resources/art/icon${size}.png $dir/%{name}.png
done

# Installing appdata for Gnome Software...
install -d %{buildroot}%{_metainfodir}
install -m 0644 -p lib/xdg/telegramdesktop.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%files
%doc README.md changelog.txt
%license LICENSE LEGAL
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_metainfodir}/%{name}.appdata.xml

%changelog
* Tue Jan 07 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 1.9.3-1
- Updated to version 1.9.3.

* Tue Dec 24 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.15-3
- Removed GTK2 from build requirements.

* Tue Dec 17 2019 Vitaly Zaitsev <vitaly@easycoding.org> - 1.8.15-2
- Fixed issue with menu bar on Gnome.
- Rebuilt due to Qt 5.13.2 update on Rawhide.
