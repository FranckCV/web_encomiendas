document.addEventListener('DOMContentLoaded', () => {
  const STORAGE_KEY = 'envios_masivos';
  const tbody = document.querySelector(".tabla-envios tbody");

  // function renderUltimoRegistro() {
  //   const data = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  //   tbody.innerHTML = "";

  //   if (data.length === 0) {
  //     const fila = document.createElement('tr');
  //     fila.innerHTML = `<td colspan="6">No hay envíos registrados.</td>`;
  //     tbody.appendChild(fila);
  //     return;
  //   }

  //   const envio = data[data.length - 1];

  //   const tipoRecepcion = envio.destino.tipoEntregaNombre || '-';
  //   const nombreDestinatario = envio.destinatario.razonSocial || `${envio.destinatario.nombres || ''} ${envio.destinatario.apellidos || ''}`.trim();
  //   const destino = `${envio.destino.departamento}, ${envio.destino.provincia}, ${envio.destino.distrito}`;
  //   const direccion = envio.destino.direccion || '-';
  //   const tarifa = envio.paquete.valorEnvio ? `S/ ${parseFloat(envio.paquete.valorEnvio).toFixed(2)}` : 'S/ 0.00';

  //   const fila = document.createElement('tr');
  //   fila.innerHTML = `
  //     <td>${tipoRecepcion}</td>
  //     <td>${nombreDestinatario}</td>
  //     <td>${destino}</td>
  //     <td>${direccion}</td>
  //     <td>${tarifa}</td>
  //     <td>
  //       <button class="btn-editar" data-index="${data.length - 1}">Editar</button>
  //       <button class="btn-eliminar" data-index="${data.length - 1}">Eliminar</button>
  //     </td>
  //   `;

  //   tbody.appendChild(fila);
  // }

  tbody.addEventListener('click', e => {
    if (e.target.classList.contains('btn-eliminar')) {
      const index = parseInt(e.target.dataset.index);
      let data = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
      data.splice(index, 1);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      location.reload();
    } else if (e.target.classList.contains('btn-editar')) {
      const index = parseInt(e.target.dataset.index);
      localStorage.setItem('edit_envio_index', index);
      window.location.href = '/registro-envio';
    }
  });

  renderUltimoRegistro();
});



function eliminar_storage(){
  fetch('/eliminar_envio', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  window.location.reload();
}
