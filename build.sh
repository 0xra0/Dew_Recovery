#!/usr/bin/env bash
set -eo pipefail

usage() {
  cat <<'EOF'
Usage: ./build.sh <OrangeFox source directory> <firmware images directory> [output directory]

The source directory must contain the synced OrangeFox 14.1 tree. The firmware
directory must contain the unmodified init_boot.img and vendor_boot.img from
dew EEA OS3.0.301.0.WBNEUXM. Nothing is flashed by this script.
EOF
}

if [[ $# -lt 2 || $# -gt 3 ]]; then usage >&2; exit 2; fi
repo_root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source_root=$(realpath -- "$1")
firmware_dir=$(realpath -- "$2")
output_dir=$(realpath -m -- "${3:-$repo_root/out}")
device_tree="$source_root/device/xiaomi/dew"

[[ -f "$source_root/build/envsetup.sh" ]] || { echo 'OrangeFox source tree is missing' >&2; exit 1; }
[[ -f "$firmware_dir/init_boot.img" && -f "$firmware_dir/vendor_boot.img" ]] || {
  echo 'Matching init_boot.img and vendor_boot.img are required' >&2; exit 1;
}
printf '%s  %s\n' \
  '27851c396e9ff635a59f68467bc1fa4acc58178af704e357c19c20ee373fb24f' "$firmware_dir/init_boot.img" \
  '9eca718c5647fc522bd0276c81de780ccb3c3bed4bc9783895a835483263bf5a' "$firmware_dir/vendor_boot.img" |
  sha256sum --check --status || { echo 'Firmware image hashes do not match the tested build' >&2; exit 1; }

if [[ -e "$device_tree" ]]; then
  diff -qr --exclude=.git "$repo_root/device/xiaomi/dew" "$device_tree" >/dev/null || {
    echo "Existing $device_tree differs from this repository; resolve it manually" >&2; exit 1;
  }
else
  mkdir -p -- "$(dirname -- "$device_tree")"
  cp -a -- "$repo_root/device/xiaomi/dew" "$device_tree"
fi

mkdir -p -- "$output_dir"
export OUT_DIR="${OUT_DIR:-$source_root/out}"
export ALLOW_MISSING_DEPENDENCIES=true FOX_BUILD_DEVICE=dew LC_ALL=C
export BUILD_USERNAME=builder BUILD_HOSTNAME=dew-recovery
cd -- "$source_root"
source build/envsetup.sh
lunch twrp_dew-ap2a-eng
mka adbd vendorbootimage -j"${JOBS:-8}"

image="$output_dir/OrangeFox-dew-minimal-r2-EXPERIMENTAL-vendor_boot.img"
python3 "$repo_root/scripts/repack-vendor-boot.py" \
  --source "$source_root" \
  --stock "$firmware_dir/vendor_boot.img" \
  --init-boot "$firmware_dir/init_boot.img" \
  --built "$OUT_DIR/target/product/dew/vendor_boot.img" \
  --output "$image"
python3 "$repo_root/scripts/validate-image.py" "$image" "$firmware_dir/vendor_boot.img"
sha256sum "$image"
echo "Built: $image"
