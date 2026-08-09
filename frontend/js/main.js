
import { setupNavigation, navigate } from "./navigation.js";
import { setupQuoteCustomerReuse, setupInvoiceCustomerReuse } from "./customers.js";
import { addRow } from "./form.js";
import { previewQuote, saveQuote } from "./quotes.js";
import { submitInvoice } from "./invoices.js";
import { fetchHistory, searchHistory } from "./history.js";
import { setupPdfModal } from "./pdf.js";

function setupFormButtons() {
    document.getElementById("addItemBtn").addEventListener("click", () => addRow());
    document.getElementById("invoiceBtn").addEventListener("click", submitInvoice);
    document.getElementById("previewQuoteBtn").addEventListener("click", previewQuote);
    document.getElementById("saveQuoteBtn").addEventListener("click", saveQuote);
}

function setupHistoryButtons() {
    const historyView = document.getElementById("historyView");
    const filterBtn = historyView.querySelector(".filters button.primary");
    const buttons = historyView.querySelectorAll(".filters button.primary");
    // First "Filter" button triggers fetchHistory, second "Search" button triggers searchHistory
    if (buttons[0]) buttons[0].addEventListener("click", fetchHistory);
    if (buttons[1]) buttons[1].addEventListener("click", searchHistory);
}

document.addEventListener("DOMContentLoaded", () => {
    setupNavigation();
    setupQuoteCustomerReuse();
    setupInvoiceCustomerReuse();
    setupFormButtons();
    setupHistoryButtons();
    setupPdfModal();

    navigate("receipt", document.querySelector(".nav-link.active"));
});
