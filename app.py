import customtkinter as ctk
from funkcijas import (
    create_tables,
    add_guest,
    add_room,
    add_staff,
    add_order
)

create_tables()

# Iestatām modernu izskatu
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Hotel Database (Modern)")
app.geometry("650x750")

app.iconbitmap("assets/images/hotel.ico")

# Funkcijas datu pievienošanai
def handle_add_guest():
    name = guest_name_input.get()
    surname = guest_surname_input.get()
    
    if name and surname:
        add_guest(name, surname)
        guest_name_input.delete(0, "end")
        guest_surname_input.delete(0, "end")
        guest_result.configure(text="Klients veiksmīgi pievienots!", text_color="#2ecc71")
    else:
        guest_result.configure(text="Lūdzu aizpildiet visus laukus!", text_color="#e74c3c")

def handle_add_room():
    room_num = room_number_input.get()
    avail = room_avail_input.get()
    
    try:
        add_room(int(room_num), int(avail))
        room_number_input.delete(0, "end")
        room_avail_input.delete(0, "end")
        room_result.configure(text="Istaba veiksmīgi pievienota!", text_color="#2ecc71")
    except ValueError:
        room_result.configure(text="Kļūda! Numuriem jābūt cipariem.", text_color="#e74c3c")

def handle_add_staff():
    name = staff_name_input.get()
    surname = staff_surname_input.get()
    job = staff_job_input.get()
    
    if name and surname and job:
        add_staff(name, surname, job)
        staff_name_input.delete(0, "end")
        staff_surname_input.delete(0, "end")
        staff_job_input.delete(0, "end")
        staff_result.configure(text="Personāls veiksmīgi pievienots!", text_color="#2ecc71")
    else:
        staff_result.configure(text="Lūdzu aizpildiet visus laukus!", text_color="#e74c3c")

def handle_add_order():
    g_id = order_guest_id.get()
    r_num = order_room_num.get()
    finished = order_finished_input.get()
    s_id = order_staff_id.get()
    
    try:
        add_order(int(g_id), int(r_num), int(finished), int(s_id))
        order_guest_id.delete(0, "end")
        order_room_num.delete(0, "end")
        order_finished_input.delete(0, "end")
        order_staff_id.delete(0, "end")
        order_result.configure(text="Pasūtījums veiksmīgi pievienots!", text_color="#2ecc71")
    except ValueError:
        order_result.configure(text="Kļūda! ID un istabai jābūt cipariem.", text_color="#e74c3c")


# Ritināms konteiners visam saturam (iebūvēts CustomTkinter rīks)
scrollable_frame = ctk.CTkScrollableFrame(app, width=580, height=700)
scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)


# Virsraksts
header = ctk.CTkLabel(
    scrollable_frame,
    text="Welcome to our hotel database system",
    font=ctk.CTkFont(family="Arial", size=18, weight="bold")
)
header.pack(pady=(10, 20))


# --- GUEST BLOCK ---
guest_block = ctk.CTkFrame(scrollable_frame)
guest_block.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(guest_block, text="Add a Guest", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(12, 5))

ctk.CTkLabel(guest_block, text="Name").pack()
guest_name_input = ctk.CTkEntry(guest_block, width=400)
guest_name_input.pack(pady=2)

ctk.CTkLabel(guest_block, text="Surname").pack()
guest_surname_input = ctk.CTkEntry(guest_block, width=400)
guest_surname_input.pack(pady=2)

ctk.CTkButton(guest_block, text="Save", command=handle_add_guest).pack(pady=12)
guest_result = ctk.CTkLabel(guest_block, text="")
guest_result.pack(pady=(0, 10))


# --- ROOM BLOCK ---
room_block = ctk.CTkFrame(scrollable_frame)
room_block.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(room_block, text="Add a Room", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(12, 5))

ctk.CTkLabel(room_block, text="Room number").pack()
room_number_input = ctk.CTkEntry(room_block, width=400)
room_number_input.pack(pady=2)

ctk.CTkLabel(room_block, text="Availability (1 - available, 0 - not available)").pack()
room_avail_input = ctk.CTkEntry(room_block, width=400)
room_avail_input.insert(0, "1")
room_avail_input.pack(pady=2)

ctk.CTkButton(room_block, text="Save", command=handle_add_room).pack(pady=12)
room_result = ctk.CTkLabel(room_block, text="")
room_result.pack(pady=(0, 10))


# --- STAFF BLOCK ---
staff_block = ctk.CTkFrame(scrollable_frame)
staff_block.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(staff_block, text="Add a Staff Member", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(12, 5))

ctk.CTkLabel(staff_block, text="Name").pack()
staff_name_input = ctk.CTkEntry(staff_block, width=400)
staff_name_input.pack(pady=2)

ctk.CTkLabel(staff_block, text="Surname").pack()
staff_surname_input = ctk.CTkEntry(staff_block, width=400)
staff_surname_input.pack(pady=2)

ctk.CTkLabel(staff_block, text="Job").pack()
staff_job_input = ctk.CTkEntry(staff_block, width=400)
staff_job_input.pack(pady=2)

ctk.CTkButton(staff_block, text="Save", command=handle_add_staff).pack(pady=12)
staff_result = ctk.CTkLabel(staff_block, text="")
staff_result.pack(pady=(0, 10))


# --- ORDER BLOCK ---
order_block = ctk.CTkFrame(scrollable_frame)
order_block.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(order_block, text="Add an Order", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(12, 5))

ctk.CTkLabel(order_block, text="Guest ID").pack()
order_guest_id = ctk.CTkEntry(order_block, width=400)
order_guest_id.pack(pady=2)

ctk.CTkLabel(order_block, text="Room number").pack()
order_room_num = ctk.CTkEntry(order_block, width=400)
order_room_num.pack(pady=2)

ctk.CTkLabel(order_block, text="Staff ID").pack()
order_staff_id = ctk.CTkEntry(order_block, width=400)
order_staff_id.pack(pady=2)

ctk.CTkLabel(order_block, text="An order is complete (1 - yes, 0 - no)").pack()
order_finished_input = ctk.CTkEntry(order_block, width=400)
order_finished_input.insert(0, "1")
order_finished_input.pack(pady=2)

ctk.CTkButton(order_block, text="Save", command=handle_add_order).pack(pady=12)
order_result = ctk.CTkLabel(order_block, text="")
order_result.pack(pady=(0, 10))

# Palaiz aplikāciju
app.mainloop()