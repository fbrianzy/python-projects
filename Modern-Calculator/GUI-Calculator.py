import tkinter as tk

# Fungsi untuk menangani klik tombol
def btn_click(item):
    global expression
    expression += str(item)
    input_text.set(expression)

# Fungsi untuk menghitung hasil ekspresi
def btn_equal():
    try:
        global expression
        result = str(eval(expression))  # Menghitung ekspresi
        input_text.set(result)
        expression = result  # Menyimpan hasil sebagai ekspresi baru
    except:
        input_text.set("Error")
        expression = ""

# Fungsi untuk membersihkan input
def btn_clear():
    global expression
    expression = ""
    input_text.set("")

# Fungsi untuk menghapus satu karakter terakhir
def btn_delete():
    global expression
    expression = expression[:-1]  # Menghapus karakter terakhir
    input_text.set(expression)

# Fungsi untuk menangani input dari keyboard
def key_event(event):
    key = event.keysym
    if key in "0123456789":
        btn_click(key)  # Menangani angka
    elif key in ["plus", "KP_Add"]:
        btn_click("+")  # Menangani penambahan
    elif key in ["minus", "KP_Subtract"]:
        btn_click("-")  # Menangani pengurangan
    elif key in ["asterisk", "KP_Multiply"]:
        btn_click("*")  # Menangani perkalian
    elif key in ["slash", "KP_Divide"]:
        btn_click("/")  # Menangani pembagian
    elif key == "Return":
        btn_equal()  # Menangani hasil (Enter)
    elif key == "BackSpace":
        btn_delete()  # Menangani penghapusan satu karakter (Backspace)
    elif key == "period" or key == "KP_Decimal":
        btn_click(".")  # Menangani tanda desimal
    elif key == "Escape":
        btn_clear()  # Menangani penghapusan semua (Escape)

# Membuat window utama
window = tk.Tk()
window.title("Modern Calculator - fbrianzy on Github")
window.geometry("485x520")
window.configure(bg="#222222")
window.resizable(width=False, height=False)  # Warna latar belakang modern

expression = ""
input_text = tk.StringVar()

# Frame untuk tampilan input
input_frame = tk.Frame(window, bd=25, bg="#333333", highlightbackground="#ffcc00", highlightthickness=2)
input_frame.grid(row=0, column=0)

# Entry widget untuk menampilkan input dan hasil
input_field = tk.Entry(input_frame, textvariable=input_text, font=('Arial', 20), fg="#ffffff", bg="#333333", bd=0, justify=tk.RIGHT)
input_field.grid(row=0, column=0)
# input_field.pack(ipady=20)  # Mengatur padding internal vertikal

# Frame untuk tombol
btns_frame = tk.Frame(window, bg="#222222")
btns_frame.grid(row=1, column=0, columnspan=2)

btns_font = ('Arial', 15)
btns_width = 10

# Baris pertama tombol
clear = tk.Button(window, text="C", fg="#ffffff", bg="#ff3300", font=btns_font, width=10, height=3, bd=2, command=lambda: btn_clear())
clear.grid(row=0, column=1)

delete = tk.Button(btns_frame, text="Del", fg="#ffffff", bg="#ffcc00", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_delete())
delete.grid(row=0, column=3)

# Baris kedua tombol
btn_7 = tk.Button(btns_frame, text="7", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(7))
btn_7.grid(row=0, column=0)
btn_8 = tk.Button(btns_frame, text="8", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(8))
btn_8.grid(row=0, column=1)
btn_9 = tk.Button(btns_frame, text="9", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(9))
btn_9.grid(row=0, column=2)
divide = tk.Button(btns_frame, text="/", fg="#ffffff", bg="#ffcc00", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click("/"))
divide.grid(row=1, column=3)

# Baris ketiga tombol
btn_4 = tk.Button(btns_frame, text="4", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(4))
btn_4.grid(row=1, column=0)
btn_5 = tk.Button(btns_frame, text="5", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(5))
btn_5.grid(row=1, column=1)
btn_6 = tk.Button(btns_frame, text="6", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(6))
btn_6.grid(row=1, column=2)
multiply = tk.Button(btns_frame, text="*", fg="#ffffff", bg="#ffcc00", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click("*"))
multiply.grid(row=2, column=3)

# Baris keempat tombol
btn_1 = tk.Button(btns_frame, text="1", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(1))
btn_1.grid(row=2, column=0)
btn_2 = tk.Button(btns_frame, text="2", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(2))
btn_2.grid(row=2, column=1)
btn_3 = tk.Button(btns_frame, text="3", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click(3))
btn_3.grid(row=2, column=2)
subtract = tk.Button(btns_frame, text="-", fg="#ffffff", bg="#ffcc00", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click("-"))
subtract.grid(row=3, column=3)

# Baris kelima tombol
btn_0 = tk.Button(btns_frame, text="0", fg="#ffffff", bg="#666666", font=btns_font, width=21, height=3, bd=2, command=lambda: btn_click(0))
btn_0.grid(row=3, column=0, columnspan=2)
decimal = tk.Button(btns_frame, text=".", fg="#ffffff", bg="#666666", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click("."))
decimal.grid(row=3, column=2)
add = tk.Button(btns_frame, text="+", fg="#ffffff", bg="#ffcc00", font=btns_font, width=btns_width, height=3, bd=2, command=lambda: btn_click("+"))
add.grid(row=4, column=3)

# Tombol sama dengan
equal = tk.Button(btns_frame, text="=", fg="#ffffff", bg="#00cc66", font=btns_font, width=32, height=3, bd=2, command=lambda: btn_equal())
equal.grid(row=4, column=0, columnspan=3)

# Bind event keyboard ke window
window.bind("<Key>", key_event)

window.mainloop()
