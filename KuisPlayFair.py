# === Fungsi untuk membuat matriks 5x5 ===
def generate_matrix(key):
    # Inisialisasi matriks 5x5
    mat = [['' for _ in range(5)] for _ in range(5)]

    # Inisialisasi variabel flag dengan 26 elemen False
    flag = [False] * 26

    # Untuk melacak posisi saat ini dalam matriks
    # x untuk baris, y untuk kolom
    x, y = 0, 0

    # Menambahkan huruf dari kunci ke dalam matriks
    for char in key:
        # Mengganti huruf J dengan huruf I
        if char == 'q':
            char = 'y'

        # Variabel untuk menentukan posisi (index) huruf dalam alfabet
        index = ord(char) - ord('a')

        # Mengecek apakah huruf belum ada dalam matriks
        if not flag[index]:
            # Jika belum ada, maka huruf akan dimasukkan kedalam matriks
            mat[x][y] = char
            # Kemudian flag akan diinisialisasi menjadi True
            flag[index] = True
            # Increment untuk posisi kolom (y) saat ini ke kolom berikutnya
            y += 1

        if y == 5:  # Jika sudah sampai ke kolom ke-5
            x += 1  # maka baris (xa) akan di-increment,
            y = 0  # dan mengatur kolom kembali pada kolom pertama (ke-0)

    # Menambahkan huruf selanjutnya (huruf yang belum terdapat pada kunci)
    # (A-Z kecuali J yang diganti dengan I)
    for char in range(ord('a'), ord('z') + 1):
        if char == ord('q'):  # Mengabaikan huruf J
            continue

        # Algoritma sama dengan loop sebelumnya
        index = char - ord('a')

        if not flag[index]:
            mat[x][y] = chr(char)
            flag[index] = True
            y += 1

        if y == 5:
            x += 1
            y = 0

    return mat  # Mengembalikan matriks yang berisi huruf


# === Fungsi untuk memformat teks sebelum enkripsi ===
# === Fungsi untuk memformat teks sebelum enkripsi ===
def format_message(msg):
    # Mengganti huruf q dalam teks menjadi huruf y
    msg = msg.replace('q', 'y')

    formatted_msg = ''
    i = 0
    while i < len(msg):
        char1 = msg[i]
        if char1.isalpha():  # Mengecek apakah karakter adalah huruf alfabet
            i += 1
            if i < len(msg):
                char2 = msg[i]
                if char2.isalpha():  # Mengecek apakah karakter berikutnya juga huruf alfabet
                    # Pasangan huruf alfabet, tambahkan ke formatted_msg
                    formatted_msg += char1 + char2
                    i += 1  # Langsung lanjut ke karakter berikutnya
                else:
                    # Karakter non-alfabet ditemukan, lanjutkan ke karakter berikutnya
                    i += 1
            else:
                # Karakter terakhir adalah huruf alfabet tunggal, tambahkan ke formatted_msg
                formatted_msg += char1
                i += 1
        else:
            # Karakter non-alfabet ditemukan, lanjutkan ke karakter berikutnya
            i += 1

    # Menghapus karakter 'w' yang tidak perlu jika panjang pesan ganjil
    if len(formatted_msg) % 2 != 0:
        formatted_msg = formatted_msg[:-1]

    return formatted_msg


# === Fungsi untuk memformat teks hasil dekripsi ===
def format_message_decrypt(msg):
    # Mengganti huruf 'y' yang seharusnya menjadi 'q' kembali
    msg = msg.replace('y', 'q')

    formatted_msg = ''
    i = 0
    while i < len(msg):
        char1 = msg[i]
        if char1.isalpha():  # Mengecek apakah karakter adalah huruf alfabet
            i += 1
            if i < len(msg):
                char2 = msg[i]
                if char2.isalpha():  # Mengecek apakah karakter berikutnya juga huruf alfabet
                    # Pasangan huruf alfabet, tambahkan ke formatted_msg
                    formatted_msg += char1 + char2
                    i += 1  # Langsung lanjut ke karakter berikutnya
                else:
                    # Karakter non-alfabet ditemukan, lanjutkan ke karakter berikutnya
                    i += 1
            else:
                # Karakter terakhir adalah huruf alfabet tunggal, tambahkan ke formatted_msg
                formatted_msg += char1
                i += 1
        else:
            # Karakter non-alfabet ditemukan, lanjutkan ke karakter berikutnya
            i += 1

    # Menghapus karakter 'w' yang tidak perlu jika panjang pesan ganjil
    if len(formatted_msg) % 2 != 0:
        formatted_msg = formatted_msg[:-1]

    return formatted_msg


