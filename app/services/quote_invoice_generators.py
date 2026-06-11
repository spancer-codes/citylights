import os
from datetime import date
from jinja2 import Template
from weasyprint import HTML, CSS
from .pdf_template import INVOICE_TEMPLATE, QUOTE_TEMPLATE

# IVOICE GENERATOR
def generate_invoice_file(payload: dict, invoice_number: str) -> str:
    """
    Render an HTML invoice and convert it to PDF with WeasyPrint.
 
    Args:
        payload: {
            "date_created": str,          # e.g. "2026-06-07"
            "client_name": str,
            "client_address": str,
            "client_number": str,         # phone / contact number
            "items": [
                {
                    "description": str,
                    "quantity": int | float,
                    "unit_price_ex_vat": float,
                    "unit_price_inc_vat": float,
                    "line_total": float,
                    "note": str           # optional extra line under description
                },
                ...
            ]
        }
        invoice_number: str               # e.g. "marysmith-0098"
 
    Returns:
        str: absolute path to the generated PDF file.
    """
    os.makedirs("generated_invoices", exist_ok=True)
    pdf_path = f"generated_invoices/{invoice_number}.pdf"
 
    # Derive subtotal from line items
    subtotal = sum(item.get("line_total", 0) for item in payload.get("items", []))
 
    # Render Jinja2 template
    template = Template(INVOICE_TEMPLATE)
    html_content = template.render(
        invoice_number=invoice_number,
        date_created=payload.get("date_created", str(date.today())),
        client_name=payload.get("client_name", ""),
        client_address=payload.get("client_address", ""),
        client_number=payload.get("client_number", ""),
        items=payload.get("items", []),
        subtotal=subtotal,
    )
 
    # Convert HTML → PDF
    HTML(string=html_content).write_pdf(pdf_path)
 
    return pdf_path

# QUOTE GENERATOR

def generate_quote_file(payload: dict, quote_number: str) -> str:
    """
    Takes a payload and quote number, returns path to a generated PDF quote.
 
    payload = {
        "date_created": str,           # e.g. "2026-03-26"
        "client_name": str,
        "client_address": str,         # optional
        "client_city": str,            # optional
        "client_email": str,           # optional
        "client_number": str,          # optional
        "deposit_percent": float,      # optional, e.g. 70.0
        "terms": [str, str, ...],      # optional list of T&C strings
        "items": [
            {
                "description": str,
                "quantity": int | float,
                "unit_price": float,
                "total_price": float,
                "note": str            # optional
            }
        ]
    }
    """
    os.makedirs("generated_quotes", exist_ok=True)
    pdf_path = f"generated_quotes/{quote_number}.pdf"
 
    grand_total = sum(item.get("line_total", 0) for item in payload.get("items", []))
 
    html = Template(QUOTE_TEMPLATE).render(
        quote_number=quote_number,
        date_created=payload.get("date_created", str(date.today())),
        client_name=payload.get("client_name", ""),
        client_address=payload.get("client_address", ""),
        client_city=payload.get("client_city", ""),
        client_email=payload.get("client_email", ""),
        client_number=payload.get("client_number", ""),
        deposit_percent=payload.get("deposit_percent", None),
        terms=payload.get("terms", []),
        items=payload.get("items", []),
        grand_total=grand_total,
    )
 
    HTML(string=html).write_pdf(pdf_path)
    return pdf_path