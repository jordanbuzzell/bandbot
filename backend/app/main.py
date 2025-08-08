from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import band, venue

app = FastAPI(title="BandBot API", description="Help musicians name their band and find NYC venues")

app.include_router(band.router)
app.include_router(venue.router)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("frontend/index.html")
