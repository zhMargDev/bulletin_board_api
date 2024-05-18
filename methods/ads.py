import uuid

from models.models import Ads, FavoriteAd, Base
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import create_engine, and_


async def get_(request, db):
    ad_id = request.query_params.get("id")
    category = request.query_params.get("category")
    sub_category = request.query_params.get("sub_category")
    owner_id = request.query_params.get("owner_id")
    owner_type = request.query_params.get("owner_type")
    user_id = request.query_params.get("user_id")
    user_type = request.query_params.get("user_type")

    if not ad_id:
        # Если указан пользователь то вывести все объявления пользователя
        if owner_id:
            if owner_type:
                if owner_type == 'user' or owner_type == 'shop':
                    ads = db.query(Ads).filter(and_(Ads.owner_id == owner_id, Ads.owner_type == owner_type)).all()
                    if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления указанного пользователя не найдены."})
                    else: return {'ads': ads}
        # Если указан пользователь не как owner то вывести все его избранные объявления
        if user_id:
            if user_type:
                if user_type == 'user' or user_type == 'shop':
                    # Находим все избранные объявления пользователя
                    favorite_ads = db.query(FavoriteAd).filter(and_(FavoriteAd.user_id == user_id, FavoriteAd.user_type == user_type)).all()
                    if not favorite_ads: return JSONResponse(status_code=401, content={"Error": "Избранных объявлений у данного пользователя нету."})
                    else:
                        favorite_ad_ids = [ad.ad_id for ad in favorite_ads]
                        ads = db.query(Ads).filter(Ads.id.in_(favorite_ad_ids)).all()
                        return {'ads': ads}
        if not category:
            # Если не указан id категория то отправить все объявления
            ads = db.query(Ads).all()
            if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления по указанномы категориям не найден."})
            else: return {'ads': ads}
        else:
            # Если не указан id но указана категория, то проверяем есть ли подкатегория
            if not sub_category:
                # Если нету то отправка всех объявлений которые подходят под указанную категорию
                ads = db.query(Ads).filter(Ads.category_url == category).all()
                if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления по указанномы категориям не найден."})
                else: return {'ads': ads}
            else:
                # Если подкатегория указана то отправляются все объявления которые подходят под категорию и субкатегорию 
                ads = db.query(Ads).filter(and_(Ads.category_url == category, Ads.subcategory_url == sub_category)).all()
                if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления по указанномы категориям не найден."})
                else: return {'ads': ads}
    else:
        # Если id указан то отправка категории по его id
        ads = db.query(Ads).filter(Ads.id == ad_id).one()

        if not ads: return JSONResponse(status_code=401, content={"Error": "Объявление по указанному ID адресу не найден."})
        else: return {'ads': ads}

async def post_(file, title, price, currency, description, region, owner_id, category_url, subcategory_url, db):
    SAVE_DIR = Path("imgs/ads")
    # Проверяем, что директория для сохранения существует, иначе создаем ее
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Генерируем уникальное имя файла
        unique_filename = str(uuid.uuid4()) + Path(file.filename).suffix
        # Полный путь для сохранения файла
        file_path = SAVE_DIR / unique_filename

        # Сохраняем файл
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Генерируем модель нового объявление
        new_ad = Ads(
            title = title,
            price = price,
            currency = currency,
            description = description,
            picure_url = f"/images/ads/{unique_filename}",
            region = region,
            owner_id = owner_id,
            category_url = category_url,
            subcategory_url = subcategory_url,
            views = 0,
            created=str(datetime.now())
        )
        # Добавляем в базу данных и обнавляем модель для получения id добавленного объявления
        db.add(new_ad)
        db.commit()
        db.refresh(new_ad)
        
        return new_ad
    except Exception as e:
        return {"error": str(e)}