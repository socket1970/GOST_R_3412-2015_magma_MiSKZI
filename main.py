from src.cipher import Magma

if __name__ == "__main__":
    m = Magma()
    k = m.key()  # Генерация ключа
    d = m.encode(
        """abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
абвгдеёжзийклмнопрстуфхцчшщъыьэюя
АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
1234567890
. , ! ? : ; - – ... "" ' () | ?! . , "" '' [] {}
️🚑🤡🤔🧐⬇️↙️⬅️🗑️""", k)  # Шифровка
    c = m.decode(d, k)  # Дешифрование
    print(c)
