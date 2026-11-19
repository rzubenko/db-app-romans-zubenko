import sqlite3

#jaunais datubāzes fails, ar 10 tabulām
DB_FILE = "hotel_system.db"


def connect():
    database = sqlite3.connect(DB_FILE)
    # ieslēdzam foreign keys support in SQLite
    database.execute("PRAGMA foreign_keys = ON")
    return database

def col(name, label, kind="text", **options):
    return {"name": name, "label": label, "type": kind, **options}


TABLES = {
    # 1
    "departments": {
        "singular": "Department",
        "plural": "Departments",
        "success": "Nodaļa veiksmīgi pievienota!",
        "pk": "department_id",
        "display": "{t}.department_name",
        "columns": [
            col("department_name", "Name", unique=True),
        ],
    },
    # 2
    "room_types": {
        "singular": "Room Type",
        "plural": "Room Types",
        "success": "Istabas tips veiksmīgi pievienots!",
        "pk": "type_id",
        "display": "{t}.type_name",
        "columns": [
            col("type_name", "Name", unique=True),
            col("price_per_night", "Price per night (€)", "real"),
            col("max_guests", "Max guests", "int"),
        ],
    },
    # 3
    "guests": {
        "singular": "Guest",
        "plural": "Guests",
        "success": "Klients veiksmīgi pievienots!",
        "pk": "guest_id",
        "display": "{t}.guest_name || ' ' || {t}.guest_surname",
        "columns": [
            col("guest_name", "Name"),
            col("guest_surname", "Surname"),
            col("guest_phone", "Phone (optional)", optional=True),
            col("guest_email", "E-mail (optional)", optional=True),
        ],
    },
    # 4
    "services": {
        "singular": "Service",
        "plural": "Services",
        "success": "Pakalpojums veiksmīgi pievienots!",
        "pk": "service_id",
        "display": "{t}.service_name",
        "columns": [
            col("service_name", "Name", unique=True),
            col("service_price", "Price (€)", "real"),
        ],
    },
    # 5  (room number ir primary key, jo lietotājs pats to ievada)
    "rooms": {
        "singular": "Room",
        "plural": "Rooms",
        "success": "Istaba veiksmīgi pievienota!",
        "pk": "room_number",
        "auto_pk": False,
        "display": "'Floor ' || {t}.floor",
        "columns": [
            col("room_number", "Room number", "int"),
            col("room_type_id", "Room type", "fk", ref="room_types"),
            col("floor", "Floor", "int"),
            col("room_availability", "Availability", "bool",
                labels=("Available", "Not available")),
        ],
    },
    # 6
    "staff": {
        "singular": "Staff Member",
        "plural": "Staff",
        "success": "Personāls veiksmīgi pievienots!",
        "pk": "staff_id",
        "display": "{t}.staff_name || ' ' || {t}.staff_surname",
        "columns": [
            col("staff_name", "Name"),
            col("staff_surname", "Surname"),
            col("staff_job", "Job"),
            col("department_id", "Department", "fk", ref="departments"),
        ],
    },
    # 7
    "bookings": {
        "singular": "Booking",
        "plural": "Bookings",
        "success": "Rezervācija veiksmīgi pievienota!",
        "pk": "booking_id",
        "display": "'Room ' || {t}.room_number || ', ' || {t}.check_in",
        "date_order": ("check_in", "check_out"),
        "columns": [
            col("guest_id", "Guest", "fk", ref="guests"),
            col("room_number", "Room", "fk", ref="rooms"),
            col("check_in", "Check-in date (YYYY-MM-DD)", "date"),
            col("check_out", "Check-out date (YYYY-MM-DD)", "date"),
            col("booking_status", "Status", "choice",
                choices=["Confirmed", "Checked in", "Checked out", "Cancelled"]),
        ],
    },
    # 8
    "orders": {
        "singular": "Order",
        "plural": "Orders",
        "success": "Pasūtījums veiksmīgi pievienots!",
        "pk": "order_id",
        "columns": [
            col("guest_id", "Guest", "fk", ref="guests"),
            col("room_number", "Room", "fk", ref="rooms"),
            col("service_id", "Service", "fk", ref="services"),
            col("staff_id", "Staff member", "fk", ref="staff"),
            col("order_finished", "An order is complete", "bool",
                labels=("Yes", "No")),
        ],
    },
    # 9
    "payments": {
        "singular": "Payment",
        "plural": "Payments",
        "success": "Maksājums veiksmīgi pievienots!",
        "pk": "payment_id",
        "columns": [
            col("booking_id", "Booking", "fk", ref="bookings"),
            col("payment_amount", "Amount (€)", "real"),
            col("payment_method", "Method", "choice",
                choices=["Card", "Cash", "Bank transfer"]),
            col("payment_date", "Date (YYYY-MM-DD)", "date"),
        ],
    },
    # 10
    "reviews": {
        "singular": "Review",
        "plural": "Reviews",
        "success": "Atsauksme veiksmīgi pievienota!",
        "pk": "review_id",
        "columns": [
            col("guest_id", "Guest", "fk", ref="guests"),
            col("review_rating", "Rating (5 is best)", "choice",
                choices=["5", "4", "3", "2", "1"], sql="INTEGER"),
            col("review_comment", "Comment (optional)", optional=True),
        ],
    },
    # 11
    "maintenance": {
        "singular": "Maintenance Request",
        "plural": "Maintenance",
        "success": "Remonta pieprasījums veiksmīgi pievienots!",
        "pk": "maintenance_id",
        "columns": [
            col("room_number", "Room", "fk", ref="rooms"),
            col("staff_id", "Assigned staff member", "fk", ref="staff"),
            col("maintenance_description", "Description"),
            col("maintenance_resolved", "Resolved", "bool",
                labels=("Yes", "No")),
        ],
    },
}

