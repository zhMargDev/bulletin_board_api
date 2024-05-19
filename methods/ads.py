import uuid

from models.models import Ads, FavoriteAd, Base
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy import create_engine, and_, desc
from fastapi.responses import JSONResponse

# Получение объявлений
async def get_(request, db):
    ad_id = request.query_params.get("id")
    category = request.query_params.get("category")
    sub_category = request.query_params.get("sub_category")
    owner_id = request.query_params.get("owner_id")
    owner_type = request.query_params.get("owner_type")
    user_id = request.query_params.get("user_id")
    user_type = request.query_params.get("user_type")

    limit = request.query_params.get('limit')

    if not ad_id:
        # Если указан пользователь то вывести все объявления пользователя
        if owner_id:
            if owner_type:
                if owner_type == 'user' or owner_type == 'shop':
                    if not limit: ads = db.query(Ads).filter(and_(Ads.owner_id == owner_id, Ads.owner_type == owner_type)).order_by(desc(Ads.id)).all()
                    else: ads = db.query(Ads).filter(and_(Ads.owner_id == owner_id, Ads.owner_type == owner_type)).order_by(desc(Ads.id)).limit(limit).all()
                    reversed_ads = list(reversed(ads))
                    if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления указанного пользователя не найдены."})
                    else: return {'ads': reversed_ads}
        # Если указан пользователь не как owner то вывести все его избранные объявления
        if user_id:
            if user_type:
                if user_type == 'user' or user_type == 'shop':
                    # Находим все избранные объявления пользователя
                    favorite_ads = db.query(FavoriteAd).filter(and_(FavoriteAd.user_id == user_id, FavoriteAd.user_type == user_type)).all()
                    if not favorite_ads: return JSONResponse(status_code=401, content={"Error": "Избранных объявлений у данного пользователя нету."})
                    else:
                        favorite_ad_ids = [ad.ad_id for ad in favorite_ads]
                        if not limit: ads = db.query(Ads).filter(Ads.id.in_(favorite_ad_ids)).order_by(desc(Ads.id)).all()
                        else: ads = db.query(Ads).filter(Ads.id.in_(favorite_ad_ids)).order_by(desc(Ads.id)).limit(limit).all()
                        return {'ads': ads}
        if not category:
            # Если не указан id категория то отправить все объявления
            if not limit: ads = db.query(Ads).order_by(desc(Ads.id)).all()
            else: ads = db.query(Ads).order_by(desc(Ads.id)).limit(limit).all()
            if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления по указанномы категориям не найден."})
            else: return {'ads': ads}
        else:
            # Если не указан id но указана категория, то проверяем есть ли подкатегория
            if not sub_category:
                # Если нету то отправка всех объявлений которые подходят под указанную категорию
                if not limit: ads = db.query(Ads).filter(Ads.category_url == category).order_by(desc(Ads.id)).all()
                else: ads = db.query(Ads).filter(Ads.category_url == category).order_by(desc(Ads.id)).limit(limit).all()
                if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления по указанномы категориям не найден."})
                else: return {'ads': ads}
            else:
                # Если подкатегория указана то отправляются все объявления которые подходят под категорию и субкатегорию 
                if not limit: ads = db.query(Ads).filter(and_(Ads.category_url == category, Ads.subcategory_url == sub_category)).order_by(desc(Ads.id)).all()
                else: ads = db.query(Ads).filter(and_(Ads.category_url == category, Ads.subcategory_url == sub_category)).order_by(desc(Ads.id)).limit(limit).all()
                if not ads: return JSONResponse(status_code=401, content={"Error": "Объявления по указанномы категориям не найден."})
                else: return {'ads': ads}
    else:
        # Если id указан то отправка категории по его id
        if not limit: ads = db.query(Ads).filter(Ads.id == ad_id).order_by(desc(Ads.id)).one()
        else: ads = db.query(Ads).filter(Ads.id == ad_id).order_by(desc(Ads.id)).limit(limit).one()

        if not ads: return JSONResponse(status_code=401, content={"Error": "Объявление по указанному ID адресу не найден."})
        else: return {'ads': ads}

