#!/usr/bin/env python3
"""Check the published vendor_boot layout against the matching stock image."""
import hashlib
import pathlib
import struct
import sys

if len(sys.argv) != 3:
    raise SystemExit("Usage: validate-image.py <recovery vendor_boot.img> <stock vendor_boot.img>")


def parse(path):
    data = pathlib.Path(path).read_bytes()
    u32 = lambda offset: struct.unpack_from("<I", data, offset)[0]
    assert data[:8] == b"VNDRBOOT" and u32(8) == 4 and u32(12) == 4096
    assert len(data) == 67108864, "Unexpected vendor_boot partition size"
    align = lambda size: (size + 4095) // 4096 * 4096
    ramdisk_start = align(u32(2096))
    dtb_start = ramdisk_start + align(u32(24))
    table_start = dtb_start + align(u32(2100))
    dtb = data[dtb_start:dtb_start + u32(2100)]
    fragments = []
    for i in range(u32(2116)):
        entry = table_start + i * u32(2120)
        size, offset, kind = struct.unpack_from("<III", data, entry)
        assert offset + size <= u32(24)
        name = data[entry + 12:entry + 44].split(b"\0")[0]
        fragments.append((kind, name, data[ramdisk_start + offset:ramdisk_start + offset + size]))
    return data, dtb, fragments


built, built_dtb, built_fragments = parse(sys.argv[1])
stock, stock_dtb, stock_fragments = parse(sys.argv[2])
assert built_dtb == stock_dtb, "DTB changed"
assert built_fragments[0] == stock_fragments[0], "Stock platform fragment changed"
assert len(built_fragments) == 2 and built_fragments[1][0:2] == (2, b"recovery")
assert built[16:24] == stock[16:24] and built[2076:2080] == stock[2076:2080]
print("Image structure OK; stock platform fragment and DTB preserved")
print("SHA-256:", hashlib.sha256(built).hexdigest())
