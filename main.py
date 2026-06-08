from tkinter import *
from tkinter import messagebox
import tkintermapview
from model import get_database, companies, clients, employees
from controller import *

current_mode = "companies"
selected_object = None
markers = []
mode_label = None

def center_poland():
    map_widget.set_position(52.0693, 19.4803)
    map_widget.set_zoom(6)

def company_exists(company_id):
    for company in companies:
        if company["id"] == company_id:
            return True
    return False

def get_company_clients_count(company_id):
    return len([client for client in clients if client["company_id"] == company_id])

def get_company_employees_count(company_id):
    return len([employee for employee in employees if employee["company_id"] == company_id])

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
    listbox_objects.delete(0, END)
    for marker in markers:
        marker.delete()
    markers.clear()
    for obj in database:
        text = f'{obj["id"]} | {obj["name"]} | {obj["city"]}'
        listbox_objects.insert(END, text)
        lat, lon = get_coordinates(obj["city"])
        if lat is not None:
            markers.append(map_widget.set_marker(lat, lon, text=obj["name"]))

    stats_label.config(
        text=
        f"Companies: {len(companies)}\n"
        f"Clients: {len(clients)}\n"
        f"Employees: {len(employees)}"
    )

def show_companies():
    global current_mode
    current_mode = "companies"
    refresh()
    new_object()

def show_clients():
    global current_mode
    current_mode = "clients"
    refresh()
    new_object()

def show_employees():
    global current_mode
    current_mode = "employees"
    refresh()
    new_object()

def load_selected(event=None):
    global selected_object
    entry_name.delete(0, END)

    entry_company_id.config(state="normal")
    entry_company_id.delete(0, END)

    entry_position.config(state="normal")
    entry_position.delete(0, END)

    entry_city.delete(0, END)
    selected = listbox_objects.curselection()

    if not selected:
        return

    index = selected[0]
    database = get_database(current_mode)

    selected_object = database[index]

    entry_name.delete(0, END)
    entry_company_id.delete(0, END)
    entry_position.delete(0, END)
    entry_city.delete(0, END)

    entry_name.insert(0, selected_object.get("name", ""))
    entry_city.insert(0, selected_object.get("city", ""))

    if current_mode == "companies":
        entry_company_id.config(state="normal")
        entry_company_id.insert(0, selected_object["id"])
        entry_company_id.config(state="readonly")

        entry_position.config(state="normal")
        entry_position.delete(0, END)
        entry_position.config(state="disabled")

    elif current_mode == "clients":
        entry_company_id.config(state="normal")
        entry_company_id.insert(0, selected_object["company_id"])

        entry_position.config(state="normal")
        entry_position.delete(0, END)
        entry_position.config(state="disabled")

    elif current_mode == "employees":
        entry_company_id.config(state="normal")
        entry_company_id.insert(0, selected_object["company_id"])

        entry_position.config(state="normal")
        entry_position.insert(0, selected_object.get("position", ""))

    if current_mode == "companies":
        company_id = selected_object["id"]

        clients_count = get_company_clients_count(company_id)
        employees_count = get_company_employees_count(company_id)

        company_info_label.config(
            text=
            f"Employees: {employees_count}\n"
            f"Clients: {clients_count}"
        )
    else:
        company_info_label.config(text="")
    lat, lon = get_coordinates(selected_object["city"])

    if lat is not None:
        map_widget.set_position(lat, lon)
        map_widget.set_zoom(12)

def add_object_gui():
    database = get_database(current_mode)
    obj = {"name": entry_name.get(), "city": entry_city.get()}
    if current_mode != "companies":
        try:
            obj["company_id"] = int(entry_company_id.get())
        except:
            messagebox.showerror("Error", "Company ID must be a number")
            return
    if current_mode != "companies":
        try:
            obj["company_id"] = int(entry_company_id.get())
        except:
            messagebox.showerror("Error", "Company ID must be a number")
            return
        if not company_exists(obj["company_id"]):
            messagebox.showerror("Error", "Company ID does not exist")
            return

    if current_mode == "employees":
        obj["position"] = entry_position.get()

    add_object(database, obj)

    refresh()

