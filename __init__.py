import builtins
import os
from typing import Literal, Union, BinaryIO

pattern = {0: ' ', 1: '0', 2: 'a', 3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'f', 8: 'g', 9: 'h', 10: 'i', 11: 'j', 12: 'k', 13: 'l', 14: 'm', 15: 'n', 16: 'o', 17: 'p', 18: 'q', 19: 'r', 20: 's', 21: 't', 22: 'u', 23: 'v', 24: 'w', 25: 'x', 26: 'y', 27: 'z', 28: 'A', 29: 'B', 30: 'C', 31: 'D', 32: 'E', 33: 'F', 34: 'G', 35: 'H', 36: 'I', 37: 'J', 38: 'K', 39: 'L', 40: 'M', 41: 'N', 42: 'O', 43: 'P', 44: 'Q', 45: 'R', 46: 'S', 47: 'T', 48: 'U', 49: 'V', 50: 'W', 51: 'X', 52: 'Y', 53: 'Z', 54: '{', 55: '}', 56: '1', 57: '2', 58: '3', 59: '4', 60: '5', 61: '6', 62: '7', 63: '8', 64: '9', 65: '"', 66: ':', 67: ';', 68: '`', 69: '/', 70: '*', 71: '-', 72: '+', 73: "\\", 74: ")", 75: "(", 76: ",", 77: "."}
pattern2 = {' ': 0, '0': 1, 'a': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6, 'f': 7, 'g': 8, 'h': 9, 'i': 10, 'j': 11, 'k': 12, 'l': 13, 'm': 14, 'n': 15, 'o': 16, 'p': 17, 'q': 18, 'r': 19, 's': 20, 't': 21, 'u': 22, 'v': 23, 'w': 24, 'x': 25, 'y': 26, 'z': 27, 'A': 28, 'B': 29, 'C': 30, 'D': 31, 'E': 32, 'F': 33, 'G': 34, 'H': 35, 'I': 36, 'J': 37, 'K': 38, 'L': 39, 'M': 40, 'N': 41, 'O': 42, 'P': 43, 'Q': 44, 'R': 45, 'S': 46, 'T': 47, 'U': 48, 'V': 49, 'W': 50, 'X': 51, 'Y': 52, 'Z': 53, '{': 54, '}': 55, '1': 56, '2': 57, '3': 58, '4': 59, '5': 60, '6': 61, '7': 62, '8': 63, '9': 64, '"': 65, ':': 66, ';': 67, '`': 68, '/': 69, '*': 70, '-': 71, '+': 72, "\\": 73, ")": 74, "(": 75, ",": 76, ".": 77}
image = {0: ' ', 1: '0', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9', 11: '0', 12: '(', 13: ')', 14: ',', 15: '.'}
image2 = {' ': 0, '0': 11, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10, '(': 12, ')': 13, ',': 14, '.': 15}


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
        return self.bits[2:][idx]

    def decode(self, format: Literal["ASCII", "base10", "base15", "bytearray"]):
        if format == "base10":
            return int(self.bits, 2)
        elif format == "base15":
            return hex(int(self.bits, 2))
        elif format == "ASCII":
            return chr(int(self.bits, 2))
        elif format == "bytearray":
            result = bytearray()
            value = self.bits[2:]
            while len(value) % 8 != 0:
                value += "0"
            for i in range(0, len(value), 8):
                result.append(int(value[i:i+8], 2))
            return result

    @staticmethod
    def encode(format: Literal["ASCII", "base10", "base15", "bytearray"], value: int | str | bytearray):
        if format == "base10":
            return bit_array(bin(value))
        elif format == "base15":
            return bit_array(bin(int(value, 16)))
        elif format == "ASCII":
            return bit_array(bin(ord(value)))
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


class file(object):
    def __init__(self, object: BinaryIO, type: Literal["image", "text", "custom"]) -> None:
        self.object = object
        self.type = type

    def read(self) -> str | None:
        if self.type == "image":
            raw = self.object.read()
            bits = bit_array.encode("bytearray", raw)
            raw_bits = bits.bits[2:]  # Strip '0b'
            result = ""
            for i in range(0, len(raw_bits), 8):
                byte = raw_bits[i:i + 8]
                if len(byte) < 8:
                    continue
                val = int(byte, 2)
                ch = image.get(val, '?')
                print(f"Byte: {byte} → val: {val} → char: '{ch}'")  # DEBUG
                result += ch
            return result
        if self.type == "text":
            raw = self.object.read()
            bits = bit_array.encode("bytearray", raw).bits[2:]  # strip '0b'

            result = ""
            for i in range(0, len(bits), 7):
                chunk = bits[i:i + 7]
                if len(chunk) < 7:
                    continue
                val = int(chunk, 2)
                char = pattern.get(val, '?')
                result += char
            return result

    def write(self, data: tuple[int, int, int] | str):
        if self.type == "image":
            d = ""
            for char in data:
                val = image2.get(char)
                if val is None:
                    print(f"Unmapped character during write: {char}")
                    continue
                bits = format(val, "08b")
                print(f"Char '{char}' -> val: {val} -> bits: {bits}")  # DEBUG
                d += bits
            d = bit_array("0b" + d)
            bytes_data = d.decode("bytearray")
            self.object.write(bytes_data)

        elif self.type == "text":
            bits = ""
            for char in data:
                val = pattern2.get(char)
                if val is None:
                    print(f"Skipping unmapped char: {char}")
                    continue
                bits += format(val, "07b")

            while len(bits) % 8 != 0:
                bits += "0"

            byte_data = bytearray()
            for i in range(0, len(bits), 8):
                byte = bits[i:i + 8]
                byte_data.append(int(byte, 2))

            self.object.write(byte_data)

if __name__ == "__main__":
    f = open("test.bin", mode="w+b")
    b = file(f, "text")
    b.write('(255, 255, 255, 255), (0, 0, 0, 0.25)')
    f.close()

    f = open("test.bin", mode="r+b")
    b = file(f, "text")
    print(b.read())
    f.close()

    print(os.path.getsize("test.bin"))
    print(os.path.getsize("data.txt"))

