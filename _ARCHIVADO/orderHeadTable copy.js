
  document.addEventListener("DOMContentLoaded", function () {
    const table = document.querySelector(".table_listado");
    const headers = table.querySelectorAll("thead th");
    let sortDirection = {}; // Para saber en qué orden está cada columna

    headers.forEach((header, index) => {
      if (!header.classList.contains("opciones_column")) {
        // header.style.cursor = "pointer";
        header.addEventListener("click", () => {
          // const content = header.querySelector('.th_content');
          // const elementP = content.querySelector('p').textContent;
          // let directionIcon = 'down';
          
          const tbody = table.querySelector("tbody");
          const rows = Array.from(tbody.querySelectorAll("tr"));
          
          const currentDirection = sortDirection[index] || 'desc';
          const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
          sortDirection[index] = newDirection;
          // directionIcon = 'up' ? 'down' : 'up';
          // content.innerHTML = `<p>${elementP}</p> <i class="fa-solid fa-caret-${directionIcon}"></i>`;

          rows.sort((rowA, rowB) => {
            const cellA = rowA.cells[index].innerText.trim();
            const cellB = rowB.cells[index].innerText.trim();

            const isNumeric = !isNaN(cellA) && !isNaN(cellB);

            if (isNumeric) {
              return newDirection === 'asc'
                ? parseFloat(cellA) - parseFloat(cellB)
                : parseFloat(cellB) - parseFloat(cellA);
            } else {
              return newDirection === 'asc'
                ? cellA.localeCompare(cellB)
                : cellB.localeCompare(cellA);
            }
          });

          // Limpiamos y volvemos a insertar las filas ordenadas
          tbody.innerHTML = '';
          rows.forEach(row => tbody.appendChild(row));
        });
      }
    });
  });