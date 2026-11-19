import sqlite3
from datetime import date, datetime

import customtkinter as ctk
from funkcijas import (
    TABLES,
    create_tables,
    add_record,
    get_records,
    get_options,
    visible_columns
)

create_tables()

#Iestatām modernu izskatu
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("Hotel Database")
app.geometry("1000x700")

app.iconbitmap("assets/images/hotel.ico")

SUCCESS_COLOR = "#2ecc71"
ERROR_COLOR = "#e74c3c"
NO_DATA = "— add records first —"

#Veidojam dropdown izskatu
DROPDOWN_STYLE = {
    "fg_color": "white",
    "button_color": "white",
    "button_hover_color": "#e5e5e5",
    "text_color": "black",
    "dropdown_fg_color": "white",
    "dropdown_hover_color": "#e5e5e5",
    "dropdown_text_color": "black",
}

forms = {}

#Palīglīdzekļi cilnām
def format_value(column, value):
    """Turns a database value into text for the table."""
    if value is None:
        return ""
    if column["type"] == "bool":
        return column["labels"][0] if value else column["labels"][1]
    if column["type"] == "real":
        return f"{float(value):.2f}"
    return value


def fill_table(frame, headers, rows):
    """Clears the frame and draws a table with the given headers and rows."""
    for widget in frame.winfo_children():
        widget.destroy()
    for col in range(20):
        frame.grid_columnconfigure(col, weight=0)

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


def refresh_view():
    table = plural_to_table[view_selector.get()]
    columns = visible_columns(table)
    rows = [
        [format_value(column, value) for column, value in zip(columns, record)]
        for record in get_records(table)
    ]
    fill_table(view_table, [column["label"] for column in columns], rows)


def refresh_dropdowns():
    """Reloads the options of every dropdown that is filled from another table."""
    for table, form in forms.items():
        for column in TABLES[table]["columns"]:
            if column["type"] != "fk":
                continue
            widget = form["inputs"][column["name"]]
            options = get_options(column["ref"]) or [NO_DATA]
            current = widget.get()
            widget.configure(values=options)
            widget.set(current if current in options else options[0])


def refresh_all():
    refresh_dropdowns()
    refresh_view()

#funkcijas datu pievienošanai
def read_form(table):
    """Reads and checks the form. Returns (values, error_message)."""
    spec = TABLES[table]
    values = {}

    for column in spec["columns"]:
        name = column["name"]
        label = column["label"]
        kind = column["type"]
        raw = forms[table]["inputs"][name].get().strip()

        if kind == "bool":
            values[name] = 1 if raw == column["labels"][0] else 0
            continue

        if kind == "fk":
            if raw == NO_DATA:
                ref_name = TABLES[column["ref"]]["plural"]
                return None, f"Kļūda! Vispirms pievienojiet ierakstu: {ref_name}."
            values[name] = int(raw.split(" - ")[0])
            continue

        if kind == "choice":
            values[name] = raw
            continue

        if raw == "":
            if column.get("optional"):
                values[name] = None
                continue
            return None, "Lūdzu aizpildiet visus laukus!"

        try:
            if kind == "int":
                values[name] = int(raw)
            elif kind == "real":
                values[name] = float(raw.replace(",", "."))
            elif kind == "date":
                datetime.strptime(raw, "%Y-%m-%d")
                values[name] = raw
            else:
                values[name] = raw
        except ValueError:
            if kind == "date":
                return None, f"Kļūda! «{label}» jābūt datumam formātā GGGG-MM-DD."
            return None, f"Kļūda! «{label}» jābūt skaitlim."

    if "date_order" in spec:
        start, end = spec["date_order"]
        if values[end] < values[start]:
            return None, "Kļūda! Izbraukšanas datums nevar būt pirms iebraukšanas datuma."

    return values, None


