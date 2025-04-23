import struct
import argparse
from typing import List, BinaryIO

CHAR_MAP = {
    0x18: 'A', 0x2D: 'B', 0x2B: 'C', 0x20: 'D', 0x25: 'E', 0x31: 'F',
    0x29: 'G', 0x23: 'H', 0x1A: 'I', 0x3B: 'J', 0x33: 'K', 0x2A: 'L',
    0x1E: 'M', 0x2C: 'N', 0x21: 'O', 0x2F: 'P', 0x3E: 'Q', 0x26: 'R',
    0x1D: 'S', 0x1C: 'T', 0x35: 'U', 0x39: 'V', 0x22: 'W', 0x46: 'X',
    0x24: 'Y', 0x3F: 'Z', 0x03: 'a', 0x15: 'b', 0x0F: 'c', 0x0C: 'd',
    0x01: 'e', 0x13: 'f', 0x10: 'g', 0x09: 'h', 0x05: 'i', 0x34: 'j',
    0x16: 'k', 0x0A: 'l', 0x0E: 'm', 0x06: 'n', 0x04: 'o', 0x14: 'p',
    0x37: 'q', 0x08: 'r', 0x07: 's', 0x02: 't', 0x0D: 'u', 0x19: 'v',
    0x12: 'w', 0x36: 'x', 0x11: 'y', 0x32: 'z', 0x38: '0', 0x3D: '1',
    0x3A: '2', 0x41: '3', 0x4A: '4', 0x42: '5', 0x4E: '6', 0x45: '7',
    0x57: '8', 0x59: '9', 0x00: ' ', 0x30: '-', 0x3C: '#', 0x43: '&',
    0x0B: '.', 0x1F: ',', 0x17: '!', 0x1B: "'", 0x27: '<', 0x28: '>',
    0x2E: '?', 0x44: '/', 0x48: ':', 0x4B: ')', 0x4C: '(', 0x4F: '$',
    0x50: '*', 0x51: '>', 0x54: '<', 0x40: '"', 0x56: '+', 0x5B: '%'
}

class DataReader:
    def read_value(self, file: BinaryIO, fmt: str):
        size = struct.calcsize(fmt)
        data = file.read(size)
        if len(data) != size:
            raise EOFError(f"EOF reading '{fmt}'")
        return struct.unpack(fmt, data)[0]

    def decode_text(self, file: BinaryIO) -> str:
        buffer = bytearray()
        while True:
            chunk = file.read(1)
            if not chunk:
                break
            byte = chunk[0]
            if byte == 0xFF:
                next_byte = file.read(1)
                if next_byte and next_byte[0] == 0xFF:
                    break
                break
            buffer.append(byte)
        return ''.join(CHAR_MAP.get(b, f"[{b:02x}]") for b in buffer)

    def load_names(self, slus_path: str) -> (List[str], List[str]):
        card_names = []
        duelist_names = []
        with open(slus_path, 'rb') as slus:
            for i in range(722):
                slus.seek(0x1C6002 + i * 2)
                ptr = self.read_value(slus, '<H')
                slus.seek(0x1C6800 + ptr - 0x6000)
                card_names.append(self.decode_text(slus))
            for i in range(39):
                slus.seek(0x1C6652 + i * 2)
                ptr = self.read_value(slus, '<H')
                slus.seek(0x1C6800 + ptr - 0x6000)
                duelist_names.append(self.decode_text(slus))
        return card_names, duelist_names

    def load_drops(self, mrg_path: str) -> List[tuple]:
        drops = []
        with open(mrg_path, 'rb') as mrg:
            for i in range(39):
                base = 0xE9B000 + 0x1800 * i
    
                # S/A-Pow drops
                mrg.seek(base + 0x5B4)
                sa_pow = [self.read_value(mrg, '<H') for _ in range(722)]
    
                # B/C/D drops
                mrg.seek(base + 0xB68)
                bcd_pow = [self.read_value(mrg, '<H') for _ in range(722)]
    
                # S/A-Tec drops
                mrg.seek(base + 0x111C)
                sa_tec = [self.read_value(mrg, '<H') for _ in range(722)]
    
                drops.append((sa_tec, bcd_pow, sa_pow))
        return drops


    def load(self, slus_path: str, mrg_path: str):
        cards, duelists = self.load_names(slus_path)
        drops = self.load_drops(mrg_path)
        return cards, duelists, drops


def export_spoiler(output_file: str, names: List[str], drops: List[tuple]):
    with open(output_file, 'w', encoding='utf-8') as out:
        for name, (tec, bcd, pow_) in zip(names[1], drops):
            out.write(f"{name} S/A-Tec drops\n")
            entries = [(i+1, r) for i, r in enumerate(tec) if r]
            out.write(f"Possibilities: {len(entries)}\n")
            out.write("Total Rate: 2048\n")
            for idx, rate in entries:
                out.write(f"    => #{idx} {names[0][idx-1]}\n")
                out.write(f"        Rate: {rate}/2048\n")
            out.write("\n")
            out.write(f"{name} B/C/D drops\n")
            entries = [(i+1, r) for i, r in enumerate(bcd) if r]
            out.write(f"Possibilities: {len(entries)}\n")
            out.write("Total Rate: 2048\n")
            for idx, rate in entries:
                out.write(f"    => #{idx} {names[0][idx-1]}\n")
                out.write(f"        Rate: {rate}/2048\n")
            out.write("\n")
            out.write(f"{name} S/A-Pow drops\n")
            entries = [(i+1, r) for i, r in enumerate(pow_) if r]
            out.write(f"Possibilities: {len(entries)}\n")
            out.write("Total Rate: 2048\n")
            for idx, rate in entries:
                out.write(f"    => #{idx} {names[0][idx-1]}\n")
                out.write(f"        Rate: {rate}/2048\n")
            out.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Export drops to spoiler file in strict format")
    parser.add_argument("slus_file")
    parser.add_argument("mrg_file")
    parser.add_argument("output_file")
    args = parser.parse_args()

    reader = DataReader()
    card_names, duelist_names, drops = reader.load(args.slus_file, args.mrg_file)
    export_spoiler(args.output_file, (card_names, duelist_names), drops)

if __name__ == "__main__":
    main()
