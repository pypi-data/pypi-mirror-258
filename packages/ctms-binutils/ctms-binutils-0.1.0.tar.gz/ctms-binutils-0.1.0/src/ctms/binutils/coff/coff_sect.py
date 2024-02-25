import json
from ctypes import *
from typing import Iterable
from .. import clib

class CoffSection:
	def __init__(self, data: bytearray, jsect: dict[str, object]):
		self._name      = jsect['name']
		self._phys_addr = jsect['phys_addr']
		self._virt_addr = jsect['virt_addr']
		self._flags     = jsect['flags']
		self._data      = CoffSection._get_data(data, jsect)
		
	def _get_data(data: bytearray, jsect: dict[str, object]) -> bytearray:
		addr = jsect['data_addr']
		size = jsect['data_size']
		return data[addr:addr + size]
		
	@property
	def name(self) -> str:
		return self._name
		
	@property
	def phys_addr(self) -> int:
		return self._phys_addr
		
	@property
	def virt_addr(self) -> int:
		return self._virt_addr
	
	@property
	def flags(self) -> int:
		return self._flags
		
	@property
	def data(self) -> bytearray:
		return self._data

class CoffSectionTable:
	def __init__(self, data: bytearray, hcoff: int):
		self._hcoff = hcoff
		self._sects = CoffSectionTable._load_sects(data, hcoff)
		self._tbl   = CoffSectionTable._load_tbl(self._sects)
		
	def copy_sects(self, dst: bytearray, addr: int):
		data_len = len(dst)
		pdst     = (c_char * data_len).from_buffer(dst)		
		if not clib.coff_cpy_sects(self._hcoff, pdst, addr, data_len):
			clib.error()
			
	def keys(self) -> Iterable[str]:
		return self._tbl.keys()
		
	def values(self) -> Iterable[CoffSection]:
		return self._tbl.values()
		
	def items(self) -> Iterable[tuple[str, CoffSection]]:
		return self._tbl.items()
		
	def _load_sects(data: bytearray, hcoff: int) -> list[CoffSection]:
		jdata = clib.coff_load_sects(hcoff)
		if jdata is None:
			clib.error()
		jsects = json.loads(cast(jdata, c_char_p).value.decode())
		sects  = []
		clib.free_buff(jdata)
		for jsect in jsects:
			sects.append(CoffSection(data, jsect))
		return sects
		
	def _load_tbl(sects: list[CoffSection]) -> dict[str, CoffSection]:
		tbl = {}
		for sect in sects:
			tbl[sect.name] = sect
		return tbl
		
	def __getitem__(self, key: int | str):
		return self._sects[key] if isinstance(key, int) else self._tbl[key]
		
	def __iter__(self) -> Iterable[CoffSection]:
		return iter(self._sects)
		