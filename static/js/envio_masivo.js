//Validaciones
//Teléfono
const regexTelefono = /^9\d{8}$/;
//documentos
const regexDNI = /^\d{8}$/;
const regexRUC = /^(10|20)\d{9}$/;
const regexPasaporte = /^[A-Z0-9]{6,12}$/i;
const regexCE = /^[A-Z0-9]{9,12}$/i;
//Nombre completo
const regexNombre = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ ]{2,60}$/;
//Correo
const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

const STORAGE_KEY = 'enviosMasivosTemp';



 const tipoDoc = document.getElementById('remitente-tipo-doc');
const numeroDoc = document.getElementById('remitente-numero-doc');
const mensajeDoc = document.getElementById('mensaje-validacion');

numeroDoc.addEventListener('input', () => {
  const tipo = tipoDoc.value;
  const valor = numeroDoc.value.trim();

  let valido = false;
  let mensaje = '';

  switch (tipo) {
    case '1': valido = regexDNI.test(valor); mensaje = 'Debe tener 8 dígitos.'; break;
    case '2': valido = regexRUC.test(valor); mensaje = 'Debe comenzar con 10 o 20 y tener 11 dígitos.'; break;
    case '3': valido = regexCE.test(valor); mensaje = 'Debe tener 9-12 caracteres alfanuméricos.'; break;
    case '4': valido = regexPasaporte.test(valor); mensaje = 'Debe tener 6-12 caracteres alfanuméricos.'; break;
    default: mensaje = 'Seleccione tipo de documento.'; break;
  }

  if (valor === '') {
    mensajeDoc.style.display = 'none';
    numeroDoc.style.borderColor = '';
  } else if (valido) {
    mensajeDoc.style.display = 'none';
    numeroDoc.style.borderColor = '#48bb78';
  } else {
    mensajeDoc.style.display = 'block';
    mensajeDoc.textContent = mensaje;
    numeroDoc.style.borderColor = '#fc8181';
  }
});

tipoDoc.addEventListener('change', () => {
  const valorActual = numeroDoc.value.trim();
  if (valorActual !== '') {
    numeroDoc.dispatchEvent(new Event('input'));  
  }
});

const telefonoRemitente = document.getElementById('remitente-telefono');
const mensajeTelefono = document.getElementById('mensaje-validacion-telefono');

telefonoRemitente.addEventListener('input', () => {
  const telefono = telefonoRemitente.value.trim();
  const valido = regexTelefono.test(telefono);

  if (telefono === '') {
    mensajeTelefono.style.display = 'none';
    telefonoRemitente.style.borderColor = '';
  } else if (valido) {
    mensajeTelefono.style.display = 'none';
    telefonoRemitente.style.borderColor = 'green';
  } else {
    mensajeTelefono.style.display = 'block';
    mensajeTelefono.textContent = 'El teléfono debe comenzar con 9 y tener 9 dígitos.';
    telefonoRemitente.style.borderColor = 'red';
  }
});



//////////////////////////////////////////////////////////////////////
let enviosMasivos = [];
let editIndex = -1;
let pasoActual = 1;
let cargarDatosEjemplo = false;

const {
  sucursales,
} = window.CONFIG_ENVIO || {};

document.addEventListener("DOMContentLoaded", function () {


  initTabs();
  // initUbigeo();
  origenUbigeo();
  mostrarCamposDestino();
  toggleFolios();
  toggleArticulos();
  mostrarCamposReceptor();
});

