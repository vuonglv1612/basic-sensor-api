import json
import os
from datetime import datetime
from typing import Optional

import aioredis
import pytz
import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI(title="Temperature and Humidity Sensor API", version="0.1.0")
redis_uri = os.getenv("REDIS_URI", "redis://localhost:6379")
secret_api_key = os.getenv("API_KEY")

app.mount("/static", StaticFiles(directory="static"), name="static")


async def get_storage():
    return await aioredis.Redis.from_url(redis_uri)


def gen_sensor_key(sensor_name):
    return f"sensor:{sensor_name}"


@app.get("/", include_in_schema=False)
async def read_item(request: Request, storage: aioredis.Redis = Depends(get_storage)):
    sensors = await storage.keys("sensor:*")
    data = {"sensors": [sensor.decode("utf-8").split(":")[1] for sensor in sensors]}
    return templates.TemplateResponse("index.html", {"request": request, "sensors": data["sensors"]})


@app.post("/api/metrics")
async def add_metrics(
    sensor: str,
    temperature_c: int,
    humidity: Optional[int] = None,
    api_key: Optional[str] = None,
    storage: aioredis.Redis = Depends(get_storage),
):
    if secret_api_key:
        if not api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if api_key != secret_api_key:
            raise HTTPException(status_code=401, detail="API key is invalid")
    now = datetime.now(tz=pytz.timezone("Asia/Ho_Chi_Minh"))
    data = {
        "sensor": sensor,
        "temperature_c": temperature_c,
        "humidity": humidity,
        "timestamp": now.isoformat(),
    }
    await storage.set(gen_sensor_key(sensor), json.dumps(data))
    return data


@app.get("/api/metrics")
async def get_metrics(sensor: str, storage: aioredis.Redis = Depends(get_storage)):
    value = await storage.get(gen_sensor_key(sensor))
    if value:
        data = json.loads(value)
        return data
    raise HTTPException(status_code=404, detail="Sensor not found")


@app.get("/metrics", include_in_schema=False)
async def get_metrics(request: Request, sensor: str, storage: aioredis.Redis = Depends(get_storage)):
    value = await storage.get(gen_sensor_key(sensor))
    if value:
        data = json.loads(value)
        return templates.TemplateResponse("metrics.html", {"request": request, "data": data, "sensor": sensor})
    raise HTTPException(status_code=404, detail="Sensor not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
