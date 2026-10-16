import tkinter as tk
from funkcijas import (
    create_tables,
    add_guest,
    add_room,
    add_staff,
    add_order
)

create_tables()

#pievienojam funkcijas pie pogiem

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


#galvenais logs
window = tk.Tk()
window.title("Hotel Database")
window.geometry("600x900")

#virsraksts
header = tk.Label(
    window,
    text="Welcome to our hotel database system",
    font=("Arial", 18, "bold")
)
header.pack(pady=10)


#guests
guest_block = tk.LabelFrame(window, text="Add a guest", padx=10, pady=5)
guest_block.pack(fill="x", padx=20, pady=5)

tk.Label(guest_block, text="Name").pack()
guest_name_input = tk.Entry(guest_block, width=50)
guest_name_input.pack(pady=2)

tk.Label(guest_block, text="Surname").pack()
guest_surname_input = tk.Entry(guest_block, width=50)
guest_surname_input.pack(pady=2)

tk.Button(guest_block, text="Save", command=handle_add_guest).pack(pady=5)
guest_result = tk.Label(guest_block, text="", fg="green")
guest_result.pack()


#rooms
room_block = tk.LabelFrame(window, text="Add a room", padx=10, pady=5)
room_block.pack(fill="x", padx=20, pady=5)

tk.Label(room_block, text="Room number").pack()
room_number_input = tk.Entry(room_block, width=50)
room_number_input.pack(pady=2)

tk.Label(room_block, text="Availability (1 - available, 0 - not available)").pack()
room_avail_input = tk.Entry(room_block, width=50)
room_avail_input.insert(0, "1")  # default value
room_avail_input.pack(pady=2)

tk.Button(room_block, text="Save", command=handle_add_room).pack(pady=5)
room_result = tk.Label(room_block, text="", fg="green")
room_result.pack()


#staff
staff_block = tk.LabelFrame(window, text="Add a staff member", padx=10, pady=5)
staff_block.pack(fill="x", padx=20, pady=5)

tk.Label(staff_block, text="Name").pack()
staff_name_input = tk.Entry(staff_block, width=50)
staff_name_input.pack(pady=2)

tk.Label(staff_block, text="Surname").pack()
staff_surname_input = tk.Entry(staff_block, width=50)
staff_surname_input.pack(pady=2)

tk.Label(staff_block, text="Job").pack()
staff_job_input = tk.Entry(staff_block, width=50)
staff_job_input.pack(pady=2)

tk.Button(staff_block, text="Save", command=handle_add_staff).pack(pady=5)
staff_result = tk.Label(staff_block, text="", fg="green")
staff_result.pack()

#orders
order_block = tk.LabelFrame(window, text="Add an order", padx=10, pady=5)
order_block.pack(fill="x", padx=20, pady=5)

tk.Label(order_block, text="Guest ID").pack()
order_guest_id = tk.Entry(order_block, width=50)
order_guest_id.pack(pady=2)

tk.Label(order_block, text="Room number").pack()
order_room_num = tk.Entry(order_block, width=50)
order_room_num.pack(pady=2)

tk.Label(order_block, text="Staff ID").pack()
order_staff_id = tk.Entry(order_block, width=50)
order_staff_id.pack(pady=2)

tk.Label(order_block, text="An order is complete (1 - yes, 0 - no)").pack()
order_finished_input = tk.Entry(order_block, width=50)
order_finished_input.insert(0, "1")
order_finished_input.pack(pady=2)

tk.Button(order_block, text="Save", command=handle_add_order).pack(pady=5)
order_result = tk.Label(order_block, text="", fg="green")
order_result.pack()

#palais aplikāciju
window.mainloop()