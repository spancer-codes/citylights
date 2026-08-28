import os
import json
from weasyprint import HTML
from app.schemas import InvoiceOut, QuoteOut
from .pdf_template import INVOICE_TEMPLATE, QUOTE_TEMPLATE
from jinja2 import Template

def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
    
def quote_pdf(payload: dict):
    if not payload:
        return {"error": "Invoice not found"}
    
    os.makedirs("generated_quotes", exist_ok=True)
    pdf_path = f"generated_quotes/{payload.client_quote_number}.pdf"

    html = Template(QUOTE_TEMPLATE).render(
        quote_number=payload.client_quote_number,
        date_created=payload.client_date,
        client_name=payload.client_name,
        client_address=payload.client_address,

        client_city=payload.quote_data.get("client_city"),
        client_email=payload.quote_data.get("client_email"),
        client_number=payload.quote_data.get("client_number"),

        deposit_percent=safe_float(payload.quote_data.get("deposit_percent")),
        terms=payload.quote_data.get("terms", []),

        items=payload.quote_data.get("items", []),
        grand_total=safe_float(payload.quote_data.get("subtotal")),

        show_pricing=payload.quote_data.get(""),
        total_labour=safe_float(payload.quote_data.get("total_labour", "")),
    )

    HTML(string=html).write_pdf(pdf_path)
    filename = f'{payload.client_quote_number}.pdf'
    return pdf_path, filename

def invoice_pdf(payload: dict):
    if not payload:
        return {"error": "Invoice not found"}

    invoice_data = (
        json.loads(payload.invoice_data)
        if isinstance(payload.invoice_data, str)
        else payload.invoice_data
    )

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
    filename = f'{invoice_data.get("invoice_number")}.pdf'

    return pdf_path, filename