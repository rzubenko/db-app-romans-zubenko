import sqlite3

def connect():
    database = sqlite3.connect("veikals.db")
    database.execute("PRAGMA foreign_keys = ON")
    return database

def add_client(name, surname):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO klienti (vards, uzvards) VALUES (?, ?)", (name, surname))
    database.commit()
    klienti_id = cursor.lastrowid
    database.close()
    return klienti_id

def add_product(name, price):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO preces (nosaukums, cena) VALUES (?, ?)", (name, price))
    database.commit()
    preces_id = cursor.lastrowid
    database.close()
    return preces_id

def add_order(client_id, product_id):
    database = connect()
    cursor = database.cursor()
    cursor.execute("INSERT INTO pasutijumi (klienti_id, preces_id) VALUES (?, ?)", (client_id, product_id))
    database.commit()
    order_id = cursor.lastrowid
    database.close()
    return order_id

def get_product():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT preces_id, nosaukums, cena FROM preces")
    product = cursor.fetchall()
    database.close()
    return product

def get_client():
    database = connect()
    cursor = database.cursor()
    cursor.execute("SELECT klienti_id, vards, uzvards FROM klienti")
    client = cursor.fetchall()
    database.close()
    return client

def get_orders():
    database = connect()
    cursor = database.cursor()
    cursor.execute("""
            SELECT
                pasutijumi.pasutijumi_id,
                klienti.vards,
                klienti.uzvards,
                preces.nosaukums,
                preces.cena
                        
            FROM pasutijumi
            
            JOIN klienti
                ON pasutijumi.klienti_id = klienti.klienti_id
            
            JOIN preces
                ON pasutijumi.preces_id = preces.preces_id
                
            ORDER BY pasutijumi.pasutijumi_id
        """)
    client = cursor.fetchall()
    database.close()
    return client