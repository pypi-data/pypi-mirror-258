from ctypes import *
from pathlib import Path
from typing import Self
from .coff_sect import CoffSectionTable
from .. import clib

class CoffObject:
	def __init__(self, data: bytes):
		self._data  = bytearray(data)
		self._hcoff = CoffObject._load(self._data)
		
	def loadf(fpath: str | Path) -> Self:
		fpath = fpath if isinstance(fpath, Path) else Path(fpath)
		return CoffObject(fpath.read_bytes())
		
	def _load(data: bytearray) -> int:
		data_len = len(data)
		datap    = (c_char * data_len).from_buffer(data)
		hcoff    = clib.coff_load(datap, data_len)
		if not(hcoff):
			clib.error()		
		return hcoff
		
	@property
	def sects(self) -> CoffSectionTable:
		try:
			return self._sects
		except:
			self._sects = CoffSectionTable(self._data, self._hcoff)
			return self._sects
		