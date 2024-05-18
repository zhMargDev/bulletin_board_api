import models.config as conf

from models.models import *

from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from pathlib import Path


from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from passlib.context import CryptContext


# Создаем экземпляр FastAPI
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Фиксированная соль
fixed_salt = "2b12mIwJnkR8ltHk6HcdVL"

# Создаем соединение с базой данных
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.USERNAME}:{conf.PASSWORD}@{conf.IP_ADDRESS}:{conf.PORT}/{conf.DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем объект для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для создания хеша пароля
def get_password_hash(password: str):
    return pwd_context.hash(password, salt=fixed_salt)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

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

# Регистрация
@app.post('/register')
async def registre_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    user = db.query(User).filter(User.mail == data.get('mail')).all()

    if user:
        return JSONResponse(status_code=401, content={"Error": "Такая электронная почта уже зарегестрирована."})

    # Хешируем пароль
    hashed_password = get_password_hash(data.get('password'))

    new_user = User(
        mail=data.get('mail'),
        name=data.get('name'),
        surname=data.get('surname'),
        password=hashed_password,
        last_active=str(datetime.now()),
        created=str(datetime.now())
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Авторизация
@app.post('/login')
async def login_user(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    hashed_password = get_password_hash(data.get('password'))

    user = db.query(User).filter(and_(User.password == hashed_password, User.mail == data.get('mail'))).all()
    
    if len(user) == 0:
        return JSONResponse(status_code=401, content={"Error": "Пользователь не найден."})
    else:
        return user[0]

@app.post('/user_authorization_check')
async def user_authorization_check(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    user = db.query(User).filter(and_(User.id == data.get('id'), User.password == data.get('key'), User.mail == data.get('mail'))).all()

    if len(user) == 0:
        return JSONResponse(status_code=401, content={"Error": "Пользователь не найден."})
    else:
        return {'data': True}

@app.get("/categories")
async def get_categories( db: Session = Depends(get_db), request: Request = None):
    if request.query_params.get("url"):
        url = request.query_params.get("url")
        categories = db.query(Categories).filter(Categories.url == url).one()
        
        sub_url = request.query_params.get("sub_url")

        if sub_url == 'all' or not sub_url:
            sub_categories = db.query(SubCategories).filter(SubCategories.p_category_url == url).all()
        else:
            sub_categories = db.query(SubCategories).filter(SubCategories.url == sub_url).one()
        
    else:
        categories = db.query(Categories).all()
        sub_categories = False

    sub_url = request.query_params.get("sub_url")
    if not sub_url:
        sub_categories = db.query(SubCategories).all()


    if not categories:
        return JSONResponse(status_code=404, content={"Error": "Категории не найдены."})
    else:
        return {'categories': categories, 'sub_categories': sub_categories}

@app.get('/ads')
async def get_ads(db: Session = Depends(get_db), request: Request = None):
    id = request.query_params.get("id")

    if not id:
        return {'data':db.query(Ads).all()}
    else:
        ads = db.query(Ads.id == id).one()

        if not ads:
            return JSONResponse(status_code=404, content={"Error": "Объявление по указанному ID адресу не найден."})
        else:
            return {'ads': ads}

@app.get('/regions')
async def get_regions(db: Session = Depends(get_db), request: Request = None):
    url = request.query_params.get('url')

    if not url:
        return {'regions ':db.query(Regions).all()}
    else:
        regions = db.query(Regions.url == url).one()

        if not regions:
            return JSONResponse(status_code=404, content={"Error": "Объявление по указанному URL нету региона."})
        else:
            return {'regions': regions}

