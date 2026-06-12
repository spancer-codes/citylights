from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Boolean, ForeignKey, Text
from .db.database import Base
from datetime import datetime

class Quotes(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    client_quote_number = Column(String,unique=True, nullable=True)
    client_date = Column(DateTime, index=True)
    client_name = Column(String, index=True)
    client_address = Column(String, index=True)
    total_amount = Column(Float, nullable=True)
    status = Column(String, nullable=True, default="pending")
    quote_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 
    cached_pdf_path = Column(String, nullable=True)
    request_hash = Column(String, unique=True, nullable=True, index=True)
          
class Invoices(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    client_number = Column(String, index=True)
    source_quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=True)
    client_name = Column(String, index=True)
    client_address = Column(String, index=True)
    client_date = Column(DateTime, index=True)
    total_amount = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="pending")
    is_finalized = Column(Boolean, nullable=False, default=False)
    invoice_data = Column(JSON, nullable=True)
    final_pdf_path = Column(String, nullable=True)
    created_at = Column(DateTime, index=True)
    invoice_number = Column(String, nullable=True, unique=True, index=True)
    request_hash = Column(String, unique=True, nullable=True, index=True)

# Whatsapp generated quote models
class AIGeneratedQuote(Base):
    __tablename__ = "ai_generated_quotes"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, default="whatsapp")  # whatsapp, email, manual
    raw_message = Column(Text, nullable=False)

    extracted_client_name = Column(String, nullable=True)
    selected_client_name = Column(String, nullable=True)
    client_address = Column(String, nullable=True)
    client_city = Column(String, nullable=True)

    job_type = Column(String, nullable=True)
    location = Column(String, nullable=True)

    extracted_items = Column(JSON, nullable=True) # raw AI extracted items
    edited_items_json = Column(JSON, nullable=True)      # final reviewed items

    subtotal = Column(Float, nullable=True)
    tax = Column(Float, default=0)
    discount = Column(Float, default=0)
    total = Column(Float, nullable=True)

    status = Column(String, default="pending_review")
    # pending_client, pending_review, approved, rejected, converted

    validation_notes = Column(Text, nullable=True)

    final_quote_id = Column(Integer, ForeignKey("quotes.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)