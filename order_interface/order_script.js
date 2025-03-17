document.addEventListener("DOMContentLoaded", () => {
    // Get references to key elements
    const orderSummary = document.getElementById("order-summary");
    const checkoutBtn = document.getElementById("checkout-btn");
    const downPaymentText = document.getElementById("down-payment-text");
    const receiptUpload = document.getElementById("receipt-upload");
    const modal = document.getElementById("order-details-modal");
    const modalClose = document.getElementById("modal-close");
    const modalContent = document.getElementById("modal-content");

    if (!orderSummary || !checkoutBtn || !downPaymentText || !receiptUpload || !modal || !modalClose || !modalContent) {
        console.error("One or more required elements are missing.");
        return;
    }

    let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

    function renderOrderSummary() {
        orderSummary.innerHTML = "";
        let totalCost = 0;

        if (cartItems.length === 0) {
            orderSummary.innerHTML = "<p class='error-message'>Your cart is empty. Please add items before proceeding.</p>";
            checkoutBtn.disabled = true;
            return;
        }

        const selectedItems = cartItems.filter(item => item.selected);
        if (selectedItems.length === 0) {
            orderSummary.innerHTML = "<p class='error-message'>No items selected for checkout. Please select items to proceed.</p>";
            checkoutBtn.disabled = true;
            return;
        }

        selectedItems.forEach((item, index) => {
            const orderRow = document.createElement("tr");
            const showDelete = item.status === "No partial pay";

            orderRow.innerHTML = `
                <td>${item.orderNumber}</td>
                <td><span class="status ${item.statusClass}">${item.status}</span></td>
                <td>${item.dateOrdered}</td>
                <td><strong>$${item.price}</strong></td>
                <td>
                    <span class="tooltip">
                        <i class="fa-solid fa-eye view-icon" data-index="${index}"></i>
                        <span class="tooltip-text">View order details</span>
                    </span>
                    ${showDelete ? `
                    <span class="tooltip">
                        <i class="fa-solid fa-trash delete-icon" data-index="${index}"></i>
                        <span class="tooltip-text">Remove order</span>
                    </span>` : ""}
                </td>
            `;
            orderSummary.appendChild(orderRow);
            totalCost += item.price;
        });

        const minDownPayment = (totalCost * 0.3).toFixed(2);
        const maxDownPayment = (totalCost * 0.5).toFixed(2);
        downPaymentText.innerHTML = `Down Payment Required: <span>$${minDownPayment} - $${maxDownPayment}</span>`;

        attachIconEventListeners();
    }

    function attachIconEventListeners() {
        document.querySelectorAll(".view-icon").forEach(icon => {
            icon.addEventListener("click", event => {
                const index = event.target.getAttribute("data-index");
                showOrderDetails(index);
            });
        });

        document.querySelectorAll(".delete-icon").forEach(icon => {
            icon.addEventListener("click", event => {
                const index = event.target.getAttribute("data-index");
                cartItems.splice(index, 1);
                localStorage.setItem("cartItems", JSON.stringify(cartItems));
                renderOrderSummary();
            });
        });
    }

    function showOrderDetails(index) {
        const order = cartItems[index];
        if (!order) return;

        modalContent.innerHTML = `
            <h2>Order #${order.orderNumber}</h2>
            <table class="details-table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Quantity</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    ${order.items.map(item => `
                        <tr>
                            <td>${item.name}</td>
                            <td>${item.quantity} pcs</td>
                            <td><strong>$${item.price}</strong></td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
            <p>Status: <span class="status-label">${order.status}</span></p>
            <p>Date ordered: ${order.dateOrdered}</p>
            <p>Total: <strong>$${order.price}</strong></p>
            <div class="modal-actions">
                <button class="btn" id="return-btn">Return</button>
                ${order.status === "No partial pay" ? '<button class="btn btn-danger" id="cancel-order-btn">Cancel Order</button>' : ''}
            </div>
        `;

        modal.classList.remove("hidden");

        document.getElementById("return-btn").addEventListener("click", () => {
            modal.classList.add("hidden");
        });

        if (order.status === "No partial pay") {
            document.getElementById("cancel-order-btn").addEventListener("click", () => {
                cartItems.splice(index, 1);
                localStorage.setItem("cartItems", JSON.stringify(cartItems));
                modal.classList.add("hidden");
                renderOrderSummary();
            });
        }
    }

    checkoutBtn.addEventListener("click", () => {
        if (cartItems.length === 0) {
            alert("Your cart is empty. Please add items before proceeding to checkout.");
            return;
        }

        const selectedItems = cartItems.filter(item => item.selected);
        if (selectedItems.length === 0) {
            alert("No items selected for checkout. Please select items to proceed.");
            return;
        }

        if (!receiptUpload.files.length) {
            alert("Please upload a receipt as proof of down payment before proceeding.");
            return;
        }

        alert("Proceeding to checkout...");
        localStorage.setItem("cartItems", JSON.stringify([]));
        renderOrderSummary();
    });

    modalClose.addEventListener("click", () => {
        modal.classList.add("hidden");
    });

    renderOrderSummary();
});
