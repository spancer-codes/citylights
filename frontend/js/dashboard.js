// dashboard.js
// Dashboard tab: summary stat cards and the monthly revenue bar chart.

import { DASHBOARD_API } from "./config.js";

export async function loadDashboard() {
    try {
        const res = await fetch(DASHBOARD_API);
        if (!res.ok) { console.error("Failed to fetch dashboard"); return; }
        const data = await res.json();

        document.getElementById("totalQuotes").innerText     = data.total_quotes;
        document.getElementById("totalInvoices").innerText   = data.total_invoices;
        document.getElementById("convertedQuotes").innerText = data.total_quotes_converted;
        document.getElementById("conversionRate").innerText  = (data.conversion_rate * 100).toFixed(2) + "%";

        renderRevenue(data.monthly_revenue || data.montthly_revenue);
    } catch (err) {
        console.error("Dashboard error:", err);
    }
}

export function renderRevenue(data) {
    const container = document.getElementById("revenueList");
    if (!data || data.length === 0) {
        container.innerHTML = "<p style='color:var(--muted);font-size:14px;'>No revenue data available.</p>";
        return;
    }

    const max = Math.max(...data.map(r => Number(r.revenue)));

    container.innerHTML = data.map(r => {
        const amount = Number(r.revenue);
        const pct    = max > 0 ? Math.round((amount / max) * 100) : 0;
        return `
            <div class="revenue-row">
                <span class="revenue-month">${r.month}</span>
                <div class="revenue-bar-track">
                    <div class="revenue-bar-fill" style="width:${pct}%"></div>
                </div>
                <span class="revenue-amount">R ${amount.toFixed(2)}</span>
            </div>`;
    }).join("");
}