function origenUbigeo() {
  const selectDep = document.getElementById('origen-departamento');
  const selectProv = document.getElementById('origen-provincia');
  const selectDist = document.getElementById('origen-distrito');



  selectDep.innerHTML = `<option disabled selected value="">Seleccione departamento</option>`;
  selectProv.innerHTML = `<option disabled selected value="">Seleccione provincia</option>`;
  selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;


  Object.keys(sucursales).forEach(dep => {
    selectDep.append(new Option(dep, dep));
  });

  selectDep.addEventListener('change', () => {
    const dep = selectDep.value;
    selectProv.innerHTML = '<option disabled selected value="">Seleccione provincia</option>';
    selectDist.innerHTML = '<option disabled selected value="">Seleccione distrito</option>';

    if (sucursales[dep]) {
      Object.keys(sucursales[dep]).forEach(prov => {
        selectProv.append(new Option(prov, prov));
      });
    }
  });

  selectProv.addEventListener('change', () => {
    const dep = selectDep.value;
    const prov = selectProv.value;
    selectDist.innerHTML = '<option disabled selected value="">Seleccione distrito</option>';

    if (sucursales[dep] && sucursales[dep][prov]) {
      Object.keys(sucursales[dep][prov]).forEach(dist => {
        selectDist.append(new Option(dist, dist));
      });
    }
  });


}


function initUbigeo() {
  const selectDep = document.getElementById('m-departamento') || document.getElementById('select-departamento');
  const selectProv = document.getElementById('m-provincia') || document.getElementById('select-provincia');
  const selectDist = document.getElementById('m-distrito') || document.getElementById('select-distrito');
  const selectTienda = document.getElementById('m-tienda') || document.getElementById('select-sucursal');

  const origenDist = document.getElementById('origen-distrito')?.value;

  selectDep.innerHTML = `<option disabled selected value="">Seleccione departamento</option>`;
  selectProv.innerHTML = `<option disabled selected value="">Seleccione provincia</option>`;
  selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;
  selectTienda.innerHTML = `<option disabled selected value="">Seleccione sucursal</option>`;

  // Agregar solo departamentos con al menos una provincia con al menos un distrito distinto al de origen
  Object.entries(sucursales).forEach(([dep, provincias]) => {
    const provinciasValidas = Object.entries(provincias).filter(([prov, distritos]) => {
      const distritosValidos = Object.keys(distritos).filter(dist => dist !== origenDist);
      return distritosValidos.length > 0;
    });

    if (provinciasValidas.length > 0) {
      selectDep.append(new Option(dep, dep));
    }
  });

  selectDep.addEventListener('change', () => {
    const dep = selectDep.value;
    selectProv.innerHTML = '<option disabled selected value="">Seleccione provincia</option>';
    selectDist.innerHTML = '<option disabled selected value="">Seleccione distrito</option>';
    selectTienda.innerHTML = '<option disabled selected value="">Seleccione sucursal</option>';

    if (sucursales[dep]) {
      Object.entries(sucursales[dep]).forEach(([prov, distritos]) => {
        const distritosValidos = Object.keys(distritos).filter(dist => dist !== origenDist);
        if (distritosValidos.length > 0) {
          selectProv.append(new Option(prov, prov));
        }
      });
    }
  });

  selectProv.addEventListener('change', () => {
    const dep = selectDep.value;
    const prov = selectProv.value;
    selectDist.innerHTML = '<option disabled selected value="">Seleccione distrito</option>';
    selectTienda.innerHTML = '<option disabled selected value="">Seleccione sucursal</option>';

    if (sucursales[dep] && sucursales[dep][prov]) {
      Object.keys(sucursales[dep][prov]).forEach(dist => {
        if (dist !== origenDist) {
          selectDist.append(new Option(dist, dist));
        }
      });
    }
  });

  selectDist.addEventListener('change', () => {
    const dep = selectDep.value;
    const prov = selectProv.value;
    const dist = selectDist.value;
    selectTienda.innerHTML = '<option disabled selected value="">Seleccione sucursal</option>';

    if (sucursales[dep] && sucursales[dep][prov] && sucursales[dep][prov][dist]) {
      sucursales[dep][prov][dist].forEach(s => {
        const text = `${s.direc}`;
        selectTienda.append(new Option(text, s.id));
      });
    }
  });
}



document.getElementById('origen-distrito').addEventListener('change', () => {
  initUbigeo();
});


// // === 7. PERSISTENCIA CON LOCALSTORAGE ===
// function restoreFormData() {
//   const STORAGE_KEY = 'form-envio-data';
//   const form = document.getElementById('formulario-envio');
//   const savedData = JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};

