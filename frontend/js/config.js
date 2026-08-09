// config.js
// Centralized API endpoint constants and static configuration.
// No mutable state lives here — see state.js for that.

export const QUOTE_PREVIEW_API     = "/quote/preview";
export const QUOTE_SAVE_API        = "/quote/finalize";
export const INVOICE_API           = "/invoice";
export const QUOTE_CUSTOMERS_API   = "/customers/quotes";
export const INVOICE_CUSTOMERS_API = "/customers/invoices";
export const QUOTE_HISTORY_API     = "/quote_db";
export const INVOICE_HISTORY_API   = "/invoice_db";
export const SEARCH_API            = "/search";
export const DASHBOARD_API         = "/dashboard";

export const MODES = {
    receipt: { title: "Create Invoice" },
    quote:   { title: "Create Quote" }
};
