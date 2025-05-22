//Agregar lo siguiente en el html
// <div class="mapa-container col">
  //          <div id="map"></div>
    //    </div> */


// Inicializar el mapa
const map = L.map('map').setView([-9.1900, -75.0152], 5); // Vista centrada en Perú

// Agregar capa de mapa base
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);