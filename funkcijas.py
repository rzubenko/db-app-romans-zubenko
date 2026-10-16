import sqlite3

def connect():
    database = sqlite3.connect("hotel.db")
    # Enable foreign keys support in SQLite
    database.execute("PRAGMA foreign_keys = ON")
    return database

# --- TABLE CREATION ---
def create_tables():
    database = connect()
    cursor = database.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guests(
            guest_id INTEGER PRIMARY KEY,
            guest_name TEXT NOT NULL,
            guest_surname TEXT NOT NULL)
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms(
            room_number INTEGER PRIMARY KEY,
            room_availability BOOLEAN DEFAULT 1)
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff(
            staff_id INTEGER PRIMARY KEY,
            staff_name TEXT NOT NULL,
            staff_surname TEXT NOT NULL,
            staff_job TEXT NOT NULL)
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER PRIMARY KEY,
            guest_id INTEGER,
            room_number INTEGER,
            order_finished BOOLEAN DEFAULT 1,
            staff_id INTEGER,
            
            FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
            FOREIGN KEY (room_number) REFERENCES rooms(room_number),
            FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
        )
    """)
    
    database.commit()
    database.close()

# --- ADD FUNCTIONS ---
def add_guest(name, surname):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT OR IGNORE INTO guests (guest_name, guest_surname) VALUES (?, ?)", (name, surname))
    database.commit()
    guest_id = cursor.lastrowid
    database.close()
    return guest_id

def add_room(room_number, availability=1):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT OR IGNORE INTO rooms (room_number, room_availability) VALUES (?, ?)", (room_number, availability))
    database.commit()
    database.close()

def add_staff(name, surname, job):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT OR IGNORE INTO staff (staff_name, staff_surname, staff_job) VALUES (?, ?, ?)", (name, surname, job))
    database.commit()
    staff_id = cursor.lastrowid
    database.close()
    return staff_id

def add_order(guest_id, room_number, order_finished, staff_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO orders (guest_id, room_number, order_finished, staff_id) 
        VALUES (?, ?, ?, ?)
    """, (guest_id, room_number, order_finished, staff_id))
    database.commit()
    order_id = cursor.lastrowid
    database.close()
    return order_id

# --- GET / SELECT FUNCTIONS ---
def get_guests():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT guest_id, guest_name, guest_surname FROM guests")
    guests = cursor.fetchall()
    database.close()
    return guests

def get_rooms():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT room_number, room_availability FROM rooms")
    rooms = cursor.fetchall()
    database.close()
    return rooms

def get_staff():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT staff_id, staff_name, staff_surname, staff_job FROM staff")
    staff = cursor.fetchall()
    database.close()
    return staff

def get_orders():
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
        SELECT
            orders.order_id,
            guests.guest_name,
            guests.guest_surname,
            rooms.room_number,
            orders.order_finished,
            staff.staff_name,
            staff.staff_surname
        FROM orders
        JOIN guests ON orders.guest_id = guests.guest_id
        JOIN rooms ON orders.room_number = rooms.room_number
        JOIN staff ON orders.staff_id = staff.staff_id
        ORDER BY orders.order_id
    """)
    orders = cursor.fetchall()
    database.close()
    return orders

# --- TEST / EXAMPLE EXECUTION ---
if __name__ == "__main__":
    # 1. Initialize tables
    create_tables()
    
    # 2. Add sample data
    add_guest("Romans", "Zubenko")
    add_room(1, 1)
    add_staff("Antons", "Mahno", "Cleaner")
    add_order(guest_id=1, room_number=1, order_finished=1, staff_id=1)
    
    # 3. Print results to verify
    print("\nKLIENTI:")
    for g in get_guests():
        print(g)
        
    print("\nISTABAS:")
    for r in get_rooms():
        print(r)
        
    print("\nPERSONĀLS:")
    for s in get_staff():
        print(s)
        
    print("\nPASŪTĪJUMI:")
    for o in get_orders():
        print(o)