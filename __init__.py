import builtins
from os import PathLike
from typing import Literal, Union, Optional


class bit_array(object):
    def __init__(self, bits: str | int):
        if isinstance(bits, str) and bits.startswith('0b'):
            self.bits = bits
        elif isinstance(bits, int):
            self.bits = bin(bits)
        else:
            raise TypeError('Invalid input')

    def __len__(self):
        return len(self.bits[2:])

    def __getitem__(self, idx):
        return bit_array(self.bits[2:][idx])

    def decode(self, format: Literal["ASCII", "base10", "base15", "bytearray"]):
        if format == "base10":
            return int(self.bits, 2)
        elif format == "base15":
            return hex(int(self.bits, 2))
        elif format == "ASCII":
            value = self.bits[2:]
            if len(value) % 8 != 0:
                raise ValueError("Bit length not divisible by 8 for ASCII decoding.")
            chars = [chr(int(value[i:i + 8], 2)) for i in range(0, len(value), 8)]
            return ''.join(chars)

        elif format == "bytearray":
            result = bytearray()
            value = self.bits[2:]
            while len(value) % 8 != 0:
                value += "0"
            for i in range(0, len(value), 8):
                result.append(int(value[i:i+8], 2))
            return result

    def split(self, bit: Union["bit_array", str, int]):
        if isinstance(bit, str):
            self.bits = "0b" + self.bits[2:].split(bit)
        elif isinstance(bit, int):
            self.bits = self.bits.split(str(bin(bit)))
        elif isinstance(bit, bit_array):
            self.bits = self.bits.split(bit.bits)

    @staticmethod
    def encode(format: Literal["ASCII", "base10", "base15", "bytearray"], value: int | str | bytearray):
        if format == "base10":
            return bit_array(bin(value))
        elif format == "base15":
            return bit_array(bin(int(value, 16)))
        elif format == "ASCII":
            if not isinstance(value, str):
                raise ValueError("ASCII encoding requires a string.")
            result = "".join(f"{ord(c):08b}" for c in value)
            return bit_array("0b" + result)

        elif format == "bytearray":
            result = ""
            for i in value:
                result += builtins.format(i, "08b")
            return bit_array("0b" + result)
        else:
             raise TypeError(f"Invalid {format} format")

    def append(self, value: Union[int , "bit_array" , str]):
        if isinstance(value, str):
            self.bits += value
        elif isinstance(value, int):
            self.bits += bin(value)[2:]
        elif isinstance(value, bit_array):
            self.bits += value.bits[2:]
        else:
            raise TypeError(f'{type(value)} is invalid type for appending')

    def __delitem__(self, key: int):
        bits = self.bits[2:]
        bits = bits[:key] + bits[key+1:]
        self.bits = "0b" + bits

    def __repr__(self):
        return f"bit_array({self.bits})"

class open(object):
    def __init__(
        self,
        file: Union[PathLike[str], str],
        mode: Literal["w", "r"],
        decoding: Optional[Literal["ASCII", "base10", "base15", "bytearray"]] = None,
        buffering: bool = True
    ):
        self.buffer = None
        self.mode = mode
        self.decoding = decoding
        self.allow_buffer = buffering
        self.file = builtins.open(file, mode + "b")

    def write(self, data: Union[bytearray, "bit_array"]):
        if self.allow_buffer:
            self.buffer = data
        if isinstance(data, bit_array):
            self.file.write(data.decode("bytearray"))
        elif isinstance(data, bytearray):
            self.file.write(data)
        else:
            raise TypeError(f"Unsupported type for write: {type(data)}")

    def read(self):
        raw = self.file.read()
        data = bit_array.encode("bytearray", raw)
        if self.allow_buffer:
            self.buffer = data
        if self.decoding:
            return data.decode(self.decoding)
        return data

    @staticmethod
    def compress(data: bytearray | bit_array, size: int = None, encoding: Literal["ASCII", "base10", "base15", "bytearray"] = "bytearray") -> None | bytearray | int | str:
        if isinstance(data, bit_array):
            if size is None:
                raise ValueError("Size must be specified when using bit_array.")
            raw = data.decode("bytearray")
        elif isinstance(data, bytearray):
            if size is None:
                raise ValueError("Size must be specified when using bytearray.")
            raw = data
        else:
            raise TypeError("data must be a bytearray or bit_array")

        result = bytearray()

        for row_start in range(0, len(raw), size):
            for i in range(min(size, len(raw) - row_start)):
                idx = row_start + i
                left = raw[idx - 1] if i > 0 else 0
                result.append((raw[idx] - left) % 256)

        return bit_array(bit_array.encode("bytearray", result).bits).decode(encoding)

    @staticmethod
    def decompress(data: bytearray | bit_array, size: int, decoding: Literal["ASCII", "base10", "base15", "bytearray"] = "bytearray") -> None | bytearray | int | str:
        if isinstance(data, bit_array):
            raw = data.decode("bytearray")
        elif isinstance(data, bytearray):
            raw = data
        else:
            raise TypeError("data must be a bytearray or bit_array")

        result = bytearray()

        for row_start in range(0, len(raw), size):
            for i in range(size):
                idx = row_start + i
                left = result[idx - 1] if i > 0 else 0
                result.append((raw[idx] + left) % 256)

        return bit_array(bit_array.encode("bytearray", result).bits).decode(decoding)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

print("1010"[1:4])