//   for (let [id, value] of Object.entries(savedData)) {
//     const field = document.getElementById(id);
//     if (field) {
//       field.value = value;
//       field.dispatchEvent(new Event('change'));
//     }
//   }

//   form.querySelectorAll('input,select,textarea').forEach(el => {
//     el.addEventListener('change', () => {
//       const currentdata = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
//       currentdata[el.id] = el.value;
//       localStorage.setItem(STORAGE_KEY, JSON.stringify(currentdata));
//     });
//   });

//   form.addEventListener('submit', () => {
//     localStorage.removeItem(STORAGE_KEY);
//   });
// }





function limpiarFormularioMasivo() {
  editIndex = -1;

  document.getElementById('m-tipoEntrega').value = '';
  mostrarCamposDestino();

  document.getElementById('select-departamento').value = '';
  document.getElementById('select-provincia').innerHTML = '<option value="">Seleccione provincia</option>';
  document.getElementById('select-distrito').innerHTML = '<option value="">Seleccione distrito</option>';
  document.getElementById('select-sucursal').innerHTML = '<option value="">Seleccione tienda</option>';

  document.getElementById('m-direccion').value = '';
  document.getElementById('m-referencia').value = '';

  document.getElementById('m-tipoEmpaque').value = '';
  toggleFolios();
  toggleArticulos();

  document.getElementById('m-tipoArticulo').value = '';
  document.getElementById('m-descripcionArticulo').value = '';
  document.getElementById('m-valorEnvio').value = '';
  document.getElementById('m-peso').value = '';
  document.getElementById('m-largo').value = '';
  document.getElementById('m-ancho').value = '';
  document.getElementById('m-alto').value = '';
  document.getElementById('m-folios').value = '';

  document.getElementById('m-tipoDocumento').value = '';
  mostrarCamposReceptor();

  document.getElementById('m-nroDocumento').value = '';
  document.getElementById('m-celular').value = '';
  document.getElementById('m-razonSocial').value = '';
  document.getElementById('m-contacto').value = '';
  document.getElementById('m-nombres').value = '';
  document.getElementById('m-apellidos').value = '';

}

function confirmarLimpiarFormulario() {
  confirmarAccion('¿Estás seguro que deseas limpiar el formulario?', () => {
    limpiarFormularioMasivo();
  });
}

