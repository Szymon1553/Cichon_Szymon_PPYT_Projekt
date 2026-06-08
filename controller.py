from model import users, cities

def check_login(login, password):
    for user in users:
        if user["login"] == login and user["password"] == password:
            return True
    return False

def get_next_id(database):
    if not database:
        return 1
    return max(obj["id"] for obj in database) + 1

def add_object(database, object_data):
    object_data["id"] = get_next_id(database)
    database.append(object_data)

def update_object(database, index, object_data):
    object_data["id"] = database[index]["id"]
    database[index] = object_data

def delete_object(database, index):
    database.pop(index)

def dms_to_decimal(value):
    value = value.replace("°", " ").replace("'", " ")
    degree, minute, direction = value.split()
    decimal = float(degree) + float(minute) / 60
    if direction in ["W", "S"]:
        decimal *= -1
    return round(decimal, 6)

def get_coordinates(city):
    city = city.strip().lower()
    for item in cities:
        if item["name"].lower() == city:
            lat = dms_to_decimal(item["lat"])
            lon = dms_to_decimal(item["lon"])
            return lat, lon
    return None, None