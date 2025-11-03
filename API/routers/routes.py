from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi import APIRouter
from data.filehandler import add_user, add_basket, add_item_to_basket, save_json
from data.filereader import get_user_by_id, get_basket_by_user_id, get_all_users, get_total_price_of_basket, load_json

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''

routers = APIRouter()

@routers.post('/adduser', response_model=User)
def adduser(user: User) -> User:
    try: #check if user exists already
        get_user_by_id(user.id)
        raise HTTPException(status_code=400, detail=f"User with ID {user.id} already exists")
    except ValueError: #if not add it
        add_user(user.model_dump())
        return JSONResponse(content=user.model_dump(), status_code=201)

@routers.post('/addshoppingbag')
def addshoppingbag(userid: int) -> str:
    try:
        get_user_by_id(userid) #make sure user exists
        try:
            get_basket_by_user_id(userid) #make sure user doesn't have basket
            raise HTTPException(status_code=400, detail=f"User with ID {userid} already has a basket")
        except ValueError:
            data = load_json()
            basket_id = max(b["id"] for b in data["Baskets"]) + 1
            basket = {"id": basket_id, "user_id": userid, "items": []}
            add_basket(basket)
            return JSONResponse(content=f"Basket for user with id {userid} created successfully", status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    try:
        get_user_by_id(userid) #make sure user exists
        items = get_basket_by_user_id(userid) #make sure user has basket
        
        add_item_to_basket(userid, item.model_dump())
        
        data = load_json()
        userBasket = next(b for b in data["Baskets"] if b["user_id"] == userid)
        return JSONResponse(content=userBasket, status_code=201)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.put('/updateitem', response_model=Basket)
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    try:
        get_user_by_id(userid) #make sure user exists

        data = load_json()
        basket = next((b for b in data["Baskets"] if b["user_id"] == userid), None)
        if not basket:
            raise HTTPException(status_code=404, detail=f"Basket with User ID {userid} doesn't exist")

        item = next((i for i in basket["items"] if i["item_id"] == itemid), None)
        if not item:
            raise HTTPException(status_code=404, detail=f"Item with ID {itemid} not found in basket for user with ID {userid}")

        item.update(updateItem.model_dump()) #update item

        save_json(data)

        return JSONResponse(content=basket, status_code=200)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.delete('/deleteitem',  response_model=Basket)
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        get_user_by_id(userid) #make sure user exists

        data = load_json()
        basket = next((b for b in data["Baskets"] if b["user_id"] == userid), None)
        if not basket:
            raise HTTPException(status_code=404, detail=f"Basket with User ID {userid} doesn't exist")

        basket_length = len(basket["items"])
        basket["items"] = list(item for item in basket["items"] if item["item_id"] != itemid)
        if len(basket["items"]) == basket_length:
            raise HTTPException(status_code=404, detail=f"Item with ID {itemid} not found in basket for user with ID {userid}")
        
        save_json(data)

        return JSONResponse(content=basket, status_code=200)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.get('/user', response_model=User)
def user(userid: int) -> User:
    try:
        user = get_user_by_id(userid)
        return JSONResponse(content=user, status_code=200)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@routers.get('/users', response_model=list[User])
def users() -> list[User]:
    users = get_all_users()
    return JSONResponse(content=users, status_code=200)

@routers.get('/shoppingbag', response_model=list[Item])
def shoppingbag(userid: int) -> list[Item]:
    try:
        get_user_by_id(userid)
        items = get_basket_by_user_id(userid) #make sure user has basket
        return JSONResponse(content=items, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.get('/getusertotal', response_model=float)
def getusertotal(userid: int) -> float:
    try:
        get_user_by_id(userid)
        total = get_total_price_of_basket(userid) #make sure user has basket
        return JSONResponse(content=total, status_code=200)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))



