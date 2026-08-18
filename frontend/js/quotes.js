import { state } from "./state.js";
import { QUOTE_PREVIEW_API, QUOTE_SAVE_API, QUOTE_HISTORY_API } from "./config.js";
import { setRequestStatus, setButtonLoading, escapeHtml, formatMoney, getQuoteNumber, getQuotePdfPath, getQuoteTotalAmount } from "./utils.js";
import { buildQuotePayload } from "./form.js";
import { openPdfBlob, downloadBlob, previewPdf } from "./pdf.js";

export async function previewQuote() {
    if (state.isPreviewingQuote || state.isSavingQuote || state.isSubmittingInvoice) return;
    const payload = buildQuotePayload();
    if (!payload) return;

    const btn = document.getElementById("previewQuoteBtn");
    state.isPreviewingQuote = true;
    setButtonLoading(btn, "Preparing Preview...", true);
    document.getElementById("saveQuoteBtn").disabled = true;
    setRequestStatus("Generating quote preview. Please wait...", "info");

    try {
        const res = await fetch(QUOTE_PREVIEW_API, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.text();
            setRequestStatus("Failed to generate quote preview.", "error");
            alert("Preview error: " + err);
            return;
        }
        openPdfBlob(await res.blob());
        setRequestStatus("Quote preview loaded successfully.", "success");
    } catch (error) {
        console.error(error);
        setRequestStatus("Preview request failed.", "error");
        alert("Preview request failed.");
    } finally {
        state.isPreviewingQuote = false;
        setButtonLoading(btn, "Preparing Preview...", false);
        if (!state.isSavingQuote && !state.isSubmittingInvoice) {
            document.getElementById("saveQuoteBtn").disabled = false;
        }
    }
}

export async function saveQuote() {
    if (state.isSavingQuote || state.isPreviewingQuote || state.isSubmittingInvoice) return;
    const payload = buildQuotePayload();
    if (!payload) return;

    const btn        = document.getElementById("saveQuoteBtn");
    const previewBtn = document.getElementById("previewQuoteBtn");

    state.isSavingQuote = true;
    setButtonLoading(btn, "Processing Quote...", true);
    if (previewBtn) previewBtn.disabled = true;
    document.getElementById("addItemBtn").disabled = true;
    setRequestStatus("Saving quote and preparing download. Please wait...", "info");

    try {
        const res = await fetch(QUOTE_SAVE_API, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.text();
            setRequestStatus("Failed to save quote.", "error");
            alert("Save error: " + err);
            return;
        }
        const blob = await res.blob();
        if (!blob || blob.size === 0) {
            setRequestStatus("Received empty file from server.", "error");
            alert("Save error: server returned an empty file.");
            return;
        }
        downloadBlob(blob, "quote.pdf");
        setRequestStatus("Quote saved successfully. Download should start automatically.", "success");
    } catch (error) {
        console.error(error);
        setRequestStatus("Save and download failed.", "error");
        alert("Save and download failed: " + error.message);
    } finally {
        state.isSavingQuote = false;
        setButtonLoading(btn, "Processing Quote...", false);
        if (previewBtn) previewBtn.disabled = false;
        document.getElementById("addItemBtn").disabled = false;
    }
}

export async function loadQuotesList() {
    const container = document.getElementById("quotesList");
    container.innerHTML = `<div class="empty-state">Loading quotes…</div>`;
    try {
        const res = await fetch(QUOTE_HISTORY_API);
        if (!res.ok) throw new Error("Failed to fetch quotes");
        const quotes = await res.json();
        if (!quotes || quotes.length === 0) {
            container.innerHTML = `<div class="empty-state">No quotes available yet.</div>`;
            return;
        }
        container.innerHTML = `
            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>Quote Number</th>
                            <th>Client Name</th>
                            <th>Address</th>
                            <th>Date</th>
                            <th>Type</th>
                            <th>Total Amount</th>
                            <th>Preview</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${quotes.map(q => {
                            const num       = getQuoteNumber(q);
                            const pdfPath   = getQuotePdfPath(q);
                            const total     = getQuoteTotalAmount(q);
                            const isScope   = (q.quote_type || "priced") === "scope_only";
                            const typeLabel = isScope ? "Scope Only" : "Priced";
                            const typeClass = isScope ? "badge-scope" : "badge-priced";
                            return `
                                <tr>
                                    <td>${escapeHtml(num)}</td>
                                    <td>${escapeHtml(q.client_name || "-")}</td>
                                    <td>${escapeHtml(q.client_address || "-")}</td>
                                    <td>${q.client_date ? new Date(q.client_date).toLocaleDateString() : "-"}</td>
                                    <td><span class="type-badge ${typeClass}">${typeLabel}</span></td>
                                    <td>${isScope ? "-" : formatMoney(total)}</td>
                                    <td>
                                        ${pdfPath
                                            ? `<button class="secondary" data-pdf-path="${escapeHtml(pdfPath)}" data-action="preview-quote-pdf">Preview</button>`
                                            : `<span class="muted-text">No PDF</span>`}
                                    </td>
                                </tr>`;
                        }).join("")}
                    </tbody>
                </table>
            </div>`;

        container.querySelectorAll('[data-action="preview-quote-pdf"]').forEach(btn => {
            btn.addEventListener("click", function () {
                const fileName = this.dataset.pdfPath.split("/").pop();
                previewPdf(`/pdf/quote/${encodeURIComponent(fileName)}`);
            });
        });
    } catch (err) {
        console.error(err);
        container.innerHTML = `<div class="empty-state">Failed to load quotes.</div>`;
    }
}