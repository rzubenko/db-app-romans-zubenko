import customtkinter as ctk
from funkcijas import (
    create_tables,
    add_guest,
    add_room,
    add_staff,
    add_order,
    get_guests,
    get_rooms,
    get_staff,
    get_orders
)

create_tables()

# Iestatām modernu izskatu
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Hotel Database")
app.geometry("650x750")

app.iconbitmap("assets/images/hotel.ico")


# ---------------------------------------------------------------
# HELPERS FOR THE VIEW TABS
# ---------------------------------------------------------------
def fill_table(frame, headers, rows):
    """Clears the frame and draws a table with the given headers and rows."""
    for widget in frame.winfo_children():
        widget.destroy()

    for col, title in enumerate(headers):
        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=col, padx=10, pady=(5, 8), sticky="w")
        frame.grid_columnconfigure(col, weight=1)

    if not rows:
        ctk.CTkLabel(frame, text="No records yet.").grid(
            row=1, column=0, columnspan=len(headers), pady=20
        )
        return

    for r, row in enumerate(rows, start=1):
        for c, value in enumerate(row):
            ctk.CTkLabel(frame, text=str(value)).grid(
                row=r, column=c, padx=10, pady=3, sticky="w"
            )


def yes_no(value):
    return "Yes" if value else "No"


def make_view_tab(parent, title):
    """Creates the title + scrollable table area for a view tab."""
    ctk.CTkLabel(
        parent, text=title, font=ctk.CTkFont(size=15, weight="bold")
    ).pack(pady=(5, 5))
    table = ctk.CTkScrollableFrame(parent)
    table.pack(fill="both", expand=True, padx=5, pady=5)
    return table


def refresh_all():
    fill_table(guests_table, ["ID", "Name", "Surname"], get_guests())

    fill_table(
        rooms_table,
        ["Room number", "Available"],
        [(num, yes_no(avail)) for num, avail in get_rooms()]
    )

    fill_table(staff_table, ["ID", "Name", "Surname", "Job"], get_staff())

    fill_table(
        orders_table,
        ["Order ID", "Guest", "Room", "Finished", "Staff member"],
        [
            (oid, f"{gname} {gsurname}", room, yes_no(done), f"{sname} {ssurname}")
            for oid, gname, gsurname, room, done, sname, ssurname in get_orders()
        ]
    )


# ---------------------------------------------------------------
# FUNKCIJAS DATU PIEVIENOŠANAI
# (they use the input widgets, so they must live in this file)
# ---------------------------------------------------------------
def handle_add_guest():
    name = guest_name_input.get()
    surname = guest_surname_input.get()

    if name and surname:
        add_guest(name, surname)
        guest_name_input.delete(0, "end")
        guest_surname_input.delete(0, "end")
        guest_result.configure(text="Klients veiksmīgi pievienots!", text_color="#2ecc71")
        refresh_all()
    else:
        guest_result.configure(text="Lūdzu aizpildiet visus laukus!", text_color="#e74c3c")

def handle_add_room():
    room_num = room_number_input.get()
    avail = 1 if room_avail_input.get() == "Available" else 0

    try:
        add_room(int(room_num), avail)
        room_number_input.delete(0, "end")
        room_avail_input.set("Available")
        room_result.configure(text="Istaba veiksmīgi pievienota!", text_color="#2ecc71")
        refresh_all()
    except ValueError:
        room_result.configure(text="Kļūda! Istabas numuram jābūt skaitlim.", text_color="#e74c3c")

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
        refresh_all()
    else:
        staff_result.configure(text="Lūdzu aizpildiet visus laukus!", text_color="#e74c3c")

def handle_add_order():
    g_id = order_guest_id.get()
    r_num = order_room_num.get()
    finished = 1 if order_finished_input.get() == "Yes" else 0
    s_id = order_staff_id.get()

    try:
        add_order(int(g_id), int(r_num), finished, int(s_id))
        order_guest_id.delete(0, "end")
        order_room_num.delete(0, "end")
        order_finished_input.set("Yes")
        order_staff_id.delete(0, "end")
        order_result.configure(text="Pasūtījums veiksmīgi pievienots!", text_color="#2ecc71")
        refresh_all()
    except ValueError:
        order_result.configure(text="Kļūda! ID un istabai jābūt cipariem.", text_color="#e74c3c")


# ---------------------------------------------------------------
# TABS AT THE TOP
# ---------------------------------------------------------------
tabs = ctk.CTkTabview(app)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

tab_add = tabs.add("Add Data")      # the original design lives here
tab_guests = tabs.add("Guests")
tab_rooms = tabs.add("Rooms")
tab_staff = tabs.add("Staff")
tab_orders = tabs.add("Orders")

guests_table = make_view_tab(tab_guests, "All Guests")
rooms_table = make_view_tab(tab_rooms, "All Rooms")
staff_table = make_view_tab(tab_staff, "All Staff Members")
orders_table = make_view_tab(tab_orders, "All Orders")

# Refresh the tables every time the user switches tabs
tabs.configure(command=refresh_all)

# Ritināms konteiners visam saturam (iebūvēts CustomTkinter rīks)
scrollable_frame = ctk.CTkScrollableFrame(tab_add, width=580, height=650)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)


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

ctk.CTkLabel(room_block, text="Availability").pack()
room_avail_input = ctk.CTkOptionMenu(room_block, width=400, values=["Available", "Not available"])
room_avail_input.set("Available")
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

ctk.CTkLabel(order_block, text="An order is complete").pack()
order_finished_input = ctk.CTkOptionMenu(order_block, width=400, values=["Yes", "No"])
order_finished_input.set("Yes")
order_finished_input.pack(pady=2)

ctk.CTkButton(order_block, text="Save", command=handle_add_order).pack(pady=12)
order_result = ctk.CTkLabel(order_block, text="")
order_result.pack(pady=(0, 10))


# Fill the tables with existing data on startup
refresh_all()

# Palaiz aplikāciju
app.mainloop()