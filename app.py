import tkinter as tk
from funkcijas import (
    create_tables,
    add_guest,
    add_room,
    add_staff,
    add_order
)

create_tables()

# pievienojam funkcijas pie pogām
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


# galvenais logs
window = tk.Tk()
window.title("Hotel Database")
window.geometry("620x700")

# Canvas un Scrollbar izveide
main_canvas = tk.Canvas(window, borderwidth=0, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

# Piesaistām rāmi pie audekla vidusdaļas (centrēšanai)
canvas_window = main_canvas.create_window((310, 0), window=scrollable_frame, anchor="n")

def configure_canvas(event):
    main_canvas.itemconfig(canvas_window, width=event.width)
    main_canvas.coords(canvas_window, event.width / 2, 0)

main_canvas.bind("<Configure>", configure_canvas)
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Peles ritināšanas atbalsts
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)


# virsraksts (centrēts)
header = tk.Label(
    scrollable_frame,
    text="Welcome to our hotel database system",
    font=("Arial", 18, "bold")
)
header.pack(pady=15, anchor="center")


# guests
guest_block = tk.LabelFrame(scrollable_frame, text="Add a guest", padx=15, pady=10)
guest_block.pack(padx=20, pady=8, anchor="center")

tk.Label(guest_block, text="Name").pack(anchor="center")
guest_name_input = tk.Entry(guest_block, width=45, justify="center")
guest_name_input.pack(pady=2, anchor="center")

tk.Label(guest_block, text="Surname").pack(anchor="center")
guest_surname_input = tk.Entry(guest_block, width=45, justify="center")
guest_surname_input.pack(pady=2, anchor="center")

tk.Button(guest_block, text="Save", command=handle_add_guest, width=15).pack(pady=8, anchor="center")
guest_result = tk.Label(guest_block, text="", fg="green")
guest_result.pack(anchor="center")


# rooms
room_block = tk.LabelFrame(scrollable_frame, text="Add a room", padx=15, pady=10)
room_block.pack(padx=20, pady=8, anchor="center")

tk.Label(room_block, text="Room number").pack(anchor="center")
room_number_input = tk.Entry(room_block, width=45, justify="center")
room_number_input.pack(pady=2, anchor="center")

tk.Label(room_block, text="Availability (1 - available, 0 - not available)").pack(anchor="center")
room_avail_input = tk.Entry(room_block, width=45, justify="center")
room_avail_input.insert(0, "1")  # default value
room_avail_input.pack(pady=2, anchor="center")

tk.Button(room_block, text="Save", command=handle_add_room, width=15).pack(pady=8, anchor="center")
room_result = tk.Label(room_block, text="", fg="green")
room_result.pack(anchor="center")


# staff
staff_block = tk.LabelFrame(scrollable_frame, text="Add a staff member", padx=15, pady=10)
staff_block.pack(padx=20, pady=8, anchor="center")

tk.Label(staff_block, text="Name").pack(anchor="center")
staff_name_input = tk.Entry(staff_block, width=45, justify="center")
staff_name_input.pack(pady=2, anchor="center")

tk.Label(staff_block, text="Surname").pack(anchor="center")
staff_surname_input = tk.Entry(staff_block, width=45, justify="center")
staff_surname_input.pack(pady=2, anchor="center")

tk.Label(staff_block, text="Job").pack(anchor="center")
staff_job_input = tk.Entry(staff_block, width=45, justify="center")
staff_job_input.pack(pady=2, anchor="center")

tk.Button(staff_block, text="Save", command=handle_add_staff, width=15).pack(pady=8, anchor="center")
staff_result = tk.Label(staff_block, text="", fg="green")
staff_result.pack(anchor="center")


# orders
order_block = tk.LabelFrame(scrollable_frame, text="Add an order", padx=15, pady=10)
order_block.pack(padx=20, pady=8, anchor="center")

tk.Label(order_block, text="Guest ID").pack(anchor="center")
order_guest_id = tk.Entry(order_block, width=45, justify="center")
order_guest_id.pack(pady=2, anchor="center")

tk.Label(order_block, text="Room number").pack(anchor="center")
order_room_num = tk.Entry(order_block, width=45, justify="center")
order_room_num.pack(pady=2, anchor="center")  # Fixed here

tk.Label(order_block, text="Staff ID").pack(anchor="center")
order_staff_id = tk.Entry(order_block, width=45, justify="center")
order_staff_id.pack(pady=2, anchor="center")

tk.Label(order_block, text="An order is complete (1 - yes, 0 - no)").pack(anchor="center")
order_finished_input = tk.Entry(order_block, width=45, justify="center")
order_finished_input.insert(0, "1")
order_finished_input.pack(pady=2, anchor="center")

tk.Button(order_block, text="Save", command=handle_add_order, width=15).pack(pady=8, anchor="center")
order_result = tk.Label(order_block, text="", fg="green")
order_result.pack(anchor="center")

# palaiz aplikāciju
window.mainloop()