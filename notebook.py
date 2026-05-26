from tkinter import *
from controller import password
from model import companies, clients, employees

import tkintermapview


def login():

    login_name = entry_login.get()

    pass_word = entry_password.get()

    if password(login_name, pass_word):

        login_window.destroy()

        open_main_window()


def show_companies():

    current_mode.set("companies")

    listbox_objects.delete(0, END)

    map_widget.delete_all_marker()

    for idx, company in enumerate(companies):

        listbox_objects.insert(
            idx,
            company.name
        )

        map_widget.set_marker(
            company.latitude,
            company.longitude,
            text=company.name
        )


def show_clients():

    current_mode.set("clients")

    listbox_objects.delete(0, END)

    map_widget.delete_all_marker()

    for idx, client in enumerate(clients):

        listbox_objects.insert(
            idx,
            client.name
        )

        map_widget.set_marker(
            client.latitude,
            client.longitude,
            text=client.name
        )


def show_employees():

    current_mode.set("employees")

    listbox_objects.delete(0, END)

    map_widget.delete_all_marker()

    for idx, employee in enumerate(employees):

        listbox_objects.insert(
            idx,
            employee.name
        )

        map_widget.set_marker(
            employee.latitude,
            employee.longitude,
            text=employee.name
        )


def open_main_window():

    global listbox_objects
    global map_widget
    global current_mode

    main = Tk()

    main.title("Cleaning Company Manager")

    main.geometry("1400x800")

    current_mode = StringVar()

    frame_left = Frame(main)

    frame_left.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky=N
    )

    frame_map = Frame(main)

    frame_map.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    label_section = Label(
        frame_left,
        text="Select category",
        font=("Arial", 14)
    )

    label_section.grid(
        row=0,
        column=0,
        columnspan=3,
        pady=10
    )

    button_companies = Button(
        frame_left,
        text="Companies",
        width=15,
        command=show_companies
    )

    button_clients = Button(
        frame_left,
        text="Clients",
        width=15,
        command=show_clients
    )

    button_employees = Button(
        frame_left,
        text="Employees",
        width=15,
        command=show_employees
    )

    button_companies.grid(row=1, column=0, padx=5)

    button_clients.grid(row=1, column=1, padx=5)

    button_employees.grid(row=1, column=2, padx=5)

    label_list = Label(
        frame_left,
        text="Objects list",
        font=("Arial", 12)
    )

    label_list.grid(
        row=2,
        column=0,
        columnspan=3,
        pady=10
    )

    listbox_objects = Listbox(
        frame_left,
        width=50,
        height=20
    )

    listbox_objects.grid(
        row=3,
        column=0,
        columnspan=3
    )

    button_show = Button(
        frame_left,
        text="Show",
        width=12
    )

    button_add = Button(
        frame_left,
        text="Add",
        width=12
    )

    button_edit = Button(
        frame_left,
        text="Edit",
        width=12
    )

    button_delete = Button(
        frame_left,
        text="Delete",
        width=12
    )

    button_show.grid(row=4, column=0, pady=10)

    button_add.grid(row=4, column=1, pady=10)

    button_edit.grid(row=5, column=0, pady=5)

    button_delete.grid(row=5, column=1, pady=5)

    frame_form = Frame(frame_left)

    frame_form.grid(
        row=6,
        column=0,
        columnspan=3,
        pady=20,
        sticky=W
    )

    label_form = Label(
        frame_form,
        text="Input module",
        font=("Arial", 12)
    )

    label_form.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=10
    )

    # NAME

    label_name = Label(
        frame_form,
        text="Name"
    )

    label_name.grid(
        row=1,
        column=0,
        sticky=W
    )

    entry_name = Entry(
        frame_form,
        width=25
    )

    entry_name.grid(
        row=1,
        column=1,
        pady=2
    )

    # COMPANY ID

    label_company_id = Label(
        frame_form,
        text="Company ID"
    )

    label_company_id.grid(
        row=2,
        column=0,
        sticky=W
    )

    entry_company_id = Entry(
        frame_form,
        width=25
    )

    entry_company_id.grid(
        row=2,
        column=1,
        pady=2
    )

    # POSITION

    label_position = Label(
        frame_form,
        text="Position"
    )

    label_position.grid(
        row=3,
        column=0,
        sticky=W
    )

    entry_position = Entry(
        frame_form,
        width=25
    )

    entry_position.grid(
        row=3,
        column=1,
        pady=2
    )

    # CITY

    label_city = Label(
        frame_form,
        text="City"
    )

    label_city.grid(
        row=4,
        column=0,
        sticky=W
    )

    entry_city = Entry(
        frame_form,
        width=25
    )

    entry_city.grid(
        row=4,
        column=1,
        pady=2
    )

    # LATITUDE

    label_latitude = Label(
        frame_form,
        text="Latitude"
    )

    label_latitude.grid(
        row=5,
        column=0,
        sticky=W
    )

    entry_latitude = Entry(
        frame_form,
        width=25
    )

    entry_latitude.grid(
        row=5,
        column=1,
        pady=2
    )

    # LONGITUDE

    label_longitude = Label(
        frame_form,
        text="Longitude"
    )

    label_longitude.grid(
        row=6,
        column=0,
        sticky=W
    )

    entry_longitude = Entry(
        frame_form,
        width=25
    )

    entry_longitude.grid(
        row=6,
        column=1,
        pady=2
    )

    frame_details = Frame(frame_left)

    frame_details.grid(
        row=6,
        column=0,
        columnspan=3,
        pady=20
    )

    label_details = Label(
        frame_details,
        text="Object details",
        font=("Arial", 12)
    )

    label_details.grid(row=0, column=0)

    map_widget = tkintermapview.TkinterMapView(
        frame_map,
        width=700,
        height=700,
        corner_radius=5
    )

    map_widget.grid(row=0, column=0)

    map_widget.set_position(52.2297, 21.0122)

    map_widget.set_zoom(6)

    main.mainloop()


def open_login_window():

    global login_window
    global entry_login
    global entry_password

    login_window = Tk()

    login_window.title("Login")

    login_window.geometry("300x220")

    label_title = Label(
        login_window,
        text="Zaloguj się",
        font=("Arial", 16)
    )

    label_title.pack(pady=10)

    label_login = Label(
        login_window,
        text="Login"
    )

    label_login.pack()

    entry_login = Entry(
        login_window,
        width=25
    )

    entry_login.pack(pady=5)

    label_password = Label(
        login_window,
        text="Password"
    )

    label_password.pack()

    entry_password = Entry(
        login_window,
        width=25,
        show="*"
    )

    entry_password.pack(pady=5)

    button_confirm = Button(
        login_window,
        text="Confirm",
        width=15,
        command=login
    )

    button_confirm.pack(pady=10)

    button_exit = Button(
        login_window,
        text="Exit",
        width=15,
        command=login_window.destroy
    )

    button_exit.pack()

    login_window.mainloop()


open_login_window()