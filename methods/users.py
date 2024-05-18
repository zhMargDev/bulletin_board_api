import uuid

from pathlib import Path
from models.models import User, Base
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import desc
from datetime import datetime
from passlib.context import CryptContext
from fastapi.responses import JSONResponse


# Фиксированная соль
fixed_salt = "2b12mIwJnkR8ltHk6HcdVL"

# Создаем объект для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для создания хеша пароля
def get_password_hash(password: str):
    return pwd_context.hash(password, salt=fixed_salt)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Получение пользователей
async def get_(request, db):
    user_id = request.query_params.get('id')
    limit = request.query_params.get('limit')

    if not user_id:
        # Получение данных пользователя кроме пароля
        if not limit: users = db.query(User).options(load_only(User.id, User.name, User.mail, User.surname, 
                        User.sex, User.age, User.phone, User.rating, User.last_active, User.about, 
                        User.created)).order_by(desc(User.id)).all()
        else: users = db.query(User).options(load_only(User.id, User.name, User.mail, User.surname, 
                        User.sex, User.age, User.phone, User.rating, User.last_active, User.about, 
                        User.created)).order_by(desc(User.id)).limit(limit).all()
    else:
        users = db.query(User).filter(User.id == user_id).options(load_only(User.id, User.name, User.mail, User.surname, 
                        User.sex, User.age, User.phone, 
                        User.rating, User.last_active, User.about, User.created)).order_by(desc(User.id)).one()
            
    if not users: return JSONResponse(status_code=404, content={'Error': 'Пользователи не были найдены.'})
    else: return {'user': users}

# Изменение данных пользоателя
async def put_(id, db, file=None, mail=None, password=None, name=None, surname=None, sex=None, age=None, phone=None, rating=None, last_active=None, about=None):
    if not id: return JSONResponse(status_code=404, content={"Error": "ID не указан."})
    
    try:
        user = db.query(User).filter(User.id == id).first()
        
        if file is not None:
            SAVE_DIR = Path("imgs/users")
            # Проверяем, что директория для сохранения существует, иначе создаем ее
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Генерируем уникальное имя файла
            unique_filename = str(uuid.uuid4()) + Path(file.filename).suffix
            # Полный путь для сохранения файла
            file_path = SAVE_DIR / unique_filename
            # Сохраняем файл
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            user.avatar = f"/images/users/{unique_filename}"

        if mail is not None: user.mail = mail
        if password is not None:
            hashed_password = get_password_hash(password)
            user.password = hashed_password
        if name is not None: user.name = name
        if surname is not None: user.surname = surname
        if sex is not None: user.sex = sex
        if age is not None: user.age = age
        if phone is not None: user.phone = phone
        if rating is not None: user.rating = rating
        if last_active is not None: user.last_active = last_active
        if about is not None: user.about = about
            
        db.commit()
        db.refresh(user)

        return user
    except Exception as e:
        return JSONResponse(status_code=401, content={"Error": str(e)})

# Удаление пользователя
async def delete_(response, db):
    data = await request.json()
    user_id = data.get('id')

    try:
        # Находим объявление по его id
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            # Удаляем найденное объявление
            db.delete(user)
            db.commit()
            return {"message": "Пользователь успешно удалено."}
        else:
            return {"error": "Ползователя не найдено."}
    except IntegrityError as e:
        db.rollback()
        return {"error": str(e)}

# Регистрация
async def register_(request, db):
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
async def login_(request, db):
    data = await request.json()

    hashed_password = get_password_hash(data.get('password'))

    user = db.query(User).filter(and_(User.password == hashed_password, User.mail == data.get('mail'))).all()
    
    if len(user) == 0:
        return JSONResponse(status_code=401, content={"Error": "Пользователь не найден."})
    else:
        return user[0]

# Проверка пользователя
async def authorization_check_(request, db):
    data = await request.json()

    user = db.query(User).filter(and_(User.id == data.get('id'), User.password == data.get('key'), User.mail == data.get('mail'))).all()

    if len(user) == 0:
        return JSONResponse(status_code=401, content={"Error": "Пользователь не найден."})
    else:
        return {'data': True}