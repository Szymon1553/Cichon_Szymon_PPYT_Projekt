import requests
from bs4 import BeautifulSoup
from model import users

def password(login, pass_word):
    for user in users:
        if user.login == login:
            if user.password == pass_word:
                return True

    return False

def add_object(objects_data: list, object_class) -> None:
    object_data = vars(objects_data[0]).keys()
    values = []
    for attribute in object_data:
        if attribute == "id":
            values.append(len(objects_data) + 1)
        elif attribute in ["latitude", "longitude"]:
            values.append(float(input(f"{attribute}: ")))
        elif attribute == "company_id":
            values.append(int(input(f"{attribute}: ")))
        else:
            values.append(input(f"{attribute}: "))
    new_object = object_class(*values)
    objects_data.append(new_object)


def delete_object(objects_data: list) -> None:
    object_id = int(input("Object ID to delete: "))
    for obj in objects_data:
        if obj.id == object_id:
            objects_data.remove(obj)
            break


def update_object(objects_data: list) -> None:
    object_id = int(input("Object ID to update: "))
    for obj in objects_data:
        if obj.id == object_id:
            for attribute in vars(obj):
                if attribute == "id":
                    continue
                current_value = getattr(obj, attribute)
                new_value = input(
                    f"{attribute} ({current_value}): "
                )
                if attribute in ["latitude", "longitude"]:
                    setattr(obj, attribute, float(new_value))
                elif attribute == "company_id":
                    setattr(obj, attribute, int(new_value))
                else:
                    setattr(obj, attribute, new_value)
            break


def get_coordinates(location: str) -> list:
    url = f"https://pl.wikipedia.org/wiki/{location}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response_html = BeautifulSoup(response.text, 'html.parser')
    response_html_latitude = float(response_html.select('.latitude')[1].text.replace(",", "."))
    response_html_longitude = float(response_html.select('.longitude')[1].text.replace(",", "."))
    return [response_html_latitude, response_html_longitude]
