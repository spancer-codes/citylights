// utils.js
// Pure helper functions: formatting, escaping, and small data accessors.
// Nothing here touches event listeners or app state.

export function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g,  "&amp;")
        .replace(/</g,  "&lt;")
        .replace(/>/g,  "&gt;")
        .replace(/"/g,  "&quot;")
        .replace(/'/g,  "&#039;");
}

export function setRequestStatus(message = "", type = "info") {
    const el = document.getElementById("requestStatus");
    if (!el) return;
    if (!message) {
        el.className   = "status-box";
        el.textContent = "";
        return;
    }
    el.className   = `status-box ${type}`;
    el.textContent = message;
}

export function setButtonLoading(button, loadingText, isLoading) {
    if (!button) return;
    if (isLoading) {
        if (!button.dataset.originalText) {
            button.dataset.originalText = button.innerText;
        }
        button.innerText = loadingText;
        button.disabled  = true;
    } else {
        button.innerText = button.dataset.originalText || button.innerText;
        button.disabled  = false;
    }
}

export function getQuotePdfPath(q)    { return q.cached_pdf_path || q.client_quote_pdf || ""; }
export function getInvoicePdfPath(inv) { return inv.final_pdf_path || inv.client_invoice_pdf || inv.invoice || ""; }
export function getQuoteNumber(q)      { return q.client_quote_number || q.quote_number || "-"; }
export function getInvoiceNumber(inv)  { return inv.invoice_number || inv.client_invoice_number || "-"; }

export function getQuoteTotalAmount(q) {
    const direct = Number(q.total_amount);
    if (!Number.isNaN(direct) && direct > 0) return direct;
    try {
        const payload = typeof q.quote_data === "string" ? JSON.parse(q.quote_data) : q.quote_data;
        const total   = Number(payload?.total);
        if (!Number.isNaN(total)) return total;
    } catch (e) {
        // quote_data wasn't valid JSON or didn't have a usable total — fall through to 0
    }
    return 0;
}

export function formatMoney(amount) {
    return Number(amount || 0).toFixed(2);
}
