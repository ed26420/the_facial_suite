document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("payment-form");
    if (!form) return;

    const publishableKey = form.dataset.stripeKey;
    const clientSecret = form.dataset.clientSecret;
    const amountInCents = Number(form.dataset.amount || 0);
    const cartTotal = form.dataset.cartTotal || "0.00";

    if (!publishableKey) {
        console.error("Missing STRIPE_PUBLISHABLE_KEY on #payment-form.");
        return;
    }

    const stripe = Stripe(publishableKey);
    const elements = stripe.elements();

    const elementStyle = {
        base: {
            fontSize: "16px",
            color: "#32325d",
            "::placeholder": { color: "#aab7c4" }
        }
    };

    // Mount Split Card Elements
    const cardNumberElement = elements.create("cardNumber", { style: elementStyle });
    cardNumberElement.mount("#card-number-element");

    const cardExpiryElement = elements.create("cardExpiry", { style: elementStyle });
    cardExpiryElement.mount("#card-expiry-element");

    const cardCvcElement = elements.create("cardCvc", { style: elementStyle });
    cardCvcElement.mount("#card-cvv-element");

    // Configure Wallet / Express Checkout (Apple Pay / Google Pay)
    if (amountInCents > 0) {
        const paymentRequest = stripe.paymentRequest({
            country: "AE",
            currency: "aed",
            total: {
                label: "The Facial Suite",
                amount: amountInCents
            },
            requestPayerName: true,
            requestPayerEmail: true
        });

        const paymentRequestButton = elements.create("paymentRequestButton", {
            paymentRequest: paymentRequest
        });

        paymentRequest.canMakePayment().then(function (result) {
            if (result) {
                paymentRequestButton.mount("#payment-request-button");
            } else {
                const msg = document.getElementById("wallet-unavailable-message");
                if (msg) msg.style.display = "block";
            }
        });

        paymentRequest.on("paymentmethod", async (event) => {
            try {
                const result = await stripe.confirmCardPayment(
                    clientSecret,
                    { payment_method: event.paymentMethod.id },
                    { handleActions: false }
                );

                if (result.error) {
                    event.complete("fail");
                    alert(result.error.message);
                    return;
                }

                event.complete("success");
                let paymentIntent = result.paymentIntent;

                if (paymentIntent && paymentIntent.status === "requires_action") {
                    const confirmResult = await stripe.confirmCardPayment(clientSecret);
                    if (confirmResult.error) {
                        alert(confirmResult.error.message);
                        return;
                    }
                    paymentIntent = confirmResult.paymentIntent;
                }

                if (paymentIntent && paymentIntent.status === "succeeded") {
                    document.getElementById("payment_intent_id").value = paymentIntent.id;
                    form.submit();
                }
            } catch (error) {
                event.complete("fail");
                console.error("Stripe wallet error:", error);
                alert("There was a problem processing your payment.");
            }
        });
    }

    // Handle Standard Card Form Submission
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const submitBtn = document.getElementById("submit-btn");
        const buttonText = document.getElementById("button-text");

        submitBtn.disabled = true;
        buttonText.innerText = "Processing Payment...";

        const firstName = document.querySelector('input[name="first_name"]').value;
        const lastName = document.querySelector('input[name="last_name"]').value;

        const result = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardNumberElement,
                billing_details: {
                    name: `${firstName} ${lastName}`
                }
            }
        });

        if (result.error) {
            alert(result.error.message);
            submitBtn.disabled = false;
            buttonText.innerText = `Checkout & Pay AED ${cartTotal}`;
            return;
        }

        if (result.paymentIntent && result.paymentIntent.status === "succeeded") {
            document.getElementById("payment_intent_id").value = result.paymentIntent.id;
            form.submit();
        }
    });
});