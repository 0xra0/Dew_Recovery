#
#	This file is part of the OrangeFox Recovery Project
# 	Copyright (C) 2025 The OrangeFox Recovery Project
#
#	OrangeFox is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	any later version.
#
#	OrangeFox is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
# 	This software is released under GPL version 3 or any later version.
#	See <http://www.gnu.org/licenses/>.
#
# 	Please maintain this if you use this script or any part of it
#

export FOX_VIRTUAL_AB_DEVICE=1
export FOX_ENABLE_APP_MANAGER=0
export FOX_RECOVERY_VENDOR_BOOT_PARTITION="/dev/block/by-name/vendor_boot"
export FOX_RECOVERY_SYSTEM_PARTITION="/dev/block/mapper/system"
export FOX_RECOVERY_VENDOR_PARTITION="/dev/block/mapper/vendor"
export FOX_VENDOR_BOOT_RECOVERY=1
export FOX_USE_XZ_UTILS=1
export FOX_USE_UPDATED_MAGISKBOOT=1
export FOX_TARGET_DEVICES=dew
export TARGET_DEVICE_ALT=dew
export FOX_DISABLE_UPDATEZIP=1
export FOX_DELETE_AROMAFM=1
export FOX_DELETE_MAGISK_ADDON=1
export FOX_DELETE_INITD_ADDON=1
export FOX_REMOVE_BASH=1
export FOX_REMOVE_AAPT=1
export FOX_VARIANT="A15"

export FOX_VANILLA_BUILD=1
export OF_DISABLE_MIUI_SPECIFIC_FEATURES=1
export FOX_USE_XZ_UTILS=0
export FOX_USE_NANO_EDITOR=0
export FOX_USE_BASH_SHELL=0
export FOX_REMOVE_ZIP_BINARY=1
export FOX_USE_TAR_BINARY=0
export FOX_USE_GREP_BINARY=0
export FOX_USE_SED_BINARY=0
export FOX_USE_ZSTD_BINARY=0
export FOX_USE_FSCK_EROFS_BINARY=0
export FOX_USE_PATCHELF_BINARY=0
