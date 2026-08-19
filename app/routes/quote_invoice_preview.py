import os
import json
from weasyprint import HTML, CSS
from fastapi import Depends
from app.models import Quotes, Invoices
from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.routes.routes import quote_to_payload
from jinja2 import Template
from app.services.pdf_template import INVOICE_TEMPLATE, QUOTE_TEMPLATE

router = APIRouter()

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

@router.get("/quote/preview/{quote_id}")
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quotes).filter(Quotes.id == quote_id).first()

    os.makedirs("generated_quotes", exist_ok=True)
    pdf_path = f"generated_quotes/{quote.client_quote_number}.pdf"

    html = Template(QUOTE_TEMPLATE).render(
        quote_number=quote.client_quote_number,
        date_created=quote.client_date,
        client_name=quote.client_name,
        client_address=quote.client_address,

        client_city=quote.quote_data.get("client_city"),
        client_email=quote.quote_data.get("client_email"),
        client_number=quote.quote_data.get("client_number"),

        deposit_percent=safe_float(quote.quote_data.get("deposit_percent")),
        terms=quote.quote_data.get("terms", []),

        items=quote.quote_data.get("items", []),
        grand_total=safe_float(quote.quote_data.get("subtotal")),

        show_pricing=quote.quote_data.get("show_pricing", ""),
        total_labour=safe_float(quote.quote_data.get("total_labour", "")),
    )

    HTML(string=html).write_pdf(pdf_path)
    return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="quote-preview.pdf"
        )

@router.get("/invoice/preview/{invoice_id}")
def get_invoice(invoice_id, db : Session =Depends(get_db)):
    invoice = db.query(Invoices).filter(Invoices.id == invoice_id).first()

    invoice_data = json.loads(invoice.invoice_data)

    invoice_number=invoice_data.get("invoice_number")
    os.makedirs("generated_invoices", exist_ok=True)
    pdf_path = f"generated_invoices/{invoice_number}.pdf"

    template = Template(INVOICE_TEMPLATE)
    html = Template(INVOICE_TEMPLATE).render(
        invoice_number=invoice_data.get("invoice_number"),
        client_name=invoice_data.get("client_name"),
        client_address=invoice_data.get("client_address"),
        client_number=invoice_data.get("client_number"),
        date_created=invoice_data.get("date_created"),

        items=invoice_data.get("items", []),
        subtotal=safe_float(invoice_data.get("subtotal")),
        tax=safe_float(invoice_data.get("tax")),
        total=safe_float(invoice_data.get("total")),
        notes=invoice_data.get("notes"),
    )
    HTML(string=html).write_pdf(pdf_path)

    return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename="quote-preview.pdf"
        )