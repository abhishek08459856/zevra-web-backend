console.log("JS loaded");

document.getElementById("add").onclick = function () {
    let no_of_product = parseInt(document.getElementById("products").value) || 0;
    if (no_of_product <= 0) return;

    let container = document.querySelector(".form-new");
    let html = "";

    for (let i = 0; i < no_of_product; i++) {
        html += `
        <div class="s_no">${i + 1}.</div>
        <div class="form-row product-row">
            <div class="form-group category-group">
                <label>category:</label>
                <select name="category" class="category">
                    <option value="">metal</option>
                    <option value="gold">Gold</option>
                    <option value="silver">Silver</option>
                </select>
            </div>
            <div class="form-group">
                <label>product name:</label>
                <input type="text" name="product_name" placeholder="product name">
            </div>
            <div class="form-group">
                <label>weight :</label>
                <input type="text" name="weight" class="weight" placeholder="weight in gram">
            </div>
            <div class="form-group">
                <label>rate :</label>
                <input type="text" name="rate" class="rate" placeholder="rate">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label>m.charge :</label>
                <input type="text" name="making_charge" class="making_charge" placeholder="making charge">
            </div>
            <div class="form-group">
                <label>amount :</label>
                <input type="number" name="amount" class="amount" placeholder="amount" readonly>
            </div>
        </div>`;
    }

    container.insertAdjacentHTML('beforeend', html);

    function calculateAmount(row) {
        let category = row.querySelector(".category");
        let weight = row.querySelector(".weight");
        let rate = row.querySelector(".rate");
        let mcharge = row.nextElementSibling.querySelector(".making_charge");
        let amount = row.nextElementSibling.querySelector(".amount");

        let w = parseFloat(weight.value) || 0;
        let r = parseFloat(rate.value) || 0;
        let m = parseFloat(mcharge.value) || 0;
        let cat = (category.value || "").toLowerCase();

        if (cat === "gold") {
            amount.value = ((w * r) + (w * m)).toFixed(2);
        } else if (cat === "silver") {
            amount.value = ((w * r) + m).toFixed(2);
        } else {
            amount.value = 0;
        }

        // Update total_amount
        let total = 0;
        container.querySelectorAll(".amount").forEach(a => {
            total += parseFloat(a.value) || 0;
        });
        let totalField = document.querySelector('input[name="total_amount"]');
        if (totalField) totalField.value = total.toFixed(2);
    }

    // Add listeners
    let productRows = container.querySelectorAll(".product-row");
    productRows.forEach(function (row) {
        let category = row.querySelector(".category");
        let weight = row.querySelector(".weight");
        let rate = row.querySelector(".rate");
        let mcharge = row.nextElementSibling.querySelector(".making_charge");

        [category, weight, rate, mcharge].forEach(input => {
            if (!input.dataset.listener) {
                input.dataset.listener = true;
                input.addEventListener("input", () => calculateAmount(row));
                input.addEventListener("change", () => calculateAmount(row));
            }
        });

        // Gold carat dropdown
        if (!category.dataset.caratListener) {
            category.dataset.caratListener = true;
            category.addEventListener("change", () => {
                let caratGroup = row.querySelector(".carat-group");

                if (category.value === "gold") {
                    if (!caratGroup) {
                        let caratHTML = `
                        <div class="form-group carat-group">
                            <label>carat:</label>
                            <select name="carat" class="carat">
                                <option value="">carat</option>
                                <option value="18">18k</option>
                                <option value="22">22k</option>
                                <option value="24">24k</option>
                            </select>
                        </div>`;
                        let catGroup = row.querySelector(".category-group");
                        catGroup.insertAdjacentHTML('afterend', caratHTML);
                    }
                } else {
                    if (caratGroup) caratGroup.remove();
                }
                calculateAmount(row);
            });
        }
    });
};
