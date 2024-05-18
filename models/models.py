from sqlalchemy import Column, Boolean, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Создание базового класса моделей SQLAlchemy
Base = declarative_base()

# Определение модели для таблицы categories
class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    types = Column(String(100), nullable=False)
    icon_url = Column(String(200), nullable=False)
    created = Column(String(100), nullable=False)

class SubCategories(Base):
    __tablename__ = 'sub_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    p_category_url = Column(String(100), nullable=False)
    created = Column(String(100), nullable=False)

class Ads(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True)
    activated = Column(Boolean, default=False)
    title = Column(String(100), nullable=False)
    price = Column(String(100), nullable=False)
    currency = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    picure_url = Column(String(200), nullable=False)
    region = Column(String(100), nullable=False)
    owner_id = Column(Integer, nullable=False)
    owner_type = Column(String(100), nullable=False)
    category_url = Column(String(100), nullable=False)
    subcategory_url = Column(String(100), nullable=False)
    views = Column(Integer, nullable=False)
    created = Column(String(100), nullable=False)

class FavoriteAd(Base):
    __tablename__ = 'favorites_ads'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    user_type = Column(String(100), nullable=False)
    ad_id = Column(Integer, nullable=False)
    created = Column(String(100), nullable=False)

class Regions(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    region = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    created = Column(String(100), nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    mail = Column(String(100), nullable=False)
    password = Column(String(300), nullable=False)
    name = Column(String(100), nullable=True)
    surname = Column(String(100), nullable=True)
    sex = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    phone = Column(String(100), nullable=True)
    rating = Column(String(100), nullable=True)
    last_active = Column(String(100), nullable=False)
    about = Column(String(1000), nullable=True)
    created = Column(String(100), nullable=False)

class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    mail = Column(String(100), nullable=False)
    password = Column(String(300), nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=True)
    rating = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    web_site = Column(String(100), nullable=True)
    last_active = Column(String(100), nullable=False)
    about = Column(String(1000), nullable=True)
    created = Column(String(100), nullable=False)
