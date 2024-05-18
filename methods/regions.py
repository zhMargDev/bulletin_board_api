from models.models import Regions, Base
from sqlalchemy.orm import sessionmaker, load_only

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