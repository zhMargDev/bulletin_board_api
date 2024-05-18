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

""" Регистрация """
@app.post('/register')
async def registre_user(request: Request, db: Session = Depends(get_db)):
    return await user.register_(request, db)

""" Аторизация """
@app.post('/login')
async def login_user(request: Request, db: Session = Depends(get_db)):
    return await user.login_(request, db)

""" Проверка пользователя на факт авторизоанности """
@app.post('/user_authorization_check')
async def user_authorization_check(request: Request, db: Session = Depends(get_db)):
    return await user.authorization_check_(request, db)

""" Категории """
@app.get("/categories")
async def get_categories( db: Session = Depends(get_db), request: Request = None):
    return await categories.get_(request, db)
    
""" Объявления """
@app.get('/ads')
async def get_ads(db: Session = Depends(get_db), request: Request = None):
    return await ads.get_(request, db)

    """ Добавление нового объявления """
@app.post('/ads')
async def upload_files(file: UploadFile = File(...), title: str = Form(...), price: str = Form(...), 
currency: str = Form(...), description: str = Form(...), region: str = Form(...), owner_id: int = Form(...), 
owenr_type: str = Form(...), category_url: str = Form(...), subcategory_url: str = Form(...),db: Session = Depends(get_db)):
    return await ads.post_(file, title, price, currency, description, region, owner_id, category_url, subcategory_url, db)
    

""" Регионы """
@app.get('/regions')
async def get_regions(db: Session = Depends(get_db), request: Request = None):
    return await regions.get_(request, db)

""" Аккаунты пользователей """
@app.get('/user')
async def get_user(db: Session = Depends(get_db), request: Request = None):
    return await users.get_(request, db)
    