from __future__ import annotations
from typing import Self, BinaryIO
from contextlib import AbstractContextManager
from struct import unpack as up, pack as pk
from enum import Enum
from pathlib import Path
from io import BytesIO


class BinaryEndian(Enum):
    LITTLE = "<"
    BIG = ">"


class BinaryReader(AbstractContextManager):
    def __init__(self, file_path: Path, endian: BinaryEndian = BinaryEndian.LITTLE):
        self.file_path = file_path
        self.endian = endian
        self.fp = None

    def __enter__(self) -> Self:
        return self.open()

    def __exit__(self, *e):
        return self.close()

    def open(self) -> Self:
        self.fp = open(self.file_path, "rb")
        return self

    def close(self):
        return self.fp.close()

    def read(self, number: int) -> bytes:
        return self.fp.read(number)

    def unpack(self, type: str, size: int) -> int:
        return up(f"{self.endian.value}{type}", self.read(size))[0]

    def read_ubyte(self) -> int:
        return self.unpack("B", 1)

    def read_byte(self) -> int:
        return self.unpack("b", 1)

    def read_ushort(self) -> int:
        return self.unpack("H", 2)

    def read_short(self) -> int:
        return self.unpack("h", 2)

    def read_uint(self) -> int:
        return self.unpack("I", 4)

    def read_int(self) -> int:
        return self.unpack("i", 4)

    def read_ulong(self) -> int:
        return self.unpack("Q", 8)

    def read_long(self) -> int:
        return self.unpack("q", 8)

    def seek(self, offset: int) -> int:
        return self.fp.seek(offset)

    def tell(self) -> int:
        return self.fp.tell()

    def skip(self, number: int) -> int:
        return self.seek(self.tell() + number)

    def read_utf8_string(self, length: int) -> str:
        return self.read(length).decode("utf-8")

    def read_utf8_nt_string(self, nt: int = 0) -> str:
        byte_array = bytearray()
        while (byte := self.read_ubyte()) != nt:
            byte_array.append(byte)
        return bytes(byte_array).decode("utf-8")

    def align(self, number: int) -> int:
        offset = self.tell()
        align = (number - (offset % number)) % number
        return self.seek(offset + align)


class MemoryWriter(BytesIO):
    def __init__(self, endian: BinaryEndian = BinaryEndian.LITTLE):
        self.endian = endian

    def pack(self, type: str, number: int) -> int:
        return self.write(pk(f"{self.endian.value}{type}", number))

    def write_ubyte(self, number: int) -> int:
        return self.pack("B", number)

    def write_byte(self, number: int) -> int:
        return self.pack("b", number)

    def write_ushort(self, number: int) -> int:
        return self.pack("H", number)

    def write_short(self, number: int) -> int:
        return self.pack("h", number)

    def write_uint(self, number: int) -> int:
        return self.pack("I", number)

    def write_int(self, number: int) -> int:
        return self.pack("i", number)

    def write_ulong(self, number: int) -> int:
        return self.pack("Q", number)

    def write_long(self, number: int) -> int:
        return self.pack("q", number)

    def write_utf8_string(self, string: str) -> int:
        return self.write(string.encode("utf-8"))

    def write_utf8_nt_string(self, string: str, nt: int = 0) -> int:
        return self.write_utf8_string(string) + self.write_ubyte(nt)

    def align(self, number: int) -> int:
        offset = self.tell()
        align = (number - (offset % number)) % number
        return self.seek(offset + align)

    def skip(self, number: int) -> int:
        return self.seek(self.tell() + number)


class BinaryWriter(AbstractContextManager):
    def __init__(self, file_path: Path, endian: BinaryEndian = BinaryEndian.LITTLE):
        self.endian = endian
        self.file_path = file_path
        self.fp = None

    def __enter__(self) -> Self:
        return self.open()

    def __exit__(self, *e):
        return self.close()

    def open(self) -> Self:
        self.fp = open(self.file_path, "wb")
        return self

    def close(self):
        return self.fp.close()

    def write(self, buffer: BinaryIO) -> int:
        return self.fp.write(buffer)

    def pack(self, type: str, number: int) -> int:
        return self.write(pk(f"{self.endian.value}{type}", number))

    def write_ubyte(self, number: int) -> int:
        return self.pack("B", number)

    def write_byte(self, number: int) -> int:
        return self.pack("b", number)

    def write_ushort(self, number: int) -> int:
        return self.pack("H", number)

    def write_short(self, number: int) -> int:
        return self.pack("h", number)

    def write_uint(self, number: int) -> int:
        return self.pack("I", number)

    def write_int(self, number: int) -> int:
        return self.pack("i", number)

    def write_ulong(self, number: int) -> int:
        return self.pack("Q", number)

    def write_long(self, number: int) -> int:
        return self.pack("q", number)

    def write_utf8_string(self, string: str) -> int:
        return self.write(string.encode("utf-8"))

    def write_utf8_nt_string(self, string: str, nt: int = 0) -> int:
        return self.write_utf8_string(string) + self.write_ubyte(nt)

    def align(self, number: int) -> int:
        offset = self.tell()
        align = (number - (offset % number)) % number
        return self.seek(offset + align)

    def skip(self, number: int) -> int:
        return self.seek(self.tell() + number)
