// invoices.js
// Invoice generation and the quote -> invoice conversion flow.

import { state } from "./state.js";
import { INVOICE_API } from "./config.js";
import { setRequestStatus, setButtonLoading, formatMoney } from "./utils.js";
import { buildInvoicePayload } from "./form.js";
import { downloadBlob, previewPdf } from "./pdf.js";

export async function submitInvoice() {
    if (state.isSubmittingInvoice || state.isSavingQuote || state.isPreviewingQuote) return;
    const payload = buildInvoicePayload();
    if (!payload) return;

    const btn = document.getElementById("invoiceBtn");
    state.isSubmittingInvoice = true;
    setButtonLoading(btn, "Generating Invoice...", true);
    document.getElementById("addItemBtn").disabled = true;
    setRequestStatus("Generating invoice and preparing download. Please wait...", "info");

    try {
        const res = await fetch(INVOICE_API, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.text();
            throw new Error(err);
        }
        const blob = await res.blob();
        setRequestStatus("Invoice generated successfully.", "success");
        downloadBlob(blob, "invoice.pdf");
    } catch (error) {
        console.error("Invoice error:", error);
        setRequestStatus("Invoice request failed.", "error");
    } finally {
        state.isSubmittingInvoice = false;
        setButtonLoading(btn, "Generating Invoice...", false);
        document.getElementById("addItemBtn").disabled = false;
    }
}

// fetchHistoryRef is injected at call time (rather than imported directly)
// to avoid a circular import between invoices.js and history.js, since
// history.js renders the "Convert to Invoice" buttons that call this function.
export async function convertQuoteToInvoice(quoteId, quoteTotal, quoteNumber, fetchHistoryRef) {
    const total = Number(quoteTotal);
    if (!quoteId)              { alert("Quote ID is missing.");                            return; }
    if (!total || total <= 0)  { alert("This quote does not have a valid total amount.");  return; }

    const minAmount  = total * 0.60;
    const amountText = prompt(
        `Enter amount paid for quote ${quoteNumber}.\nMinimum allowed: ${formatMoney(minAmount)}\nMaximum allowed: ${formatMoney(total)}`
    );
    if (amountText === null) return;

    const amountPaid = Number(amountText);
    if (Number.isNaN(amountPaid)) { alert("Please enter a valid amount.");                                                          return; }
    if (amountPaid > total)        { alert("Amount paid cannot exceed the quote amount.");                                          return; }
    if (amountPaid < minAmount)    { alert(`Amount paid cannot be less than 60% of the quote amount.\nMinimum required: ${formatMoney(minAmount)}`); return; }

    const confirmed = confirm(
        `Are you sure you want to convert quote ${quoteNumber} to an invoice?\n\nQuote Total: ${formatMoney(total)}\nAmount Paid: ${formatMoney(amountPaid)}`
    );
    if (!confirmed) return;

    try {
        setRequestStatus("Converting quote to invoice. Please wait...", "info");
        const res  = await fetch(`/quotes/${quoteId}/convert-to-invoice`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ amount_paid: amountPaid })
        });
        const data = await res.json();

        if (!res.ok || data["failed to convert quote"]) {
            alert(data["failed to convert quote"] || "Failed to convert quote.");
            setRequestStatus("Failed to convert quote to invoice.", "error");
            return;
        }

        const filePath = data.final_pdf_path;
        if (!filePath) {
            alert("Invoice was created, but no PDF path was returned.");
            setRequestStatus("Invoice created, but preview path is missing.", "error");
            if (fetchHistoryRef) fetchHistoryRef();
            return;
        }

        previewPdf(`/pdf/invoice/${encodeURIComponent(filePath.split("/").pop())}`);
        setRequestStatus("Quote converted successfully. New invoice is ready.", "success");
        if (fetchHistoryRef) fetchHistoryRef();
    } catch (error) {
        console.error(error);
        alert("Conversion request failed.");
        setRequestStatus("Conversion request failed.", "error");
    }
}
