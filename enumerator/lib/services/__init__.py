from .http import HttpEnumeration
from .ftp import FtpEnumeration
from .nbt import NbtEnumeration
from .ssh import SshEnumeration
from .rpc import RpcEnumeration

http = HttpEnumeration()
ftp = FtpEnumeration()
nbt = NbtEnumeration()
ssh = SshEnumeration()
rpc = RpcEnumeration()

service_modules = [http, ftp, nbt, ssh, rpc]
