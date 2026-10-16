from funkcijas import(
    add_client,
    add_product,
    add_order,
    get_product,
    get_client,
    get_orders
)

while True:
    print("\nMaxima")
    print("1 - Pievienot klientu")
    print("2 - Pievienot preci")
    print("3 - Pievienot pasutijumu")
    print("4 - Paradit pasutijumu")

    choice = input("Izvele: ")

    if choice == "1":
        name = input("Klienta vards")
        surname = input("Klienta uzvards")
        client_id = add_client(name, surname)
        print("Klients pievienots. ID:", client_id)


    elif choice == "2":
        name = input("Preces vards")
        price = input("Precces cena")
        product_id = add_product(name, price)
        print("Prece pievienota. ID:", product_id)


    elif choice == "3":
        print("\nKlientu saraksts:")
        for client in get_client():
            print(client)

        print("\nPrecu saraksts:")
        for product in get_product():
            print(product)

        client = input("Klienta ID: ")
        product = input("Precces ID: ")
        order_id = add_order(client, price)
        print("Pasutijums pievienots. ID:", order_id)

    
    elif choice == "4":
        print("\nPasutijumu saraksts:")
        for order in get_orders():
            print(order)

    if choice == "0":
        break