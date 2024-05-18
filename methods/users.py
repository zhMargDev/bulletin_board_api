from models.models import User, Base
from sqlalchemy.orm import sessionmaker, load_only
from datetime import datetime
from passlib.context import CryptContext


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


async def get_(request, db):
    user_id = request.query_params.get('id')

    if not user_id:
        # Получение данных пользователя кроме пароля
        users = db.query(User).options(load_only(User.id, User.name, User.mail, User.surname, 
                        User.sex, User.age, User.phone, 
                        User.rating, User.last_active, User.about, User.created)).all()
    else:
        users = db.query(User).filter(User.id == user_id).options(load_only(User.id, User.name, User.mail, User.surname, 
                        User.sex, User.age, User.phone, 
                        User.rating, User.last_active, User.about, User.created)).one()
            
    if not users: return JSONResponse(status_code=404, content={'Error': 'Пользователи не были найдены.'})
    else: return {'user': users}

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

async def login_(request, db):
    data = await request.json()

    hashed_password = get_password_hash(data.get('password'))

    user = db.query(User).filter(and_(User.password == hashed_password, User.mail == data.get('mail'))).all()
    
    if len(user) == 0:
        return JSONResponse(status_code=401, content={"Error": "Пользователь не найден."})
    else:
        return user[0]

async def authorization_check_(request, db):
    data = await request.json()

    user = db.query(User).filter(and_(User.id == data.get('id'), User.password == data.get('key'), User.mail == data.get('mail'))).all()

    if len(user) == 0:
        return JSONResponse(status_code=401, content={"Error": "Пользователь не найден."})
    else:
        return {'data': True}