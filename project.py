# Import library yang dibutuhkan
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

# =============================
# Fungsi-fungsi untuk manipulasi gambar
# =============================

# Fungsi untuk memuat gambar dari path dan mengubahnya jadi hitam putih (binary)
def load_gambar(path):
    img = Image.open(path).convert('1')  # konversi ke mode '1' (black & white)
    return img

# Fungsi untuk menyimpan gambar ke file
def save_gambar(img, nama_file):
    img.save(nama_file)
    messagebox.showinfo("Sukses", f"Gambar disimpan: {nama_file}")

# Fungsi untuk melakukan operasi Dilasi (Dilation)
def dilasi(img):
    lebar, tinggi = img.size
    hasil = Image.new('1', (lebar, tinggi))  # buat gambar kosong hitam putih
    pixels = img.load()
    output = hasil.load()
    # Iterasi setiap piksel (kecuali tepi gambar)
    for x in range(1, lebar - 1):
        for y in range(1, tinggi - 1):
            nilai = 0
            # Periksa tetangga 3x3
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if pixels[x + dx, y + dy] == 255:
                        nilai = 255
            output[x, y] = nilai
    return hasil

# Fungsi untuk melakukan operasi Erosi (Erosion)
def erosi(img):
    lebar, tinggi = img.size
    hasil = Image.new('1', (lebar, tinggi))  # buat gambar kosong hitam putih
    pixels = img.load()
    output = hasil.load()
    # Iterasi setiap piksel (kecuali tepi gambar)
    for x in range(1, lebar - 1):
        for y in range(1, tinggi - 1):
            nilai = 255
            # Periksa tetangga 3x3
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if pixels[x + dx, y + dy] == 0:
                        nilai = 0
            output[x, y] = nilai
    return hasil

# Fungsi untuk operasi Opening (Erosi diikuti Dilasi)
def opening(img):
    return dilasi(erosi(img))

# Fungsi untuk operasi Closing (Dilasi diikuti Erosi)
def closing(img):
    return erosi(dilasi(img))

# =============================
# Fungsi-fungsi untuk antarmuka Tkinter
# =============================

# Fungsi untuk memilih file gambar dari komputer
def pilih_file():
    global gambar_asli
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if path:
        gambar_asli = load_gambar(path)
        label_path.config(text=path)  # tampilkan path file di label
        tampilkan_gambar(gambar_asli)  # tampilkan gambar preview

# Fungsi untuk menampilkan gambar di label
def tampilkan_gambar(img):
    img_preview = img.resize((400, 400))  # resize gambar agar pas ditampilkan
    img_tk = ImageTk.PhotoImage(img_preview)
    label_gambar.config(image=img_tk)
    label_gambar.image = img_tk  # simpan referensi untuk mencegah garbage collection

# Fungsi untuk memproses Dilasi
def proses_dilasi():
    if gambar_asli:
        hasil = dilasi(gambar_asli)
        save_gambar(hasil, "output_dilasi.png")
        tampilkan_gambar(hasil)

# Fungsi untuk memproses Erosi
def proses_erosi():
    if gambar_asli:
        hasil = erosi(gambar_asli)
        save_gambar(hasil, "output_erosi.png")
        tampilkan_gambar(hasil)

# Fungsi untuk memproses Opening
def proses_opening():
    if gambar_asli:
        hasil = opening(gambar_asli)
        save_gambar(hasil, "output_opening.png")
        tampilkan_gambar(hasil)

# Fungsi untuk memproses Closing
def proses_closing():
    if gambar_asli:
        hasil = closing(gambar_asli)
        save_gambar(hasil, "output_closing.png")
        tampilkan_gambar(hasil)

# =============================
# Setup jendela utama Tkinter
# =============================

# Membuat window utama
root = tk.Tk()
root.title("Morfologi Citra Hitam Putih")
root.geometry("600x600")  # Ukuran window

# Variabel global untuk menyimpan gambar asli
gambar_asli = None

# Tombol untuk memilih gambar
btn_pilih = tk.Button(root, text="Pilih Gambar", command=pilih_file)
btn_pilih.pack(pady=5)

# Label untuk menampilkan path file yang dipilih
label_path = tk.Label(root, text="Belum ada file dipilih")
label_path.pack()

# Label untuk menampilkan preview gambar
label_gambar = tk.Label(root)
label_gambar.pack(pady=5)

# Frame untuk menampung tombol operasi
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

# Tombol-tombol operasi (Dilasi, Erosi, Opening, Closing)
btn_dilasi = tk.Button(frame_buttons, text="Dilasi", command=proses_dilasi)
btn_dilasi.grid(row=0, column=0, padx=5)

btn_erosi = tk.Button(frame_buttons, text="Erosi", command=proses_erosi)
btn_erosi.grid(row=0, column=1, padx=5)

btn_opening = tk.Button(frame_buttons, text="Opening", command=proses_opening)
btn_opening.grid(row=0, column=2, padx=5)

btn_closing = tk.Button(frame_buttons, text="Closing", command=proses_closing)
btn_closing.grid(row=0, column=3, padx=5)

# Menjalankan aplikasi Tkinter
root.mainloop()
