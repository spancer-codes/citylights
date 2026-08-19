from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routes.routes import router as routes_router
from app.routes.invoices import router as invoice_router
from app.routes.quotes import router as quotes_router
from app.services.search import router as search_router
from app.routes import customers, dashboard, quote_invoice_preview
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return RedirectResponse(url="/static/index (1).html")
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_methods=["*"],          
    allow_headers=["*"],
)
app.include_router(invoice_router)
app.include_router(quotes_router)
app.include_router(routes_router)
app.include_router(search_router)
app.include_router(customers.router)
app.include_router(dashboard.router)
app.include_router(quote_invoice_preview.router)
