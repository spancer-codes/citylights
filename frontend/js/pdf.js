// pdf.js
// Blob download helper and PDF preview modal control.

import { state } from "./state.js";

export function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a   = document.createElement("a");
    a.href     = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function openPdfBlob(blob) {
    if (state.previewBlobUrl) URL.revokeObjectURL(state.previewBlobUrl);
    state.previewBlobUrl = URL.createObjectURL(blob);
    document.getElementById("pdfFrame").src           = state.previewBlobUrl;
    document.getElementById("pdfModal").style.display = "flex";
}

export function previewPdf(url) {
    if (state.previewBlobUrl) {
        URL.revokeObjectURL(state.previewBlobUrl);
        state.previewBlobUrl = null;
    }
    document.getElementById("pdfFrame").src           = url;
    document.getElementById("pdfModal").style.display = "flex";
}

export function closePdf() {
    document.getElementById("pdfFrame").src           = "";
    document.getElementById("pdfModal").style.display = "none";
    if (state.previewBlobUrl) {
        URL.revokeObjectURL(state.previewBlobUrl);
        state.previewBlobUrl = null;
    }
}

export function setupPdfModal() {
    const closeBtn = document.querySelector("#pdfModal .modal-close");
    if (closeBtn) closeBtn.addEventListener("click", closePdf);
}