SQL_TYPES = {
    "text": "TEXT",
    "int": "INTEGER",
    "real": "REAL",
    "date": "TEXT",
    "bool": "INTEGER",
    "choice": "TEXT",
    "fk": "INTEGER",
}


#izveidojam tabulas
def create_tables():
    database = connect()
    cursor = database.cursor()

    for table, spec in TABLES.items():
        lines = []

        if spec.get("auto_pk", True):
            lines.append(f"{spec['pk']} INTEGER PRIMARY KEY")

        for column in spec["columns"]:
            line = f"{column['name']} {column.get('sql', SQL_TYPES[column['type']])}"
            if column["name"] == spec["pk"]:
                line += " PRIMARY KEY"
            elif not column.get("optional"):
                line += " NOT NULL"
            if column.get("unique"):
                line += " UNIQUE"
            lines.append(line)

        for column in spec["columns"]:
            if column["type"] == "fk":
                ref = column["ref"]
                lines.append(
                    f"FOREIGN KEY ({column['name']}) "
                    f"REFERENCES {ref}({TABLES[ref]['pk']})"
                )

        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table} (\n    "
            + ",\n    ".join(lines)
            + "\n)"
        )

    database.commit()
    database.close()


#funkcijas
def add_record(table, values):
    """Inserts one record. `values` is a dict {column_name: value}.
    Raises sqlite3.IntegrityError if the record breaks a rule
    (duplicate key, unique name, bad foreign key)."""
    if table not in TABLES:
        raise ValueError(f"Unknown table: {table}")

    names = list(values)
    marks = ", ".join("?" for _ in names)

    database = connect()
    try:
        cursor = database.cursor()
        cursor.execute(
            f"INSERT INTO {table} ({', '.join(names)}) VALUES ({marks})",
            [values[name] for name in names]
        )
        database.commit()
        return cursor.lastrowid
    finally:
        database.close()


def visible_columns(table):
    """Columns shown when viewing a table (auto IDs get an 'ID' column)."""
    spec = TABLES[table]
    columns = list(spec["columns"])
    if spec.get("auto_pk", True):
        columns.insert(0, {"name": spec["pk"], "label": "ID", "type": "int"})
    return columns


def get_records(table):
    """All rows of a table. Foreign keys are replaced with readable names
    (for example a guest ID becomes the guest's name and surname)."""
    spec = TABLES[table]
    selects = []
    joins = []

    for column in visible_columns(table):
        if column["type"] == "fk":
            ref = column["ref"]
            alias = f"j_{column['name']}"
            selects.append(TABLES[ref]["display"].format(t=alias))
            joins.append(
                f"LEFT JOIN {ref} AS {alias} "
                f"ON t.{column['name']} = {alias}.{TABLES[ref]['pk']}"
            )
        else:
            selects.append(f"t.{column['name']}")

    database = connect()
    cursor = database.cursor()
    cursor.execute(
        f"SELECT {', '.join(selects)} FROM {table} AS t "
        f"{' '.join(joins)} ORDER BY t.{spec['pk']}"
    )
    records = cursor.fetchall()
    database.close()
    return records


def get_options(table):
    """Dropdown entries for a table, like '3 - Anna Berzina'."""
    spec = TABLES[table]
    display = spec["display"].format(t="t")

    database = connect()
    cursor = database.cursor()
    cursor.execute(
        f"SELECT t.{spec['pk']}, {display} FROM {table} AS t "
        f"ORDER BY t.{spec['pk']}"
    )
    rows = cursor.fetchall()
    database.close()
    return [f"{record_id} - {label}" for record_id, label in rows]