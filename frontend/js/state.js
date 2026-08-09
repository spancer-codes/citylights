// state.js
// Shared mutable state. Exported as a single object (rather than separate
// `let` bindings) so that every importing module sees live updates —
// reassigning `state.currentMode = 'quote'` in one module is visible
// everywhere else that imported `state`.

export const state = {
    currentMode: "receipt",
    previewBlobUrl: null,

    allQuoteCustomers: [],
    filteredQuoteCustomers: [],
    allInvoiceCustomers: [],
    filteredInvoiceCustomers: [],

    isPreviewingQuote: false,
    isSavingQuote: false,
    isSubmittingInvoice: false
};