# === Fungsi untuk menyesuaikan posisi huruf pada matriks ===
def get_position(mat, char):
    # Loop untuk baris sebanyak 5x
    for row in range(5):
        # Loop untuk kolom sebanyak 5x
        for col in range(5):
            # Mengecek apakah elemen pada matriks pada posisi (row)(col) sama dengan huruf yang dicari
            if mat[row][col] == char:
                # Jika sama, kembalikan nilai kolom dan baris
                return row, col


# === Fungsi untuk mengenkripsi ===
def encrypt(message, mat):
    ciphertext = ''  # Variabel untuk menyimpan hasil dari enkripsi
    i = 0

    while i < len(message):
        # Pasangan 2 Huruf
        char1 = message[i]  # Huruf pertama
        char2 = message[i + 1]  # Huruf kedua

        pos1 = get_position(mat, char1)  # Posisi pertama pada matriks
        pos2 = get_position(mat, char2)  # Posisi keuda pada matriks

        x1, y1 = pos1  # Baris dan kolom huruf pertama
        x2, y2 = pos2  # Baris dan kolom huruf kedua

        # Jika berada pada baris yang sama, geser ke kanan
        if x1 == x2:
            # Menambahkan huruf pertama hasil enkripsi
            ciphertext += mat[x1][(y1 - 1) % 5]
            # Menambahkan huruf kedua hasil enkripsi
            ciphertext += mat[x2][(y2 - 1) % 5]
        # Jika berada pada kolom yang sama, geser ke bawah
        elif y1 == y2:
            ciphertext += mat[(x1 - 1) % 5][y1]
            ciphertext += mat[(x2 - 1) % 5][y2]
        # Jika berada pada baris dan kolom yang berbeda
        else:
            ciphertext += mat[x2][y1]
            ciphertext += mat[x1][y2]

        i += 2

    return ciphertext


# === Fungsi untuk mendekripsi ===
def decrypt(ciphertext, mat):
    plaintext = ''
    i = 0

    while i < len(ciphertext):
        char1 = ciphertext[i]
        char2 = ciphertext[i + 1]

        pos1 = get_position(mat, char1)
        pos2 = get_position(mat, char2)

        x1, y1 = pos1
        x2, y2 = pos2

        if x1 == x2:
            plaintext += mat[x1][(y1 + 1) % 5]
            plaintext += mat[x2][(y2 + 1) % 5]
        elif y1 == y2:
            plaintext += mat[(x1 + 1) % 5][y1]
            plaintext += mat[(x2 + 1) % 5][y2]
        else:
            plaintext += mat[x2][y1]
            plaintext += mat[x1][y2]

        i += 2

    return plaintext


# Output Matriks
def matrix(mat):
    print("\nMatriks:")
    for row in mat:
        print(' '.join(row))


# Enkripsi
def inputEncrypt():
    plaintext = input("Input Plain Text: ")
    key = input(f"Input kunci: ").replace(' ', '').lower()

    mat = generate_matrix(key)
    matrix(mat)

    formatted_msg = format_message(plaintext)
    ciphertext = encrypt(formatted_msg, mat)

    print("\nPlain Text: ", plaintext)
    print("Formatted Text: ", formatted_msg, "[", ' '.join(
        formatted_msg[i:i + 2] for i in range(0, len(formatted_msg), 2)), "]")
    print("Encrypted Text: ", ciphertext, "[", ' '.join(
        ciphertext[i:i + 2] for i in range(0, len(ciphertext), 2)), "]")


# Dekripsi
def inputDecrypt():
    ciphertext = input("Input Cipher Text: ").replace(' ', '').lower()
    key = input(f"Input kunci: ").replace(' ', '').lower()

    mat = generate_matrix(key)
    matrix(mat)

    # formatted_msg = format_message(ciphertext)
    decrypted_msg = decrypt(ciphertext, mat)
    # print("\nFormatted Text: ", formatted_msg, "[", ' '.join(
    #     formatted_msg[i:i+2] for i in range(0, len(formatted_msg), 2)), "]")
    print("\nDecrypted Text: ", decrypted_msg, "[", ' '.join(
        decrypted_msg[i:i + 2] for i in range(0, len(decrypted_msg), 2)), "]")
    print("Plain Text: ", format_message_decrypt(decrypted_msg))
