import models.config as conf

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Categories, SubCategories, Ads, Regions, Base



def fill_categories():
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.USERNAME}:{conf.PASSWORD}@{conf.IP_ADDRESS}:{conf.PORT}/{conf.DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Создаем сессию базы данных
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    # Данные категорий
    categories_data = [
        {
            'name': 'Жилье',
            'url': 'housing',
            'types': 'basic',
            'icon_url': f'{conf.HOST_URL}/images/categories/build.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Коммерческая',
            'url': 'commercial',
            'types': 'basic',
            'icon_url': f'{conf.HOST_URL}/images/categories/build.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Обслуживание',
            'url': 'services',
            'types': 'basic',
            'icon_url': f'{conf.HOST_URL}/images/categories/build.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Ремонт',
            'url': 'repair',
            'types': 'related',
            'icon_url': f'{conf.HOST_URL}/images/categories/build.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Строительство',
            'url': 'construction',
            'types': 'related',
            'icon_url': f'{conf.HOST_URL}/images/categories/build.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Недвижимость в соцсетях',
            'url': 'soc_network_builds',
            'types': 'related',
            'icon_url': f'{conf.HOST_URL}/images/categories/build.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Инвестиции, готовый бизнес',
            'url': 'investments_business',
            'types': 'related',
            'icon_url': f'{conf.HOST_URL}/images/categories/business.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Мебель',
            'url': 'furniture',
            'types': 'other',
            'icon_url': f'{conf.HOST_URL}/images/categories/furniture.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Оборудование, электроника',
            'url': 'electronics',
            'types': 'other',
            'icon_url': f'{conf.HOST_URL}/images/categories/electronics.svg',
            'created': str(datetime.now())
        },
        {
            'name': 'Материалы',
            'url': 'materials',
            'types': 'other',
            'icon_url': f'{conf.HOST_URL}/images/categories/furniture.svg',
            'created': str(datetime.now())
        },
    ]

    # Добавляем данные в базу данных
    for category_data in categories_data:
        categories = Categories(**category_data)
        db.add(categories)

    # Сохраняем изменения в базе данных
    db.commit()

    # Закрываем сессию базы данных
    db.close()

def fill_sub_categories():
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.USERNAME}:{conf.PASSWORD}@{conf.IP_ADDRESS}:{conf.PORT}/{conf.DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Создаем сессию базы данных
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    # Данные категорий
    categories_data = [
        {
            'name': 'Специалист',
            'url': 'speciolist',
            'p_category_url': 'construction',
            'created': str(datetime.now())
        },
        {
            'name': 'Под офис',
            'url': 'office',
            'p_category_url': 'commercial',
            'created': str(datetime.now())
        },
        {
            'name': 'Под магазин',
            'url': 'shop',
            'p_category_url': 'commercial',
            'created': str(datetime.now())
        },
        {
            'name': 'Под склад',
            'url': 'stock',
            'p_category_url': 'commercial',
            'created': str(datetime.now())
        },
        {
            'name': 'Здание',
            'url': 'building',
            'p_category_url': 'commercial',
            'created': str(datetime.now())
        },
        {
            'name': 'Земленой участок',
            'url': 'land_plot',
            'p_category_url': 'commercial',
            'created': str(datetime.now())
        },
        {
            'name': 'Место в парковке',
            'url': 'parking',
            'p_category_url': 'commercial',
            'created': str(datetime.now())
        },
        {
            'name': 'Прочее',
            'url': 'other',
            'p_category_url': 'commercial',
            'created': str(datetime.now())
        },
        {
            'name': 'Компания',
            'url': 'company',
            'p_category_url': 'soc_network_builds',
            'created': str(datetime.now())
        },
        {
            'name': 'Комната',
            'url': 'room',
            'p_category_url': 'housing',
            'created': str(datetime.now())
        },
        {
            'name': 'Квартира',
            'url': 'apartment',
            'p_category_url': 'housing',
            'created': str(datetime.now())
        },
        {
            'name': 'Дом',
            'url': 'house',
            'p_category_url': 'housing',
            'created': str(datetime.now())
        },
        {
            'name': 'Дача с участком',
            'url': 'country_house',
            'p_category_url': 'housing',
            'created': str(datetime.now())
        },
        {
            'name': 'Гараж',
            'url': 'garage',
            'p_category_url': 'housing',
            'created': str(datetime.now())
        },
        {
            'name': 'Прочее',
            'url': 'other',
            'p_category_url': 'housing',
            'created': str(datetime.now())
        },
        {
            'name': 'Телеграм',
            'url': 'telegram',
            'p_category_url': 'investments_business',
            'created': str(datetime.now())
        }
    ]

    # Добавляем данные в базу данных
    for category_data in categories_data:
        categories = SubCategories(**category_data)
        db.add(categories)

    # Сохраняем изменения в базе данных
    db.commit()

    # Закрываем сессию базы данных
    db.close()

def fill_ads():
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.USERNAME}:{conf.PASSWORD}@{conf.IP_ADDRESS}:{conf.PORT}/{conf.DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Создаем сессию базы данных
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    # Данные категорий
    ads = [
        {
            'title': 'Студия 35 кв/м',
            'price': '35000/м',
            'currency': 'Rub',
            'description': 'fwqfgqwgf qbhiu qg w biqwbuq gwgbq wqbiguw',
            'picure_url': f'{conf.HOST_URL}/images/ads/fj1.png',
            'region': 'Россия, Хабаровск',
            'owner_id': 1,
            'category_url': 'housing',
            'subcategory_url': 'none',
            'views': 0,
            'created': str(datetime.now())
        },
        {
            'title': 'Студия 35 кв/м недалеко от торгового центра ',
            'price': '35000',
            'currency': 'Rub',
            'description': 'fwqfgqwgf qbhiu qg w biqwbuq gwgbq wqbiguw',
            'picure_url': f'{conf.HOST_URL}/images/ads/fj2.png',
            'region': 'Россия, Хабаровск',
            'owner_id': 1,
            'category_url': 'housing',
            'subcategory_url': 'none',
            'views': 0,
            'created': str(datetime.now())
        },
        {
            'title': 'Студия 35 кв/м',
            'price': '35000/м',
            'currency': 'Rub',
            'description': 'fwqfgqwgf qbhiu qg w biqwbuq gwgbq wqbiguw',
            'picure_url': f'{conf.HOST_URL}/images/ads/fj4.png',
            'region': 'Россия, Хабаровск',
            'owner_id': 1,
            'category_url': 'housing',
            'subcategory_url': 'none',
            'views': 0,
            'created': str(datetime.now())
        },
        {
            'title': 'Видео карта GEFORS GTX',
            'price': '50000',
            'currency': 'Rub',
            'description': 'fwqfgqwgf qbhiu qg w biqwbuq gwgbq wqbiguw',
            'picure_url': f'{conf.HOST_URL}/images/ads/fj5.png',
            'region': 'Россия, Хабаровск',
            'owner_id': 1,
            'category_url': 'electronics',
            'subcategory_url': 'none',
            'views': 0,
            'created': str(datetime.now())
        },
        {
            'title': 'Iphone XS',
            'price': '180000',
            'currency': 'Rub',
            'description': 'fwqfgqwgf qbhiu qg w biqwbuq gwgbq wqbiguw',
            'picure_url': f'{conf.HOST_URL}/images/ads/fj3.png',
            'region': 'Россия, Хабаровск',
            'owner_id': 1,
            'category_url': 'electronics',
            'subcategory_url': 'none',
            'views': 0,
            'created': str(datetime.now())
        },
    ]

    # Добавляем данные в базу данных
    for ad in ads:
        ad_ = Ads(**ad)
        db.add(ad_)

    # Сохраняем изменения в базе данных
    db.commit()

    # Закрываем сессию базы данных
    db.close()
        

def fill_regions():
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{conf.USERNAME}:{conf.PASSWORD}@{conf.IP_ADDRESS}:{conf.PORT}/{conf.DB_NAME}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Создаем сессию базы данных
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    # Данные категорий
    regions = [
        {
            'region': 'Арагацотн',
            'url': 'aragacotn',
            'created': str(datetime.now())
        },
        {
            'region': 'Арарат',
            'url': 'ararat',
            'created': str(datetime.now())
        },
        {
            'region': 'Армавир',
            'url': 'armavir',
            'created': str(datetime.now())
        },
        {
            'region': 'Гегаркуник',
            'url': 'gegharkunik',
            'created': str(datetime.now())
        },
        {
            'region': 'Лори',
            'url': 'lori',
            'created': str(datetime.now())
        },
        {
            'region': 'Котайк',
            'url': 'kotayk',
            'created': str(datetime.now())
        },
        {
            'region': 'Ширак',
            'url': 'shirak',
            'created': str(datetime.now())
        },
        {
            'region': 'Сюник',
            'url': 'syunik',
            'created': str(datetime.now())
        },
        {
            'region': 'Вайоц Дзор',
            'url': 'vayoc_dzor',
            'created': str(datetime.now())
        },
        {
            'region': 'Тавуш',
            'url': 'tavush',
            'created': str(datetime.now())
        },
    ]

    # Добавляем данные в базу данных
    for region in regions:
        region_ = Regions(**region)
        db.add(region_)

    # Сохраняем изменения в базе данных
    db.commit()

    # Закрываем сессию базы данных
    db.close()