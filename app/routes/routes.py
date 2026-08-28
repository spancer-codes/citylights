import os
import re
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.db.database import get_db
from app.models import Quotes, Invoices
#from app.schemas import (WhatsAppExtractRequest,AIGeneratedQuoteResponse,SelectClientRequest,ApproveQuoteRequest)
from app.services.quote_to_invoice import convert_quote_to_invoice
from app.services.quote_invoice_generators import QuoteType
from app.utils.pdf_creator import invoice_pdf, quote_pdf
#from app.ai.ai_quote_extract import extract_from_whatsapp

router = APIRouter()

QUOTE_PDF_FOLDER = "generated_quotes"
INVOICE_PDF_FOLDER = "generated_invoices"

def quote_to_payload(q):
    return {
        "date_created": str(q.date_created),
        "client_name": q.client_name,
        "client_address": q.client_address,
        "client_city": q.client_city,
        "client_email": q.client_email,
        "client_number": q.client_number,
        "deposit_percent": q.deposit_percent,
        "terms": q.terms or [],
        "items": q.items or [],  # ensure this is a list of dicts
        "show_pricing": (q.quote_type or QuoteType.PRICED) != QuoteType.SCOPE_ONLY,
    }

# serve pdf for preview
@router.get("/pdf/{type}/{filename}")
def serve_pdf(type: str, filename: str):
    filename = os.path.basename(filename)

    if type == "quote":
        path = os.path.join(QUOTE_PDF_FOLDER, filename)
    elif type == "invoice":
        path = os.path.join(INVOICE_PDF_FOLDER, filename)
    else:
        raise HTTPException(status_code=400, detail="Invalid type")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=path,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Accept-Ranges": "bytes"
        }
    )

# Quote to Invoice conversion route
@router.post("/quotes/{quote_id}/convert-to-invoice")
def convert_quote_to_invoice_route(
    quote_id: int,
    amount_paid: float = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    quote = db.query(Quotes).filter(Quotes.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    if (quote.quote_type or QuoteType.PRICED) == QuoteType.SCOPE_ONLY:
        raise HTTPException(
            status_code=400,
            detail="This quote has no item pricing (scope-of-work only) and cannot be converted directly to an invoice. Create a priced quote first.",
        )

    return convert_quote_to_invoice(quote_id, amount_paid, db)

@router.get("/quote/preview/{quote_id}")
def get_quote(quote_id: int, db: Session = Depends(get_db)):
    quote = db.query(Quotes).filter(Quotes.id == quote_id).first()

    pdf_path, filename = quote_pdf(quote)
    return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename
        )

@router.get("/invoice/preview/{invoice_id}")
def get_invoice(invoice_id: int, db : Session =Depends(get_db)):
    invoice = db.query(Invoices).filter(Invoices.id == invoice_id).first()

    pdf_path, filename = invoice_pdf(invoice)
    return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=filename
        )

"""
# whatsapp quote extraction route
@router.post("/ai-generated-quotes/from-whatsapp", response_model=AIGeneratedQuoteResponse)
def create_ai_quote(payload: WhatsAppExtractRequest, db: Session = Depends(get_db)):

    extracted = extract_from_whatsapp(payload.message)

    status = "pending_client" if not extracted["client_name"] else "pending_review"

    new_quote = AIGeneratedQuote(
        raw_message=payload.message,
        extracted_client_name=extracted["client_name"],
        location=extracted["location"],
        job_type=extracted["job_type"],
        extracted_items=extracted["items"],
        status=status
    )

    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)

    return new_quote

@router.get("/ai-generated-quotes/client-search")
def client_search(name: str, db: Session = Depends(get_db)):
    results = search_clients(db, name)
    return [r[0] for r in results]

@router.post("/ai-generated-quotes/{quote_id}/select-client")
def select_client(quote_id: int, payload: SelectClientRequest, db: Session = Depends(get_db)):

    quote = db.query(AIGeneratedQuote).get(quote_id)

    if not quote:
        raise HTTPException(404, "Quote not found")

    quote.selected_client_name = payload.client_name
    quote.status = "pending_review"

    db.commit()

    return {"message": "Client selected"}

@router.post("/ai-generated-quotes/{quote_id}/approve")
def approve_quote(quote_id: int, payload: ApproveQuoteRequest, db: Session = Depends(get_db)):

    ai_quote = db.query(AIGeneratedQuote).get(quote_id)

    if not ai_quote:
        raise HTTPException(404, "AI Quote not found")

    if not ai_quote.selected_client_name:
        raise HTTPException(400, "Client not selected")

    # Convert items to your existing quote format
    items = []
    subtotal = 0

    for item in payload.reviewed_items:
        unit_price = 0  # user will fill later or from UI
        total = (item.quantity or 1) * unit_price

        items.append({
            "description": item.name,
            "quantity": item.quantity or 1,
            "unit_price": unit_price,
            "line_total": total
        })

        subtotal += total

    # Create real quote
    new_quote = Quotes(
        client_name=ai_quote.selected_client_name,
        client_address=ai_quote.location,
        client_city="Harare",
        items=items,
        subtotal=subtotal,
        total=subtotal
    )

    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)

    # Update AI table
    ai_quote.reviewed_items = [item.dict() for item in payload.reviewed_items]
    ai_quote.status = "converted"
    ai_quote.final_quote_id = new_quote.id

    db.commit()

    return {"message": "Quote created", "quote_id": new_quote.id}
"""