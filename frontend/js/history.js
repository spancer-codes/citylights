import {
    SEARCH_API,
    QUOTE_HISTORY_API,
    INVOICE_HISTORY_API
} from "./config.js";
import {
    escapeHtml,
    formatMoney,
    getQuoteNumber,
    getQuotePdfPath,
    getQuoteTotalAmount,
    getInvoiceNumber,
    getInvoicePdfPath
} from "./utils.js";
import { previewPdf } from "./pdf.js";
import { convertQuoteToInvoice } from "./invoices.js";

export async function fetchHistory() {
    const start = document.getElementById("startDate").value;
    const end   = document.getElementById("endDate").value;

    let quoteUrl   = QUOTE_HISTORY_API;
    let invoiceUrl = INVOICE_HISTORY_API;

    if (start && end) {
        quoteUrl   += `?start_date=${start}&end_date=${end}`;
        invoiceUrl += `?start_date=${start}&end_date=${end}`;
    }

    try {
        const [quotesRes, invoicesRes] = await Promise.all([
            fetch(quoteUrl),
            fetch(invoiceUrl)
        ]);

        if (!quotesRes.ok || !invoicesRes.ok) {
            alert("Error fetching history");
            return;
        }

        renderQuotes(await quotesRes.json());
        renderInvoices(await invoicesRes.json());

    } catch (error) {
        console.error(error);
        alert("Failed to load history");
    }
}

export function renderQuotes(quotes) {
    const tbody = document.querySelector("#historyQuotesTable tbody");
    tbody.innerHTML = "";

    if (!quotes || quotes.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="table-empty">No quotes found</td></tr>`;
        return;
    }

    quotes.forEach(q => {
        const num        = getQuoteNumber(q);
        const pdfPath    = getQuotePdfPath(q);
        const total      = getQuoteTotalAmount(q);
        const canConvert = (q.status || "").toLowerCase() !== "converted";

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${escapeHtml(num)}</td>
            <td>${escapeHtml(q.client_name || "-")}</td>
            <td>${escapeHtml(q.client_address || "-")}</td>
            <td>${q.client_date ? new Date(q.client_date).toLocaleDateString() : "-"}</td>
            <td>${formatMoney(total)}</td>

            <td>
                ${pdfPath
                    ? `<button class="secondary"
                        data-action="preview-quote-pdf"
                        data-quote-id="${q.id}">
                        Preview
                       </button>`
                    : `<span class="muted-text">No PDF</span>`}
            </td>

            <td>
                ${canConvert
                    ? `<button class="primary"
                        data-action="convert-quote"
                        data-quote-id="${q.id}"
                        data-total="${total}"
                        data-number="${escapeHtml(num)}">
                        Convert to Invoice
                       </button>`
                    : `<span class="converted-label">Converted</span>`}
            </td>
        `;

        tbody.appendChild(row);
    });

    /* Preview Quotes */
    tbody.querySelectorAll('[data-action="preview-quote-pdf"]').forEach(btn => {
        btn.addEventListener("click", function () {
            const quoteId = this.dataset.quoteId;
            previewPdf(`/quote/preview/${quoteId}`);
        });
    });

    /* Convert Quote */
    tbody.querySelectorAll('[data-action="convert-quote"]').forEach(btn => {
        btn.addEventListener("click", function () {
            convertQuoteToInvoice(
                Number(this.dataset.quoteId),
                this.dataset.total,
                this.dataset.number,
                fetchHistory
            );
        });
    });
}

export function renderInvoices(invoices) {
    const tbody = document.querySelector("#historyInvoicesTable tbody");
    tbody.innerHTML = "";

    if (!invoices || invoices.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="table-empty">No invoices found</td></tr>`;
        return;
    }

    invoices.forEach(inv => {
        const num     = getInvoiceNumber(inv);
        const pdfPath = getInvoicePdfPath(inv);

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${escapeHtml(num)}</td>
            <td>${escapeHtml(inv.client_name || "-")}</td>
            <td>${escapeHtml(inv.client_address || "-")}</td>
            <td>${inv.client_date ? new Date(inv.client_date).toLocaleDateString() : "-"}</td>

            <td>
                ${pdfPath
                    ? `<button class="secondary"
                        data-action="preview-invoice-pdf"
                        data-invoice-id="${inv.id}">
                        Preview
                       </button>`
                    : `<span class="muted-text">No PDF</span>`}
            </td>
        `;

        tbody.appendChild(row);
    });

    /* Preview Invoices */
    tbody.querySelectorAll('[data-action="preview-invoice-pdf"]').forEach(btn => {
        btn.addEventListener("click", function () {
            const invoiceId = this.dataset.invoiceId;
            previewPdf(`/invoice/preview/${invoiceId}`);
        });
    });
}

export async function searchHistory() {
    const query = document.getElementById("searchInput").value.trim();

    if (!query) {
        fetchHistory();
        return;
    }

    try {
        const res = await fetch(`${SEARCH_API}?search=${encodeURIComponent(query)}`);

        if (!res.ok) {
            alert("Search error");
            return;
        }

        const data = await res.json();

        renderQuotes(data.quotes || []);
        renderInvoices(data.invoices || []);

    } catch (error) {
        console.error(error);
        alert("Search failed");
    }
}