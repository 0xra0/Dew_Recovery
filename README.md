# OrangeFox recovery for POCO C85 5G (`dew`)

Experimental OrangeFox 14.1 recovery packaged as a `vendor_boot` image for
the POCO C85 5G (`dew`). The [r2 release](https://github.com/0xra0/Dew_Recovery/releases/tag/r2-20261010)
booted on a slot-A phone using the unchanged EEA
`OS3.0.301.0.WBNEUXM` vendor and a ProjectInfinity-X Android 16 GSI. It
installed the [BakaSU AnyKernel3 ZIP](https://github.com/0xra0/Dew_Kernel)
through recovery; Android booted afterward. The earlier r1 image boot-looped
and must not be flashed. Read [INSTALL.md](INSTALL.md) before flashing.

The device tree, pinned base manifest, exact build scripts, and validation
notes are in this repository. The released image is a GitHub Release asset,
not a Git blob. Firmware images are **not** included: obtain the matching
Xiaomi firmware yourself and keep its stock `vendor_boot.img` for rollback.
The recovery is intentionally minimal. Userdata decryption, fastbootd, OTA,
and slot B are untested or omitted. It is intended primarily for ADB sideload
of a compatible kernel ZIP.

## Build from source

Use a Linux host with enough space and RAM for an Android 14 recovery build.
Install the Android `repo` tool and standard Android/OrangeFox build
dependencies, including Java 11, Python 3, Git, LZ4, and the `sha256sum`
utility. The original build used the [OrangeFox `fox_sync` script](https://github.com/linastorvaldz/fox_sync)
for source setup. For the recorded source revisions, start in a **new**
directory and use the pinned manifest in this repository:

```sh
git clone https://github.com/0xra0/Dew_Recovery.git
mkdir fox_14.1
cd fox_14.1
repo init -u https://github.com/0xra0/Dew_Recovery.git -b main -m manifest/source-manifest.xml
repo sync -j4 --retry-fetches=3
cd ../Dew_Recovery
```

The manifest is the build's pinned base snapshot, with the three OrangeFox
projects corrected to their actual upstreams and commits. A source sync is
large and depends on the upstream hosts still serving those commits. The local device
tree in this repository is the minimal r2 tree. It includes the prebuilt DTB
and touch firmware/modules needed by this specific device.

Extract `init_boot.img` and `vendor_boot.img` from the **unchanged**
`OS3.0.301.0.WBNEUXM` firmware into an `images` directory. The script checks
their hashes before compiling:

```sh
./build.sh ../fox_14.1 /path/to/OS3.0.301.0.WBNEUXM/images
```

The script copies the device tree into the synced source directory, runs
`lunch twrp_dew-ap2a-eng` and `mka adbd vendorbootimage`, then combines the
compiled recovery fragment with the **stock platform fragment and DTB**. Its
output is `out/OrangeFox-dew-minimal-r2-EXPERIMENTAL-vendor_boot.img`. The raw
`fox_14.1/out/target/product/dew/vendor_boot.img` omits the platform fragment
and must not be flashed. `scripts/validate-image.py` checks the final layout.
Compiler/toolchain changes can alter the output hash; the release image hash
is in [BUILD-NOTES.md](BUILD-NOTES.md). The published r2 release, not a fresh
rebuild from this repository, is the image confirmed on the phone.

For the tested flash procedure, stock rollback, and kernel ZIP warning, see
[INSTALL.md](INSTALL.md). Source and hardware findings are in
[BUILD-NOTES.md](BUILD-NOTES.md).
