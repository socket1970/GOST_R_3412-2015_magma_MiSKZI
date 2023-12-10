#        @@      @@        @@
#       @@      @@       @@
#       @@      @@      @@
# @@     @@@     @@     @@     @@@
#    @@@@@@@*        ,&@@@@@@@*
#   @                         @@     @@
#   @@                       ,@#    @@
#   @@@                     @@@  &@#
#     @@@&                @@@
#        @@@@@@@@@@@@@@@@@


from secrets import randbits

from src.textConverter import TextConverter

tBox = [
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2],
    [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
    [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
    [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
    [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
    [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
    [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
    [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1]
]


class Magma:
    def __init__(self, encoding="UTF-8"):
        self.__encoding = encoding

    @staticmethod
    def key() -> str:
        # Генерация 256 битного ключа в hex формате.
        return format(randbits(256), "x")

    def encode(self, message: str, key: str):
        # Шифрование.
        t = TextConverter(self.__encoding)
        message = t.str2bin(message, 8)
        key = self.__round_key(key)

        enc = []
        for i in message:
            enc.append(self.__G(i, key))

        return enc

    def decode(self, message: list[bytearray], key: str):
        # Дешифрование.
        key = self.__round_key(key)[::-1]
        t = TextConverter(self.__encoding)
        enc = []
        for i in message:
            enc.append(self.__G(i, key))

        return t.bin2str(enc)

    def __g(self, block: bytes, key: bytes) -> bytes:
        # g блок.
        block = self.__mod32(block, key)
        block = self.__t_box(block)
        block = self.__shift11(block)

        return block

    def __G(self, message: bytearray, key: list[bytes]) -> bytearray:
        # G блок - объединяет g блок и xor с левым полу блоком.
        L = bytearray(x for x in message[:4])
        R = bytearray(x for x in message[4:])
        for i in range(32):
            r = R
            R = self.__g(R, key[i])
            L, R = r, self.__xor(L, R)

        return bytearray(R + L)

    @staticmethod
    def __mod32(block: bytes, key: bytes) -> bytes:
        # Сумма по модулю 2^32 - (block + key) mod 2**32.
        block = int.from_bytes(block, "big")
        key = int.from_bytes(key, "big")

        block = (block + key) % 2 ** 32

        return block.to_bytes(4)

    @staticmethod
    def __t_box(block: bytes) -> bytearray:
        # Нелинейное преобразование T бокс.
        # Первые четыре бита - индекс n строки.
        # Последние четыре бита - индекс n + 1 строки.
        ans = []
        for i in range(4):
            x1 = (block[i] & 0xf0) >> 4  # Левая часть - побитовая сумма с 0xf0 (11110000) - зануляет последние 4 бита.
            x2 = block[i] & 0x0f         # Правая часть - побитовая сумма с 0x0f (00001111) - зануляет первые 4 бита.

            left = tBox[i * 2][x1]
            right = tBox[i * 2 + 1][x2]
            ans.append((left << 4) | right)

        return bytearray(ans)

    @staticmethod
    def __shift11(block: bytes) -> bytes:
        # Циклический сдвиг блока на 11 бит.
        block = int.from_bytes(block, "big")
        block = (block << 11) % (2 ** 32) | (block >> 21)

        return block.to_bytes(4)

    @staticmethod
    def __xor(L: bytes, R: bytes) -> bytes:
        # Сумма по модулю 2. -> L xor R
        L = int.from_bytes(L, "big") ^ int.from_bytes(R, "big")

        return L.to_bytes(4)

    @staticmethod
    def __round_key(key: str) -> list[bytes]:
        # Генерация 32 32-битных раундовых ключей.
        # Первые 24 - прямая последовательность ключа key, остальные 8 обратная последовательность.
        key = format(int(key, 16), "b").zfill(256)
        part_key = [int(key[i:i + 32], 2).to_bytes(8) for i in range(0, 256, 32)]
        all_key = part_key * 3 + part_key[::-1]

        return all_key
