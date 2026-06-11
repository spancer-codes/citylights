INVOICE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
 
  body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13px;
    color: #1a1a2e;
    background: #fff;
  }
 
  /* ── Page setup ── */
  @page {
    size: A4;
    margin: 0;
  }
 
  .page {
    width: 210mm;
    min-height: 297mm;
    padding: 0;
    display: flex;
    flex-direction: column;
  }
 
  /* ── Header bar ── */
  .header {
    background: #1B3A6B;
    color: #fff;
    padding: 28px 36px 24px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }
 
  .brand-name {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #fff;
  }
 
  .brand-tagline {
    font-size: 10px;
    color: rgba(255,255,255,0.55);
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 4px;
  }
 
  .invoice-meta-right { text-align: right; }
 
  .invoice-meta-right .label {
    font-size: 10px;
    color: rgba(255,255,255,0.55);
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }
 
  .invoice-meta-right .number {
    font-size: 14px;
    font-weight: 700;
    color: #0D7377;
    margin-top: 3px;
  }
 
  .invoice-meta-right .date {
    font-size: 11px;
    color: rgba(255,255,255,0.65);
    margin-top: 6px;
  }
 
  /* ── Body ── */
  .body { padding: 28px 36px; flex: 1; }
 
  /* ── Parties row ── */
  .parties {
    display: flex;
    gap: 24px;
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 0.5px solid #d0d4dc;
  }
 
  .party { flex: 1; }
 
  .party-label {
    font-size: 10px;
    font-weight: 700;
    color: #8a92a6;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
  }
 
  .party-name {
    font-size: 14px;
    font-weight: 700;
    color: #1B3A6B;
  }
 
  .party-detail {
    font-size: 12px;
    color: #5a6275;
    margin-top: 2px;
  }
 
  /* ── Items table ── */
  .items-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
  }
 
  .items-table thead tr {
    background: #1B3A6B;
    color: #fff;
  }
 
  .items-table thead th {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 10px 12px;
    text-align: left;
  }
 
  .items-table thead th.r { text-align: right; }
 
  .items-table tbody tr:nth-child(odd)  { background: #eef1f8; }
  .items-table tbody tr:nth-child(even) { background: #dce2f2; }
 
  .items-table tbody td {
    padding: 10px 12px;
    font-size: 12px;
    color: #1a1a2e;
    vertical-align: top;
  }
 
  .items-table tbody td.r { text-align: right; }
  .items-table tbody td.num { color: #3a3f52; }
 
  .item-name { font-weight: 700; }
  .item-note { font-size: 10px; color: #6b7385; margin-top: 2px; }
 
  /* ── Totals ── */
  .totals-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 28px;
  }
 
  .totals-box { width: 220px; }
 
  .totals-row {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #5a6275;
    padding: 4px 0;
  }
 
  .totals-row.grand {
    border-top: 2px solid #1B3A6B;
    margin-top: 6px;
    padding-top: 8px;
    font-size: 15px;
    font-weight: 700;
    color: #1a1a2e;
  }
 
  .totals-row.grand .amt { color: #1B3A6B; }
 
  /* ── Footer ── */
  .footer {
    border-top: 0.5px solid #d0d4dc;
    padding-top: 20px;
    display: flex;
    gap: 24px;
  }
 
  .footer-block { flex: 1; }
 
  .footer-label {
    font-size: 10px;
    font-weight: 700;
    color: #8a92a6;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
  }
 
  .footer-row {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    padding: 3px 0;
    border-bottom: 0.5px solid #eef1f8;
  }
 
  .footer-row .key { color: #8a92a6; }
  .footer-row .val { font-weight: 700; color: #1a1a2e; }
 
  .note-box {
    background: #e8f7f5;
    border-left: 3px solid #0D7377;
    padding: 10px 12px;
    font-size: 11px;
    color: #085041;
    border-radius: 0 4px 4px 0;
    margin-top: 2px;
  }
 
  .vat-note {
    font-size: 10px;
    color: #8a92a6;
    font-style: italic;
    margin-top: 8px;
  }
 
  /* ── Bottom strip ── */
  .bottom-strip {
    background: #1B3A6B;
    color: rgba(255,255,255,0.45);
    font-size: 9px;
    text-align: center;
    padding: 8px 36px;
    letter-spacing: 0.06em;
  }
</style>
</head>
<body>
<div class="page">
 
  <!-- Header -->
  <div class="header">
    <div>
      <div class="brand-name">⚡ CITY LIGHTS</div>
      <div class="brand-tagline">Electrical Services</div>
    </div>
    <div class="invoice-meta-right">
      <div class="label">Invoice</div>
      <div class="number"># {{ invoice_number }}</div>
      <div class="date">{{ date_created }}</div>
    </div>
  </div>
 
  <!-- Body -->
  <div class="body">
 
    <!-- Parties -->
    <div class="parties">
      <div class="party">
        <div class="party-label">Billed to</div>
        <div class="party-name">{{ client_name }}</div>
        {% if client_address %}<div class="party-detail">{{ client_address }}</div>{% endif %}
        {% if client_number %}<div class="party-detail">{{ client_number }}</div>{% endif %}
      </div>
      <div class="party">
        <div class="party-label">From</div>
        <div class="party-name">Leeroy</div>
        <div class="party-detail">Leeroy Antony Muzondi</div>
      </div>
    </div>
 
    <!-- Items -->
    <table class="items-table">
      <thead>
        <tr>
          <th style="width:32px">#</th>
          <th>Description</th>
          <th class="r" style="width:50px">Qty</th>
          {% if show_ex_vat %}
            <th class="r" style="width:90px">Price (ex. VAT)</th>
          {% endif %}
          <th class="r" style="width:90px">Unit Price</th>
          <th class="r" style=width:90px">Discount</th>
          <th class="r" style="width:90px">Total</th>
        </tr>
      </thead>
      <tbody>
        {% for item in items %}
        <tr>
          <td class="num">{{ loop.index }}</td>
          <td>
            <div class="item-name">{{ item.description }}</div>
            {% if item.note %}<div class="item-note">{{ item.note }}</div>{% endif %}
          </td>
          <td class="r num">
            {% if item.description|lower != "tax total" %}{{ item.quantity }}{% endif %}
          {% if show_ex_vat %}
            <td class="r num">
            {% if item.description|lower != "labour" %}
                R{{ "%.2f"|format(item.unit_price_ex_vat) }}
            {% endif %}
            </td>
            {% endif %}
          <td class="r num">
            {% if item.description|lower == "labour" %}
              R{{ "%.2f"|format(item.unit_price_ex_vat) }}
            {% else %}
              R{{ "%.2f"|format(item.unit_price_inc_vat) }}
            {% endif %}
          </td>
          <td class="r num">
            {% set expected = item.quantity * item.unit_price_ex_vat %}
            {% set discount = expected - item.line_total %}
            {% if discount > 0 %}
                R{{ "%.2f"|format(discount) }}
            {% endif %}
          </td>
          <td class="r num" style="font-weight:700">R{{ "%.2f"|format(item.line_total) }}</td>
          
        </tr>
        {% endfor %}
      </tbody>
    </table>
 
    <!-- Totals -->
    <div class="totals-wrap">
      <div class="totals-box">
        <div class="totals-row"><span>Subtotal</span><span>R{{ "%.2f"|format(subtotal) }}</span></div>
        <div class="totals-row"><span>VAT</span><span style="font-style:italic;color:#aab0be">Not registered</span></div>
        <div class="totals-row grand">
          <span>Grand Total</span>
          <span class="amt">R{{ "%.2f"|format(subtotal) }}</span>
        </div>
      </div>
    </div>
 
    <!-- Footer -->
    <div class="footer">
      <div class="footer-block">
        <div class="footer-label">Banking details</div>
        <div class="footer-row"><span class="key">Account holder</span><span class="val">Leeroy Antony Muzondi</span></div>
        <div class="footer-row"><span class="key">Bank</span><span class="val">Bidvest Bank Alliance</span></div>
        <div class="footer-row"><span class="key">Branch code</span><span class="val">683000</span></div>
        <div class="footer-row"><span class="key">Account type</span><span class="val">Current</span></div>
        <div class="footer-row"><span class="key">Account number</span><span class="val">7860 2801 824</span></div>
        <div class="vat-note">Not VAT registered</div>
      </div>
      <div class="footer-block">
        <div class="footer-label">Payment note</div>
        <div class="note-box">
          Please ensure payment is directed to Bidvest Bank Alliance,
          branch code <strong>683000</strong>. Use the invoice number
          <strong>{{ invoice_number }}</strong> as your payment reference.
        </div>
      </div>
    </div>
 
  </div><!-- /body -->
 
  <!-- Bottom strip -->
  <div class="bottom-strip">
    City Lights Electrical Services &nbsp;·&nbsp; Invoice {{ invoice_number }}
  </div>
 
</div>
</body>
</html>
"""

QUOTE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: Arial, Helvetica, sans-serif; font-size: 13px; color: #1a1a2e; background: #fff; }
 
  @page { size: A4; margin: 0; }
 
  .page { width: 210mm; min-height: 297mm; display: flex; flex-direction: column; }
 
  /* ── Header ── */
  .header {
    background: #1B3A6B; color: #fff;
    padding: 28px 36px 24px;
    display: flex; justify-content: space-between; align-items: flex-start;
  }
  .brand-name { font-size: 22px; font-weight: 700; letter-spacing: 0.06em; color: #fff; }
  .brand-tagline { font-size: 10px; color: rgba(255,255,255,0.55); letter-spacing: 0.14em; text-transform: uppercase; margin-top: 4px; }
  .header-right { text-align: right; }
  .header-right .label { font-size: 10px; color: rgba(255,255,255,0.55); text-transform: uppercase; letter-spacing: 0.1em; }
  .header-right .number { font-size: 14px; font-weight: 700; color: #0D7377; margin-top: 3px; }
  .header-right .q-date { font-size: 11px; color: rgba(255,255,255,0.65); margin-top: 6px; }
 
  /* ── Body ── */
  .body { padding: 28px 36px; flex: 1; }
 
  /* ── Parties ── */
  .parties { display: flex; gap: 24px; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 0.5px solid #d0d4dc; }
  .party { flex: 1; }
  .party-label { font-size: 10px; font-weight: 700; color: #8a92a6; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
  .party-name { font-size: 14px; font-weight: 700; color: #1B3A6B; }
  .party-detail { font-size: 12px; color: #5a6275; margin-top: 2px; }
 
  /* ── Items table ── */
  .items-table { width: 100%; border-collapse: collapse; margin-bottom: 16px; }
  .items-table thead tr { background: #1B3A6B; color: #fff; }
  .items-table thead th { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; padding: 10px 12px; text-align: left; }
  .items-table thead th.r { text-align: right; }
  .items-table tbody tr:nth-child(odd)  { background: #eef1f8; }
  .items-table tbody tr:nth-child(even) { background: #dce2f2; }
  .items-table tbody td { padding: 10px 12px; font-size: 12px; color: #1a1a2e; vertical-align: top; }
  .items-table tbody td.r { text-align: right; color: #3a3f52; }
  .item-name { font-weight: 700; }
  .item-note { font-size: 10px; color: #6b7385; margin-top: 2px; }
 
  /* ── Totals ── */
  .totals-wrap { display: flex; justify-content: flex-end; margin-bottom: 28px; }
  .totals-box { width: 240px; }
  .totals-row { display: flex; justify-content: space-between; font-size: 12px; color: #5a6275; padding: 4px 0; }
  .totals-row.grand { border-top: 2px solid #1B3A6B; margin-top: 6px; padding-top: 8px; font-size: 15px; font-weight: 700; color: #1a1a2e; }
  .totals-row.grand .amt { color: #1B3A6B; }
  .totals-row.deposit { background: #e8f7f5; padding: 6px 8px; border-radius: 4px; margin-top: 6px; font-size: 12px; color: #085041; font-weight: 700; }
 
  /* ── Terms ── */
  .terms { margin-bottom: 24px; }
  .terms-label { font-size: 10px; font-weight: 700; color: #8a92a6; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
  .terms-item { font-size: 11px; color: #5a6275; padding: 4px 0; display: flex; gap: 8px; }
  .terms-item .tnum { color: #0D7377; font-weight: 700; min-width: 16px; }
 
  /* ── Footer ── */
  .footer { border-top: 0.5px solid #d0d4dc; padding-top: 20px; display: flex; gap: 24px; }
  .footer-block { flex: 1; }
  .footer-label { font-size: 10px; font-weight: 700; color: #8a92a6; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
  .footer-row { display: flex; justify-content: space-between; font-size: 11px; padding: 3px 0; border-bottom: 0.5px solid #eef1f8; }
  .footer-row .key { color: #8a92a6; }
  .footer-row .val { font-weight: 700; color: #1a1a2e; }
  .note-box { background: #e8f7f5; border-left: 3px solid #0D7377; padding: 10px 12px; font-size: 11px; color: #085041; border-radius: 0 4px 4px 0; margin-top: 2px; }
 
  /* ── Bottom strip ── */
  .bottom-strip { background: #1B3A6B; color: rgba(255,255,255,0.45); font-size: 9px; text-align: center; padding: 8px 36px; letter-spacing: 0.06em; }
</style>
</head>
<body>
<div class="page">
 
  <!-- Header -->
  <div class="header">
    <div>
      <div class="brand-name">CITY LIGHTS</div>
      <div class="brand-tagline">Electrical Services</div>
    </div>
    <div class="header-right">
      <div class="label">Quotation</div>
      <div class="number"># {{ quote_number }}</div>
      <div class="q-date">{{ date_created }}</div>
    </div>
  </div>
 
  <div class="body">
 
    <!-- Parties -->
    <div class="parties">
      <div class="party">
        <div class="party-label">Quotation to</div>
        <div class="party-name">{{ client_name }}</div>
        {% if client_address %}<div class="party-detail">{{ client_address }}</div>{% endif %}
        {% if client_city %}<div class="party-detail">{{ client_city }}</div>{% endif %}
        {% if client_email %}<div class="party-detail">{{ client_email }}</div>{% endif %}
        {% if client_number %}<div class="party-detail">{{ client_number }}</div>{% endif %}
      </div>
      <div class="party">
        <div class="party-label">Quotation from</div>
        <div class="party-name">Lee Electrician</div>
        <div class="party-detail">Leeroy Antony Muzondi</div>
      </div>
    </div>
 
    <!-- Items -->
    <table class="items-table">
      <thead>
        <tr>
          <th style="width:32px">#</th>
          <th>Item Description</th>
          <th class="r" style="width:55px">Qty</th>
          <th class="r" style="width:100px">Unit Price</th>
          <th class="r" style="width:100px">Total Price</th>
        </tr>
      </thead>
      <tbody>
        {% for item in items %}
        <tr>
          <td>{{ loop.index }}</td>
          <td>
            <div class="item-name">{{ item.description }}</div>
            {% if item.get('note') %}<div class="item-note">{{ item.note }}</div>{% endif %}
          </td>
          <td class="r">{{ item.quantity }}</td>
          <td class="r">R{{ "%.2f"|format(item.unit_price) }}</td>
          <td class="r" style="font-weight:700">R{{ "%.2f"|format(item.line_total) }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
 
    <!-- Totals -->
    <div class="totals-wrap">
      <div class="totals-box">
        <div class="totals-row"><span>Subtotal</span><span>R{{ "%.2f"|format(grand_total) }}</span></div>
        <div class="totals-row"><span>VAT (incl.)</span><span>All prices inclusive</span></div>
        <div class="totals-row grand"><span>Grand Total</span><span class="amt">R{{ "%.2f"|format(grand_total) }}</span></div>
        {% if deposit_percent %}
        <div class="totals-row deposit">
          <span>{{ deposit_percent }}% Deposit required</span>
          <span>R{{ "%.2f"|format(grand_total * deposit_percent / 100) }}</span>
        </div>
        {% endif %}
      </div>
    </div>
 
    <!-- Terms & Conditions -->
    {% if terms %}
    <div class="terms">
      <div class="terms-label">Terms &amp; Conditions</div>
      {% for term in terms %}
      <div class="terms-item"><span class="tnum">{{ loop.index }}.</span><span>{{ term }}</span></div>
      {% endfor %}
    </div>
    {% endif %}
 
    <!-- Footer -->
    <div class="footer">
      <div class="footer-block">
        <div class="footer-label">Banking details</div>
        <div class="footer-row"><span class="key">Account holder</span><span class="val">Leeroy Antony Muzondi</span></div>
        <div class="footer-row"><span class="key">Bank</span><span class="val">Bidvest Bank Alliance</span></div>
        <div class="footer-row"><span class="key">Branch code</span><span class="val">683000</span></div>
        <div class="footer-row"><span class="key">Account type</span><span class="val">Current</span></div>
        <div class="footer-row"><span class="key">Account number</span><span class="val">7860 2801 824</span></div>
      </div>
      <div class="footer-block">
        <div class="footer-label">Payment note</div>
        <div class="note-box">
          Please ensure payment is directed to Bidvest Bank Alliance,
          branch code <strong>683000</strong>. Use quote number
          <strong>{{ quote_number }}</strong> as your payment reference.
        </div>
      </div>
    </div>
 
  </div>
 
  <div class="bottom-strip">
    City Lights Electrical Services &nbsp;·&nbsp; Quotation {{ quote_number }}
  </div>
 
</div>
</body>
</html>
"""