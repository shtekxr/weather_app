from fastapi import APIRouter, Depends, Request, Response
from src.services import get_weather, autocomplete_city
from src.models import CityHistory, get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/weather/{city}")
async def weather(city: str, request: Request, response: Response, db: Session = Depends(get_db)):
    last_city = request.cookies.get("last_city")
    data = await get_weather(city, last_city)

    city_entry = db.query(CityHistory).filter(CityHistory.city == city).first()
    if city_entry:
        city_entry.count += 1
    else:
        city_entry = CityHistory(city=city, count=1)
        db.add(city_entry)
    db.commit()

    response.set_cookie(
        key="last_city",
        value=city,
        max_age=360000,
        expires=360000,
    )
    return JSONResponse(content=data, headers=response.headers)


@router.get("/autocomplete/{query}")
async def autocomplete(query: str):
    suggestions = await autocomplete_city(query)
    return suggestions


@router.get("/history")
async def history(db: Session = Depends(get_db)):
    cities = db.query(CityHistory).all()
    return [{"city": city.city, "count": city.count} for city in cities]
