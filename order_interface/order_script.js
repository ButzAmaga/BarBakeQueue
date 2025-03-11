document.addEventListener("DOMContentLoaded", () => {
    // Get references to elements in the order interface
    const orderSummary = document.getElementById("order-summary");
    const checkoutBtn = document.getElementById("checkout-btn");
    const downPaymentText = document.getElementById("down-payment-text");
    const receiptUpload = document.getElementById("receipt-upload");

    // Retrieve cart items from local storage (this should be updated dynamically)
    const cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];

    // Function to render the order summary dynamically
    function renderOrderSummary() {
        orderSummary.innerHTML = ""; // Clear previous order summary
        let totalCost = 0;

        // Check if the cart is empty and disable checkout if true
        if (cartItems.length === 0) {
            orderSummary.innerHTML = "<p class='error-message'>Your cart is empty. Please add items before proceeding.</p>";
            checkoutBtn.disabled = true;
            return;
        } else {
            checkoutBtn.disabled = false;
        }

        // Filter out only the items the customer chooses to proceed with
        const selectedItems = cartItems.filter(item => item.selected);

        if (selectedItems.length === 0) {
            orderSummary.innerHTML = "<p class='error-message'>No items selected for checkout. Please select items to proceed.</p>";
            checkoutBtn.disabled = true;
            return;
        }

        // Loop through each selected item and display it in the order summary
        selectedItems.forEach((item) => {
            const orderItem = document.createElement("div");
            orderItem.classList.add("order-item");
            orderItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}">
                <div class="order-item-details">
                    <h3>${item.name}</h3>
                    <p>Layer: ${item.layer}</p>
                    <p>Size: ${item.size}</p>
                    <p>Filling: ${item.filling}</p>
                    <p>Shape: ${item.shape}</p>
                </div>
                <div class="order-item-price">$${item.price}</div>
            `;
            orderSummary.appendChild(orderItem);
            totalCost += item.price;
        });

        // Calculate and display the required down payment (30-50% of total cost)
        const minDownPayment = (totalCost * 0.3).toFixed(2);
        const maxDownPayment = (totalCost * 0.5).toFixed(2);
        downPaymentText.innerHTML = `Down Payment Required: <span>$${minDownPayment} - $${maxDownPayment}</span>`;
    }

    // Checkout button event listener
    checkoutBtn.addEventListener("click", () => {
        // Prevent checkout if cart is empty or no items are selected
        if (cartItems.length === 0) {
            alert("Your cart is empty. Please add items before proceeding to checkout.");
            return;
        }
        const selectedItems = cartItems.filter(item => item.selected);
        if (selectedItems.length === 0) {
            alert("No items selected for checkout. Please select items to proceed.");
            return;
        }
        // Prevent checkout if receipt proof of down payment is not uploaded
        if (!receiptUpload.files.length) {
            alert("Please upload a receipt as proof of down payment before proceeding.");
            return;
        }
        alert("Proceeding to checkout...");
    });

    // Initial rendering of order summary when page loads
    renderOrderSummary();
});
