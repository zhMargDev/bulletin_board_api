from models.models import Regions, Base
from datetime import datetime
from sqlalchemy.orm import sessionmaker, load_only
from fastapi.responses import JSONResponse


async def get_(request, db):
    url = request.query_params.get('url')

    if not url:
        return {'regions ':db.query(Regions).all()}
    else:
        regions = db.query(Regions).filter(Regions.url == url).one()

        if not regions:
            return JSONResponse(status_code=404, content={"Error": "Объявление по указанному URL нету региона."})
        else:
            return {'regions': regions}

# Добавление региона
async def post_(request, db):
    data = request.json()

    region_name = data.get('region')
    url = data.get('url')

    if not region_name or not url: return JSONResponse(status_code=404, content={"Error": "Неправельные данные."})

    region = Regions(
        region=region_name,
        url=url,
        created = str(datetime.now())
    )

    db.add(region)
    db.commit()
    db.refresh(region)

    return region

# Изменение региона
async def put_(request, db):
    data = request.json()
    id = data.get('id')
    region_name = data.get('region')
    url = data.get('url')

    if not id: return JSONResponse(status_code=404, content={"Error": "Регион по указанному id не был найден."})

    region = db.query(Regions).filter(Regions.id == id).first()

    if region_name is not None: region.region = region_name
    if url is not None: region.url = url
    
    db.commit()
    db.refresh(region)

    return region

# Удаление региона
async def delete_(request, db):
    data = request.json()
    id = data.get('id')
    if not id: return JSONResponse(status_code=404, content={"Error": "Регион по указанному id не был найден."})

    try:
        region = db.query(Regions).filter(Regions.id == id).first()

        db.delete(region)
        db.commit()
        return {"message": "Регион успешно был удалён."}
    except IntegrityError as e:
        db.rollback()
        return {"error": str(e)}