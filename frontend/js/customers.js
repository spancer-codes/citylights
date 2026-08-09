// customers.js
// "Use previous customer details" picker logic for both the quote and
// invoice forms. Two near-identical pipelines (quote vs invoice) kept as
// separate function pairs rather than abstracted, matching the original
// code's structure and the form's different field sets.

import { state } from "./state.js";
import { QUOTE_CUSTOMERS_API, INVOICE_CUSTOMERS_API } from "./config.js";
import { escapeHtml } from "./utils.js";

/* ── Quote customer reuse ────────────────────────────────────────────── */

export async function loadQuoteCustomers() {
    const list = document.getElementById("quoteCustomerList");
    try {
        const response = await fetch(QUOTE_CUSTOMERS_API);
        if (!response.ok) throw new Error("Failed to fetch quote customers");
        state.allQuoteCustomers      = await response.json();
        state.filteredQuoteCustomers = [...state.allQuoteCustomers];
        renderQuoteCustomerList(state.filteredQuoteCustomers);
    } catch (error) {
        console.error("Error loading quote customers:", error);
        list.innerHTML = `<div class="customer-empty">Failed to load previous customers.</div>`;
    }
}

export function renderQuoteCustomerList(customers) {
    const list = document.getElementById("quoteCustomerList");
    if (!customers.length) {
        list.innerHTML = `<div class="customer-empty">No matching customers found.</div>`;
        return;
    }
    list.innerHTML = customers.map((c, i) => `
        <div class="customer-item" data-index="${i}">
            <div class="customer-name">${escapeHtml(c.client_name)}</div>
            <div class="customer-meta">
                ${escapeHtml(c.client_address)}
                ${c.client_city ? " • " + escapeHtml(c.client_city) : ""}
            </div>
        </div>
    `).join("");

    list.querySelectorAll(".customer-item").forEach(item => {
        item.addEventListener("click", function () {
            fillQuoteCustomerFields(customers[Number(this.dataset.index)]);
        });
    });
}

export function fillQuoteCustomerFields(customer) {
    document.getElementById("clientName").value          = customer.client_name    || "";
    document.getElementById("clientAddress").value       = customer.client_address || "";
    document.getElementById("clientCity").value           = customer.client_city    || "";
    document.getElementById("quoteCustomerSearch").value = customer.client_name    || "";
}

export function filterQuoteCustomers(searchTerm) {
    const term = searchTerm.trim().toLowerCase();
    state.filteredQuoteCustomers = !term
        ? [...state.allQuoteCustomers]
        : state.allQuoteCustomers.filter(c =>
            (c.client_name    || "").toLowerCase().includes(term) ||
            (c.client_address || "").toLowerCase().includes(term) ||
            (c.client_city    || "").toLowerCase().includes(term)
        );
    renderQuoteCustomerList(state.filteredQuoteCustomers);
}

export function resetQuoteCustomerReuse() {
    const toggle = document.getElementById("usePreviousQuoteCustomer");
    const picker = document.getElementById("quoteCustomerPicker");
    const search = document.getElementById("quoteCustomerSearch");
    if (toggle) toggle.checked = false;
    if (picker) picker.classList.add("hidden");
    if (search) search.value = "";
}

export function setupQuoteCustomerReuse() {
    const toggle = document.getElementById("usePreviousQuoteCustomer");
    const picker = document.getElementById("quoteCustomerPicker");
    const search = document.getElementById("quoteCustomerSearch");
    if (!toggle || !picker || !search || toggle.dataset.bound === "true") return;

    toggle.addEventListener("change", async function () {
        if (this.checked) {
            picker.classList.remove("hidden");
            if (state.allQuoteCustomers.length === 0) {
                await loadQuoteCustomers();
            } else {
                state.filteredQuoteCustomers = [...state.allQuoteCustomers];
                renderQuoteCustomerList(state.filteredQuoteCustomers);
            }
        } else {
            picker.classList.add("hidden");
            search.value = "";
            state.filteredQuoteCustomers = [...state.allQuoteCustomers];
            renderQuoteCustomerList(state.filteredQuoteCustomers);
        }
    });

    search.addEventListener("input", function () { filterQuoteCustomers(this.value); });
    toggle.dataset.bound = "true";
}

