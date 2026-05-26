
from controller import password

my_login = input("podaj login: ")
my_password = input("podaj password: ")
value = password(my_login, my_password)
if value == True:
    print("properly logged in")
else:
    print("wrong login or password")