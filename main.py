from tkinter import *
from tkinter import messagebox
import tkintermapview
from model import get_database, companies, clients, employees, save_data, load_data
from controller import *
import random

current_mode = "companies"
selected_object = None
mode_label = None
markers = []
filtered_objects = []

def center_poland():
    global selected_object

    selected_object = None

    map_widget.set_position(52.0693, 19.4803)
    map_widget.set_zoom(6)

    listbox_objects.selection_clear(0, END)

    company_info_label.config(text="")
    employees_listbox.delete(0, END)
    clients_listbox.delete(0, END)

    new_object()
    refresh()

def company_exists(company_id):
    for company in companies:
        if company["id"] == company_id:
            return True
    return False

def generate_coordinates(city, object_type, object_id):
    lat, lon = get_coordinates(city)

    if lat is None:
        return None, None

    if object_type == "company":
        return lat, lon

    random.seed(f"{object_type}{object_id}")

    if object_type == "employee":
        lat += random.uniform(-0.002, 0.002)
        lon += random.uniform(-0.002, 0.002)

    elif object_type == "client":
        lat += random.uniform(-0.006, 0.006)
        lon += random.uniform(-0.006, 0.006)

    return round(lat, 6), round(lon, 6)

def get_company(company_id):
    for company in companies:
        if company["id"] == company_id:
            return company
    return None

def get_company_clients(company_id):
    return [client for client in clients if client["company_id"] == company_id]

def get_company_employees(company_id):
    return [employee for employee in employees if employee["company_id"] == company_id]

def new_object():
    global selected_object
    selected_object = None
    entry_name.delete(0, END)
    entry_company_id.delete(0, END)
    entry_position.delete(0, END)
    entry_city.delete(0, END)
    if current_mode == "companies":
        entry_company_id.config(state="readonly")
        entry_position.config(state="normal")
        entry_position.delete(0, END)
        entry_position.config(state="disabled")

    elif current_mode == "clients":
        entry_company_id.config(state="normal")
        entry_position.config(state="normal")
        entry_position.delete(0, END)
        entry_position.config(state="disabled")

    elif current_mode == "employees":
        entry_company_id.config(state="normal")
        entry_position.config(state="normal")

def refresh():
    global markers

    database = get_database(current_mode)

    markers_database = database

    if current_mode == "companies" and selected_object is not None:
        company_id = selected_object["id"]

        markers_database = [
            selected_object,
            *[e for e in employees if e["company_id"] == company_id],
            *[c for c in clients if c["company_id"] == company_id]
        ]

    filter_list()

    for marker in markers:
        marker.delete()

    markers.clear()

    for obj in markers_database:

        lat = obj["latitude"]
        lon = obj["longitude"]

        if "position" in obj:
            label = f"👤 {obj['name']}"

        elif "company_id" in obj:
            label = f"📋 {obj['name']}"

        else:
            label = f"🏢 {obj['name']}"

        markers.append(
            map_widget.set_marker(
                lat,
                lon,
                text=label
            )
        )

    stats_label.config(
        text=
        f"Firmy: {len(companies)}\n"
        f"Klienci: {len(clients)}\n"
        f"Pracownicy: {len(employees)}"
    )

def change_mode(mode):
    global current_mode

    current_mode = mode

    search_entry.delete(0, END)

    refresh()
    new_object()

def filter_list(event=None):
    global filtered_objects

    if "search_entry" not in globals():
        return

    search_text = search_entry.get().lower()

    database = get_database(current_mode)

    filtered_objects = []

    listbox_objects.delete(0, END)

    for obj in database:
        text = f'{obj["id"]} | {obj["name"]} | {obj["city"]}'

        if search_text in text.lower():
            filtered_objects.append(obj)
            listbox_objects.insert(END, text)

