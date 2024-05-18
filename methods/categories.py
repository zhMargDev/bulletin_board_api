from models.models import Categories, SubCategories, Base
from sqlalchemy.orm import sessionmaker, load_only
from fastapi.responses import JSONResponse


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