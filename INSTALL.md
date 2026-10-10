# Install and restore

This procedure is for an unlocked POCO C85 5G (`dew`) on EEA
`OS3.0.301.0.WBNEUXM`, with slot A active and **bootloader fastboot**
(`is-userspace: no`). R2 booted on this setup. Do not flash the r1 image or
the raw build output. Keep the matching stock `vendor_boot.img` from this
firmware at hand. A flash always carries a boot-loop risk.

Download `OrangeFox-dew-minimal-r2-EXPERIMENTAL-vendor_boot.img` from the
[r2 release](https://github.com/0xra0/Dew_Recovery/releases/tag/r2-20261010).
Verify its SHA-256 before flashing:

```sh
sha256sum OrangeFox-dew-minimal-r2-EXPERIMENTAL-vendor_boot.img
# Expected: 5930b9cdb30d790cb57a66cee3770c51721f7eaf1d99bca98f990f8c4b564aae
```

Extract the stock image from your **same** Xiaomi EEA firmware package. On
the local build host it is at
`/mnt/sata/dew_eea_global_images_OS3.0.301.0.WBNEUXM_16.0/images/vendor_boot.img`.
Its expected SHA-256 is
`9eca718c5647fc522bd0276c81de780ccb3c3bed4bc9783895a835483263bf5a`.
Do not use an image from another firmware or device.

Boot Android normally first, enable USB debugging, and enter bootloader mode:

```sh
adb reboot bootloader
fastboot devices
fastboot getvar current-slot
fastboot getvar is-userspace
```

Proceed only when the slot is `a` and `is-userspace` is `no`. Do **not** reboot
to fastbootd. Flash the recovery to slot A's `vendor_boot`, then boot Android
and enter recovery:

```sh
fastboot flash vendor_boot_a OrangeFox-dew-minimal-r2-EXPERIMENTAL-vendor_boot.img
fastboot reboot
adb reboot recovery
```

R2 supports the tested ADB sideload path for an AnyKernel3 ZIP. The
[BakaSU kernel repository](https://github.com/0xra0/Dew_Kernel) has its own
installation and boot-partition rollback instructions. Installing a kernel ZIP
from recovery still modifies `boot` and can cause a kernel boot loop.

If recovery shows a POCO logo, black screen, or reboot loop, hold Power and
Volume Down to return to bootloader fastboot. Confirm `current-slot: a` and
`is-userspace: no`, then restore the matching stock `vendor_boot.img`:

```sh
fastboot flash vendor_boot_a vendor_boot.img
fastboot reboot
```

If Android loops after installing a kernel ZIP, restoring `vendor_boot` alone
will not undo the kernel change. Follow the kernel repository's instructions
to restore the known-working `boot_a` image. Do not wipe userdata for either
loop. Slot B was not tested; do not substitute `_b` without validating its
firmware and having a slot-B backup.
