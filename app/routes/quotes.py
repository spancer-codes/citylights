import os
import json
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from datetime import datetime, date, timedelta
from app.models import Quotes
from app.schemas import QuoteRequest
from app.db.database import get_db
from app.services.quote_invoice_generators import (
    generate_priced_quote_file,
    generate_scope_quote_file,
    QUOTE_TYPE_PRICED,
    QUOTE_TYPE_SCOPE_ONLY,
)
from app.utils.quote_invoice_utils import slugify_name, build_quote_payload

from sqlalchemy.orm import Session
from app.db.locks import acquire_client_lock, make_request_hash

router = APIRouter()

# create quote router
@router.post("/quote/finalize")
def finalize_quote(data: QuoteRequest, db: Session = Depends(get_db)):
    try:
        today = date.today()
        request_hash = make_request_hash(data)

        acquire_client_lock(db, data.client_name, today)

        existing = db.query(Quotes).filter(
            Quotes.request_hash == request_hash
        ).first()

        if existing:
            if existing.cached_pdf_path and os.path.exists(existing.cached_pdf_path):
                return FileResponse(
                    existing.cached_pdf_path,
                    media_type="application/pdf",
                    filename=f"{existing.client_quote_number}-quote.pdf",
                )

            if existing.quote_type == QUOTE_TYPE_SCOPE_ONLY:
                result = generate_scope_quote_file(existing.quote_data, existing.client_quote_number)
            else:
                result = generate_priced_quote_file(existing.quote_data, existing.client_quote_number)

            existing.cached_pdf_path = result["pdf_path"]
            existing.updated_at = datetime.utcnow()
            db.commit()

            return FileResponse(
                result["pdf_path"],
                media_type="application/pdf",
                filename=f"{existing.client_quote_number}-quote.pdf",
            )

        quote_type = QUOTE_TYPE_PRICED if data.show_pricing else QUOTE_TYPE_SCOPE_ONLY

        new_quote = Quotes(
            client_name=data.client_name,
            client_address=data.client_address,
            client_date=today,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            client_quote_number=None,
            total_amount=None,
            quote_data=None,
            cached_pdf_path=None,
            quote_type=quote_type,
            request_hash=request_hash,
        )

        db.add(new_quote)
        db.flush()

        slug = slugify_name(data.client_name)
        sequence = f"{new_quote.id:04d}"
        quote_number = f"{slug}-{sequence}"

        payload, total_amount = build_quote_payload(data, quote_number)

        if data.show_pricing:
            result = generate_priced_quote_file(payload, quote_number)
        else:
            result = generate_scope_quote_file(payload, quote_number)

        new_quote.client_quote_number = quote_number
        new_quote.total_amount = total_amount
        new_quote.quote_data = payload
        new_quote.cached_pdf_path = result["pdf_path"]

        db.commit()
        db.refresh(new_quote)

        return FileResponse(
            result["pdf_path"],
            media_type="application/pdf",
            filename=f"{quote_number}-quote.pdf",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create quote: {str(e)}")


# quotes preview router =-----------
@router.post("/quote/preview")
def preview_quote(data: QuoteRequest):
    try:
        slug = slugify_name(data.client_name)
        preview_number = f"{slug}-preview"
        payload, _ = build_quote_payload(data, slug)

        if data.show_pricing:
            result = generate_priced_quote_file(payload, preview_number)
        else:
            result = generate_scope_quote_file(payload, preview_number)

        return FileResponse(
            result["pdf_path"],
            media_type="application/pdf",
            filename="quote-preview.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get all quotes in the db
@router.get("/quote_db")
def get_all_quotes(
    db: Session = Depends(get_db),
    limit: int = 5,
    start_date: date = Query(None),
    end_date: date = Query(None)
):
    query = db.query(Quotes)

    if start_date and end_date:
        query = query.filter(
            Quotes.client_date >= start_date,
            Quotes.client_date <= end_date
        )
    else:
        last_month = date.today() - timedelta(days=30)
        query = query.filter(Quotes.client_date >= last_month)

    quotes = query.order_by(Quotes.client_date.desc()).limit(limit).all()

    return [
        {
            "id": q.id,
            "client_quote_number": q.client_quote_number or "",
            "client_name": q.client_name or "",
            "client_address": q.client_address or "",
            "client_date": q.client_date,
            "total_amount": float(q.total_amount or 0.0),
            "cached_pdf_path": q.cached_pdf_path or f"generated_quotes/{q.client_quote_number}.pdf" or "",
            "status": q.status or "pending",
            "quote_type": q.quote_type or "priced",
        }
        for q in quotes
    ]