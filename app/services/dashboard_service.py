from sqlalchemy.orm import Session
from sqlalchemy import func, text
from app.models import Quotes, Invoices

def get_basic_stats(db: Session) -> dict:
    total_quotes = db.query(func.count(Quotes.id)).scalar()
    total_invoices = db.query(func.count(Invoices.id)).scalar()
    converted_quotes = db.query(func.count(Invoices.id))\
        .filter(Invoices.source_quote_id.is_not(None))\
        .scalar()
    if total_quotes > 0:
        conversion_rate = (converted_quotes / total_quotes)
   
    return {
        "total_quotes": total_quotes,
        "total_invoices": total_invoices,
        "total_quotes_converted": converted_quotes,
        "conversion_rate": conversion_rate
    }
def get_revenue_stats(db: Session) ->list:
    results = db.execute(text("""
        SELECT
            to_char(i.client_date, 'Mon YYYY') AS month,
            SUM(
                CASE 
                    WHEN item->>'description' ILIKE '%labour%' 
                    THEN (item->>'line_total')::float
                    ELSE 0
                END
            ) AS revenue
        FROM invoices i,
        LATERAL jsonb_array_elements(i.invoice_data::jsonb->'items') AS item
        GROUP BY month, date_trunc('month', i.client_date)
        ORDER BY date_trunc('month', i.client_date);
    """)).fetchall()
    return [
        {
            "month": row.month, 
            "revenue": float(row.revenue) if row.revenue is not None else 0.0
        }
        for row in results
    ]
def get_invoices_per_month(db: Session) -> list:
    results = db.query(func.to_char(Invoices.client_date, "Mon YYYY").label('month'),
                       func.count(Invoices.id).label("count")
                       )\
                       .group_by(func.to_char(Invoices.client_date, "Mon YYYY"))\
                       .order_by(func.min(Invoices.client_date))\
                       .all()
    return [
        {
            "month": row.month,
            "count": row.count
        }
        for row in results
    ]

def get_dashboard_data(db: Session) -> dict:
    return{
        **get_basic_stats(db),
        "montthly_revenue": get_revenue_stats(db),
        "invoices_per_month": get_invoices_per_month(db)
    }