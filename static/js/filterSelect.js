function applyFilters() {
    const estadoSelect = document.getElementById('filterSelect');
    const columnElement = estadoSelect.getAttribute('data-column')
    const selectedValue = estadoSelect ? estadoSelect.value : '0';
    const rows = document.querySelectorAll(itemElement);

    rows.forEach(row => {
        const itemValue = row.getAttribute(columnElement);
        row.style.display = (selectedValue === '0' || itemValue === selectedValue) ? '' : 'none';
    });

}

applyFilters();

