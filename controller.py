import requests
from bs4 import BeautifulSoup
import folium
from model import users

def password(login, pass_word):
    for n in users:
        if n["login"] == login:
            user_password = n["password"]
    if pass_word == user_password:
        return True
    else:
        return False

def read_data(users_data: list) -> None:
    for user in users_data:
        print(
            f"Twój znajomy {user['username']} z miejscowości {user['location']} opublikował "
            f"{user['posts']} wiadomości. Ostatnia wiadomość: {user['usermessage'][-1]}")


def add_user(users_data: list) -> None:
    name = input('Podaj imię: ')
    place = input('Podaj miejscowość: ')
    post_num = int(input('Ile masz postów: '))
    mes_info = input('Przekaż wiadomość: ').split()
    users_data.append({"username": name, "location": place, "posts": post_num, "usermessage": mes_info})


def delete_user(users_data: list) -> None:
    name = input("Podaj imię użytkownika do usunięcia: ")
    for user in users_data:
        if user["username"] == name:
            users_data.remove(user)


def update_user(users_data: list)->None:
    name = input("Podaj imię użytkownika do zmiany: ")
    for user in users_data:
        if user["username"] == name:
            user["username"] = input('Podaj imię: ')
            user["location"] = input('Podaj miejscowość: ')
            user["posts"] = int(input('Ile masz postów: '))
            user["usermessage"] = input('Przekaż wiadomość: ').split()


def get_mapa(users_data: list):
    m = folium.Map([52, 21], zoom_start=12)
    for user in users_data:
        folium.Marker(
            location=get_coordinates(user["location"]),
            tooltip="Click me!",
            popup=user["username"],
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

    m.save("mapa.html")

def get_coordinates(location: str) -> list:
    url = f"https://pl.wikipedia.org/wiki/{location}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response_html = BeautifulSoup(response.text, 'html.parser')
    response_html_latitude = float(response_html.select('.latitude')[1].text.replace(",", "."))
    response_html_longitude = float(response_html.select('.longitude')[1].text.replace(",", "."))
    return [response_html_latitude, response_html_longitude]
