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

  // Generate receipt data
  const generateReceiptData = (orderData: any): ReceiptData => {
    const now = new Date();
    return {
      receiptNumber: orderData.receiptNumber || `RCP-${Date.now()}`,
      orderType: orderData.orderType || "dine-in",
      customerName: orderData.customerName || "Guest",
      tableNumber: orderData.tableNumber || "N/A",
      items: orderData.items.map((item: any) => ({
        name: item.name,
        quantity: item.quantity,
        unitPrice: item.unitPrice || item.price,
        total: (item.unitPrice || item.price) * item.quantity,
      })),
      subtotal: orderData.subtotal || store.subtotal,
      tax: orderData.tax || store.tax,
      total: orderData.total || store.total,
      paymentMode: orderData.paymentMode || "cash",
      paymentStatus: orderData.paymentStatus || "completed",
      date: now.toLocaleDateString("en-KE"),
      time: now.toLocaleTimeString("en-KE", {
        hour: "2-digit",
        minute: "2-digit",
      }),
      cashier: orderData.cashier || "Cashier",
      changeDue: orderData.changeDue,
      amountReceived: orderData.amountReceived,
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
            `${item.name} x${item.quantity} KSH ${item.unitPrice.toFixed(
              2
            )} = KSH ${item.total.toFixed(2)}`
          );
        });

        encoder.text("-".repeat(32));
        encoder.text(`Subtotal: KSH ${data.subtotal.toFixed(2)}`);
        encoder.text(`Tax (10%): KSH ${data.tax.toFixed(2)}`);
        encoder.text(`TOTAL: KSH ${data.total.toFixed(2)}`);
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

  // Browser print fallback (works everywhere)
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

  // NEW: Download receipt as HTML file
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

  // Generate HTML receipt
  const generateReceiptHTML = (data: ReceiptData): string => {
    // ... (keep your existing HTML generation code)
    const isDebt = data.paymentMode === "debt";
    const isMpesa = data.paymentMode === "mpesa";

    return `
      <!DOCTYPE html>
      <html>
        <head>
          <meta charset="UTF-8">
          <title>Receipt - ${data.receiptNumber}</title>
          <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
              font-family: 'Courier New', monospace;
              background: #fff;
              padding: 20px;
              max-width: 300px;
              margin: 0 auto;
            }
            .receipt {
              background: white;
              padding: 20px;
              border: 1px solid #e5e0d5;
              border-radius: 8px;
            }
            .header {
              text-align: center;
              border-bottom: 2px dashed #e5e0d5;
              padding-bottom: 16px;
              margin-bottom: 16px;
            }
            .shop-name {
              font-size: 24px;
              font-weight: 800;
              color: #1b4332;
              letter-spacing: -1px;
              font-family: 'Playfair Display', serif;
            }
            .shop-sub { font-size: 11px; color: #6b7280; margin-top: 2px; }
            .receipt-title { font-size: 12px; font-weight: 600; color: #e07a5f; letter-spacing: 2px; margin-top: 4px; }
            .receipt-number { font-size: 16px; font-weight: 700; color: #1b4332; margin-top: 2px; }
            .divider { border: none; border-top: 1px dashed #e5e0d5; margin: 12px 0; }
            .info-row { display: flex; justify-content: space-between; font-size: 12px; padding: 2px 0; color: #374151; }
            .info-label { color: #6b7280; }
            .items-header { font-weight: 700; font-size: 13px; color: #1b4332; border-bottom: 1px solid #e5e0d5; padding-bottom: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; }
            .item-row { display: flex; justify-content: space-between; font-size: 12px; padding: 4px 0; color: #374151; }
            .item-name { flex: 1; }
            .item-qty { margin: 0 8px; color: #6b7280; }
            .item-price { font-weight: 600; }
            .payment-summary { border-top: 2px dashed #e5e0d5; margin-top: 12px; padding-top: 12px; }
            .summary-row { display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; color: #374151; }
            .summary-row.total { font-size: 18px; font-weight: 800; color: #1b4332; border-top: 2px solid #1b4332; margin-top: 4px; padding-top: 8px; }
            .summary-row .amount { color: #e07a5f; }
            .payment-detail { font-size: 11px; color: #6b7280; padding: 4px 0; border-top: 1px solid #e5e0d5; margin-top: 8px; }
            .change-row { color: #2d6a4f; font-weight: 700; }
            .footer { text-align: center; font-size: 11px; color: #6b7280; border-top: 2px dashed #e5e0d5; padding-top: 16px; margin-top: 16px; }
            .footer .thanks { font-weight: 600; color: #1b4332; font-size: 14px; }
            .status-badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; text-transform: uppercase; }
            .status-badge.completed { background: #2d6a4f20; color: #2d6a4f; }
            .status-badge.pending { background: #e07a5f20; color: #e07a5f; }
            .mpesa-detail { background: #f0f9f4; padding: 8px; border-radius: 4px; margin-top: 8px; font-size: 11px; }
            .debt-note { background: #fff3e0; padding: 8px; border-radius: 4px; margin-top: 8px; font-size: 11px; color: #e07a5f; text-align: center; }
            @media print { body { padding: 0; } .receipt { border: none; border-radius: 0; } .no-print { display: none; } }
          </style>
        </head>
        <body>
          <div class="receipt">
            <div class="header">
              <div class="shop-name">☕ BABADEACON</div>
              <div class="shop-sub">Premium Coffee & Snacks</div>
              <div class="receipt-title">PURCHASE RECEIPT</div>
              <div class="receipt-number">${data.receiptNumber}</div>
            </div>

            <div class="info-row">
              <span class="info-label">Date</span>
              <span>${data.date} ${data.time}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Order Type</span>
              <span>${data.orderType.replace("-", " ").toUpperCase()}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Customer</span>
              <span>${data.customerName}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Table</span>
              <span>${data.tableNumber}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Cashier</span>
              <span>${data.cashier}</span>
            </div>

            <hr class="divider">

            <div class="items-header">
              <span>Item</span>
              <span>Qty</span>
              <span>Price</span>
              <span>Total Price</span>
            </div>
            ${data.items
              .map(
                (item) => `
              <div class="item-row">
                <span class="item-name">${item.name}</span>
                <span class="item-qty">${item.quantity}</span>
                <span class="item-price">${item.unitPrice.toFixed(2)}</span>
                <span class="item-price">KSH ${item.total.toFixed(2)}</span>
              </div>
            `
              )
              .join("")}

            <div class="payment-summary">
              <div class="summary-row">
                <span>Subtotal</span>
                <span>KSH ${data.subtotal.toFixed(2)}</span>
              </div>
              <div class="summary-row">
                <span>Tax (10%)</span>
                <span>KSH ${data.tax.toFixed(2)}</span>
              </div>
              ${
                data.amountReceived
                  ? `
                <div class="summary-row">
                  <span>Amount Received</span>
                  <span>KSH ${data.amountReceived.toFixed(2)}</span>
                </div>
              `
                  : ""
              }
              ${
                data.changeDue
                  ? `
                <div class="summary-row change-row">
                  <span>Change Due</span>
                  <span>KSH ${data.changeDue.toFixed(2)}</span>
                </div>
              `
                  : ""
              }
              <div class="summary-row total">
                <span>TOTAL</span>
                <span class="amount">KSH ${data.total.toFixed(2)}</span>
              </div>
            </div>

            <div class="payment-detail">
              <div class="info-row">
                <span class="info-label">Payment Method</span>
                <span>${data.paymentMode.toUpperCase()}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Status</span>
                <span class="status-badge ${data.paymentStatus}">${
      data.paymentStatus
    }</span>
              </div>
            </div>

            ${
              isMpesa
                ? `
              <div class="mpesa-detail">
                <div class="info-row">
                  <span>M-Pesa Number</span>
                  <span>${data.mpesaNumber || "N/A"}</span>
                </div>
                ${
                  data.mpesaReceipt
                    ? `
                  <div class="info-row">
                    <span>M-Pesa Receipt</span>
                    <span>${data.mpesaReceipt}</span>
                  </div>
                `
                    : ""
                }
                <div style="margin-top:4px;font-size:10px;color:#6b7280;text-align:center;">
                  ✅ Payment confirmed via M-Pesa
                </div>
              </div>
            `
                : ""
            }

            ${
              isDebt
                ? `
              <div class="debt-note">
                <strong>📋 DEBT ORDER</strong><br>
                Payment due in 7 days<br>
                Please settle this amount to clear outstanding balance.
              </div>
            `
                : ""
            }

            <div class="footer">
              <div class="thanks">Thank you for your order!</div>
              <div style="margin-top:4px;">Visit us again at BABADEACON COFFEE</div>
              <div style="margin-top:4px;font-size:10px;color:#9ca3af;">
                This is a system generated receipt
              </div>
            </div>
          </div>
          <div style="text-align:center;margin-top:16px;" class="no-print">
            <button onclick="window.print()" style="padding:10px 30px;background:#1b4332;color:white;border:none;border-radius:8px;cursor:pointer;font-size:16px;">
              🖨️ Print Receipt
            </button>
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
      text += `  ${item.name.padEnd(20)} ${
        item.quantity
      } x KSH ${item.unitPrice.toFixed(2)} = KSH ${item.total.toFixed(2)}\n`;
    });

    text += `
${dash}
  Subtotal: KSH ${data.subtotal.toFixed(2)}
  Tax (10%): KSH ${data.tax.toFixed(2)}
${line}
  TOTAL: KSH ${data.total.toFixed(2)}
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
    downloadReceipt, // <-- Make sure to export this
    generateReceiptData,
    generateReceiptHTML,
    generateReceiptText,
  };
}
