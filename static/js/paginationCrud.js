document.addEventListener("DOMContentLoaded", function () {
  const table = document.querySelector(".table_listado");
  const headers = table.querySelectorAll("thead th");
  const allRows = Array.from(document.querySelectorAll("#productTableBody tr"));
  const prevBtn = document.querySelector(".previous-page");
  const nextBtn = document.querySelector(".next-page");
  const pageNumbersContainer = document.getElementById("pageNumbers");
  const selectCantidad = document.getElementById("cant_pag");
  const filters = document.querySelectorAll(".filterSelect");
  const searchInput = document.getElementById("value_search");

  let currentPage = 1;
  let rowsPerPage = parseInt(selectCantidad.value);
  let filteredRows = [...allRows];
  let sortDirection = {}; // Almacena orden actual de cada columna
  let currentSort = { index: null, direction: null }; // Para recordar última columna ordenada

  // Para mantener textos originales de headers al reiniciar íconos
  const originalTexts = [];
  headers.forEach((header, index) => {
    if (!header.classList.contains("opciones_column")) {
      const content = header.querySelector('.th_content');
      const originalText = content.querySelector('p').textContent;
      originalTexts[index] = originalText;
    }
  });

  function applyFilters() {
    const activeFilters = {};
    filters.forEach(filter => {
      const type = filter.dataset.type;
      const id = filter.id;
      const value = filter.value;
      if (!activeFilters[id]) activeFilters[id] = {};
      activeFilters[id].type = type;
      activeFilters[id].value = value;
    });

    const searchTerm = searchInput?.value?.trim().toLowerCase() || '';

    filteredRows = allRows.filter(row => {
      const matchesFilters = Object.entries(activeFilters).every(([id, config]) => {
        const dataType = config.type;
        const filterValue = config.value;
        const dataKey = id.replace(/_ini$|_fin$/, '');
        const rowValue = row.dataset[dataKey];

        if (filterValue === "") return true;

        if (dataType === 'date') return rowValue === filterValue;
        if (dataType === 'date_ini') return rowValue >= filterValue;
        if (dataType === 'date_fin') return rowValue <= filterValue;

        return rowValue === filterValue;
      });

      const matchesSearch = !searchInput || Array.from(row.querySelectorAll("p"))
        .some(cell => cell.textContent.toLowerCase().includes(searchTerm));

      return matchesFilters && matchesSearch;
    });

    // Si hay ordenamiento activo, lo reaplicamos sobre los datos filtrados
    if (currentSort.index !== null) {
      sortRows(currentSort.index, currentSort.direction);
    }

    currentPage = 1;
    showPage(currentPage);
  }

  function sortRows(index, direction) {
    filteredRows.sort((rowA, rowB) => {
      const cellA = rowA.cells[index].innerText.trim();
      const cellB = rowB.cells[index].innerText.trim();
      const isNumeric = !isNaN(cellA) && !isNaN(cellB);

      if (isNumeric) {
        return direction === 'asc'
          ? parseFloat(cellA) - parseFloat(cellB)
          : parseFloat(cellB) - parseFloat(cellA);
      } else {
        return direction === 'asc'
          ? cellA.localeCompare(cellB)
          : cellB.localeCompare(cellA);
      }
    });
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
    const maxVisible = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2));
    let endPage = startPage + maxVisible - 1;
    if (endPage > totalPages) {
      endPage = totalPages;
      startPage = Math.max(1, endPage - maxVisible + 1);
    }

    if (startPage > 1) {
      createPageButton(1);
      if (startPage > 2) createDots();
    }
    for (let i = startPage; i <= endPage; i++) {
      createPageButton(i);
    }
    if (endPage < totalPages) {
      if (endPage < totalPages - 1) createDots();
      createPageButton(totalPages);
    }

    function createPageButton(i) {
      const btn = document.createElement("a");
      btn.href = "javascript:void(0)";
      btn.textContent = i;
      btn.className = "page-number";
      if (i === currentPage) btn.classList.add("active");
      btn.addEventListener("click", () => showPage(i));
      pageNumbersContainer.appendChild(btn);
    }
    function createDots() {
      const dots = document.createElement("span");
      dots.textContent = "...";
      dots.className = "dots";
      pageNumbersContainer.appendChild(dots);
    }
  }

  // Eventos filtros
  filters.forEach(filter => filter.addEventListener("change", applyFilters));
  if (searchInput) searchInput.addEventListener("input", applyFilters);
  selectCantidad.addEventListener("change", () => {
    rowsPerPage = parseInt(selectCantidad.value);
    currentPage = 1;
    showPage(currentPage);
  });
  prevBtn.addEventListener("click", () => { if (currentPage > 1) showPage(currentPage - 1); });
  nextBtn.addEventListener("click", () => {
    const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
    if (currentPage < totalPages) showPage(currentPage + 1);
  });

  // Ordenamiento de columnas
  headers.forEach((header, index) => {
    if (!header.classList.contains("opciones_column")) {
      const content = header.querySelector('.th_content');
      header.addEventListener("click", () => {
        const currentDirection = sortDirection[index] || 'desc';
        const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
        sortDirection = {};
        sortDirection[index] = newDirection;
        currentSort = { index, direction: newDirection };

        // Reiniciar íconos
        headers.forEach((h, i) => {
          if (!h.classList.contains("opciones_column")) {
            const cont = h.querySelector('.th_content');
            cont.innerHTML = `<p>${originalTexts[i]}</p>`;
          }
        });

        // Colocar ícono en columna actual
        const directionIcon = newDirection === 'asc' ? 'down' : 'up';
        content.innerHTML = `<p>${originalTexts[index]}</p> <i class="fa-solid fa-caret-${directionIcon}"></i>`;

        // Ordenar y mostrar
        sortRows(index, newDirection);
        currentPage = 1;
        showPage(currentPage);
      });
    }
  });

  applyFilters(); // inicializar
});