def reset_form(table):
    """Clears the text fields and puts dropdowns back to their first choice."""
    for column in TABLES[table]["columns"]:
        widget = forms[table]["inputs"][column["name"]]
        kind = column["type"]

        if kind in ("bool", "choice"):
            widget.set(widget.cget("values")[0])
        elif kind != "fk":
            widget.delete(0, "end")
            if kind == "date":
                widget.insert(0, date.today().isoformat())


def handle_save(table):
    result = forms[table]["result"]
    values, error = read_form(table)

    if error:
        result.configure(text=error, text_color=ERROR_COLOR)
        return

    try:
        add_record(table, values)
    except sqlite3.IntegrityError:
        result.configure(text="Kļūda! Šāds ieraksts jau pastāv.", text_color=ERROR_COLOR)
        return

    reset_form(table)
    result.configure(text=TABLES[table]["success"], text_color=SUCCESS_COLOR)
    refresh_all()


def build_form_block(parent, table):
    """Builds one 'Add a ...' block with the same look for every table."""
    spec = TABLES[table]
    article = "an" if spec["singular"][0] in "AEIOU" else "a"

    block = ctk.CTkFrame(parent)
    block.pack(fill="x", padx=10, pady=10)

    ctk.CTkLabel(
        block,
        text=f"Add {article} {spec['singular']}",
        font=ctk.CTkFont(size=15, weight="bold")
    ).pack(pady=(12, 5))

    inputs = {}
    for column in spec["columns"]:
        ctk.CTkLabel(block, text=column["label"]).pack()
        kind = column["type"]

        if kind == "bool":
            widget = ctk.CTkOptionMenu(
                block, width=400, values=list(column["labels"]), **DROPDOWN_STYLE
            )
        elif kind == "choice":
            widget = ctk.CTkOptionMenu(
                block, width=400, values=column["choices"], **DROPDOWN_STYLE
            )
        elif kind == "fk":
            widget = ctk.CTkOptionMenu(
                block, width=400, values=[NO_DATA], **DROPDOWN_STYLE
            )
        else:
            widget = ctk.CTkEntry(block, width=400)

        widget.pack(pady=2)
        inputs[column["name"]] = widget

    ctk.CTkButton(
        block, text="Save", command=lambda t=table: handle_save(t)
    ).pack(pady=12)

    result = ctk.CTkLabel(block, text="")
    result.pack(pady=(0, 10))

    forms[table] = {"inputs": inputs, "result": result}
    reset_form(table)

#cilnu dizains
tabs = ctk.CTkTabview(app)
tabs.pack(fill="both", expand=True, padx=10, pady=10)

tab_add = tabs.add("Add Data")      #oriģinālais dizains šeit
tab_view = tabs.add("View Data")

#Atjaunot cilnes katru reizi, kad lietotājs kaut ko maina
tabs.configure(command=refresh_all)

#ADD DATA TAB
#ritināms konteiners visam saturam (iebūvēts CustomTkinter rīks)
scrollable_frame = ctk.CTkScrollableFrame(tab_add, width=580, height=650)
scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Virsraksts
header = ctk.CTkLabel(
    scrollable_frame,
    text="Welcome to our hotel database system",
    font=ctk.CTkFont(family="Arial", size=18, weight="bold")
)
header.pack(pady=(10, 20))

#Viens bloks katrai tabulai
for table_name in TABLES:
    build_form_block(scrollable_frame, table_name)

#VIEW DATA TAB
plural_to_table = {spec["plural"]: name for name, spec in TABLES.items()}

ctk.CTkLabel(
    tab_view, text="Choose a table", font=ctk.CTkFont(size=15, weight="bold")
).pack(pady=(5, 5))

view_selector = ctk.CTkOptionMenu(
    tab_view,
    width=300,
    values=list(plural_to_table),
    command=lambda _value: refresh_view(),
    **DROPDOWN_STYLE
)
view_selector.pack(pady=5)

view_table = ctk.CTkScrollableFrame(tab_view)
view_table.pack(fill="both", expand=True, padx=5, pady=5)


#aizpildīt dropdown ar eksistējošo informāciju no tabulām
refresh_all()

#palaiž aplikāciju
app.mainloop()