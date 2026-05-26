# =========================================
# CLASSES
# =========================================

class User:

    def __init__(
        self,
        id,
        login,
        password
    ):

        self.id = id
        self.login = login
        self.password = password


class Company:

    def __init__(
        self,
        id,
        name,
        city,
        latitude,
        longitude
    ):

        self.id = id
        self.name = name
        self.city = city
        self.latitude = latitude
        self.longitude = longitude


class Client:

    def __init__(
        self,
        id,
        name,
        company_id,
        city,
        latitude,
        longitude
    ):

        self.id = id
        self.name = name
        self.company_id = company_id
        self.city = city
        self.latitude = latitude
        self.longitude = longitude


class Employee:

    def __init__(
        self,
        id,
        name,
        company_id,
        position,
        city,
        latitude,
        longitude
    ):

        self.id = id
        self.name = name
        self.company_id = company_id
        self.position = position
        self.city = city
        self.latitude = latitude
        self.longitude = longitude


# =========================================
# USERS
# =========================================

users = [

    User(
        1,
        "admin",
        "admin123"
    ),

    User(
        2,
        "szymon",
        "ppyt2025"
    )
]

# =========================================
# COMPANIES
# =========================================

companies = [

    Company(
        1,
        "CleanHouse",
        "Warszawa",
        52.2297,
        21.0122
    ),

    Company(
        2,
        "FreshCleaning",
        "Kraków",
        50.0647,
        19.9450
    ),

    Company(
        3,
        "EcoWash",
        "Gdańsk",
        54.3520,
        18.6466
    )
]

# =========================================
# CLIENTS
# =========================================

clients = [

    Client(
        1,
        "Jan Kowalski",
        1,
        "Warszawa",
        52.2400,
        21.0000
    ),

    Client(
        2,
        "Anna Nowak",
        1,
        "Warszawa",
        52.2500,
        21.0300
    ),

    Client(
        3,
        "Piotr Zieliński",
        2,
        "Kraków",
        50.0600,
        19.9500
    ),

    Client(
        4,
        "Maria Wiśniewska",
        3,
        "Gdańsk",
        54.3600,
        18.6400
    )
]

# =========================================
# EMPLOYEES
# =========================================

employees = [

    Employee(
        1,
        "Tomasz Wiśniewski",
        1,
        "Cleaner",
        "Warszawa",
        52.2200,
        21.0200
    ),

    Employee(
        2,
        "Karolina Mazur",
        1,
        "Driver",
        "Warszawa",
        52.2100,
        21.0100
    ),

    Employee(
        3,
        "Michał Kaczmarek",
        2,
        "Cleaner",
        "Kraków",
        50.0500,
        19.9400
    ),

    Employee(
        4,
        "Natalia Lewandowska",
        3,
        "Manager",
        "Gdańsk",
        54.3400,
        18.6500
    )
]