# Добавление нового объявления
async def post_(file, title, price, currency, description, region, owner_id, category_url, subcategory_url, db):
    try:
        SAVE_DIR = Path("imgs/ads")
        # Проверяем, что директория для сохранения существует, иначе создаем ее
        SAVE_DIR.mkdir(parents=True, exist_ok=True)
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
            picture_url = f"/images/ads/{unique_filename}",
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
        return JSONResponse(status_code=401, content={"Error": str(e)})

# Изменение объявления
async def put_(id, db, file=None, title=None, price=None, currency=None, description=None, region=None, owner_id=None, category_url=None, subcategory_url=None):
    if not id: return JSONResponse(status_code=404, content={"Error": "ID не указан."})
    
    try:
        ad = db.query(Ads).filter(Ads.id == id).first()
        
        if file is not None:
            SAVE_DIR = Path("imgs/ads")
            # Проверяем, что директория для сохранения существует, иначе создаем ее
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Генерируем уникальное имя файла
            unique_filename = str(uuid.uuid4()) + Path(file.filename).suffix
            # Полный путь для сохранения файла
            file_path = SAVE_DIR / unique_filename
            # Сохраняем файл
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            ad.picture_url = f"/images/ads/{unique_filename}"

        if title is not None: ad.title = title
        if price is not None: ad.price = price
        if currency is not None: ad.currency = currency
        if description is not None: ad.description = description
        if region is not None: ad.region = region
        if owner_id is not None: ad.owner_id = owner_id
        if category_url is not None: ad.category_url = category_url
        if subcategory_url is not None: ad.subcategory_url = subcategory_url
            
        db.commit()
        db.refresh(ad)

        return ad
    except Exception as e:
        return JSONResponse(status_code=401, content={"Error": str(e)})

# Удаление объявления
async def delete_(db, request):
    data = await request.json()
    ad_id = data.get('id')

    try:
        # Находим объявление по его id
        ad = db.query(Ads).filter(Ads.id == ad_id).first()
        if ad:
            # Проверяем, есть ли записи в таблице FavoriteAd, связанные с объявлением
            favorite_ads = db.query(FavoriteAd).filter(FavoriteAd.ad_id == ad_id).all()

            if favorite_ads:
                # Удаляем все связанные записи из таблицы FavoriteAd
                db.query(FavoriteAd).filter(FavoriteAd.ad_id == ad_id).delete()
            # Удаляем найденное объявление
            db.delete(ad)
            db.commit()
            return {"message": "Объявление успешно удалено."}
        else:
            return {"error": "Объявление не найдено."}
    except IntegrityError as e:
        db.rollback()
        return {"error": str(e)}

# Изменение статуса 
async def change_status(db, request):
    data = await request.json()
    ad_id = data.get('id')
    activated = data.get('activated')
    
    if not ad_id: return JSONResponse(status_code=404, content={"Error": "ID не указан."})
    elif not activated: return JSONResponse(status_code=404, content={"Error": "Не указан статус."})
    elif type(activated) is not bool: return JSONResponse(status_code=404, content={"Error": "Статус должен быть или ture или false."})
    try:
        ad = db.query(Ads).filter(Ads.id == id).first()

        ad.activated = activated

        db.commit()
        db.refresh(ad)

        return ad
    except Exception as e:
        return JSONResponse(status_code=401, content={"Error": str(e)})

# Добавление в избранные
async def add_to_favorites(db, request):
    data = await request.json()
    user_id = data.get('user_id')
    user_type = data.get('user_type')
    ad_id = data.get('ad_id')

    if not user_id or not user_type or not ad_id:
        return JSONResponse(status_code=404, content={"Error": "Не все параметры указаны."})
    else:
        favorite = FavoriteAd(
            user_id = user_id,
            user_type = user_type,
            ad_id = ad_id,
            created=str(datetime.now())
        )
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        
        return favorite

# Удаление из избранных
async def remove_favorite(db, request):
    data = await request.json()
    favorite_ad_id = data.get('id')

    try:
        # Находим объявление по его id
        favorite_ads = db.query(FavoriteAd).filter(FavoriteAd.id == favorite_ads).first()
        if favorite_ads:
            db.delete(favorite_ads)
            db.commit()
            return {"message": "Объявление успешно удалено."}
        else:
            return {"error": "Объявление не найдено."}
    except IntegrityError as e:
        db.rollback()
        return {"error": str(e)}