def load_selected(event=None):
    global selected_object

    selected = listbox_objects.curselection()

    if not selected:
        return

    index = selected[0]
    selected_object = filtered_objects[index]

    entry_name.delete(0, END)

    entry_company_id.config(state="normal")
    entry_company_id.delete(0, END)

    entry_position.config(state="normal")
    entry_position.delete(0, END)

    entry_city.delete(0, END)

    entry_name.insert(0, selected_object.get("name", ""))
    entry_city.insert(0, selected_object.get("city", ""))

    if current_mode == "companies":
        entry_company_id.insert(0, selected_object["id"])
        entry_company_id.config(state="readonly")

        entry_position.config(state="disabled")

    elif current_mode == "clients":
        entry_company_id.insert(0, selected_object["company_id"])

        entry_position.config(state="disabled")

    elif current_mode == "employees":
        entry_company_id.insert(0, selected_object["company_id"])

        entry_position.insert(
            0,
            selected_object.get("position", "")
        )

    if current_mode == "companies":
        company_id = selected_object["id"]

        company_clients = get_company_clients(company_id)
        company_employees = get_company_employees(company_id)

        employees_listbox.delete(0, END)
        clients_listbox.delete(0, END)

        for employee in company_employees:
            employees_listbox.insert(
                END,
                employee["name"]
            )

        for client in company_clients:
            clients_listbox.insert(
                END,
                client["name"]
            )

        company_info_label.config(
            text=
            f"Company ID: {company_id}\n"
            f"Name: {selected_object['name']}\n"
            f"City: {selected_object['city']}\n\n"
            f"Employees: {len(company_employees)}\n"
            f"Clients: {len(company_clients)}"
        )

    else:
        employees_listbox.delete(0, END)
        clients_listbox.delete(0, END)

        company = get_company(selected_object["company_id"])

        if company:

            if current_mode == "employees":
                company_info_label.config(
                    text=
                    f"Employee ID: {selected_object['id']}\n"
                    f"Position: {selected_object['position']}\n\n"
                    f"Company:\n"
                    f"{company['name']}\n"
                    f"{company['city']}"
                )

            else:
                company_info_label.config(
                    text=
                    f"Client ID: {selected_object['id']}\n\n"
                    f"Company:\n"
                    f"{company['name']}\n"
                    f"{company['city']}"
                )

        else:
            company_info_label.config(
                text="Company not found"
            )

    map_widget.set_position(
        selected_object["latitude"],
        selected_object["longitude"]
    )

    map_widget.set_zoom(12)

    refresh()

def add_object_gui():
    database = get_database(current_mode)

    if not entry_name.get().strip():
        messagebox.showerror(
            "Error",
            "Name cannot be empty"
        )
        return

    if not entry_city.get().strip():
        messagebox.showerror(
            "Error",
            "City cannot be empty"
        )
        return

    obj = {
        "name": entry_name.get(),
        "city": entry_city.get()
    }

    if current_mode != "companies":
        try:
            obj["company_id"] = int(entry_company_id.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Company ID must be a number"
            )
            return

        if not company_exists(obj["company_id"]):
            messagebox.showerror(
                "Error",
                "Company ID does not exist"
            )
            return

    if current_mode == "employees":

        if not entry_position.get().strip():
            messagebox.showerror(
                "Error",
                "Position cannot be empty"
            )
            return

        obj["position"] = entry_position.get()

    new_id = get_next_id(database)

    if current_mode == "companies":
        lat, lon = generate_coordinates(
            obj["city"],
            "company",
            new_id
        )

    elif current_mode == "employees":
        lat, lon = generate_coordinates(
            obj["city"],
            "employee",
            new_id
        )

    else:
        lat, lon = generate_coordinates(
            obj["city"],
            "client",
            new_id
        )

    if lat is None:
        messagebox.showerror(
            "Error",
            "City not found in database"
        )
        return

    obj["latitude"] = lat
    obj["longitude"] = lon

    add_object(database, obj)

    save_data()

    new_object()

    refresh()

