from tkinter import *
from controller import password
import tkintermapview
# =========================================
# LOGIN FUNCTION
# =========================================

def login():

    login_name = entry_login.get()
    pass_word = entry_password.get()

    if password(login_name, pass_word):
        login_window.destroy()
        open_main_window()

# =========================================
# MAIN APPLICATION WINDOW
# =========================================

def open_main_window():

    main = Tk()

    main.title("Cleaning Company Manager")

    main.geometry("1400x800")

    # =========================================
    # LEFT SIDE
    # =========================================

    frame_left = Frame(main)

    frame_left.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky=N
    )

    # =========================================
    # RIGHT SIDE - MAP
    # =========================================

    frame_map = Frame(main)

    frame_map.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    # =========================================
    # OBJECT TYPE SELECTION
    # =========================================

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
        width=15
    )

    button_clients = Button(
        frame_left,
        text="Clients",
        width=15
    )

    button_employees = Button(
        frame_left,
        text="Employees",
        width=15
    )

    button_companies.grid(row=1, column=0, padx=5)

    button_clients.grid(row=1, column=1, padx=5)

    button_employees.grid(row=1, column=2, padx=5)

    # =========================================
    # ACTIVE OBJECT LIST
    # =========================================

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

    # =========================================
    # CRUD BUTTONS
    # =========================================

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

    # =========================================
    # DETAILS SECTION
    # =========================================

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

    # =========================================
    # MAP SECTION
    # =========================================

    map_widget = tkintermapview.TkinterMapView(
        frame_map,
        width=700,
        height=700,
        corner_radius=5
    )

    map_widget.grid(row=0, column=0)

    map_widget.set_position(52.2297, 21.0122)

    map_widget.set_zoom(6)

    # =========================================
    # LOOP
    # =========================================

    main.mainloop()

# =========================================
# LOGIN WINDOW
# =========================================

login_window = Tk()

login_window.title("Login")

login_window.geometry("300x220")

# =========================================
# TITLE
# =========================================

label_title = Label(
    login_window,
    text="Login System",
    font=("Arial", 16)
)

label_title.pack(pady=10)

# =========================================
# LOGIN
# =========================================

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

# =========================================
# PASSWORD
# =========================================

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

# =========================================
# BUTTONS
# =========================================

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

# =========================================
# LOOP
# =========================================

login_window.mainloop()