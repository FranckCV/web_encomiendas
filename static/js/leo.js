// Función para alternar un menú específico
function toggleMenu(menuId) {
    // Primero cerramos todos los menús
    const menus = document.querySelectorAll('.menu_ayuda');
    menus.forEach(menu => {
        if (menu.id !== menuId) {
            menu.classList.remove('show');
        }
    });
    
    // Luego alternamos el menú seleccionado
    const targetMenu = document.getElementById(menuId);
    targetMenu.classList.toggle('show');
}

// Cerrar menú cuando se hace clic fuera
document.addEventListener('click', function(event) {
    // Verificar si el clic NO fue en un botón de menú
    const isMenuButton = event.target.closest('.ayuda_toggle');
    
    // Si no se hizo clic en un botón de menú ni en un menú abierto, cerramos todos
    if (!isMenuButton) {
        const isInsideMenu = event.target.closest('.menu_ayuda');
        if (!isInsideMenu) {
            const menus = document.querySelectorAll('.menu_ayuda');
            menus.forEach(menu => menu.classList.remove('show'));
        }
    }
});



