from ctypes import *
from . import clib

def fill(data: bytearray, value: int = 0xFF) -> None:
	data_len = len(data)
	memset(_get_ptr(data, data_len), value, data_len)
	
def rev16_u16(value: int) -> int:
	return clib.rev16_u16(value)
	
def rev16_u32(value: int) -> int:
	return clib.rev16_u32(value)
	
def rev16_u64(value: int) -> int:
	return clib.rev16_u64(value)

def rev16_buff(data: bytearray) -> None:
	data_len = len(data)
	clib.rev16_buff(_get_ptr(data, data_len), data_len >> 1)
	
def crc32(data: bytes | bytearray) -> int:
	data_len = len(data)
	return clib.crc32(_get_ptr(data, data_len), data_len)
	
def _get_ptr(data: bytes | bytearray, data_len: int) -> bytes | c_void_p:
	return (c_char * data_len).from_buffer(data) if isinstance(data, bytearray) else data