import os
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox


class PlayfairApp:
    def __init__(self, root):
        self.mat = None
        self.root = root
        self.root.title("Playfair Cipher App")

        # ==== Fields for Variables ====
        self.key = None
        self.file_name = None
        self.action = "Encrypt"
        self.plaintext = None
        self.output_text = None

        # ==== Window Frame ====
        self.window_frame1 = tk.Frame(root, borderwidth=2)
        self.window_frame1.pack(pady=5, padx=5, ipadx=5, ipady=5)

        self.window_frame2 = tk.Frame(root, borderwidth=2)
        self.window_frame2.pack(pady=5, padx=5, ipadx=5, ipady=5)

        self.window_frame3 = tk.Frame(root, borderwidth=2)
        self.window_frame3.pack(pady=5, padx=5, ipadx=5, ipady=5)
        self.window_frame3.pack_forget()

        self.window_frame4 = tk.Frame(root, borderwidth=2)
        self.window_frame4.pack(fill="both", pady=5, padx=5, ipadx=5, ipady=5)

        # Insert Text
        insert_label = tk.Label(self.window_frame1, text="Insert Text : ", anchor='w', justify="left")
        insert_label.pack(fill='both')
        self.text = tk.Text(self.window_frame1, wrap="word", width=50, height=5)
        self.text.pack(pady=10)

        # Browse File
        browse_button = tk.Button(self.window_frame1, text="Browse File", command=self.browse_file)
        self.file_name = tk.Label(self.window_frame1, text="")
        browse_button.pack(side="left")
        self.file_name.pack(side="left", ipadx=5)

        # ==== Sub Window Frame 2 ====
        subWindow_frame2 = tk.Frame(self.window_frame2, borderwidth=2)
        subWindow_frame2.pack(fill='both')

        # Insert Key
        key_label = tk.Label(subWindow_frame2, text="Insert Key : ")
        key_label.pack(side="left")
        self.key_var = tk.StringVar(value=self.key)
        self.key_entry = tk.Entry(self.window_frame2, textvariable=self.key_var, width=40, borderwidth=2,
                                  relief="groove")
        self.key_entry.pack(side="left")

        # Action Combo Box
        self.action_items = ('Encrypt', 'Decrypt')
        self.action_combo_box_var = tk.StringVar(value=self.action_items[0])
        self.action_combo_box = ttk.Combobox(self.window_frame2, textvariable=self.action_combo_box_var,
                                             state="readonly")
        self.action_combo_box['values'] = self.action_items
        self.action_combo_box.pack(side="left")
        self.action_combo_box.bind("<<ComboboxSelected>>", lambda event: self.on_combo_box_select(event))

        # ==== Sub Window Frame 4 ====
        subWindowFrame4 = tk.Frame(self.window_frame4, borderwidth=2)
        subWindowFrame4.pack(fill='both', expand=True)

        calculate_button = tk.Button(subWindowFrame4, text="Calculate", command=self.calculate)
        calculate_button.pack(side="left", fill='both', expand=True, pady=5)

        save_button = tk.Button(subWindowFrame4, text="Save File", command=self.save_file)
        save_button.pack(side="left", fill='both', expand=True, pady=5)

        exit_button = tk.Button(subWindowFrame4, text="Exit", command=root.quit)
        exit_button.pack(side="left", fill='both', expand=True, pady=5)

    def on_combo_box_select(self, event):
        self.action = self.action_combo_box.get()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                file_content = file.read().strip()

            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, file_content)
            self.update_data_label(file_path)

    def update_data_label(self, txt_result):
        if txt_result is not None:
            self.file_name.config(text="Txt File : " + os.path.basename(txt_result))
        else:
            self.file_name.config(text="Txt File : Empty")

    def save_file(self):
        encrypted_text = self.text.get("1.0", "end-1c").strip()

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, "w") as file:
                file.write(encrypted_text)
            tk.messagebox.showinfo("File Saved", "File saved successfully!")

    def repack_window_frame34(self):
        self.window_frame4.pack_forget()
        self.window_frame3.pack(pady=5, padx=5, ipadx=5, ipady=5)
        self.window_frame4.pack(fill="both", pady=5, padx=5, ipadx=5, ipady=5)

    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()

    def encrypt_text(self, key):
        self.key = key.replace(' ', '').lower()
        self.key = self.clean_text(self.key)

        self.mat = self.generate_matrix()
        self.matrix(self.mat)

        formatted_msg = self.format_message(self.plaintext)
        ciphertext = self.encrypt(formatted_msg, self.mat)

        return ciphertext

    def calculate(self):
        self.clear_frame(self.window_frame3)

        self.key = self.key_var.get()
        if self.action == "Encrypt" and self.key_var.get() != "":
            self.plaintext = self.text.get("1.0", "end-1c").strip()
            encrypted_text = self.encrypt_text(self.key)
            self.output_text.insert(tk.END, encrypted_text)
            self.output_text.config(state="disabled")
            self.repack_window_frame34()

        elif self.action == "Decrypt" and self.key_var.get() != "":
            self.plaintext = self.text.get("1.0", "end-1c").strip()
            decrypted_text = self.decrypt_text(self.plaintext)
            self.output_text.insert(tk.END, decrypted_text)
            self.output_text.config(state="disabled")
            self.repack_window_frame34()

    def matrix(self, mat):
        # ==== Sub Window Frame 3 ====
        subWindowFrame3_1 = tk.Frame(self.window_frame3, borderwidth=2)
        subWindowFrame3_1.pack(fill='both', expand=True)

        subWindowFrame3_2 = tk.Frame(self.window_frame3, borderwidth=2)
        subWindowFrame3_2.pack(fill='both', expand=True)

        matrix_label = tk.Label(subWindowFrame3_1, text="Key Matrix : ")
        matrix_label.pack(side="left", fill='both')

        output_label = tk.Label(subWindowFrame3_1, text="Output text : ")
        output_label.pack(side="left", fill='both', padx=75)

        matrix_frame = tk.Frame(subWindowFrame3_2, relief="groove", borderwidth=2)
        matrix_frame.columnconfigure(0, weight=1)
        matrix_frame.columnconfigure(1, weight=1)
        matrix_frame.columnconfigure(2, weight=1)
        matrix_frame.columnconfigure(3, weight=1)
        matrix_frame.columnconfigure(4, weight=1)
        matrix_frame.rowconfigure(0, weight=1)
        matrix_frame.rowconfigure(1, weight=1)
        matrix_frame.rowconfigure(2, weight=1)
        matrix_frame.rowconfigure(3, weight=1)
        matrix_frame.rowconfigure(4, weight=1)
        matrix_frame.pack(side='left', pady=5)

        for row in mat:
            for col in row:
                matrix_label = tk.Label(matrix_frame, text=col.upper(), relief="groove")
                matrix_label.grid(row=mat.index(row), column=row.index(col), sticky="nsew", ipadx=5, ipady=5)

        # Output Text
        self.output_text = tk.Text(subWindowFrame3_2, wrap="word", width=40, height=10)
        self.output_text.pack(pady=10, padx=15)

    def generate_matrix(self):
        # Inisialisasi matriks 5x5
        mat = [['' for _ in range(5)] for _ in range(5)]

        # Inisialisasi variabel flag dengan 26 elemen False
        flag = [False] * 26

        # Untuk melacak posisi saat ini dalam matriks
        # x untuk baris, y untuk kolom
        x, y = 0, 0

        # Menambahkan huruf dari kunci ke dalam matriks
        for char in self.key:
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

    def format_message(self, msg):
        # Mengganti huruf q dalam teks menjadi huruf y
        msg = msg.replace('q', 'y')
        msg = msg.lower()

        formatted_msg = self.clean_text(msg)
        print(formatted_msg)

        # Add 'z' if the length of the message is odd
        i = 1
        while i < len(formatted_msg):
            if formatted_msg[i - 1] == formatted_msg[i]:
                formatted_msg = formatted_msg[:i] + 'z' + formatted_msg[i:]
            i += 2

        if len(formatted_msg) % 2 != 0:
            formatted_msg += 'z'
        print(formatted_msg)
        return formatted_msg

    def format_message_decrypt(self, msg):
        msg = msg.lower()

        formatted_msg = self.clean_text(msg)

        return formatted_msg

    def clean_text(self, msg):
        formatted_msg = ''
        i = 0
        while i < len(msg):
            char1 = msg[i]
            if char1.isalpha():
                formatted_msg += char1
            i += 1
        return formatted_msg

    def encrypt(self, message, mat):
        ciphertext = ''  # Variabel untuk menyimpan hasil dari enkripsi
        i = 0

        while i < len(message):
            # Pasangan 2 Huruf
            char1 = message[i]  # Huruf pertama
            char2 = message[i + 1]  # Huruf kedua

            pos1 = self.get_position(mat, char1)  # Posisi pertama pada matriks
            pos2 = self.get_position(mat, char2)  # Posisi kedua pada matriks

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

    def decrypt_text(self, ciphertext):
        self.key = self.key.replace(' ', '').lower()
        self.key = self.clean_text(self.key)

        mat = self.generate_matrix()
        self.matrix(mat)

        ciphertext_formatted = self.format_message_decrypt(ciphertext)
        print(ciphertext_formatted)

        plaintext = ''
        i = 0

        while i < len(ciphertext_formatted):
            char1 = ciphertext_formatted[i]
            char2 = ciphertext_formatted[i + 1]

            pos1 = self.get_position(mat, char1)
            pos2 = self.get_position(mat, char2)

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

        if plaintext.endswith('z'):
            plaintext = plaintext[:-1]

        i = 1
        while i < len(plaintext) - 1:
            if plaintext[i - 1] == plaintext[i + 1]:
                plaintext = plaintext.replace('z', '')
            i += 2

        plaintext = plaintext.replace('y', 'q')

        return plaintext

    # === Fungsi untuk menyesuaikan posisi huruf pada matriks ===
    def get_position(self, mat, char):
        # Loop untuk baris sebanyak 5x
        for row in range(5):
            # Loop untuk kolom sebanyak 5x
            for col in range(5):
                # Mengecek apakah elemen pada matriks pada posisi (row)(col) sama dengan huruf yang dicari
                if mat[row][col] == char:
                    # Jika sama, kembalikan nilai kolom dan baris
                    return row, col


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x550")
    root.resizable(False, False)
    app = PlayfairApp(root)
    root.mainloop()
