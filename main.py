import models.config as conf
import methods.users as users
import methods.ads as ads
import methods.categories as categories
import methods.regions as regions

from pathlib import Path
from typing import List
from models.models import *
from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем экземпляр FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Создаем соединение с базой данных
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.USERNAME}:{conf.PASSWORD}@{conf.IP_ADDRESS}:{conf.PORT}/{conf.DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()

# Отправка картинки по названию
@app.get("/images/{folder}/{img}")
async def get_image(img: str, folder: str, request: Request):
    image_path = Path(f"imgs/{folder}/{img}")
    if not image_path.is_file():
        return JSONResponse(status_code=404, content={"Error": "Картинка не найдена."})
    
    return FileResponse(image_path)


""" Пользователи """
@app.get('/user')
async def get_user(db: Session = Depends(get_db), request: Request = None):
    return await users.get_(request, db)

    """ Регистрация """
@app.post('/register')
async def registre_user(request: Request, db: Session = Depends(get_db)):
    return await user.register_(request, db)

    """ Аторизация """
@app.post('/login')
async def login_user(request: Request, db: Session = Depends(get_db)):
    return await user.login_(request, db)

    """ Изменение данных пользователя """
@app.put('/user')
async def change_user(id: int = Form(...), db: Session = Depends(get_db), file: UploadFile = File(None), mail: str = Form(None), password: str = Form(None),
name: str = Form(None), surname: str = Form(None), sex: str = Form(None), age: int = Form(None), phone: str = Form(None), rating: str = Form(None), 
last_active: str = Form(None), about: str = Form(None)):
    return await users.put_(id=id, db=db, file=file, mail=mail, password=password, name=name, surname=surname, sex=sex, age=age, phone=phone, rating=rating, last_active=last_active, about=about)
    
    """ Удаление пользователя """
@app.delete('/user')
async def delete_user(db: Session = Depends(get_db), request: Request = None):
    return await users.delete_(response, db)


    """ Проверка пользователя на факт авторизоанности """
@app.post('/user_authorization_check')
async def user_authorization_check(request: Request, db: Session = Depends(get_db)):
    return await user.authorization_check_(request, db)

""" Категории """
@app.get("/categories")
async def get_categories( db: Session = Depends(get_db), request: Request = None):
    return await categories.get_(request, db)

    """ Добавление категории """
    """ Изменение категории """
    """ Удаление категории """


    
""" Объявления """
@app.get('/ads')
async def get_ads(db: Session = Depends(get_db), request: Request = None):
    return await ads.get_(request, db)

    """ Добавление нового объявления """
@app.post('/ads')
async def add_new_ad(file: UploadFile = File(...), title: str = Form(...), price: str = Form(...), 
currency: str = Form(...), description: str = Form(...), region: str = Form(...), owner_id: int = Form(...), 
owenr_type: str = Form(...), category_url: str = Form(...), subcategory_url: str = Form(...),db: Session = Depends(get_db)):
    return await ads.post_(file=file, title=title, price=price, currency=currency, description=description, region=region, owner_id=owner_id, category_url=category_url, subcategory_url=subcategory_url, db=db)

    """ Изменение значений объявления """
@app.put('/ads')
async def update_ad(id: int = Form(...), db: Session = Depends(get_db), file: UploadFile = File(None), title: str = Form(None), price: str = Form(None), 
currency: str = Form(None), description: str = Form(None), region: str = Form(None), owner_id: int = Form(None), 
owenr_type: str = Form(None), category_url: str = Form(None), subcategory_url: str = Form(None)):
    return await ads.put_(id=id, db=db, file=file, title=title, price=price, currency=currency, description=description, region=region, owner_id=owner_id, category_url=category_url, subcategory_url=subcategory_url)

    """ Изменение статуса объявления """
@app.put('/ads/change_status')
async def change_status(db: Session = Depends(get_db), request: Request = None):
    return await ads.change_status(db, request)

    """ Удаление объявления """
@app.delete('/ads')
async def delete_ad(db: Session = Depends(get_db), request: Request = None):
    return await ads.delete_(db, request)

    """ Добавление в избранные """
@app.post('/ads/add_to_favorite')
async def add_to_favorites(db: Session = Depends(get_db), request: Request = None):
    return await ads.add_to_favorites(db, request)

    """ Удаление из избранных """
@app.delete('/ads/favorite')
async def delete_favorite_ad(db: Session = Depends(get_db), request: Request = None):
    return await ads.remove_favorite(db, request)



""" Регионы """
@app.get('/regions')
async def get_regions(db: Session = Depends(get_db), request: Request = None):
    return await regions.get_(request, db)

    """ Добавление ругиона """
    """ Изменение ругиона """
    """ Удаление ругиона """


    """ Магазины """
    """ Получение данных магазинов """
    """ Регистрация магазина """
    """ Проверка на авторизованность в магазин """
    """ Аторизация в магазин """
    """ Изменение данных магазина """
    """ Удаление данных магазина """
    