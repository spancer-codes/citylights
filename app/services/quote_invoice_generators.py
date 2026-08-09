import os
from datetime import date
from jinja2 import Template
from weasyprint import HTML, CSS
from .pdf_template import INVOICE_TEMPLATE, QUOTE_TEMPLATE
from typing import Literal

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


# QuoteType is a type hint only — Literal has no runtime attributes like
# .PRICED or .SCOPE_ONLY, so the actual values live in these constants.
QuoteType = Literal["priced", "scope_only"]
QUOTE_TYPE_PRICED: QuoteType = "priced"
QUOTE_TYPE_SCOPE_ONLY: QuoteType = "scope_only"


def _render_quote_pdf(payload: dict, quote_number: str, show_pricing: bool) -> tuple[str, float, float]:
    """
    Shared rendering logic for both quote types.
    Returns (pdf_path, grand_total, total_labour).
    """
    os.makedirs("generated_quotes", exist_ok=True)
    pdf_path = f"generated_quotes/{quote_number}.pdf"

    items = payload.get("items", [])

    grand_total = sum(item.get("total_price", 0) for item in items)

    # Total labour = sum of any line items described as "labour".
    # Falls back to grand_total if no item is explicitly labelled "labour",
    # so a labour-only quote still shows a sensible number.
    labour_items = [item for item in items if "labour" in item.get("description", "").lower()]
    total_labour = sum(item.get("total_price", 0) for item in labour_items) if labour_items else grand_total

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
        items=items,
        grand_total=grand_total,
        show_pricing=show_pricing,
        total_labour=total_labour,
    )

    HTML(string=html).write_pdf(pdf_path)
    return pdf_path, grand_total, total_labour


def generate_priced_quote_file(payload: dict, quote_number: str) -> dict:
    """
    Generates an itemized quote PDF (Scope + Qty + Unit Price + Total Price).

    payload = {
        "date_created": str,
        "client_name": str,
        "client_address": str,     # optional
        "client_city": str,        # optional
        "client_email": str,       # optional
        "client_number": str,      # optional
        "deposit_percent": float,  # optional
        "terms": [str, ...],       # optional
        "items": [
            {"description": str, "quantity": int | float, "unit_price": float,
             "total_price": float, "note": str}  # note optional
        ]
    }

    Returns:
        {"pdf_path": str, "quote_number": str, "quote_type": "priced",
         "grand_total": float}
    """
    pdf_path, grand_total, _ = _render_quote_pdf(payload, quote_number, show_pricing=True)

    return {
        "pdf_path": pdf_path,
        "quote_number": quote_number,
        "quote_type": QUOTE_TYPE_PRICED,
        "grand_total": grand_total,
    }


def generate_scope_quote_file(payload: dict, quote_number: str) -> dict:
    """
    Generates a scope-of-work-only quote PDF (no per-item pricing shown,
    just a Total Labour figure).

    payload = {
        "date_created": str,
        "client_name": str,
        "client_address": str,     # optional
        "client_city": str,        # optional
        "client_email": str,       # optional
        "client_number": str,      # optional
        "deposit_percent": float,  # optional
        "terms": [str, ...],       # optional
        "items": [
            {"description": str, "note": str}  # note optional; pricing fields
                                                  # are ignored for rendering
                                                  # but may still be present
                                                  # in payload for internal use
        ]
    }

    Returns:
        {"pdf_path": str, "quote_number": str, "quote_type": "scope_only",
         "total_labour": float}
    """
    pdf_path, _, total_labour = _render_quote_pdf(payload, quote_number, show_pricing=False)

    return {
        "pdf_path": pdf_path,
        "quote_number": quote_number,
        "quote_type": QUOTE_TYPE_SCOPE_ONLY,
        "total_labour": total_labour,
    }










def generate_quote_file__(payload: dict, quote_number: str) -> str:
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
        "show_pricing": bool,          # optional, default True. False -> show Scope of Work + Total Labour only
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

    items = payload.get("items", [])

    # fixed: was reading "line_total", but items use "total_price"
    grand_total = sum(item.get("total_price", 0) for item in items)

    # Total labour = sum of any line items described as "labour".
    # Falls back to grand_total if no item is explicitly labelled "labour",
    # so a labour-only quote still shows a sensible number.
    labour_items = [item for item in items if "labour" in item.get("description", "").lower()]
    total_labour = sum(item.get("total_price", 0) for item in labour_items) if labour_items else grand_total

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
        items=items,
        grand_total=grand_total,
        show_pricing=payload.get("show_pricing", True),
        total_labour=total_labour,
    )

    HTML(string=html).write_pdf(pdf_path)
    return pdf_path
