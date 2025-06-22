const API_URL = 'http://192.168.100.15:8000/obtener_coordenadas';

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

async function mostrarMapaViaje(viajeIndex, viaje) {
  const mapDiv = document.getElementById(`map-viaje-${viajeIndex}`) || document.getElementById("map");
  mapDiv.innerHTML = "";

  const map = new google.maps.Map(mapDiv, {
    center: {
      lat: parseFloat(viaje.iniciolat_via),
      lng: parseFloat(viaje.iniciolon_via)
    },
    zoom: 14,
  });

  const inicio = {
    lat: parseFloat(viaje.iniciolat_via),
    lng: parseFloat(viaje.iniciolon_via)
  };

  const fin = {
    lat: parseFloat(viaje.finlat_via),
    lng: parseFloat(viaje.finlon_via)
  };

  crearMarcadorConInfo(map, inicio, "Inicio del Viaje", "http://maps.google.com/mapfiles/ms/icons/green-dot.png");
  crearMarcadorConInfo(map, fin, "Fin del Viaje", "http://maps.google.com/mapfiles/ms/icons/red-dot.png");

  await dibujarRutaPolyline(map, inicio, fin);

  let marcadorFirebase = null;
let infoWindowFirebase = null;

// Suponiendo que `viaje.id` contiene el ID de seguimiento en Firebase
const refFirebase = firebase.database().ref(`ubicaciones/${viaje.id}`);

refFirebase.on('value', snapshot => {
  const data = snapshot.val();
  if (data && data.latitud && data.longitud) {
    const lat = data.latitud;
    const lng = data.longitud;

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
      map.setCenter({ lat, lng });  // Opcional: centrar en el vehículo
    } else {
      marcadorFirebase.setPosition({ lat, lng });
      infoWindowFirebase.setPosition({ lat, lng });
    }
  }
});


}

function crearMarcadorConInfo(map, pos, titulo, icono) {
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
}


async function dibujarRutaPolyline(map, inicio, fin) {
  const API_KEY = 'AIzaSyBMLaqfr73_v_K7PfOhAq39cmjg7lKZT6o';  // Usa una API key válida con acceso a Routes API

  const response = await fetch(`https://routes.googleapis.com/directions/v2:computeRoutes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Goog-Api-Key': API_KEY,
      'X-Goog-FieldMask': 'routes.polyline.encodedPolyline'
    },
    body: JSON.stringify({
      origin: {
        location: {
          latLng: { latitude: inicio.lat, longitude: inicio.lng }
        }
      },
      destination: {
        location: {
          latLng: { latitude: fin.lat, longitude: fin.lng }
        }
      },
      travelMode: "DRIVE"
    })
  });

  const data = await response.json();
  const ruta = data.routes?.[0];
  const polylineEncoded = data.routes?.[0]?.polyline?.encodedPolyline;

  if (polylineEncoded) {
    const path = google.maps.geometry.encoding.decodePath(polylineEncoded);
    const polyline = new google.maps.Polyline({
      path,
      geodesic: true,
      strokeColor: "#1976D2",
      strokeOpacity: 1.0,
      strokeWeight: 5
    });
    polyline.setMap(map);



  } else {
    console.warn("No se pudo obtener la ruta desde Google Routes API");
  }
}


// Inicializar automáticamente usando parámetros URL
window.addEventListener('load', () => {
  const params = new URLSearchParams(window.location.search);
  const viaje = {
    iniciolat_via: params.get("lat1"),
    iniciolon_via: params.get("lon1"),
    finlat_via: params.get("lat2"),
    finlon_via: params.get("lon2"),
    id : params.get('id')
  };

  if (viaje.iniciolat_via && viaje.finlat_via) {
    mostrarMapaViaje(0, viaje);
  } else {
    console.warn("Coordenadas no proporcionadas en la URL");
  }
});
