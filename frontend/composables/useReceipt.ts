// frontend/composables/useReceipt.ts
import { ref } from "vue";
import { usePosStore } from "~/stores/pos";

// Try different import approaches
// Option 1: Default import
import PrinterEncoder from "@point-of-sale/receipt-printer-encoder";

interface ReceiptData {
  receiptNumber: string;
  orderType: string;
  customerName: string;
  tableNumber: string;
  items: any[];
  subtotal: number;
  tax: number;
  total: number;
  paymentMode: string;
  paymentStatus: string;
  date: string;
  time: string;
  cashier: string;
  changeDue?: number;
  amountReceived?: number;
  mpesaNumber?: string;
  mpesaReceipt?: string;
}

export function useReceipt() {
  const store = usePosStore();
  const isPrinting = ref(false);
  const isConnected = ref(false);
  const printerDevice = ref<any>(null);
  const receiptData = ref<ReceiptData | null>(null);

  // Helper function to safely convert to number
  const toNumber = (value: any): number => {
    if (value === null || value === undefined) return 0;
    if (typeof value === "string") {
      const parsed = parseFloat(value);
      return isNaN(parsed) ? 0 : parsed;
    }
    if (typeof value === "number") return value;
    return 0;
  };

  // Helper function to safely format currency
  const formatCurrency = (value: any): string => {
    const num = toNumber(value);
    return num.toFixed(2);
  };

  // Generate receipt data - FIXED: Handle all data types
  const generateReceiptData = (orderData: any): ReceiptData => {
    const now = new Date();

    // Safely map items with proper number conversion
    const items = (orderData.items || []).map((item: any) => ({
      name: item.name || item.product_name || "Unknown Item",
      quantity: toNumber(item.quantity),
      unitPrice: toNumber(item.unitPrice || item.price),
      total: toNumber(
        (item.unitPrice || item.price || 0) * (item.quantity || 1)
      ),
    }));

    return {
      receiptNumber: orderData.receiptNumber || `RCP-${Date.now()}`,
      orderType: orderData.orderType || "dine-in",
      customerName: orderData.customerName || "Guest",
      tableNumber: orderData.tableNumber || "N/A",
      items: items,
      subtotal: toNumber(orderData.subtotal || store.subtotal),
      tax: toNumber(orderData.tax || store.tax),
      total: toNumber(orderData.total || store.total),
      paymentMode: orderData.paymentMode || "cash",
      paymentStatus: orderData.paymentStatus || "completed",
      date: now.toLocaleDateString("en-KE"),
      time: now.toLocaleTimeString("en-KE", {
        hour: "2-digit",
        minute: "2-digit",
      }),
      cashier: orderData.cashier || "Cashier",
      changeDue:
        orderData.changeDue !== undefined
          ? toNumber(orderData.changeDue)
          : undefined,
      amountReceived:
        orderData.amountReceived !== undefined
          ? toNumber(orderData.amountReceived)
          : undefined,
      mpesaNumber: orderData.mpesaNumber,
      mpesaReceipt: orderData.mpesaReceipt,
    };
  };

  // Connect to Bluetooth printer
  const connectPrinter = async () => {
    try {
      if (!navigator.bluetooth) {
        console.warn("Web Bluetooth is not supported in this browser");
        return false;
      }

      const device = await navigator.bluetooth.requestDevice({
        acceptAllDevices: true,
        optionalServices: ["000018f0-0000-1000-8000-00805f9b34fb"],
      });

      const server = await device.gatt?.connect();
      if (!server) throw new Error("Failed to connect to printer");

      printerDevice.value = device;
      isConnected.value = true;

      localStorage.setItem(
        "pos_printer_device",
        JSON.stringify({
          name: device.name,
          id: device.id,
        })
      );

      return true;
    } catch (error) {
      console.error("Failed to connect to printer:", error);
      return false;
    }
  };

  // Print with ESC/POS (Bluetooth/USB)
  const printWithESC = async (orderData: any) => {
    if (!isConnected.value) {
      const connected = await connectPrinter();
      if (!connected) {
        printWithBrowser(orderData);
        return false;
      }
    }

    try {
      isPrinting.value = true;
      const data = generateReceiptData(orderData);

      let encoder;
      try {
        encoder = new PrinterEncoder();
      } catch (initError) {
        console.warn("Printer encoder init failed, using fallback:", initError);
        return printWithBrowser(orderData);
      }

      try {
        encoder.initialize();
        encoder.text("☕ BABADEACON COFFEE");
        encoder.newline();
        encoder.text("PURCHASE RECEIPT");
        encoder.newline();
        encoder.text(`#${data.receiptNumber}`);
        encoder.newline();
        encoder.newline();

        encoder.text(`Date: ${data.date} ${data.time}`);
        encoder.text(`Customer: ${data.customerName}`);
        encoder.text(`Table: ${data.tableNumber}`);
        encoder.newline();

        encoder.text("-".repeat(32));
        data.items.forEach((item) => {
          encoder.text(
            `${item.name} x${item.quantity} KSH ${formatCurrency(
              item.unitPrice
            )} = KSH ${formatCurrency(item.total)}`
          );
        });

        encoder.text("-".repeat(32));
        encoder.text(`Subtotal: KSH ${formatCurrency(data.subtotal)}`);
        encoder.text(`Tax (10%): KSH ${formatCurrency(data.tax)}`);
        encoder.text(`TOTAL: KSH ${formatCurrency(data.total)}`);
        encoder.newline();

        encoder.text(`Payment: ${data.paymentMode.toUpperCase()}`);
        encoder.text(`Status: ${data.paymentStatus}`);
        encoder.newline();

        encoder.text("Thank you for your order!");
        encoder.text("Visit us again!");
        encoder.newline();
        encoder.newline();

        encoder.cut();

        const encodedData = encoder.encode();

        const server = await printerDevice.value.gatt?.connect();
        const service = await server?.getPrimaryService(
          "000018f0-0000-1000-8000-00805f9b34fb"
        );
        const characteristic = await service?.getCharacteristic(
          "00002af1-0000-1000-8000-00805f9b34fb"
        );

        const chunkSize = 1024;
        for (let i = 0; i < encodedData.length; i += chunkSize) {
          const chunk = encodedData.slice(i, i + chunkSize);
          await characteristic?.writeValue(chunk);
        }

        isPrinting.value = false;
        return true;
      } catch (apiError) {
        console.warn(
          "Printer API error, falling back to browser print:",
          apiError
        );
        return printWithBrowser(orderData);
      }
    } catch (error) {
      console.error("Print error:", error);
      isPrinting.value = false;
      return printWithBrowser(orderData);
    }
  };

  // Browser print fallback (works everywhere) - FIXED: Use formatCurrency
  const printWithBrowser = (orderData: any) => {
    try {
      const data = generateReceiptData(orderData);
      const html = generateReceiptHTML(data);

      const printWindow = window.open("", "_blank", "width=400,height=600");
      if (printWindow) {
        printWindow.document.write(html);
        printWindow.document.close();

        printWindow.onload = function () {
          setTimeout(() => {
            printWindow.print();
            printWindow.close();
          }, 500);
        };
        return true;
      }
      return false;
    } catch (error) {
      console.error("Browser print error:", error);
      return false;
    }
  };

  // NEW: Download receipt as HTML file - FIXED: Use formatCurrency
  const downloadReceipt = (orderData: any) => {
    try {
      const data = generateReceiptData(orderData);
      const html = generateReceiptHTML(data);

      // Create blob and download
      const blob = new Blob([html], { type: "text/html" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `receipt-${data.receiptNumber}.html`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      return true;
    } catch (error) {
      console.error("Error downloading receipt:", error);
      return false;
    }
  };

  // Generate HTML receipt - FIXED: Use formatCurrency everywhere
  const generateReceiptHTML = (data: ReceiptData): string => {
    const isDebt = data.paymentMode === "debt";
    const isMpesa = data.paymentMode === "mpesa";
    const showTable =
      data.orderType === "dine-in" &&
      !!data.tableNumber &&
      data.tableNumber !== "N/A";
    const hasAmountReceived = data.amountReceived != null;
    const hasChangeDue = data.changeDue != null;
    const statusClass =
      data.paymentStatus === "completed" || data.paymentStatus === "paid"
        ? "completed"
        : "pending";

    // Format all currency values
    const format = (val: any) => formatCurrency(val);

    return `
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>Receipt - ${data.receiptNumber}</title>
          <link rel="preconnect" href="https://fonts.googleapis.com">
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
          <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,900&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
          <style>
            :root {
              --paper: #fbf6ec;
              --page-bg: #ece4d2;
              --ink: #1b4332;
              --ink-light: #2d6a4f;
              --ember: #c1572f;
              --espresso: #2c1810;
              --mist: #847d6e;
              --rule: #d9cdb2;
            }
            * { margin: 0; padding: 0; box-sizing: border-box; }
            html, body {
              background: var(--page-bg);
              font-family: 'IBM Plex Mono', 'Courier New', monospace;
              color: var(--espresso);
            }
            body {
              padding: 32px 16px 48px;
              display: flex;
              flex-direction: column;
              align-items: center;
            }
            .perforation {
              width: 320px;
              display: flex;
              justify-content: space-between;
              padding: 0 18px;
              margin-bottom: 6px;
            }
            .perforation span {
              width: 11px;
              height: 11px;
              border-radius: 50%;
              background: var(--page-bg);
              box-shadow: inset 0 1px 2px rgba(44, 24, 16, .2);
            }
            .ticket-wrap {
              width: 320px;
              filter: drop-shadow(0 16px 22px rgba(44, 24, 16, .3));
            }
            .ticket {
              background: var(--paper);
              padding: 26px 24px 16px;
              border-radius: 6px 6px 0 0;
            }
            .ticket-tear {
              height: 16px;
              background: var(--paper);
              clip-path: polygon(
                0% 0%, 100% 0%,
                100% 30%, 92.9% 100%, 85.7% 30%, 78.6% 100%, 71.4% 30%, 64.3% 100%,
                57.1% 30%, 50% 100%, 42.9% 30%, 35.7% 100%, 28.6% 30%, 21.4% 100%,
                14.3% 30%, 7.1% 100%, 0% 30%
              );
            }
            .header { text-align: center; }
            .shop-mark {
              display: flex;
              align-items: baseline;
              justify-content: center;
              gap: 7px;
            }
            .shop-mark .cup { font-size: 21px; }
            .shop-name {
              font-family: 'Fraunces', serif;
              font-weight: 700;
              font-size: 25px;
              letter-spacing: -0.5px;
              color: var(--ink);
            }
            .shop-sub {
              font-size: 10px;
              letter-spacing: 2px;
              text-transform: uppercase;
              color: var(--mist);
              margin-top: 3px;
            }
            .eyebrow {
              display: inline-block;
              font-size: 10px;
              font-weight: 600;
              letter-spacing: 2.5px;
              text-transform: uppercase;
              color: var(--ember);
              margin-top: 16px;
            }
            .receipt-number {
              font-size: 14px;
              font-weight: 600;
              color: var(--ink);
              margin-top: 4px;
            }
            .rule {
              border: none;
              border-top: 1px dashed var(--rule);
              margin: 18px 0;
            }
            .rule.tight { margin: 4px 0 12px; }
            .rule.heavy { border-top: 1.5px solid var(--ink); margin: 10px 0; }
            .meta-row {
              display: grid;
              grid-template-columns: auto 1fr;
              gap: 5px 12px;
              font-size: 11px;
            }
            .meta-label {
              color: var(--mist);
              letter-spacing: .5px;
              text-transform: uppercase;
              font-size: 9.5px;
              align-self: center;
            }
            .meta-value {
              text-align: right;
              font-weight: 500;
            }
            .items-head {
              display: grid;
              grid-template-columns: 1fr 30px 80px;
              gap: 8px;
              font-size: 10px;
              letter-spacing: 1.5px;
              text-transform: uppercase;
              color: var(--ember);
              font-weight: 600;
              padding-bottom: 8px;
              border-bottom: 1.5px solid var(--ink);
            }
            .items-head span:nth-child(2) { text-align: center; }
            .items-head span:nth-child(3) { text-align: right; }
            .item-row {
              display: grid;
              grid-template-columns: 1fr 30px 80px;
              gap: 8px;
              align-items: start;
              font-size: 12px;
              padding: 10px 0;
              border-bottom: 1px dotted var(--rule);
            }
            .item-row:last-of-type { border-bottom: none; }
            .item-name .unit-price {
              display: block;
              font-size: 10px;
              color: var(--mist);
              margin-top: 1px;
            }
            .item-qty { text-align: center; color: var(--mist); }
            .item-amount {
              text-align: right;
              font-weight: 600;
              font-variant-numeric: tabular-nums;
            }
            .summary-row {
              display: flex;
              justify-content: space-between;
              font-size: 12px;
              padding: 4px 0;
            }
            .summary-row .label { color: var(--mist); }
            .summary-row.change .value { color: var(--ink-light); font-weight: 700; }
            .total-row {
              display: flex;
              justify-content: space-between;
              align-items: baseline;
            }
            .total-row .label {
              font-family: 'Fraunces', serif;
              font-weight: 700;
              font-size: 15px;
              color: var(--ink);
              letter-spacing: .3px;
            }
            .total-row .value {
              font-family: 'Fraunces', serif;
              font-weight: 700;
              font-size: 23px;
              color: var(--ember);
            }
            .payment-row {
              display: flex;
              justify-content: space-between;
              align-items: center;
              font-size: 11px;
              margin-top: 16px;
            }
            .payment-method { font-weight: 600; letter-spacing: .5px; }
            .status-badge {
              display: inline-block;
              padding: 3px 10px;
              border-radius: 100px;
              font-size: 9px;
              font-weight: 700;
              letter-spacing: 1px;
              text-transform: uppercase;
            }
            .status-badge.completed { background: rgba(45, 106, 79, .12); color: var(--ink-light); }
            .status-badge.pending { background: rgba(193, 87, 47, .12); color: var(--ember); }
            .note-block {
              margin-top: 14px;
              padding: 12px;
              border-radius: 6px;
              font-size: 11px;
              line-height: 1.5;
            }
            .note-block.mpesa { background: rgba(45, 106, 79, .08); }
            .note-block.mpesa .meta-row { font-size: 11px; }
            .note-block.mpesa .confirm {
              text-align: center;
              margin-top: 8px;
              padding-top: 8px;
              border-top: 1px dashed rgba(45, 106, 79, .25);
              font-size: 10px;
              color: var(--ink-light);
              font-weight: 600;
              letter-spacing: .3px;
            }
            .note-block.debt {
              background: rgba(193, 87, 47, .08);
              text-align: center;
              color: var(--espresso);
            }
            .note-block.debt strong {
              display: block;
              letter-spacing: 1.5px;
              text-transform: uppercase;
              font-size: 10px;
              color: var(--ember);
              margin-bottom: 5px;
            }
            .footer { text-align: center; margin-top: 22px; }
            .footer .thanks {
              font-family: 'Fraunces', serif;
              font-style: italic;
              font-weight: 600;
              font-size: 15px;
              color: var(--ink);
            }
            .footer .visit {
              font-size: 10px;
              color: var(--mist);
              margin-top: 5px;
              letter-spacing: .3px;
            }
            .footer .system-note {
              font-size: 8.5px;
              color: var(--mist);
              opacity: .75;
              margin-top: 12px;
              letter-spacing: 1px;
              text-transform: uppercase;
            }
            .print-btn-wrap { margin-top: 24px; text-align: center; }
            .print-btn {
              padding: 11px 30px;
              background: var(--ink);
              color: var(--paper);
              border: none;
              border-radius: 100px;
              cursor: pointer;
              font-family: 'IBM Plex Mono', monospace;
              font-size: 12px;
              font-weight: 600;
              letter-spacing: 1px;
              text-transform: uppercase;
            }
            .print-btn:hover { background: var(--ink-light); }
            @media print {
              html, body { background: var(--paper); padding: 0; }
              .perforation span { box-shadow: none; }
              .no-print { display: none; }
              .ticket-wrap { filter: none; width: auto; }
            }
          </style>
        </head>
        <body>
          <div class="perforation">
            <span></span><span></span><span></span><span></span><span></span>
            <span></span><span></span><span></span><span></span><span></span>
          </div>

          <div class="ticket-wrap">
            <div class="ticket">
              <div class="header">
                <div class="shop-mark">
                  <span class="cup">☕</span>
                  <span class="shop-name">Babadeacon</span>
                </div>
                <div class="shop-sub">Coffee &amp; Snacks</div>
                <div class="eyebrow">Purchase Receipt</div>
                <div class="receipt-number">№ ${data.receiptNumber}</div>
              </div>

              <hr class="rule">

              <div class="meta-row">
                <span class="meta-label">Date</span>
                <span class="meta-value">${data.date} · ${data.time}</span>
                <span class="meta-label">Order</span>
                <span class="meta-value">${data.orderType
                  .replace("-", " ")
                  .toUpperCase()}</span>
                ${
                  showTable
                    ? `
                <span class="meta-label">Table</span>
                <span class="meta-value">${data.tableNumber}</span>`
                    : ""
                }
                <span class="meta-label">Customer</span>
                <span class="meta-value">${data.customerName}</span>
                <span class="meta-label">Cashier</span>
                <span class="meta-value">${data.cashier}</span>
              </div>

              <hr class="rule">

              <div class="items-head">
                <span>Item</span>
                <span>Qty</span>
                <span>Amount</span>
              </div>
              ${data.items
                .map(
                  (item) => `
              <div class="item-row">
                <span class="item-name">${
                  item.name
                }<span class="unit-price">KSH ${format(
                    item.unitPrice
                  )} each</span></span>
                <span class="item-qty">${item.quantity}</span>
                <span class="item-amount">${format(item.total)}</span>
              </div>`
                )
                .join("")}

              <hr class="rule tight">

              <div class="summary-row">
                <span class="label">Subtotal</span>
                <span class="value">KSH ${format(data.subtotal)}</span>
              </div>
              <div class="summary-row">
                <span class="label">Tax (10%)</span>
                <span class="value">KSH ${format(data.tax)}</span>
              </div>
              ${
                hasAmountReceived
                  ? `
              <div class="summary-row">
                <span class="label">Amount Received</span>
                <span class="value">KSH ${format(data.amountReceived!)}</span>
              </div>`
                  : ""
              }
              ${
                hasChangeDue
                  ? `
              <div class="summary-row change">
                <span class="label">Change Due</span>
                <span class="value">KSH ${format(data.changeDue!)}</span>
              </div>`
                  : ""
              }

              <hr class="rule heavy">

              <div class="total-row">
                <span class="label">Total</span>
                <span class="value">KSH ${format(data.total)}</span>
              </div>

              <div class="payment-row">
                <span class="meta-label">Payment</span>
                <span class="payment-method">${data.paymentMode.toUpperCase()}</span>
                <span class="status-badge ${statusClass}">${
      data.paymentStatus
    }</span>
              </div>

              ${
                isMpesa
                  ? `
              <div class="note-block mpesa">
                <div class="meta-row">
                  <span class="meta-label">M-Pesa No.</span>
                  <span class="meta-value">${data.mpesaNumber || "N/A"}</span>
                  ${
                    data.mpesaReceipt
                      ? `
                  <span class="meta-label">M-Pesa Code</span>
                  <span class="meta-value">${data.mpesaReceipt}</span>`
                      : ""
                  }
                </div>
                <div class="confirm">✓ Payment confirmed via M-Pesa</div>
              </div>`
                  : ""
              }

              ${
                isDebt
                  ? `
              <div class="note-block debt">
                <strong>Debt Order</strong>
                Payment due within 7 days. Please settle this balance to clear your account.
              </div>`
                  : ""
              }

              <div class="footer">
                <div class="thanks">Thank you for your order</div>
                <div class="visit">Visit us again at Babadeacon Coffee</div>
                <div class="system-note">System-generated receipt</div>
              </div>
            </div>
            <div class="ticket-tear"></div>
          </div>

          <div class="print-btn-wrap no-print">
            <button class="print-btn" onclick="window.print()">Print Receipt</button>
          </div>
        </body>
      </html>
    `;
  };

  // Generate receipt text for console
  const generateReceiptText = (orderData: any): string => {
    const data = generateReceiptData(orderData);
    const line = "=".repeat(48);
    const dash = "-".repeat(48);
    const format = (val: any) => formatCurrency(val);

    let text = `
${line}
  ☕ BABADEACON COFFEE
  Premium Coffee & Snacks
${line}
  RECEIPT: ${data.receiptNumber}
${dash}
  Date: ${data.date} ${data.time}
  Customer: ${data.customerName}
  Table: ${data.tableNumber}
${dash}
  ITEMS:
`;
    data.items.forEach((item) => {
      text += `  ${item.name.padEnd(20)} ${item.quantity} x KSH ${format(
        item.unitPrice
      )} = KSH ${format(item.total)}\n`;
    });

    text += `
${dash}
  Subtotal: KSH ${format(data.subtotal)}
  Tax (10%): KSH ${format(data.tax)}
${line}
  TOTAL: KSH ${format(data.total)}
${line}
  Payment: ${data.paymentMode.toUpperCase()}
  Status: ${data.paymentStatus}
  
  Thank you for your order!
  Visit us again at BABADEACON COFFEE
${line}
`;
    return text;
  };

  // Main print function
  const printReceipt = async (orderData: any, useESC: boolean = true) => {
    try {
      isPrinting.value = true;

      if (useESC) {
        const result = await printWithESC(orderData);
        if (result) {
          isPrinting.value = false;
          return true;
        }
      }

      const result = printWithBrowser(orderData);
      isPrinting.value = false;
      return result;
    } catch (error) {
      console.error("Print receipt error:", error);
      isPrinting.value = false;
      return false;
    }
  };

  return {
    isPrinting,
    isConnected,
    receiptData,
    connectPrinter,
    printReceipt,
    downloadReceipt,
    generateReceiptData,
    generateReceiptHTML,
    generateReceiptText,
  };
}
