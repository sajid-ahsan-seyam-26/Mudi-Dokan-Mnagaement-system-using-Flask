// ----------------------------------------------------
// Show current year in footer
// ----------------------------------------------------
document.getElementById("year").textContent = new Date().getFullYear();


// ----------------------------------------------------
// Confirm before delete
// ----------------------------------------------------
function confirmDelete() {
    return confirm("Are you sure you want to delete this?");
}


// ----------------------------------------------------
// Validate Add Product Form
// ----------------------------------------------------
function validateProductForm() {
    let name = document.getElementById("name").value;
    let category = document.getElementById("category").value;
    let supplier = document.getElementById("supplier").value;
    let unit = document.getElementById("unit").value;
    let buyPrice = document.getElementById("buy_price").value;
    let sellPrice = document.getElementById("sell_price").value;
    let stock = document.getElementById("stock").value;
    let lowStockLimit = document.getElementById("low_stock_limit").value;

    if (name === "" || category === "" || supplier === "" || unit === "" || buyPrice === "" || sellPrice === "" || stock === "" || lowStockLimit === "") {
        alert("Please fill all fields.");
        return false;
    }

    if (buyPrice <= 0 || sellPrice <= 0) {
        alert("Price must be greater than 0.");
        return false;
    }

    if (stock < 0 || lowStockLimit < 0) {
        alert("Stock cannot be negative.");
        return false;
    }

    return true;
}


// ----------------------------------------------------
// Validate Sale Form
// ----------------------------------------------------
function validateSaleForm(availableStock) {
    let customerName = document.getElementById("customer_name").value;
    let quantity = document.getElementById("quantity").value;
    let saleDate = document.getElementById("sale_date").value;

    if (customerName === "" || quantity === "" || saleDate === "") {
        alert("Please fill all required fields.");
        return false;
    }

    if (quantity <= 0) {
        alert("Quantity must be greater than 0.");
        return false;
    }

    if (parseInt(quantity) > availableStock) {
        alert("Not enough stock available.");
        return false;
    }

    return true;
}


// ----------------------------------------------------
// Calculate total amount on sale page
// ----------------------------------------------------
function calculateTotal(price) {
    let quantity = document.getElementById("quantity").value;
    let total = price * quantity;

    if (quantity === "" || quantity < 0) {
        total = 0;
    }

    document.getElementById("totalAmount").textContent = "৳" + total.toFixed(2);
}


// ----------------------------------------------------
// Validate Restock Form
// ----------------------------------------------------
function validateRestockForm() {
    let addStock = document.getElementById("add_stock").value;
    let buyPrice = document.getElementById("buy_price").value;
    let sellPrice = document.getElementById("sell_price").value;

    if (addStock === "" || buyPrice === "" || sellPrice === "") {
        alert("Please fill all fields.");
        return false;
    }

    if (addStock <= 0) {
        alert("Stock quantity must be greater than 0.");
        return false;
    }

    if (buyPrice <= 0 || sellPrice <= 0) {
        alert("Price must be greater than 0.");
        return false;
    }

    return true;
}
