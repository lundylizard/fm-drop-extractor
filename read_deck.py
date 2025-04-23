from pymem import Pymem

DECK_ADDRESS_START = 0x0132A220
DECK_SIZE = 80

def read_deck_card_ids(pm):
    raw = pm.read_bytes(DECK_ADDRESS_START, DECK_SIZE)
    return [int.from_bytes(raw[i:i+2], 'little') for i in range(0, DECK_SIZE, 2)]

def main():
    try:
        pm = Pymem("ePSXe.exe")
        card_ids = read_deck_card_ids(pm)
        card_ids.sort()
        print("Deck Card IDs:", " ".join(str(cid) for cid in card_ids))
    except Exception as e:
        print(f"[!] Failed to read deck: {e}")

if __name__ == "__main__":
    main()