def edit_object_gui():
    global selected_object

    if selected_object is None:
        return

    selected_object["name"] = entry_name.get()
    selected_object["city"] = entry_city.get()

    if current_mode != "companies":
        try:
            company_id = int(entry_company_id.get())
        except:
            messagebox.showerror("Error", "Company ID must be a number")
            return
        if not company_exists(company_id):
            messagebox.showerror("Error", "Company ID does not exist")
            return

        selected_object["company_id"] = company_id

    if current_mode == "employees":
        selected_object["position"] = entry_position.get()

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

    refresh()

def login():
    if check_login(entry_login.get(), entry_password.get()):
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Wrong login or password")

def open_main_window():
    global listbox_objects
    global map_widget
    global entry_name
    global entry_company_id
    global entry_position
    global entry_city
    global stats_label
    global company_info_label

    window = Tk()
    window.title("Cleaning Company Manager")
    window.geometry("1200x700")

    top_frame = Frame(window)
    top_frame.pack(fill=X, pady=5)

    Button(top_frame, text="Companies", width=15, command=show_companies).pack(side=LEFT, padx=5)
    Button(top_frame, text="Clients", width=15, command=show_clients).pack(side=LEFT, padx=5)
    Button(top_frame, text="Employees", width=15, command=show_employees).pack(side=LEFT, padx=5)
    Button(top_frame, text="Home", width=15, command=center_poland).pack(side=LEFT, padx=5)

    center_frame = Frame(window)
    center_frame.pack(fill=BOTH, expand=True)

    listbox_objects = Listbox(center_frame, width=45)
    listbox_objects.pack(side=LEFT, fill=Y)
    listbox_objects.bind("<<ListboxSelect>>", load_selected)

    map_widget = tkintermapview.TkinterMapView(center_frame)
    map_widget.pack(side=LEFT, fill=BOTH, expand=True)
    stats_frame = Frame(center_frame, width=180)
    stats_frame.pack(side=RIGHT, fill=Y, padx=10)

    Label(stats_frame, text="Statistics", font=("Arial", 12, "bold")).pack(pady=10)

    stats_label = Label(
        stats_frame,
        justify=LEFT,
        anchor="nw",
        font=("Arial", 10)
    )

    stats_label.pack(fill=X)

    Label(stats_frame, text="Company Details", font=("Arial", 12, "bold")).pack(pady=(20, 10))

    company_info_label = Label(
        stats_frame,
        justify=LEFT,
        anchor="nw",
        font=("Arial", 10)
    )

    company_info_label.pack(fill=X)
    map_widget.set_position(52.0693, 19.4803)
    map_widget.set_zoom(6)

    form_frame = Frame(window)
    form_frame.pack(fill=X, padx=10, pady=10)

    Label(form_frame, text="Name").grid(row=0, column=0, sticky=W)
    Label(form_frame, text="Company ID").grid(row=1, column=0, sticky=W)
    Label(form_frame, text="Position").grid(row=2, column=0, sticky=W)
    Label(form_frame, text="City").grid(row=3, column=0, sticky=W)

    entry_name = Entry(form_frame, width=30)
    entry_company_id = Entry(form_frame, width=30)
    entry_position = Entry(form_frame, width=30)
    entry_city = Entry(form_frame, width=30)

    entry_name.grid(row=0, column=1, padx=5)
    entry_company_id.grid(row=1, column=1, padx=5)
    entry_position.grid(row=2, column=1, padx=5)
    entry_city.grid(row=3, column=1, padx=5)

    Button(form_frame, text="New", width=15, command=new_object).grid(row=4, column=0, pady=10)
    Button(form_frame, text="Add", width=15, command=add_object_gui).grid(row=4, column=1, pady=10)
    Button(form_frame, text="Edit", width=15, command=edit_object_gui).grid(row=4, column=2, pady=10)
    Button(form_frame, text="Delete", width=15, command=delete_object_gui).grid(row=4, column=3, pady=10)

    refresh()
    window.mainloop()

def open_login_window():
    global login_window
    global entry_login
    global entry_password

    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("300x180")

    Label(login_window, text="Login").pack(pady=5)
    entry_login = Entry(login_window)
    entry_login.pack()

    Label(login_window, text="Password").pack(pady=5)
    entry_password = Entry(login_window, show="*")
    entry_password.pack()

    Button(login_window, text="Login", width=15, command=login).pack(pady=15)
    login_window.mainloop()

open_login_window()