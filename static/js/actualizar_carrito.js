function actualizarCantidadCarrito() {
    const carrito = JSON.parse(localStorage.getItem('carrito') || '[]');
    const totalCantidad = carrito.reduce((sum, item) => sum + (item.quantity || 0), 0);

    const cantidadEl = document.getElementById("cantidad_carrito");
    if (cantidadEl) {
        cantidadEl.textContent = totalCantidad;
        cantidadEl.style.display = totalCantidad > 0 ? "block" : "none";
    }
}
