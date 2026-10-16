import tkinter as tk
from funkcijas import (
    create_tables,
    add_guest,
    add_room,
    add_staff,
    add_order
)

# Ensure tables exist when starting the app
create_tables()

# --- BUTTON EVENT FUNCTIONS ---

def handle_add_guest():
    name = guest_name_input.get()
    surname = guest_surname_input.get()
    
    if name and surname:
        add_guest(name, surname)
        guest_name_input.delete(0, tk.END)
        guest_surname_input.delete(0, tk.END)
        guest_result.config(text="Klients veiksmīgi pievienots!", fg="green")
    else:
        guest_result.config(text="Lūdzu aizpildiet visus laukus!", fg="red")

def handle_add_room():
    room_num = room_number_input.get()
    avail = room_avail_input.get()
    
    try:
        add_room(int(room_num), int(avail))
        room_number_input.delete(0, tk.END)
        room_avail_input.delete(0, tk.END)
        room_result.config(text="Istaba veiksmīgi pievienota!", fg="green")
    except ValueError:
        room_result.config(text="Kļūda! Numuriem jābūt cipariem.", fg="red")

def handle_add_staff():
    name = staff_name_input.get()
    surname = staff_surname_input.get()
    job = staff_job_input.get()
    
    if name and surname and job:
        add_staff(name, surname, job)
        staff_name_input.delete(0, tk.END)
        staff_surname_input.delete(0, tk.END)
        staff_job_input.delete(0, tk.END)
        staff_result.config(text="Personāls veiksmīgi pievienots!", fg="green")
    else:
        staff_result.config(text="Lūdzu aizpildiet visus laukus!", fg="red")

def handle_add_order():
    g_id = order_guest_id.get()
    r_num = order_room_num.get()
    finished = order_finished_input.get()
    s_id = order_staff_id.get()
    
    try:
        add_order(int(g_id), int(r_num), int(finished), int(s_id))
        order_guest_id.delete(0, tk.END)
        order_room_num.delete(0, tk.END)
        order_finished_input.delete(0, tk.END)
        order_staff_id.delete(0, tk.END)
        order_result.config(text="Pasūtījums veiksmīgi pievienots!", fg="green")
    except ValueError:
        order_result.config(text="Kļūda! ID un istabai jābūt cipariem.", fg="red")


# --- MAIN WINDOW ---
window = tk.Tk()
window.title("Viesnīcas datubāze")
window.geometry("600x900")

# Virsraksts
header = tk.Label(
    window,
    text="Viesnīcas Vadības Sistēma",
    font=("Arial", 18, "bold")
)
header.pack(pady=10)

# --- 1. GUESTS BLOCK ---
guest_block = tk.LabelFrame(window, text="Pievienot klientu (Guest)", padx=10, pady=5)
guest_block.pack(fill="x", padx=20, pady=5)

tk.Label(guest_block, text="Vārds").pack()
guest_name_input = tk.Entry(guest_block, width=50)
guest_name_input.pack(pady=2)

tk.Label(guest_block, text="Uzvārds").pack()
guest_surname_input = tk.Entry(guest_block, width=50)
guest_surname_input.pack(pady=2)

tk.Button(guest_block, text="Pievienot klientu", command=handle_add_guest).pack(pady=5)
guest_result = tk.Label(guest_block, text="", fg="green")
guest_result.pack()

# --- 2. ROOMS BLOCK ---
room_block = tk.LabelFrame(window, text="Pievienot istabu (Room)", padx=10, pady=5)
room_block.pack(fill="x", padx=20, pady=5)

tk.Label(room_block, text="Istabas numurs (Room Number)").pack()
room_number_input = tk.Entry(room_block, width=50)
room_number_input.pack(pady=2)

tk.Label(room_block, text="Pieejamība (1 - brīvs, 0 - aizņemts)").pack()
room_avail_input = tk.Entry(room_block, width=50)
room_avail_input.insert(0, "1")  # default value
room_avail_input.pack(pady=2)

tk.Button(room_block, text="Pievienot istabu", command=handle_add_room).pack(pady=5)
room_result = tk.Label(room_block, text="", fg="green")
room_result.pack()

# --- 3. STAFF BLOCK ---
staff_block = tk.LabelFrame(window, text="Pievienot personālu (Staff)", padx=10, pady=5)
staff_block.pack(fill="x", padx=20, pady=5)

tk.Label(staff_block, text="Vārds").pack()
staff_name_input = tk.Entry(staff_block, width=50)
staff_name_input.pack(pady=2)

tk.Label(staff_block, text="Uzvārds").pack()
staff_surname_input = tk.Entry(staff_block, width=50)
staff_surname_input.pack(pady=2)

tk.Label(staff_block, text="Amats (Job)").pack()
staff_job_input = tk.Entry(staff_block, width=50)
staff_job_input.pack(pady=2)

tk.Button(staff_block, text="Pievienot personālu", command=handle_add_staff).pack(pady=5)
staff_result = tk.Label(staff_block, text="", fg="green")
staff_result.pack()

# --- 4. ORDERS BLOCK ---
order_block = tk.LabelFrame(window, text="Pievienot pasūtījumu (Order)", padx=10, pady=5)
order_block.pack(fill="x", padx=20, pady=5)

tk.Label(order_block, text="Klienta ID (Guest ID)").pack()
order_guest_id = tk.Entry(order_block, width=50)
order_guest_id.pack(pady=2)

tk.Label(order_block, text="Istabas numurs (Room Number)").pack()
order_room_num = tk.Entry(order_block, width=50)
order_room_num.pack(pady=2)

tk.Label(order_block, text="Pasūtījums pabeigts? (1 - jā, 0 - nē)").pack()
order_finished_input = tk.Entry(order_block, width=50)
order_finished_input.insert(0, "1")
order_finished_input.pack(pady=2)

tk.Label(order_block, text="Darbinieka ID (Staff ID)").pack()
order_staff_id = tk.Entry(order_block, width=50)
order_staff_id.pack(pady=2)

tk.Button(order_block, text="Pievienot pasūtījumu", command=handle_add_order).pack(pady=5)
order_result = tk.Label(order_block, text="", fg="green")
order_result.pack()

# Start application
window.mainloop()