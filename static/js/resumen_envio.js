

document.addEventListener('DOMContentLoaded', () => {
  const STORAGE_KEY = 'enviosMasivosTemp';

  let enviosMasivos = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  if (!Array.isArray(enviosMasivos)) {
    enviosMasivos = [];
    localStorage.setItem(STORAGE_KEY, JSON.stringify(enviosMasivos));
  }

  // 2. Referencias al DOM
  const tableBody = document.querySelector('.tabla-envios tbody');
  const btnAgregar = document.querySelector('.btn-agregar');
  const btnPagar  = document.getElementById('btn-continuar');

  // 3. Función para renderizar la tabla
  function renderTabla() {
    if (enviosMasivos.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" style="text-align:center; padding:1rem;">
            No hay envíos registrados.
          </td>
        </tr>
      `;
      return;
    }

    tableBody.innerHTML = enviosMasivos.map((envio, idx) => {
      // Destinatario
      let nombreDest;
      if (envio.destinatario.tipoDocumento === '2') {
        nombreDest = envio.destinatario.razonSocial;
      } else {
        nombreDest = `${envio.destinatario.nombres} ${envio.destinatario.apellidos}`.trim();
      }
      // Tarifa (valor declarado como ejemplo)
      const tarifa = (parseFloat(envio.paquete.valorEnvio) || 0).toFixed(2);

      return `
        <tr>
          <td>${envio.destino.tipoEntrega}</td>
          <td>${nombreDest}</td>
          <td>
            ${envio.destino.distrito}, 
            ${envio.destino.provincia}, 
            ${envio.destino.departamento}
          </td>
          <td>${envio.destino.direccion || '—'}</td>
          <td>S/ ${tarifa}</td>
          <td>
            <button class="btn-editar" data-index="${idx}">Editar</button>
            <button class="btn-eliminar" data-index="${idx}">Eliminar</button>
          </td>
        </tr>
      `;
    }).join('');
  }

  // 4. Delegación de eventos sobre la tabla
  tableBody.addEventListener('click', (e) => {
    const btn = e.target;
    if (btn.matches('.btn-editar')) {
      const idx = btn.dataset.index;
      if (confirm('¿Deseas editar este envío?')) {
        // guarda el índice para que el registro lo reciba
        localStorage.setItem('editIndex', idx);
        window.location.href = '/registro_envio';
      }
    }

    if (btn.matches('.btn-eliminar')) {
      const idx = btn.dataset.index;
      if (confirm('¿Deseas eliminar este envío?')) {
        enviosMasivos.splice(idx, 1);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(enviosMasivos));
        renderTabla();
      }
    }
  });


  btnPagar.addEventListener('click', () => {
    window.location.href = '/pagoenvio  ';
  });

  renderTabla();
});
