document.addEventListener("DOMContentLoaded", function () {
    const rows = Array.from(document.querySelectorAll("#productTableBody tr"));
    const prevBtn = document.querySelector(".previous-page");
    const nextBtn = document.querySelector(".next-page");
    const pageNumbersContainer = document.getElementById("pageNumbers");
    const selectCantidad = document.getElementById("cant_pag");
    let rowsPerPage = parseInt(selectCantidad.value);
    let currentPage = 1;

    function getTotalPages() {
        return Math.ceil(rows.length / rowsPerPage);
    }

    function showPage(page) {
        const totalPages = getTotalPages();
        if (page < 1) page = 1;
        if (page > totalPages) page = totalPages;

        rows.forEach((row, index) => {
            row.style.display = (index >= (page - 1) * rowsPerPage && index < page * rowsPerPage) ? "" : "none";
        });

        currentPage = page;
        updatePageButtons();
        updateNumberButtons();
    }

    function updatePageButtons() {
        prevBtn.classList.toggle("disable", currentPage === 1);
        nextBtn.classList.toggle("disable", currentPage === getTotalPages());
    }

    function updateNumberButtons() {
        pageNumbersContainer.innerHTML = "";
        const totalPages = getTotalPages();

        for (let i = 1; i <= totalPages; i++) {
            const btn = document.createElement("a");
            btn.href = "javascript:void(0)";
            btn.textContent = i;
            btn.className = "page-number";
            if (i === currentPage) btn.classList.add("active");

            btn.addEventListener("click", () => {
                showPage(i);
            });

            pageNumbersContainer.appendChild(btn);
        }
    }

    prevBtn.addEventListener("click", () => {
        if (currentPage > 1) showPage(currentPage - 1);
    });

    nextBtn.addEventListener("click", () => {
        if (currentPage < getTotalPages()) showPage(currentPage + 1);
    });

    // En caso de que el usuario cambie la cantidad por página
    selectCantidad.addEventListener("change", () => {
        rowsPerPage = parseInt(selectCantidad.value);
        showPage(1);
    });

    showPage(1);
});
