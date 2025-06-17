const API_URL = 'http://192.168.187.178:8000/obtener_coordenadas';

const firebaseConfig = {
  apiKey: "AIzaSyBjGScX3XgV30r1tI31_Xa21gYQDH04caA",
  authDomain: "webencomiendas.firebaseapp.com",
  databaseURL: "https://webencomiendas-default-rtdb.firebaseio.com",
  projectId: "webencomiendas",
  storageBucket: "webencomiendas.firebasestorage.app",
  messagingSenderId: "832724016070",
  appId: "1:832724016070:web:ff77388c8bb7844ad470c7"
};


firebase.initializeApp(firebaseConfig);

function mostrarMapaViaje(viajeIndex, viaje) {
  const mapDiv = document.getElementById(`map-viaje-${viajeIndex}`) || document.getElementById("map");
  mapDiv.innerHTML = "";

  const map = new google.maps.Map(mapDiv, {
    center: {
      lat: parseFloat(viaje.iniciolat_via),
      lng: parseFloat(viaje.iniciolon_via)
    },
    zoom: 14,
  });

  function crearMarcadorConInfo(pos, titulo, icono) {
    const marker = new google.maps.Marker({
      position: pos,
      map,
      title: titulo,
      icon: icono
    });

    const infoWindow = new google.maps.InfoWindow({
      content: `<div style="font-weight:bold;">${titulo}</div>`
    });

    infoWindow.open(map, marker);

    marker.addListener('click', () => {
      infoWindow.open(map, marker);
    });

    return marker;
  }

  // Marcadores de inicio y fin
  crearMarcadorConInfo(
    { lat: parseFloat(viaje.iniciolat_via), lng: parseFloat(viaje.iniciolon_via) },
    "Inicio del Viaje",
    "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
  );

  crearMarcadorConInfo(
    { lat: parseFloat(viaje.finlat_via), lng: parseFloat(viaje.finlon_via) },
    "Fin del Viaje",
    "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
  );


// Ubicación en tiempo real desde Firebase (sin necesidad de dni)
let marcadorFirebase = null;
let infoWindowFirebase = null;

// Cambia 'vehiculo_actual' por el nodo que estés usando en Firebase
const refFirebase = firebase.database().ref(`ubicaciones/6`);

console.log('viaje',viaje.id)

refFirebase.on('value', snapshot => {
  const data = snapshot.val();
  if (data && data.latitud && data.longitud) {
    const lat = data.latitud;
    const lng = data.longitud;

    console.log(lat)
    console.log(lng)

    if (!marcadorFirebase) {
      marcadorFirebase = new google.maps.Marker({
        position: { lat, lng },
        map,
        title: "Ubicación en tiempo real",
        icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
      });

      infoWindowFirebase = new google.maps.InfoWindow({
        content: `<div style="font-weight:bold; background:white; padding: 2px 6px; border-radius: 4px; border: 1px solid #666;">
                    Posición actual en tiempo real
                  </div>`
      });

      infoWindowFirebase.open(map, marcadorFirebase);
      map.setCenter({ lat, lng });
    } else {
      marcadorFirebase.setPosition({ lat, lng });
      infoWindowFirebase.setPosition({ lat, lng });
    }
  }
});

}

// Inicializar automáticamente usando parámetros URL
window.addEventListener('load', () => {
  const params = new URLSearchParams(window.location.search);
  const viaje = {
    iniciolat_via: params.get("lat1"),
    iniciolon_via: params.get("lon1"),
    finlat_via: params.get("lat2"),
    finlon_via: params.get("lon2"),
    incidentes: [] // podrías cargar desde backend si es necesario
  };

  if (viaje.iniciolat_via && viaje.finlat_via) {
    mostrarMapaViaje(0, viaje);
  } else {
    console.warn("Coordenadas no proporcionadas en la URL");
  }
});
