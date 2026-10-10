# Build record

The released r2 image was built from OrangeFox 14.1 sources, the device tree in
`device/xiaomi/dew`, and the unmodified EEA `OS3.0.301.0.WBNEUXM` firmware.
`manifest/source-manifest.xml` is the pinned `repo manifest -r` snapshot from
the build, corrected to fetch three OrangeFox projects from their actual
upstreams. The original build checked out those projects separately.
`manifest/source-revisions.json` records the most relevant source commits;
`external/se_omapi` was at `9ea6e4a9ecfe04ffb82767d7cbcab3e8dc6295af`.

The original r1 image caused a POCO-logo/black-screen reboot loop on this
phone. Its recovery ramdisk was too large for the stock load-address gap when
combined with `init_boot`; that is a plausible cause, not a confirmed crash
diagnosis. R2 removes unneeded components and fits the same gap. It retains
the stock platform vendor ramdisk and DTB byte-for-byte. The raw
`out/target/product/dew/vendor_boot.img` from the Android build does **not**
retain the platform fragment; `scripts/repack-vendor-boot.py` creates the
flashable image.

The r2 image is 67,108,864 bytes and has SHA-256
`5930b9cdb30d790cb57a66cee3770c51721f7eaf1d99bca98f990f8c4b564aae`.
Its AVB footer uses algorithm `NONE`, so an unlocked bootloader is required.
The r2 image booted into OrangeFox on the tested slot-A phone. A BakaSU
AnyKernel3 ZIP installed from OrangeFox and Android booted afterward. This
does not establish functionality of userdata decryption, fastbootd, OTA, or
slot B. The tested OS was a ProjectInfinity-X Android 16 GSI with the same
unchanged EEA vendor; installing this recovery changes `vendor_boot`, not the
GSI or vendor partitions.
