import os

import models.fill_models as fill
import models.config as conf

from models.models import Base

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



# Подключение к базе данных MySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.USERNAME}:{conf.PASSWORD}@{conf.IP_ADDRESS}:{conf.PORT}/{conf.DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создание таблиц в базе данных, если они еще не существуют
#Base.metadata.drop_all(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Создание функции для создания сессий базы данных
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    try:
        yield db()
    finally:
        db().close()

fill.fill_categories()
fill.fill_sub_categories()
fill.fill_ads()
fill.fill_regions()