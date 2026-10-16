import sqlite3

# 1. Pieslēgties pie datu bāzes
database = sqlite3.connect("hotel.db")
cursor = database.cursor()

# 2.1. Izveidot tabulu ar klientiem
cursor.execute("""
    CREATE TABLE IF NOT EXISTS guests(
        guest_id INTEGER PRIMARY KEY,
        guest_name TEXT NOT NULL,
        guest_surname TEXT NOT NULL)
""")

# 2.2. Izveidot tabulu ar istabām
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

# 2.3. Izveidot tabulu ar pasūtījumiem (orders)
# Fixed: Added guest_id, removed trailing comma
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        order_id INTEGER PRIMARY KEY,
        guest_id INTEGER,
        room_number INTEGER,
        order_finished BOOLEAN DEFAULT 1,
        staff_id INTEGER,
                
        FOREIGN KEY (guest_id)
            REFERENCES guests(guest_id),
        FOREIGN KEY (room_number)
            REFERENCES rooms(room_number),
        FOREIGN KEY (staff_id)
            REFERENCES staff(staff_id)
    )
""")

# 3. Ievietot datus tabulās
cursor.execute("""
INSERT OR IGNORE INTO guests(guest_id, guest_name, guest_surname)
    VALUES(1, 'Romans', 'Zubenko')
""")

cursor.execute("""
INSERT OR IGNORE INTO rooms(room_number, room_availability)
    VALUES(1, 1)
""")

cursor.execute("""
INSERT OR IGNORE INTO staff(staff_id, staff_name, staff_surname, staff_job)
    VALUES(1, 'Antons', 'Mahno', 'Cleaner')
""")

# Fixed: Changed table name from 'pasutijumi' to 'orders' and used guest_id
cursor.execute("""
INSERT OR IGNORE INTO orders (order_id, guest_id, room_number, order_finished, staff_id)
    VALUES(1, 1, 1, 1, 1)
""")

# 4. Saņemt datus - Klienti
cursor.execute("""
    SELECT *
    FROM guests
""")

guests_list = cursor.fetchall()
print("\nguests")
for g in guests_list:
    print(g)

# 5. Saņemt datus - Pasūtījumi (Fixed joins and included staff table)
cursor.execute("""
SELECT
    guests.guest_name,
    rooms.room_number,
    staff.staff_id
    FROM orders
    JOIN guests
        ON orders.guest_id = guests.guest_id
    JOIN rooms
        ON orders.room_number = rooms.room_number 
    JOIN staff
        ON orders.staff_id = staff.staff_id
""")

pasutijumi = cursor.fetchall()
print("\norders")
for p in pasutijumi:
    print(p)

# Saglabāt un aizvērt
database.commit()
database.close()