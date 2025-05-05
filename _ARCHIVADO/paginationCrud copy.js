document.addEventListener("DOMContentLoaded", function () {
  const allRows = Array.from(document.querySelectorAll("#productTableBody tr"));
  const prevBtn = document.querySelector(".previous-page");
  const nextBtn = document.querySelector(".next-page");
  const pageNumbersContainer = document.getElementById("pageNumbers");
  const selectCantidad = document.getElementById("cant_pag");
  const filters = document.querySelectorAll(".filterSelect");
  const FILTER_VALUE_DEFAULT = "default";
  const searchInput = document.getElementById("value_search");

  let currentPage = 1;
  let rowsPerPage = parseInt(selectCantidad.value);
  let filteredRows = [...allRows]; // Esta lista se actualiza con los filtros

  function applyFilters() {
    const activeFilters = {};
    filters.forEach(filter => {
      activeFilters[filter.id] = filter.value;
    });
  
    const searchTerm = searchInput.value.trim().toLowerCase();
  
    filteredRows = allRows.filter(row => {
      const matchesFilters = Object.entries(activeFilters).every(([key, value]) => {
        return value === FILTER_VALUE_DEFAULT || row.getAttribute(`data-${key}`) === value;
      });
  
      const matchesSearch = Array.from(row.querySelectorAll("p"))
        .some(cell => cell.textContent.toLowerCase().includes(searchTerm));
  
      return matchesFilters && matchesSearch;
    });
  
    currentPage = 1;
    showPage(currentPage);
  }
  

  function showPage(page) {
    rowsPerPage = parseInt(selectCantidad.value);
    const totalPages = Math.ceil(filteredRows.length / rowsPerPage);

    if (page < 1) page = 1;
    if (page > totalPages) page = totalPages;

    allRows.forEach(row => row.style.display = "none"); // Ocultamos todas

    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    filteredRows.slice(start, end).forEach(row => {
      row.style.display = "";
    });

    currentPage = page;
    updatePageButtons(totalPages);
    updateNumberButtons(totalPages);
  }

  function updatePageButtons(totalPages) {
    prevBtn.classList.toggle("disable", currentPage === 1);
    nextBtn.classList.toggle("disable", currentPage === totalPages || totalPages === 0);
  }

  function updateNumberButtons(totalPages) {
    pageNumbersContainer.innerHTML = "";
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

  // Eventos
  filters.forEach(filter => {
    filter.addEventListener("change", () => {
      applyFilters();
    });
  });

  selectCantidad.addEventListener("change", () => {
    rowsPerPage = parseInt(selectCantidad.value);
    currentPage = 1;
    showPage(currentPage);
  });

  prevBtn.addEventListener("click", () => {
    if (currentPage > 1) showPage(currentPage - 1);
  });

  nextBtn.addEventListener("click", () => {
    const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
    if (currentPage < totalPages) showPage(currentPage + 1);
  });

  searchInput.addEventListener("input", () => {
    applyFilters();
  });

  // Inicialización
  applyFilters();
});
