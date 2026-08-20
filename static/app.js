function useExample(button) {
    document.getElementById("query").value =
        button.textContent.trim();
}


async function askCompareX() {

    const queryInput = document.getElementById("query");
    const query = queryInput.value.trim();

    if (!query) {
        showError("Please enter a question.");
        return;
    }

    const button = document.getElementById("ask-button");

    const loading = document.getElementById("loading");
    const error = document.getElementById("error");
    const answerSection = document.getElementById("answer-section");

    error.classList.add("hidden");
    answerSection.classList.add("hidden");
    loading.classList.remove("hidden");

    button.disabled = true;

    try {

        const response = await fetch(
            "/api/v1/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    query: query,
                    limit: 3
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                `Request failed (${response.status})`
            );
        }

        const data = await response.json();

        displayResult(data);

    } catch (error) {

        showError(
            error.message ||
            "Something went wrong."
        );

    } finally {

        loading.classList.add("hidden");
        button.disabled = false;
    }
}


function displayResult(data) {

    const answerSection =
        document.getElementById("answer-section");

    const answer =
        document.getElementById("answer");

    answer.textContent =
        data.answer || "No answer was generated.";

    displayProducts(
        data.products || []
    );

    displayDocuments(
        data.documents || []
    );

    answerSection.classList.remove("hidden");
}


function displayProducts(products) {

    const card =
        document.getElementById("products-card");

    const container =
        document.getElementById("products");

    container.innerHTML = "";

    if (!products.length) {
        card.classList.add("hidden");
        return;
    }

    products.forEach(product => {

        const element =
            document.createElement("div");

        element.className = "product";

        const price =
            product.price !== null &&
            product.price !== undefined
                ? `${product.price} ${product.currency || ""}`
                : "Price unavailable";

        const rating =
            product.rating !== null &&
            product.rating !== undefined
                ? product.rating
                : "N/A";

        element.innerHTML = `
            <h3>${escapeHtml(product.name || "Unknown product")}</h3>

            <div class="product-meta">
                Brand: ${escapeHtml(product.brand || "N/A")}
            </div>

            <div class="product-meta">
                Price: ${escapeHtml(String(price))}
            </div>

            <div class="product-meta">
                Rating: ${escapeHtml(String(rating))}
            </div>
        `;

        container.appendChild(element);
    });

    card.classList.remove("hidden");
}


function displayDocuments(documents) {

    const card =
        document.getElementById("documents-card");

    const container =
        document.getElementById("documents");

    container.innerHTML = "";

    if (!documents.length) {
        card.classList.add("hidden");
        return;
    }

    documents.forEach(doc => {

        const element =
            document.createElement("div");

        element.className = "document";

        const page =
            doc.page !== undefined &&
            doc.page !== null
                ? `Page ${doc.page}`
                : "Page unavailable";

        element.innerHTML = `
            <strong>
                ${escapeHtml(page)}
            </strong>

            <p>
                ${escapeHtml(
                    doc.text || ""
                )}
            </p>
        `;

        container.appendChild(element);
    });

    card.classList.remove("hidden");
}


function showError(message) {

    const error =
        document.getElementById("error");

    error.textContent = message;

    error.classList.remove("hidden");
}


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}