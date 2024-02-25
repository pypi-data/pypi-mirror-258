from ctypes import *
from pathlib import Path

# Load the library
_lib = CDLL(Path(Path(__file__).parent, 'binutils.dll'))

# Load the library functions
free_buff   = CFUNCTYPE(c_bool, c_void_p)(('free_buff', _lib))
_get_errmsg = CFUNCTYPE(c_void_p)(('get_errmsg', _lib))

# Load the binary operations
rev16_u16  = CFUNCTYPE(c_uint16, c_uint16)(('rev16_u16', _lib))
rev16_u32  = CFUNCTYPE(c_uint32, c_uint32)(('rev16_u32', _lib))
rev16_u64  = CFUNCTYPE(c_uint64, c_uint64)(('rev16_u64', _lib))
rev16_buff = CFUNCTYPE(c_bool, c_void_p, c_int32)(('rev16_buff', _lib))
crc32      = CFUNCTYPE(c_uint32, c_void_p, c_int32)(('crc32', _lib))

# Load the coff functions
coff_load       = CFUNCTYPE(c_int64, c_char_p)(('coff_load', _lib))
coff_load_sects = CFUNCTYPE(c_void_p, c_int64)(('coff_load_sects', _lib))
coff_cpy_sects  = CFUNCTYPE(c_bool, c_int64, c_char_p, c_int64, c_int64)(('coff_cpy_sects', _lib))

def error() -> None:
	msgp = _get_errmsg()
	msg  = cast(msgp, c_char_p).value.decode()
	free_buff(msgp)
	raise Exception(msg)