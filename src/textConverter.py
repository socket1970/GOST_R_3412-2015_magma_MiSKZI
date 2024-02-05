#         @@@     @@@     @@
#          &@.      @@     @@
#          @@      @@      (@#
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


class TextConverter:
    def __init__(self, encoding="UTF-8"):
        self.__encoding = encoding

    def str2bin(self, message: str, n: int):
        message = bytearray(message, self.__encoding) # type: ignore
        # Перевод строки в бинарный формат.

        message = [message[i:i + n] for i in range(0, len(message), n)] # type: ignore
        # Дробление бинарного формата на вложенные списки по n элементов.

        self.__leveling(message[-1], n) # type: ignore
        # Выравнивание последнего элемента по n символов.

        return message

    def bin2str(self, message: list[bytearray]):
        self.__del_nul_byte(message[-1])
        # Удаление nul байтов с конца.

        message = bytearray([item for sublist in message for item in sublist]) # type: ignore
        # Преобразование вложенных списков в единый - [[0, 1], [2, 3], [4, 5]] - [0, 1, 2, 3, 4, 5]
        # и преобразование в bytearray.

        message = message.decode(self.__encoding) # type: ignore
        # Декодирование в соответствии с кодировкой.

        return message

    @staticmethod
    def __leveling(mess: bytearray, n: int):
        # Выравнивание блока mess по n битов
        mess.extend(b"\x00" * (-len(mess) % n))

    @staticmethod
    def __del_nul_byte(b: bytearray):
        # Удаление ВСЕХ nul битов
        while 0 in b:
            b.remove(0)