def edit_object_gui():
    global selected_object

    if selected_object is None:
        return

    if not entry_name.get().strip():
        messagebox.showerror(
            "Error",
            "Name cannot be empty"
        )
        return

    if not entry_city.get().strip():
        messagebox.showerror(
            "Error",
            "City cannot be empty"
        )
        return

    selected_object["name"] = entry_name.get()
    selected_object["city"] = entry_city.get()

    if current_mode != "companies":
        try:
            company_id = int(entry_company_id.get())
        except ValueError:
            messagebox.showerror(
                "Error",
                "Company ID must be a number"
            )
            return

        if not company_exists(company_id):
            messagebox.showerror(
                "Error",
                "Company ID does not exist"
            )
            return

        selected_object["company_id"] = company_id

    if current_mode == "employees":

        if not entry_position.get().strip():
            messagebox.showerror(
                "Error",
                "Position cannot be empty"
            )
            return

        selected_object["position"] = entry_position.get()

    if current_mode == "companies":
        lat, lon = generate_coordinates(
            selected_object["city"],
            "company",
            selected_object["id"]
        )

    elif current_mode == "employees":
        lat, lon = generate_coordinates(
            selected_object["city"],
            "employee",
            selected_object["id"]
        )

    else:
        lat, lon = generate_coordinates(
            selected_object["city"],
            "client",
            selected_object["id"]
        )

    if lat is None:
        messagebox.showerror(
            "Error",
            "City not found in database"
        )
        return

    selected_object["latitude"] = lat
    selected_object["longitude"] = lon

    save_data()

    refresh()

def delete_company(company_id):
    companies[:] = [c for c in companies if c["id"] != company_id]
    clients[:] = [c for c in clients if c["company_id"] != company_id]
    employees[:] = [e for e in employees if e["company_id"] != company_id]

def delete_object_gui():
    global selected_object

    if selected_object is None:
        return
    answer = messagebox.askyesno(
        "Delete",
        "Are you sure?"
    )

    if not answer:
        return
    if current_mode == "companies":
        delete_company(selected_object["id"])
    else:
        database = get_database(current_mode)
        database.remove(selected_object)

    selected_object = None

    save_data()
    refresh()

def login():
    if check_login(entry_login.get(), entry_password.get()):
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Błędny login lub hasło")