function mostrarMensajeExito(mensaje) {
  const alert = document.createElement('div');
  alert.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #48bb78;
    color: white;
    padding: 1rem 2rem;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 1000;
    animation: slideIn 0.3s ease-out;
  `;
  alert.textContent = mensaje;
  document.body.appendChild(alert);
  setTimeout(() => {
    alert.remove();
  }, 3000);
}



function initTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {

      tabButtons.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const nextTab = document.getElementById('tab-' + btn.dataset.tab);
      nextTab.classList.add('active');
    });
  });
}


function mostrarCamposDestino() {
  const tipo = document.getElementById('m-tipoEntrega').value;
  const grupoDir = document.getElementById('grupo-direccion');
  const grupoRef = document.getElementById('grupo-referencia');
  const grupoTienda = document.getElementById('grupo-tienda');

  if (tipo === '2') {
    grupoDir.style.display = 'flex';
    grupoRef.style.display = 'flex';
    grupoTienda.style.display = 'none';
  } else if (tipo === '1') {
    grupoDir.style.display = 'none';
    grupoRef.style.display = 'none';
    grupoTienda.style.display = 'flex';
  } else {
    grupoDir.style.display = 'none';
    grupoRef.style.display = 'none';
    grupoTienda.style.display = 'none';
  }
}


function toggleFolios() {
  const tipo = document.getElementById('m-tipoEmpaque').value;
  const grupoFolios = document.getElementById('grupo-folios');
  grupoFolios.style.display = (tipo === '2') ? 'flex' : 'none';
}

function toggleArticulos() {
  const tipo = document.getElementById('m-tipoEmpaque').value;
  const grupoArticulos = document.getElementById('grupo-articulos');
  grupoArticulos.style.display = (tipo === '1') ? 'flex' : 'none';
}


function mostrarCamposReceptor() {
  const tipo = document.getElementById('m-tipoDocumento').value;
  const camposRazon = document.getElementById('campo-razon-ruc');
  const camposContacto = document.getElementById('campo-contacto-ruc');
  const camposNombres = document.getElementById('campos-nombres');
  const camposApellidos = document.getElementById('campos-apellidos');


  const razon = document.getElementById('m-razonSocial');
  const contacto = document.getElementById('m-contacto');
  const nombres = document.getElementById('m-nombres');
  const apellidos = document.getElementById('m-apellidos');

  if (tipo === '2') {
    camposRazon.style.display = 'flex';
    camposContacto.style.display = 'flex';
    camposNombres.style.display = 'none';
    camposApellidos.style.display = 'none';

    razon.required = true;
    contacto.required = true;
    nombres.required = false;
    apellidos.required = false;
  }
  else if (tipo == '') {
    camposContacto.style.display = 'none';
    camposRazon.style.display = 'none';
    camposNombres.style.display = 'none';
    camposApellidos.style.display = 'none';
  }

  else {
    camposContacto.style.display = 'none';
    camposRazon.style.display = 'none';
    camposNombres.style.display = 'flex';
    camposApellidos.style.display = 'flex';

    razon.required = false;
    contacto.required = false;
    nombres.required = true;
    apellidos.required = true;
  }
}



function agregarEnvio() {
  // 1. campos de remitente
  const remitente_tipo_doc = document.getElementById('remitente-tipo-doc');
  const remitente_numero_doc = document.getElementById('remitente-numero-doc');
  const remitente_telefono = document.getElementById('remitente-telefono');
  const remitente_nombre = document.getElementById('remitente-nombre');
  const remitente_email = document.getElementById('remitente-email');

  // 2. Ubigeo destino
  const m_tipoEntrega = document.getElementById('m-tipoEntrega');
  const select_departamento = document.getElementById('select-departamento');
  const select_provincia = document.getElementById('select-provincia');
  const select_distrito = document.getElementById('select-distrito');
  const m_direccion = document.getElementById('m-direccion');
  const m_referencia = document.getElementById('m-referencia');
  const select_sucursal = document.getElementById('select-sucursal');

  // 3. Datos del paquete
  const m_tipoEmpaque = document.getElementById('m-tipoEmpaque');
  const m_tipoArticulo = document.getElementById('m-tipoArticulo');
  const m_valorEnvio = document.getElementById('m-valorEnvio');
  const m_peso = document.getElementById('m-peso');
  const m_largo = document.getElementById('m-largo');
  const m_ancho = document.getElementById('m-ancho');
  const m_alto = document.getElementById('m-alto');
  const m_folios = document.getElementById('m-folios');
  const m_descripcionArticulo = document.getElementById('m-descripcionArticulo');

  // 4. Datos del destinatario
  const m_tipoDocumento = document.getElementById('m-tipoDocumento');
  const m_nroDocumento = document.getElementById('m-nroDocumento');
  const m_celular = document.getElementById('m-celular');
  const m_razonSocial = document.getElementById('m-razonSocial');
  const m_contacto = document.getElementById('m-contacto');
  const m_nombres = document.getElementById('m-nombres');
  const m_apellidos = document.getElementById('m-apellidos');

  // 5. Ubigeo origen
  const origen_departamento = document.getElementById('origen-departamento')?.value || '';
  const origen_provincia = document.getElementById('origen-provincia')?.value || '';
  const origen_distrito = document.getElementById('origen-distrito')?.value || '';

  // 6. Crear objeto
  const envio = {
    remitente: {
      tipoDocumento: remitente_tipo_doc.value,
      numeroDocumento: remitente_numero_doc.value,
      telefono: remitente_telefono.value,
      nombre: remitente_nombre.value,
      email: remitente_email.value
    },
    origen: {
      departamento: origen_departamento,
      provincia: origen_provincia,
      distrito: origen_distrito
    },
    destino: {
      tipoEntrega: m_tipoEntrega.value,
      departamento: select_departamento.value,
      provincia: select_provincia.value,
      distrito: select_distrito.value,
      direccion: m_direccion?.value || '',
      referencia: m_referencia?.value || '',
      sucursalDestinoId: select_sucursal?.value || null
    },
    paquete: {
      tipoEmpaqueId: m_tipoEmpaque.value,
      contenidoPaqueteId: m_tipoArticulo.value,
      valorEnvio: parseFloat(m_valorEnvio.value) || 0,
      peso: parseFloat(m_peso.value) || 0,
      largo: parseFloat(m_largo.value) || 0,
      ancho: parseFloat(m_ancho.value) || 0,
      alto: parseFloat(m_alto.value) || 0,
      folios: m_folios?.value ? parseInt(m_folios.value) : null,
      descripcion: m_descripcionArticulo.value
    },
    destinatario: {
      tipoDocumento: m_tipoDocumento.value,
      nroDocumento: m_nroDocumento.value,
      celular: m_celular.value,
      razonSocial: m_razonSocial?.value || '',
      contacto: m_contacto?.value || '',
      nombres: m_nombres?.value || '',
      apellidos: m_apellidos?.value || ''
    }
  };


localStorage.setItem(STORAGE_KEY, JSON.stringify(envio));

  limpiarFormularioMasivo();

  actualizarTabla();
}


function actualizarTabla() {
  const tableContent = document.getElementById('tableContent');
  const totalEnvios = document.getElementById('totalEnvios');
  const pesoTotal = document.getElementById('pesoTotal');
  const valorTotal = document.getElementById('valorTotal');

  const stored = localStorage.getItem(STORAGE_KEY);
  const envios = stored ? JSON.parse(stored) : [];

  if (envios.length === 0) {
    tableContent.innerHTML = `
      <div class="empty-state">
        <p>No hay envíos registrados aún</p>
        <p>Comienza agregando tu primer envío</p>
      </div>
    `;
    totalEnvios.textContent = '0';
    pesoTotal.textContent = '0';
    valorTotal.textContent = '0.00';
    return;
  }

  let sumaPeso = 0;
  let sumaValor = 0;

  let html = `
    <div style="overflow-x: auto;">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Tipo</th>
            <th>Destinatario</th>
            <th>Destino</th>
            <th>Descripción</th>
            <th>Dimensiones</th>
            <th>Peso</th>
            <th>Valor</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
  `;

  envios.forEach((envio, index) => {
    const paquete = envio.paquete || {};
    const destino = envio.destino || {};
    const destinatario = envio.destinatario || {};

    sumaPeso += parseFloat(paquete.peso) || 0;
    sumaValor += parseFloat(paquete.valorEnvio) || 0;

    let nombreDestinatario = '';
    if (destinatario.tipoDocumento === '2') {
      nombreDestinatario = destinatario.razonSocial || '';
    } else {
      nombreDestinatario = `${destinatario.nombres || ''} ${destinatario.apellidos || ''}`.trim();
    }

    let badgeClass = '';
    if (destino.tipoEntrega === 'express') badgeClass = 'badge-express';
    else if (destino.tipoEntrega === 'agencia') badgeClass = 'badge-agencia';
    else badgeClass = 'badge-domicilio';

    html += `
      <tr>
        <td>${index + 1}</td>
        <td><span class="badge ${badgeClass}">${destino.tipoEntrega}</span></td>
        <td>
          <div><strong>${nombreDestinatario}</strong></div>
          <small style="color: #718096;">${destinatario.tipoDocumento || ''}: ${destinatario.nroDocumento || ''}</small>
        </td>
        <td>
          <div>${destino.distrito || ''}</div>
          <small style="color: #718096;">${destino.provincia || ''}, ${destino.departamento || ''}</small>
        </td>
        <td>
          <div>${paquete.descripcion || ''}</div>
          <small style="color: #718096;">${paquete.contenidoPaqueteId || ''} - ${paquete.tipoEmpaqueId || ''}</small>
        </td>
        <td><small>${paquete.largo || 0}x${paquete.ancho || 0}x${paquete.alto || 0} cm</small></td>
        <td>${paquete.peso || 0} kg</td>
        <td><strong>S/ ${(parseFloat(paquete.valorEnvio) || 0).toFixed(2)}</strong></td>
        <td>
          <div class="btn-actions">
            <button class="btn-small btn-editar" onclick="editarEnvio(${index})" title="Editar">
              <i class="fa fa-edit"></i>
            </button>
            <button class="btn-small btn-eliminar" onclick="eliminarEnvio(${index})" title="Eliminar">
              <i class="fa fa-trash"></i>
            </button>
          </div>
        </td>
      </tr>
    `;
  });

  html += `
        </tbody>
      </table>
    </div>
  `;

  tableContent.innerHTML = html;
  totalEnvios.textContent = envios.length;
  pesoTotal.textContent = sumaPeso.toFixed(2);
  valorTotal.textContent = sumaValor.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}


function editarEnvio(index) {
  const envio = enviosMasivos[index];
  if (!envio) return;

  const { remitente, origen, destino, paquete, destinatario } = envio;

  editIndex = index;

    const btnAgregar = document.querySelector('.btn-agregar');
  if (btnAgregar) {
    btnAgregar.textContent = '💾 Guardar cambios';
  }

  // 1. Remitente
  document.getElementById('remitente-tipo-doc').value = remitente.tipoDocumento || '';
  document.getElementById('remitente-numero-doc').value = remitente.numeroDocumento || '';
  document.getElementById('remitente-telefono').value = remitente.telefono || '';
  document.getElementById('remitente-nombre').value = remitente.nombre || '';
  document.getElementById('remitente-email').value = remitente.email || '';

  // 2. Origen (si se desea mostrar)
  document.getElementById('origen-departamento').value = origen.departamento || '';
  document.getElementById('origen-provincia').value = origen.provincia || '';
  document.getElementById('origen-distrito').value = origen.distrito || '';

  // 3. Destino
  document.getElementById('m-tipoEntrega').value = destino.tipoEntrega || '';
  mostrarCamposDestino(); // actualiza campos condicionales según tipoEntrega

  document.getElementById('select-departamento').value = destino.departamento || '';
  document.getElementById('select-provincia').value = destino.provincia || '';
  document.getElementById('select-distrito').value = destino.distrito || '';
  document.getElementById('m-direccion').value = destino.direccion || '';
  document.getElementById('m-referencia').value = destino.referencia || '';
  document.getElementById('select-sucursal').value = destino.sucursalDestinoId || '';

  // 4. Paquete
  document.getElementById('m-tipoEmpaque').value = paquete.tipoEmpaqueId || '';
  toggleFolios();
  toggleArticulos();

  document.getElementById('m-tipoArticulo').value = paquete.contenidoPaqueteId || '';
  document.getElementById('m-valorEnvio').value = paquete.valorEnvio || '';
  document.getElementById('m-peso').value = paquete.peso || '';
  document.getElementById('m-largo').value = paquete.largo || '';
  document.getElementById('m-ancho').value = paquete.ancho || '';
  document.getElementById('m-alto').value = paquete.alto || '';
  document.getElementById('m-folios').value = paquete.folios || '';
  document.getElementById('m-descripcionArticulo').value = paquete.descripcion || '';

  document.getElementById('m-tipoDocumento').value = destinatario.tipoDocumento || '';
  mostrarCamposReceptor();

  document.getElementById('m-nroDocumento').value = destinatario.nroDocumento || '';
  document.getElementById('m-celular').value = destinatario.celular || '';
  document.getElementById('m-razonSocial').value = destinatario.razonSocial || '';
  document.getElementById('m-contacto').value = destinatario.contacto || '';
  document.getElementById('m-nombres').value = destinatario.nombres || '';
  document.getElementById('m-apellidos').value = destinatario.apellidos || '';

  document.querySelector('.tab-btn[data-tab="destino"]').click();
}
