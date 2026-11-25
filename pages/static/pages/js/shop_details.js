document.addEventListener("DOMContentLoaded", function () {
    const qtyInput = document.querySelector(".input-quantity .quantity");
    const minusBtn = document.querySelector(".input-quantity .quantity-down");
    const plusBtn = document.querySelector(".input-quantity .quantity-up");

    if (qtyInput && minusBtn && plusBtn) {
        minusBtn.addEventListener("click", function () {
            const current = parseInt(qtyInput.value, 10) || 1;
            if (current > 1) {
                qtyInput.value = current - 1;
            }
        });

        plusBtn.addEventListener("click", function () {
            const current = parseInt(qtyInput.value, 10) || 1;
            qtyInput.value = current + 1;
        });
    }
});