/* ── Invoice customer reuse ──────────────────────────────────────────── */

export async function loadInvoiceCustomers() {
    const list = document.getElementById("invoiceCustomerList");
    try {
        const response = await fetch(INVOICE_CUSTOMERS_API);
        if (!response.ok) throw new Error("Failed to fetch invoice customers");
        state.allInvoiceCustomers      = await response.json();
        state.filteredInvoiceCustomers = [...state.allInvoiceCustomers];
        renderInvoiceCustomerList(state.filteredInvoiceCustomers);
    } catch (error) {
        console.error("Error loading invoice customers:", error);
        list.innerHTML = `<div class="customer-empty">Failed to load previous customers.</div>`;
    }
}

export function renderInvoiceCustomerList(customers) {
    const list = document.getElementById("invoiceCustomerList");
    if (!customers.length) {
        list.innerHTML = `<div class="customer-empty">No matching customers found.</div>`;
        return;
    }
    list.innerHTML = customers.map((c, i) => `
        <div class="customer-item" data-index="${i}">
            <div class="customer-name">${escapeHtml(c.client_name)}</div>
            <div class="customer-meta">
                ${escapeHtml(c.client_address)}
                ${c.client_number ? " • " + escapeHtml(c.client_number) : ""}
            </div>
        </div>
    `).join("");

    list.querySelectorAll(".customer-item").forEach(item => {
        item.addEventListener("click", function () {
            fillInvoiceCustomerFields(customers[Number(this.dataset.index)]);
        });
    });
}

export function fillInvoiceCustomerFields(customer) {
    document.getElementById("clientName").value            = customer.client_name    || "";
    document.getElementById("clientAddress").value         = customer.client_address || "";
    document.getElementById("clientNumber").value           = customer.client_number  || "";
    document.getElementById("clientRate").value             = customer.client_rate    ?? "";
    document.getElementById("invoiceCustomerSearch").value = customer.client_name    || "";
}

export function filterInvoiceCustomers(searchTerm) {
    const term = searchTerm.trim().toLowerCase();
    state.filteredInvoiceCustomers = !term
        ? [...state.allInvoiceCustomers]
        : state.allInvoiceCustomers.filter(c =>
            (c.client_name    || "").toLowerCase().includes(term) ||
            (c.client_address || "").toLowerCase().includes(term) ||
            (c.client_number  || "").toLowerCase().includes(term)
        );
    renderInvoiceCustomerList(state.filteredInvoiceCustomers);
}

export function resetInvoiceCustomerReuse() {
    const toggle = document.getElementById("usePreviousInvoiceCustomer");
    const picker = document.getElementById("invoiceCustomerPicker");
    const search = document.getElementById("invoiceCustomerSearch");
    if (toggle) toggle.checked = false;
    if (picker) picker.classList.add("hidden");
    if (search) search.value = "";
}

export function setupInvoiceCustomerReuse() {
    const toggle = document.getElementById("usePreviousInvoiceCustomer");
    const picker = document.getElementById("invoiceCustomerPicker");
    const search = document.getElementById("invoiceCustomerSearch");
    if (!toggle || !picker || !search || toggle.dataset.bound === "true") return;

    toggle.addEventListener("change", async function () {
        if (this.checked) {
            picker.classList.remove("hidden");
            if (state.allInvoiceCustomers.length === 0) {
                await loadInvoiceCustomers();
            } else {
                state.filteredInvoiceCustomers = [...state.allInvoiceCustomers];
                renderInvoiceCustomerList(state.filteredInvoiceCustomers);
            }
        } else {
            picker.classList.add("hidden");
            search.value = "";
            state.filteredInvoiceCustomers = [...state.allInvoiceCustomers];
            renderInvoiceCustomerList(state.filteredInvoiceCustomers);
        }
    });

    search.addEventListener("input", function () { filterInvoiceCustomers(this.value); });
    toggle.dataset.bound = "true";
}
