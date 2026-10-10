#!/usr/bin/env python3
"""Combine stock platform ramdisk/DTB with the compiled recovery fragment."""
import argparse, hashlib, pathlib, struct, subprocess, sys, tempfile
p=argparse.ArgumentParser()
p.add_argument('--source',type=pathlib.Path,required=True)
p.add_argument('--stock',type=pathlib.Path,required=True)
p.add_argument('--built',type=pathlib.Path,required=True)
p.add_argument('--init-boot',type=pathlib.Path,required=True)
p.add_argument('--output',type=pathlib.Path,required=True)
a=p.parse_args()
def parse(path):
 b=path.read_bytes();u=lambda n:struct.unpack_from('<I',b,n)[0]
 assert b[:8]==b'VNDRBOOT' and u(8)==4 and u(12)==4096
 align=lambda n:(n+4095)//4096*4096
 start=align(u(2096));dtb=start+align(u(24));table=dtb+align(u(2100));fragments=[]
 for i in range(u(2116)):
  o=table+i*u(2120);size,offset,kind=struct.unpack_from('<III',b,o)
  assert not any(b[o+44:o+108]), 'Nonzero board IDs require explicit handling'
  fragments.append((kind,b[start+offset:start+offset+size]))
 return b,b[dtb:dtb+u(2100)],fragments
stock,dtb,sf=parse(a.stock);built,bdtb,bf=parse(a.built)
assert dtb==bdtb,'Stock and compiled DTB differ'
platform=[d for k,d in sf if k==1];recovery=[d for k,d in bf if k==2]
assert len(platform)==len(recovery)==1
ib=a.init_boot.read_bytes()
assert ib[:8]==b'ANDROID!'
init_size=struct.unpack_from('<I',ib,12)[0]
align=lambda n:(n+4095)//4096*4096
combined=sum(align(n) for n in [init_size,len(platform[0]),len(recovery[0])])
gap=struct.unpack_from('<Q',stock,2104)[0]-struct.unpack_from('<I',stock,20)[0]
assert combined+1048576<=gap, f'Insufficient ramdisk-to-DTB headroom: {combined} vs {gap}'
print(f'Combined aligned ramdisks: {combined} bytes; address-gap headroom: {gap-combined} bytes')
assert struct.unpack_from('<I',stock,2124)[0]==0,'Unexpected stock bootconfig'
assert stock[16:24]==built[16:24] and stock[2076:2080]==built[2076:2080] and stock[2104:2112]==built[2104:2112]
a.output.parent.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='dew-repack-') as temp:
 t=pathlib.Path(temp)
 for name,data in [('platform.lz4',platform[0]),('recovery.lz4',recovery[0]),('dtb',dtb)]: (t/name).write_bytes(data)
 subprocess.run([sys.executable,str(a.source/'system/tools/mkbootimg/mkbootimg.py'),
  '--header_version','4','--pagesize','4096','--base','0x40078000',
  '--kernel_offset','0x00008000','--ramdisk_offset','0x07c08000',
  '--tags_offset','0x0bc08000','--dtb_offset','0x0bc08000',
  '--vendor_cmdline',stock[28:2076].split(b'\0')[0].decode(),
  '--board','','--dtb',str(t/'dtb'),'--vendor_ramdisk',str(t/'platform.lz4'),
  '--ramdisk_type','recovery','--ramdisk_name','recovery',
  '--vendor_ramdisk_fragment',str(t/'recovery.lz4'),'--vendor_boot',str(a.output)],check=True)
 subprocess.run([sys.executable,str(a.source/'external/avb/avbtool.py'),
  'add_hash_footer','--image',str(a.output),'--partition_name','vendor_boot',
  '--partition_size','67108864','--algorithm','NONE',
  '--salt',hashlib.sha256(stock).hexdigest()],check=True)
_,rdtb,rf=parse(a.output)
assert rf==[(1,platform[0]),(2,recovery[0])] and rdtb==dtb
print(hashlib.sha256(a.output.read_bytes()).hexdigest(),a.output)
