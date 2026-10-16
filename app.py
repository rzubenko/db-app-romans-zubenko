import tkinter as tk

from funkcijas import (
    add_client,
    add_order,
    add_product
)

def addFromWindow():
    name = name_input.get()
    surname = surname_input.get()

    add_client(name, surname)

    name_input.delete(0, tk.END)
    surname_input.delete(0, tk.END)

    result.config(text="klients pievienots")

def addFromWindowProduct():
    type = type_input.get()
    price = price_input.get()

    add_product(type, price)

    type_input.delete(0, tk.END)
    price_input.delete(0, tk.END)

    result2.config(text="prece pievienota")



#veidojam logu
window = tk.Tk()
window.title("Lats datubaze")
window.geometry("600x800")

#virsraksts
header = tk.Label(
    window,
    text = "Veikala datubaze",
    font = ("Arial", 20, "bold")
)
header.pack(pady = 20)

#klienta logs
client_block=tk.LabelFrame(
    window,
    text = "pievienot klientu",
    padx = 10,
    pady = 10
)
client_block.pack(fill = "x", padx = 20, pady = 20)

tk.Label(client_block, text="vards").pack()
name_input = tk.Entry(client_block, width=60)
name_input.pack(pady=5)

tk.Label(client_block, text="uzvards").pack()
surname_input = tk.Entry(client_block, width=60)
surname_input.pack(pady=5)

client_button = tk.Button(client_block, text="pievienot klientu", command=addFromWindow)
client_button.pack(pady=5)

result = tk.Label(
    client_block, text="", fg="green"
)
result.pack(pady=5)

#preces logs
product_block=tk.LabelFrame(
    window,
    text = "pievienot preci",
    padx = 10,
    pady = 10
)
product_block.pack(fill = "x", padx = 20, pady = 20)

tk.Label(product_block, text="nosaukums").pack()
type_input = tk.Entry(product_block, width=60)
type_input.pack(pady=5)

tk.Label(product_block, text="cena").pack()
price_input = tk.Entry(product_block, width=60)
price_input.pack(pady=5)

product_button = tk.Button(product_block, text="pievienot produktu", command=addFromWindowProduct)
product_button.pack(pady=5)

result2 = tk.Label(
    product_block, text="", fg="green"
)
result2.pack(pady=5)


#pasutijuma logs
order_block=tk.LabelFrame(
    window,
    text = "pievienot pasutijumu",
    padx = 10,
    pady = 10
)
order_block.pack(fill = "x", padx = 20, pady = 20)

tk.Label(order_block, text="klienta id").pack()
client_input = tk.Entry(order_block, width=60)
client_input.pack(pady=5)

tk.Label(order_block, text="preces id").pack()
product_input = tk.Entry(order_block, width=60)
product_input.pack(pady=5)

product_button = tk.Button(order_block, text="pievienot pasutijumu")
product_button.pack(pady=5)

window.mainloop()