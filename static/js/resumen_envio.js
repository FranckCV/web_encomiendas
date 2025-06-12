

// document.addEventListener('DOMContentLoaded', () => {
//   const STORAGE_KEY = 'enviosMasivosTemp';

//   let enviosMasivos = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
//   if (!Array.isArray(enviosMasivos)) {
//     enviosMasivos = [];
//     localStorage.setItem(STORAGE_KEY, JSON.stringify(enviosMasivos));
//   }

//   // 2. Referencias al DOM
//   const tableBody = document.querySelector('.tabla-envios tbody');
//   const btnAgregar = document.querySelector('.btn-agregar');
//   const btnPagar  = document.getElementById('btn-continuar');

//   // 3. Función para renderizar la tabla
//   function renderTabla() {
//     if (enviosMasivos.length === 0) {
//       tableBody.innerHTML = `
//         <tr>
//           <td colspan="6" style="text-align:center; padding:1rem;">
//             No hay envíos registrados.
//           </td>
//         </tr>
//       `;
//       return;
//     }

//     tableBody.innerHTML = enviosMasivos.map((envio, idx) => {
//       // Destinatario
//       let nombreDest;
//       if (envio.destinatario.tipoDocumento === '2') {
//         nombreDest = envio.destinatario.razonSocial;
//       } else {
//         nombreDest = `${envio.destinatario.nombres} ${envio.destinatario.apellidos}`.trim();
//       }
//       // Tarifa (valor declarado como ejemplo)
//       const tarifa = (parseFloat(envio.paquete.valorEnvio) || 0).toFixed(2);

//       return `
//         <tr>
//           <td>${envio.destino.tipoEntrega}</td>
//           <td>${nombreDest}</td>
//           <td>
//             ${envio.destino.distrito}, 
//             ${envio.destino.provincia}, 
//             ${envio.destino.departamento}
//           </td>
//           <td>${envio.destino.direccion || '—'}</td>
//           <td>S/ ${tarifa}</td>
//           <td>
//             <button class="btn-editar" data-index="${idx}">Editar</button>
//             <button class="btn-eliminar" data-index="${idx}">Eliminar</button>
//           </td>
//         </tr>
//       `;
//     }).join('');
//   }

//   // 4. Delegación de eventos sobre la tabla
//   tableBody.addEventListener('click', (e) => {
//     const btn = e.target;
//     if (btn.matches('.btn-editar')) {
//       const idx = btn.dataset.index;
//       if (confirm('¿Deseas editar este envío?')) {
//         // guarda el índice para que el registro lo reciba
//         localStorage.setItem('editIndex', idx);
//         window.location.href = '/registro_envio';
//       }
//     }

//     if (btn.matches('.btn-eliminar')) {
//       const idx = btn.dataset.index;
//       if (confirm('¿Deseas eliminar este envío?')) {
//         enviosMasivos.splice(idx, 1);
//         localStorage.setItem(STORAGE_KEY, JSON.stringify(enviosMasivos));
//         renderTabla();
//       }
//     }
//   });


//   btnPagar.addEventListener('click', () => {
//     window.location.href = '/pagoenvio  ';
//   });

//   renderTabla();
// });


// js/resumen_envio.js

// Usamos la variable global que inyectamos en la plantilla
const registros = window.REGISTROS || [];

function renderTabla() {
  const container = document.getElementById('tableContent');
  if (registros.length === 0) {
    container.innerHTML = `
      <div class="empty-state">
        <p>No hay envíos registrados aún</p>
        <p>Comienza agregando tu primer envío</p>
      </div>`;
    return;
  }
  let html = `<table>
    <thead>
      <tr>
        <th>#</th><th>Recepción</th><th>Origen</th><th>Destino</th><th>Empaque/Contenido</th>
        <th>Valor</th><th>Peso</th><th>Dimensiones</th><th>Destinatario</th><th>Modalidad pago</th>
        <th>Clave</th><th>Tarifa</th>
      </tr>
    </thead>
    <tbody>`;
  registros.forEach((r, i) => {
    html += `
      <tr>
        <td>${i+1}</td>
        <td>${r.tipoEntrega}</td>
        <td>${r.origen.departamento_origen}/${r.origen.provincia_origen}/${r.origen.distrito_origen}</td>
        <td>${r.destino.departamento}/${r.destino.provincia}/${r.destino.distrito}</td>
        <td>${
          r.tipoEmpaque === 'Folios'
            ? `${r.folios} folios`
            : `${r.tipoEmpaque} — ${r.tipoArticulo}`
        }</td>
        <td>${r.valorEnvio}</td>
        <td>${r.peso}</td>
        <td>${r.largo}×${r.ancho}×${r.alto}</td>
        <td>${r.destinatario}</td>
        <td>${r.modalidadPago}</td>
        <td>${r.clave}</td>
        <td><strong>S/ ${r.tarifa}</strong></td>
      </tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

// Llamamos al render cuando esté cargado el DOM
document.addEventListener('DOMContentLoaded', renderTabla);
