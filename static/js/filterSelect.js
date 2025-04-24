const FILTER_VALUE_DEFAULT = 'default';

function applyFilters() {
    document.querySelectorAll('.filterSelect').forEach(filter => {
        filter.addEventListener('change', function () {
            var nombreSelect = this.id;
            var elementSelect = this.value;
            const rows = document.querySelectorAll('#productTableBody tr[data-' + nombreSelect + ']');

            rows.forEach(row => {
                const itemDiv = row;
                const itemSelect = itemDiv ? itemDiv.getAttribute('data-' + nombreSelect) : null;

                if (elementSelect === `${FILTER_VALUE_DEFAULT}` || itemSelect === elementSelect) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });
}

applyFilters();