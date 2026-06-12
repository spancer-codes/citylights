import os
import json
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from datetime import datetime, date, timedelta
from app.models import Invoices
from app.schemas import InvoiceRequest, InvoiceOut
from app.db.database import get_db
from app.services.quote_invoice_generators import generate_invoice_file
from app.utils.quote_invoice_utils import slugify_name, build_invoice_payload

from sqlalchemy.orm import Session
from app.db.locks import acquire_client_lock, make_request_hash

router = APIRouter()

@router.post("/invoice")
def create_invoice(data: InvoiceRequest, db: Session = Depends(get_db)):
    try:
        today = date.today()
        request_hash = make_request_hash(data)  # fingerprint this exact request

        acquire_client_lock(db, data.client_name, today)

        # ── Look up by content fingerprint, not just client+date ──────────
        existing = db.query(Invoices).filter(
            Invoices.request_hash == request_hash
        ).first()

        if existing:
            if existing.final_pdf_path and os.path.exists(existing.final_pdf_path):
                return FileResponse(
                    existing.final_pdf_path,
                    media_type="application/pdf",
                    filename=f"{existing.invoice_number}-invoice.pdf",
                )

            # Row exists but PDF is missing — regenerate
            pdf_path = generate_invoice_file(
                json.loads(existing.invoice_data), existing.invoice_number
            )
            existing.final_pdf_path = pdf_path
            db.commit()

            return FileResponse(
                pdf_path,
                media_type="application/pdf",
                filename=f"{existing.invoice_number}-invoice.pdf",
            )

        # ── New request — insert row first to get the id ──────────────────
        new_invoice = Invoices(
            client_name=data.client_name,
            client_address=data.client_address,
            client_number=data.client_number,
            client_date=today,
            status="issued",
            is_finalized=True,
            created_at=datetime.utcnow(),
            invoice_number=None,
            total_amount=None,
            invoice_data=None,
            final_pdf_path=None,
            request_hash=request_hash,  # ← stored so retries find this row
        )

        db.add(new_invoice)
        db.flush()

        slug = slugify_name(data.client_name)
        sequence = f"{new_invoice.id:04d}"
        invoice_number = f"{slug}-{sequence}"

        payload, total_amount = build_invoice_payload(data, invoice_number)
        pdf_path = generate_invoice_file(payload, invoice_number)

        new_invoice.invoice_number = invoice_number
        new_invoice.total_amount = total_amount
        new_invoice.invoice_data = json.dumps(payload)
        new_invoice.final_pdf_path = pdf_path

        db.commit()
        db.refresh(new_invoice)

        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{invoice_number}-invoice.pdf",
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create invoice: {str(e)}")

# get all invoices for preview
@router.get("/invoice_db", response_model=List[InvoiceOut])
def get_all_invoices(
    db: Session = Depends(get_db),
    limit: int = 5,
    start_date: date = Query(None),
    end_date: date = Query(None)
):
    try:
        query = db.query(Invoices)

        if start_date and end_date:
            query = query.filter(
                Invoices.client_date >= start_date,
                Invoices.client_date <= end_date
            )
        else:
            last_month = date.today() - timedelta(days=30)
            query = query.filter(Invoices.client_date >= last_month)

        invoices = query.order_by(Invoices.client_date.desc()).limit(limit).all()

        result = []
        for inv in invoices:
            sequence = f"{inv.id:04d}"
            invoice_number = inv.invoice_number or f"{slugify_name(inv.client_name)}-{sequence}"
            pdf_path = inv.final_pdf_path or f"generated_invoices/{invoice_number}.pdf"

            result.append({
                "invoice_number": invoice_number,
                "client_name": inv.client_name or "",
                "client_address": inv.client_address or "",
                "client_date": inv.client_date,
                "invoice": pdf_path
            })

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))