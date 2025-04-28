document.addEventListener("DOMContentLoaded", function () {
  const allRows = Array.from(document.querySelectorAll("#productTableBody tr"));
  const prevBtn = document.querySelector(".previous-page");
  const nextBtn = document.querySelector(".next-page");
  const pageNumbersContainer = document.getElementById("pageNumbers");
  const selectCantidad = document.getElementById("cant_pag");
  const filters = document.querySelectorAll(".filterSelect");
  const FILTER_VALUE_DEFAULT = "default";
  const searchInput = document.getElementById("value_search");
  const headers = document.querySelectorAll(".table_listado thead th");

  let currentPage = 1;
  let rowsPerPage = parseInt(selectCantidad.value);
  let filteredRows = [...allRows];
  let currentSortColumn = null;
  let currentSortDirection = 'asc';
  const originalTexts = [];

  // Capturar los textos originales de los headers
  headers.forEach((header, index) => {
    if (!header.classList.contains("opciones_column")) {
      const content = header.querySelector('.th_content');
      const originalText = content?.querySelector('p')?.textContent?.trim();
      originalTexts[index] = originalText;
    }
  });

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

    if (currentSortColumn) {
      sortRows();
    }

    currentPage = 1;
    showPage(currentPage);
  }

  function showPage(page) {
    rowsPerPage = parseInt(selectCantidad.value);
    const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
    if (page < 1) page = 1;
    if (page > totalPages) page = totalPages;

    allRows.forEach(row => row.style.display = "none");

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

  function sortRows() {
    filteredRows.sort((a, b) => {
      const aVal = a.getAttribute(`data-${currentSortColumn}`)?.toLowerCase() || "";
      const bVal = b.getAttribute(`data-${currentSortColumn}`)?.toLowerCase() || "";

      if (!isNaN(aVal) && !isNaN(bVal)) {
        return currentSortDirection === 'asc'
          ? parseFloat(aVal) - parseFloat(bVal)
          : parseFloat(bVal) - parseFloat(aVal);
      }

      return currentSortDirection === 'asc'
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal);
    });
  }

  function handleHeaderClick(header, index) {
    if (header.classList.contains("opciones_column")) return;

    const columnName = filters[index]?.id || header.getAttribute("data-column");
    if (!columnName) return;

    if (currentSortColumn === columnName) {
      currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      currentSortColumn = columnName;
      currentSortDirection = 'asc';
    }

    // Limpiar íconos anteriores
    headers.forEach((h, i) => {
      if (!h.classList.contains("opciones_column")) {
        const cont = h.querySelector('.th_content');
        cont.innerHTML = `<p>${originalTexts[i]}</p>`;
      }
    });

    // Agregar ícono actual
    const content = header.querySelector('.th_content');
    const icon = currentSortDirection === 'asc' ? 'down' : 'up';
    content.innerHTML = `<p>${originalTexts[index]}</p> <i class="fa-solid fa-caret-${icon}"></i>`;

    sortRows();
    showPage(1);
  }

  // Eventos
  filters.forEach(filter => {
    filter.addEventListener("change", applyFilters);
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

  searchInput.addEventListener("input", applyFilters);

  headers.forEach((header, index) => {
    header.style.cursor = "pointer";
    header.addEventListener("click", () => {
      handleHeaderClick(header, index);
    });
  });

  applyFilters(); // Inicializa todo
});
