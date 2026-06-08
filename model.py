users = [
    {"id": 1, "login": "admin", "password": "admin123"},
    {"id": 2, "login": "szymon", "password": "ppyt2025"}
]

companies = [
    {"id": 1, "name": "CleanHouse", "city": "Warszawa"},
    {"id": 2, "name": "FreshCleaning", "city": "Kraków"},
    {"id": 3, "name": "EcoWash", "city": "Gdańsk"}
]

clients = [
    {"id": 1, "name": "Jan Kowalski", "company_id": 1, "city": "Warszawa"},
    {"id": 2, "name": "Anna Nowak", "company_id": 1, "city": "Warszawa"},
    {"id": 3, "name": "Piotr Zieliński", "company_id": 2, "city": "Kraków"}
]

employees = [
    {"id": 1, "name": "Tomasz Wiśniewski", "company_id": 1, "position": "Cleaner", "city": "Warszawa"},
    {"id": 2, "name": "Karolina Mazur", "company_id": 1, "position": "Driver", "city": "Warszawa"},
    {"id": 3, "name": "Michał Kaczmarek", "company_id": 2, "position": "Cleaner", "city": "Kraków"}
]


def get_database(mode):
    if mode == "companies":
        return companies
    if mode == "clients":
        return clients
    if mode == "employees":
        return employees
    return []


def load_cities():
    cities = []
    try:
        with open("Miejscowosci.txt", encoding="utf-8") as file:
            next(file)
            for line in file:
                if not line.strip():
                    continue
                parts = line.split()
                if len(parts) < 3:
                    continue
                lat = parts[-1]
                lon = parts[-2]
                name = " ".join(parts[:-2])
                cities.append({
                    "name": name,
                    "lon": lon,
                    "lat": lat
                })
    except:
        pass
    return cities
cities = load_cities()