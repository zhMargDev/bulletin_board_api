import uuid

from datetime import datetime
from pathlib import Path
from models.models import Categories, SubCategories, Base
from sqlalchemy.orm import sessionmaker, load_only
from fastapi.responses import JSONResponse

# Получение категорий
async def get_(request, db):
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

# Добавление категории
async def post_category(db, file, name, url, types):
    try:
        SAVE_DIR = Path("imgs/categories")
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
        categories = Categories(
            name = name,
            url = url,
            types = types,
            icon_url = f"/images/categories/{unique_filename}",
            created=str(datetime.now())
        )
        # Добавляем в базу данных и обнавляем модель для получения id добавленного объявления
        db.add(categories)
        db.commit()
        db.refresh(categories)
        
        return categories
    except Exception as e:
        return JSONResponse(status_code=404, content={"Error": str(e)})

# Добавление под категории
async def post_sub_category(db, request):
    data = request.json()
    name = data.get('name')
    url = data.get('url')
    p_category_url = data.get('p_category_url')
    if not name or not url or not p_category_url:
        return JSONResponse(status_code=422, content={'Error': 'Не правельные данные.'})
    else:
        subCategory = SubCategories(
            name = name,
            url = url,
            p_category_url = p_category_url,
            created=str(datetime.now())
        )
        # Добавляем в базу данных и обнавляем модель для получения id добавленного объявления
        db.add(subCategory)
        db.commit()
        db.refresh(subCategory)
        
        return subCategory

# Изменние категории
async def put_category(db, id, file=None, name=None, url=None, types=None):
    if not id: return JSONResponse(status_code=422, content={'Error': 'Неправельные данные.'})
    try:
        category = db.query(Categories).filter(Categories.id == id).first()
        
        if file is not None:
            SAVE_DIR = Path("imgs/categories")
            # Проверяем, что директория для сохранения существует, иначе создаем ее
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Генерируем уникальное имя файла
            unique_filename = str(uuid.uuid4()) + Path(file.filename).suffix
            # Полный путь для сохранения файла
            file_path = SAVE_DIR / unique_filename
            # Сохраняем файл
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            category.icon_url = f"/images/categories/{unique_filename}"

        if name is not None: category.name = name
        if url is not None: category.url = url
        if types is not None: category.types = types
            
        db.commit()
        db.refresh(category)

        return category
    except Exception as e:
        return JSONResponse(status_code=401, content={"Error": str(e)})

# Изменение под категории
async def put_sub_category(db, request):
    data = request.json()
    id = data.get('id')
    if not id: return JSONResponse(status_code=422, content={'Error': 'Неправельные данные.'})

    name = data.get('name')
    url = data.get('url')
    p_category_url = data.get('p_category_url')

    sub_category = db.query(SubCategories).filter(SubCategories.id == id).first()

    if name is not None: sub_category.name = name
    if url is not None: sub_category.url = url
    if p_category_url is not None: sub_category.p_category_url = p_category_url

    db.commit()
    db.refresh(sub_category)

    return sub_category

# Удаление категории
async def delete_category(db, request):
    data = request.json()
    id = data.get('id')

    if not id: return JSONResponse(status_code=404, content={'Error': 'Категория по id не найдено.'})

    try:
        category = db.query(Categories).filter(Categories.id == id).first()
        # Получаем все го подкатегории
        sub_categories = db.query(SubCategories).filter(SubCategories.p_category_url == id).all()

        if sub_categories:
            db.query(SubCategories).filter(SubCategories.p_category_url == id).delete()

        db.delete(category)
        db.commit()
        return {"message": "Категория и его подкатегории успешно удалены."}
    except IntegrityError as e:
        db.rollback()
        return {"error": str(e)}

# Удаление подкатегории
async def delete_sub_category(db, request):
    data = request.json()
    id = data.get('id')

    if not id: return JSONResponse(status_code=404, content={'Error': 'Категория по id не найдено.'})

    try:
        sub_category = db.query(SubCategories).filter(SubCategories.id == id).first()

        db.delete(sub_category)
        db.commit()
        return {"message": "Категория и его подкатегории успешно удалены."}
    except IntegrityError as e:
        db.rollback()
        return {"error": str(e)}