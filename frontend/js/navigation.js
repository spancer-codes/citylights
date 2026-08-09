// navigation.js
// Tab/view switching for the sidebar nav links.

import { state } from "./state.js";
import { MODES } from "./config.js";
import { setRequestStatus } from "./utils.js";
import { resetForm } from "./form.js";
import { loadQuotesList } from "./quotes.js";
import { fetchHistory } from "./history.js";
import { loadDashboard } from "./dashboard.js";

export function navigate(mode, el) {
    document.querySelectorAll(".nav-link").forEach(n => n.classList.remove("active"));
    if (el) el.classList.add("active");

    document.getElementById("dashboardView").style.display = "none";
    document.getElementById("formView").style.display      = "none";
    document.getElementById("quotesView").style.display    = "none";
    document.getElementById("jobsView").style.display      = "none";
    document.getElementById("historyView").style.display   = "none";

    setRequestStatus();

    if (mode === "dashboard") {
        document.getElementById("dashboardView").style.display = "block";
        loadDashboard();
        return;
    }

    if (mode === "quotes") {
        document.getElementById("quotesView").style.display = "block";
        loadQuotesList();
        return;
    }

    if (mode === "jobs") {
        document.getElementById("jobsView").style.display = "block";
        return;
    }

    if (mode === "history") {
        document.getElementById("historyView").style.display = "block";
        fetchHistory();
        return;
    }

    // receipt / quote form modes
    state.currentMode = mode;
    document.getElementById("pageTitle").innerText    = MODES[mode].title;
    document.getElementById("formView").style.display = "block";

    document.getElementById("quoteFields").style.display          = mode === "quote"   ? "block" : "none";
    document.getElementById("receiptFields").style.display        = mode === "receipt" ? "block" : "none";
    document.getElementById("quoteReuseSection").style.display    = mode === "quote"   ? "block" : "none";
    document.getElementById("invoiceReuseSection").style.display  = mode === "receipt" ? "block" : "none";

    document.getElementById("invoiceBtn").style.display      = mode === "receipt" ? "inline-block" : "none";
    document.getElementById("previewQuoteBtn").style.display = mode === "quote"   ? "inline-block" : "none";
    document.getElementById("saveQuoteBtn").style.display    = mode === "quote"   ? "inline-block" : "none";

    resetForm();
}

export function setupNavigation() {
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function () {
            navigate(this.dataset.mode, this);
        });
    });
}