def open_main_window():
    global listbox_objects
    global map_widget
    global entry_name
    global entry_company_id
    global entry_position
    global entry_city
    global stats_label
    global company_info_label
    global employees_listbox
    global clients_listbox
    global search_entry

    BG_COLOR = "#f4f6f8"
    PANEL_COLOR = "#ffffff"
    BUTTON_COLOR = "#4f81bd"
    BUTTON_ACTIVE = "#3d6fa8"
    BUTTON_TEXT = "white"

    window = Tk()
    window.title("Cleaning Company Manager")
    window.geometry("1200x700")
    window.configure(bg=BG_COLOR)

    top_frame = Frame(window, bg=BG_COLOR)
    top_frame.pack(fill=X, pady=5)

    Button(
        top_frame,
        text="🏢 Firmy",
        width=15,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_ACTIVE,
        command=lambda: change_mode("companies")
    ).pack(side=LEFT, padx=5)

    Button(
        top_frame,
        text="📋 Klienci",
        width=15,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_ACTIVE,
        command=lambda: change_mode("clients")
    ).pack(side=LEFT, padx=5)

    Button(
        top_frame,
        text="👤 Pracownicy",
        width=15,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_ACTIVE,
        command=lambda: change_mode("employees")
    ).pack(side=LEFT, padx=5)

    Button(
        top_frame,
        text="🏠 Home",
        width=15,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_ACTIVE,
        command=center_poland
    ).pack(side=LEFT, padx=5)

    center_frame = Frame(window, bg=BG_COLOR)
    center_frame.pack(fill=BOTH, expand=True)

    left_frame = Frame(center_frame, bg=BG_COLOR)
    left_frame.pack(side=LEFT, fill=Y)

    Label(
        left_frame,
        text="🔍 Wyszukaj",
        bg=BG_COLOR,
        font=("Arial", 10, "bold")
    ).pack(anchor=W, padx=5)

    search_entry = Entry(
        left_frame,
        width=40
    )

    search_entry.pack(
        padx=5,
        pady=(0, 5)
    )

    search_entry.bind(
        "<KeyRelease>",
        filter_list
    )

    listbox_objects = Listbox(
        left_frame,
        width=45,
        font=("Arial", 10)
    )

    listbox_objects.pack(
        fill=Y,
        expand=True,
        padx=5
    )

    listbox_objects.bind(
        "<<ListboxSelect>>",
        load_selected
    )

    map_widget = tkintermapview.TkinterMapView(center_frame)
    map_widget.pack(side=LEFT, fill=BOTH, expand=True)

    stats_frame = Frame(
        center_frame,
        bg=PANEL_COLOR,
        bd=1,
        relief="solid",
        width=220
    )
    stats_frame.pack(side=RIGHT, fill=Y, padx=10)

    Label(
        stats_frame,
        text="📊 Statystyki",
        bg=PANEL_COLOR,
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    stats_label = Label(
        stats_frame,
        justify=LEFT,
        anchor="nw",
        bg=PANEL_COLOR,
        font=("Arial", 10)
    )
    stats_label.pack(fill=X)

    Label(
        stats_frame,
        text="🏢 Szczegóły",
        bg=PANEL_COLOR,
        font=("Arial", 12, "bold")
    ).pack(pady=(20, 10))

    company_info_label = Label(
        stats_frame,
        justify=LEFT,
        anchor="nw",
        bg=PANEL_COLOR,
        font=("Arial", 10)
    )
    company_info_label.pack(fill=X)

    Label(
        stats_frame,
        text="👤 Pracownicy",
        bg=PANEL_COLOR,
        font=("Arial", 10, "bold")
    ).pack(pady=(15, 5))

    employees_listbox = Listbox(
        stats_frame,
        height=6,
        width=25
    )
    employees_listbox.pack(fill=X, padx=5)

    Label(
        stats_frame,
        text="📋 Klienci",
        bg=PANEL_COLOR,
        font=("Arial", 10, "bold")
    ).pack(pady=(15, 5))

    clients_listbox = Listbox(
        stats_frame,
        height=6,
        width=25
    )
    clients_listbox.pack(fill=X, padx=5)

    map_widget.set_position(52.0693, 19.4803)
    map_widget.set_zoom(6)

    form_frame = Frame(
        window,
        bg=BG_COLOR
    )
    form_frame.pack(fill=X, padx=10, pady=10)

    Label(form_frame, text="Nazwa", bg=BG_COLOR).grid(row=0, column=0, sticky=W)
    Label(form_frame, text="Identyfikator firmy", bg=BG_COLOR).grid(row=1, column=0, sticky=W)
    Label(form_frame, text="Stanowisko", bg=BG_COLOR).grid(row=2, column=0, sticky=W)
    Label(form_frame, text="Miasto", bg=BG_COLOR).grid(row=3, column=0, sticky=W)

    entry_name = Entry(form_frame, width=30)
    entry_company_id = Entry(form_frame, width=30)
    entry_position = Entry(form_frame, width=30)
    entry_city = Entry(form_frame, width=30)

    entry_name.grid(row=0, column=1, padx=5)
    entry_company_id.grid(row=1, column=1, padx=5)
    entry_position.grid(row=2, column=1, padx=5)
    entry_city.grid(row=3, column=1, padx=5)

    Button(
        form_frame,
        text="Nowy",
        width=15,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_ACTIVE,
        command=new_object
    ).grid(row=4, column=0, pady=10)

    Button(
        form_frame,
        text="Dodaj",
        width=15,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_ACTIVE,
        command=add_object_gui
    ).grid(row=4, column=1, pady=10)

    Button(
        form_frame,
        text="Edytuj",
        width=15,
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT,
        activebackground=BUTTON_ACTIVE,
        command=edit_object_gui
    ).grid(row=4, column=2, pady=10)

    Button(
        form_frame,
        text="Usuń",
        width=15,
        bg="#b94a48",
        fg="white",
        activebackground="#953735",
        command=delete_object_gui
    ).grid(row=4, column=3, pady=10)

    refresh()
    window.mainloop()

def open_login_window():
    global login_window
    global entry_login
    global entry_password

    load_data()
    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("300x180")

    Label(login_window, text="Login").pack(pady=5)
    entry_login = Entry(login_window)
    entry_login.pack()

    Label(login_window, text="Hasło").pack(pady=5)
    entry_password = Entry(login_window, show="*")
    entry_password.pack()

    Button(login_window, text="Zaloguj", width=15, command=login).pack(pady=15)
    login_window.mainloop()

open_login_window()