// form.js
// Generic item-table and form-payload logic shared by both the quote
// and invoice forms.

import { escapeHtml } from "./utils.js";
import { resetQuoteCustomerReuse, resetInvoiceCustomerReuse } from "./customers.js";

export function addRow(desc = "", qty = 1, price = 0) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
        <td><input value="${escapeHtml(desc)}" placeholder="Item description"></td>
        <td><input type="number" value="${qty}" min="1"></td>
        <td><input type="number" value="${price}" step="0.01" min="0"></td>
        <td><button class="danger" type="button" data-action="remove-row">Remove</button></td>
    `;
    const removeBtn = tr.querySelector('[data-action="remove-row"]');
    removeBtn.addEventListener("click", () => tr.remove());
    document.querySelector("#itemsTable tbody").appendChild(tr);
}

export function resetForm() {
    document.querySelector("#itemsTable tbody").innerHTML = "";
    addRow();
    document.getElementById("clientName").value    = "";
    document.getElementById("clientAddress").value = "";
    document.getElementById("clientCity").value    = "";
    document.getElementById("clientNumber").value  = "";
    document.getElementById("clientRate").value    = "";
    resetQuoteCustomerReuse();
    resetInvoiceCustomerReuse();
}

export function buildItems() {
    const rows  = document.querySelectorAll("#itemsTable tbody tr");
    const items = {};
    rows.forEach((row, index) => {
        const inputs = row.querySelectorAll("input");
        items[`item${index + 1}`] = {
            description: inputs[0].value.trim(),
            quantity:    Number(inputs[1].value),
            unit_price:  Number(inputs[2].value)
        };
    });
    return items;
}

export function validateItems(items) {
    const values = Object.values(items);
    if (values.length === 0) { alert("Please add at least one item."); return false; }
    for (const item of values) {
        if (!item.description) { alert("Each item must have a description."); return false; }
        if (!item.quantity || item.quantity <= 0) { alert("Each item must have a valid quantity."); return false; }
        if (Number.isNaN(item.unit_price) || item.unit_price < 0) { alert("Each item must have a valid unit price."); return false; }
    }
    return true;
}

export function buildQuotePayload() {
    const client_name    = document.getElementById("clientName").value.trim();
    const client_address = document.getElementById("clientAddress").value.trim();
    const client_city    = document.getElementById("clientCity").value.trim();
    const items          = buildItems();
    if (!client_name)    { alert("Client name is required.");    return null; }
    if (!client_address) { alert("Client address is required."); return null; }
    if (!client_city)    { alert("Client city is required.");    return null; }
    if (!validateItems(items)) return null;
    return { client_name, client_address, client_city, items };
}

export function buildInvoicePayload() {
    const client_name    = document.getElementById("clientName").value.trim();
    const client_address = document.getElementById("clientAddress").value.trim();
    const client_number  = document.getElementById("clientNumber").value.trim();
    const client_rate    = document.getElementById("clientRate").value.trim();
    const items          = buildItems();
    if (!client_name)       { alert("Client name is required.");       return null; }
    if (!client_address)    { alert("Client address is required.");    return null; }
    if (!client_number)     { alert("Client number is required.");     return null; }
    if (client_rate === "") { alert("Items tax rate is required.");    return null; }
    if (!validateItems(items)) return null;
    return { client_name, client_address, client_number, client_rate, items };
}
