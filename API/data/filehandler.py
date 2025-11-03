import json
from typing import Dict, Any
import os


'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "data.json"))

def load_json() -> Dict[str, Any]: #load json data
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file: 
        return json.load(file)

def save_json(data: Dict[str, Any]) -> None: #save json data
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def add_user(user: Dict[str, Any]) -> None:
    data = load_json()
    data["Users"].append(user) #add user to users in json
    save_json(data)


def add_basket(basket: Dict[str, Any]) -> None:
    data = load_json()
    data["Baskets"].append(basket) #add basket to baskets in json
    save_json(data)

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
    data = load_json()
    userBasket = next((basket for basket in data["Baskets"] if basket["user_id"] == user_id), None)
    if userBasket is None:
        raise ValueError(f"Basket for user ID {user_id} doesn't exist")
    userBasket["items"].append(item)
    save_json(data)
