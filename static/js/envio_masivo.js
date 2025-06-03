const { rutasTarifas } = window.CONFIG_ENVIO || {};

const STORAGE_KEY = "envios_masivos";

let editIndex = -1;
let pasoActual = 1;

// Teléfono
const regexTelefono = /^9\d{8}$/;
// Documentos
const regexDNI = /^\d{8}$/;
const regexRUC = /^(10|20)\d{9}$/;
const regexPasaporte = /^[A-Z0-9]{6,12}$/i;
const regexCE = /^[A-Z0-9]{9,12}$/i;
// Nombre completo
const regexNombre = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ ]{2,60}$/;
// Correo
const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
// Dirección
const regexDireccion = /^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑ\-,.#°º()]{5,100}$/;
//Razón
const regexRazon = /^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\.\-&]{2,100}$/;


function attachNumeroDocValidation(idTipo, idNumero, idMensaje) {
  const tipoSel = document.getElementById(idTipo);
  const inputNum = document.getElementById(idNumero);
  const spanMsg = document.getElementById(idMensaje);

  function validar() {
    const tipo = tipoSel.value;
    const valor = inputNum.value.trim();
    let valido = false;
    let texto = '';

    switch (tipo) {
      case '1': // DNI
        valido = regexDNI.test(valor);
        texto = 'Debe tener 8 dígitos.';
        break;
      case '2': // RUC
        valido = regexRUC.test(valor);
        texto = 'Debe comenzar con 10 o 20 y tener 11 dígitos.';
        break;
      case '3': // Carné de Extranjería
        valido = regexCE.test(valor);
        texto = 'Debe tener 9–12 caracteres alfanuméricos.';
        break;
      case '4': // Pasaporte
        valido = regexPasaporte.test(valor);
        texto = 'Debe tener 6–12 caracteres alfanuméricos.';
        break;
      default:
        texto = 'Seleccione tipo de documento.';
        break;
    }

    if (valor === '') {
      spanMsg.style.display = 'none';
      inputNum.style.borderColor = '';
    } else if (valido) {
      spanMsg.style.display = 'none';
      inputNum.style.borderColor = '#48bb78';
    } else {
      spanMsg.style.display = 'block';
      spanMsg.textContent = texto;
      inputNum.style.borderColor = '#fc8181';
    }
  }

  // Asocia eventos
  inputNum.addEventListener('input', validar);
  tipoSel.addEventListener('change', () => {
    if (inputNum.value.trim() !== '') {
      validar();
    }
  });
}


function attachTelefonoValidation(idInputTel, idMensajeTel) {
  const inputTel = document.getElementById(idInputTel);
  const spanMsg = document.getElementById(idMensajeTel);

  inputTel.addEventListener('input', () => {
    const valor = inputTel.value.trim();
    const valido = regexTelefono.test(valor);

    if (valor === '') {
      spanMsg.style.display = 'none';
      inputTel.style.borderColor = '';
    } else if (valido) {
      spanMsg.style.display = 'none';
      inputTel.style.borderColor = '#48bb78';
    } else {
      spanMsg.style.display = 'block';
      spanMsg.textContent = 'El teléfono debe comenzar con 9 y tener 9 dígitos.';
      inputTel.style.borderColor = '#fc8181';
    }
  });
}


function attachNombreValidation(idInputName, idMensajeName) {
  const inputName = document.getElementById(idInputName);
  const spanMsg = document.getElementById(idMensajeName);

  inputName.addEventListener('input', () => {
    const valor = inputName.value.trim();
    const valido = regexNombre.test(valor);

    if (valor === '') {
      spanMsg.style.display = 'none';
      inputName.style.borderColor = '';
    } else if (valido) {
      spanMsg.style.display = 'none';
      inputName.style.borderColor = '#48bb78';
    } else {
      spanMsg.style.display = 'block';
      spanMsg.textContent = 'Solo se permiten letras y espacios (mínimo 2 caracteres).';
      inputName.style.borderColor = '#fc8181';
    }
  });
}


function attachRazonValidation(idInputRazon, idMensajeRazon) {
  const inputRazon = document.getElementById(idInputRazon);
  const spanMsg = document.getElementById(idMensajeRazon);

  inputRazon.addEventListener('input', () => {
    const valor = inputRazon.value.trim();
    const valido = regexRazon.test(valor);

    if (valor === '') {
      spanMsg.style.display = 'none';
      inputRazon.style.borderColor = '';
    } else if (valido) {
      spanMsg.style.display = 'none';
      inputRazon.style.borderColor = '#48bb78';
    } else {
      spanMsg.style.display = 'block';
      spanMsg.textContent = 'Razón social inválida (2–100 caracteres alfanum.).';
      inputRazon.style.borderColor = '#fc8181';
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {

  initTabs();
  mostrarCamposDestino();
  toggleFolios();
  toggleArticulos();
  mostrarCamposReceptor();
  cargarOrigenes();
  actualizarTabla();


  attachNumeroDocValidation(
    'remitente-tipo-doc',
    'remitente-numero-doc',
    'mensaje-validacion-numero'
  );

  attachTelefonoValidation(
    'remitente-telefono',
    'mensaje-validacion-telefono'
  );

  attachNombreValidation(
    'remitente-nombre',
    'mensaje-validacion-nombre'
  );

  attachNumeroDocValidation(
    'm-tipoDocumento',
    'm-nroDocumento',
    'mensaje-validacion-numero-dest'
  );

  attachTelefonoValidation(
    'm-celular',
    'mensaje-validacion-telefono-dest'
  );

  attachNombreValidation(
    'm-nombres',
    'mensaje-validacion-nombre-dest'
  );

  attachNombreValidation(
    'm-apellidos',
    'mensaje-validacion-apellidos-dest'
  );

  attachRazonValidation(
    'm-razonSocial',
    'mensaje-validacion-razon-dest'
  );

  attachNombreValidation(
    'm-contacto',
    'mensaje-validacion-contacto-dest'
  );


});

let origenSeleccionado = null;
let eventosRegistrados = {
  origen: false,
  destino: false
};

function cargarOrigenes() {
  const selectDep = document.getElementById('origen-departamento');
  const selectProv = document.getElementById('origen-provincia');
  const selectDist = document.getElementById('origen-distrito');

  selectDep.innerHTML = `<option disabled selected value="">Seleccione departamento</option>`;
  selectProv.innerHTML = `<option disabled selected value="">Seleccione provincia</option>`;
  selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;

  const origenesUnicos = Object.keys(rutasTarifas);
  const departamentos = [...new Set(origenesUnicos.map(k => k.split('|')[0]))];
  departamentos.forEach(dep => selectDep.append(new Option(dep, dep)));

  if (!eventosRegistrados.origen) {
    selectDep.addEventListener('change', () => {
      selectProv.innerHTML = `<option disabled selected value="">Seleccione provincia</option>`;
      selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;
      const dep = selectDep.value;

      const provincias = origenesUnicos
        .filter(k => k.startsWith(dep + '|'))
        .map(k => k.split('|')[1]);
      [...new Set(provincias)].forEach(prov => selectProv.append(new Option(prov, prov)));
    });

    selectProv.addEventListener('change', () => {
      selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;
      const dep = selectDep.value;
      const prov = selectProv.value;

      const distritos = origenesUnicos
        .filter(k => k.startsWith(`${dep}|${prov}|`))
        .map(k => k.split('|')[2]);
      [...new Set(distritos)].forEach(dist => selectDist.append(new Option(dist, dist)));
    });

    selectDist.addEventListener('change', () => {
      const dep = selectDep.value;
      const prov = selectProv.value;
      const dist = selectDist.value;

      origenSeleccionado = `${dep}|${prov}|${dist}`;

      const destinos = rutasTarifas[origenSeleccionado];
      if (destinos && destinos.length > 0) {
        const sucursalOrigenId = destinos[0].id_origen || destinos[0].id_origen_sucursal || '';
        if (sucursalOrigenId) {
          document.getElementById('origen-sucursal-id').value = sucursalOrigenId;
        }
      }

      cargarDestinos(origenSeleccionado);
    });

    eventosRegistrados.origen = true;
  }
}

function cargarDestinos(origenKey) {
  const destinos = rutasTarifas[origenKey] || [];

  const selectDep = document.getElementById('select-departamento');
  const selectProv = document.getElementById('select-provincia');
  const selectDist = document.getElementById('select-distrito');
  const selectSucursal = document.getElementById('select-sucursal');

  selectDep.innerHTML = `<option disabled selected value="">Seleccione departamento</option>`;
  selectProv.innerHTML = `<option disabled selected value="">Seleccione provincia</option>`;
  selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;
  selectSucursal.innerHTML = `<option disabled selected value="">Seleccione sucursal</option>`;

  const deps = [...new Set(destinos.map(d => d.departamento))];
  deps.forEach(dep => selectDep.append(new Option(dep, dep)));

  if (!eventosRegistrados.destino) {
    selectDep.addEventListener('change', () => {
      selectProv.innerHTML = `<option disabled selected value="">Seleccione provincia</option>`;
      selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;
      selectSucursal.innerHTML = `<option disabled selected value="">Seleccione sucursal</option>`;

      const dep = selectDep.value;
      const provs = destinos.filter(d => d.departamento === dep).map(d => d.provincia);
      [...new Set(provs)].forEach(prov => selectProv.append(new Option(prov, prov)));
    });

    selectProv.addEventListener('change', () => {
      selectDist.innerHTML = `<option disabled selected value="">Seleccione distrito</option>`;
      selectSucursal.innerHTML = `<option disabled selected value="">Seleccione sucursal</option>`;

      const dep = selectDep.value;
      const prov = selectProv.value;
      const dists = destinos
        .filter(d => d.departamento === dep && d.provincia === prov)
        .map(d => d.distrito);
      [...new Set(dists)].forEach(dist => selectDist.append(new Option(dist, dist)));
    });

    selectDist.addEventListener('change', () => {
      const dep = selectDep.value;
      const prov = selectProv.value;
      const dist = selectDist.value;

      const sucursales = destinos.filter(d =>
        d.departamento === dep &&
        d.provincia === prov &&
        d.distrito === dist
      );

      selectSucursal.innerHTML = `<option disabled selected value="">Seleccione sucursal</option>`;
      sucursales.forEach(s => {
        const opt = new Option(s.direccion, s.id);
        selectSucursal.appendChild(opt);
      });

      if (sucursales.length > 0) {
        document.getElementById('destino-sucursal-id').value = sucursales[0].id;
        selectSucursal.value = sucursales[0].id;
      }

      selectSucursal.addEventListener('change', () => {
        document.getElementById('destino-sucursal-id').value = selectSucursal.value;
      });
    });

    eventosRegistrados.destino = true;
  }
}

/************************************************************ GENERALES ************************************************************************ */
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
  const grupoTienda = document.getElementById('grupo-tienda');

  if (tipo === '2') {
    grupoDir.style.display = 'flex';
    grupoTienda.style.display = 'none';
  } else if (tipo === '1') {
    grupoDir.style.display = 'none';
    grupoTienda.style.display = 'flex';
  } else {
    grupoDir.style.display = 'none';
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
  } else if (tipo === '') {
    camposContacto.style.display = 'none';
    camposRazon.style.display = 'none';
    camposNombres.style.display = 'none';
    camposApellidos.style.display = 'none';
  } else {
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

/************************************************************************************************************************************************* */

function validarRequeridos() {
  const contenedor = document.querySelector('.tabs-content');
  if (!contenedor) return true;

  const camposReq = contenedor.querySelectorAll('input[required], select[required], textarea[required]');

  for (let campo of camposReq) {
    const tipo = campo.tagName.toLowerCase();
    let valor = '';

    if (tipo === 'select') {
      valor = campo.value;
    } else if (tipo === 'input' || tipo === 'textarea') {
      valor = campo.value.trim();
    }

    if (!valor) {
      campo.style.borderColor = '#fc8181';

      const msgSpanId = campo.getAttribute('aria-describedby')
        || campo.getAttribute('data-error-span')
        || null;
      if (msgSpanId) {
        const spanMsg = document.getElementById(msgSpanId);
        if (spanMsg) {
          spanMsg.style.display = 'block';
          spanMsg.textContent = 'Este campo es obligatorio.';
        }
      }

      campo.focus();
      return false;
    } else {
      campo.style.borderColor = '';
      const msgSpanId = campo.getAttribute('aria-describedby')
        || campo.getAttribute('data-error-span')
        || null;
      if (msgSpanId) {
        const spanMsg = document.getElementById(msgSpanId);
        if (spanMsg) spanMsg.style.display = 'none';
      }
    }
  }

  return true;
}



function mostrarModalConfirmacion() {
  if (!validarRequeridos()) {
    document.getElementById('modalValidacion').style.display = 'flex';
    return;
  }

  document.getElementById('modalConfirmacion').style.display = 'flex';

  const confirmarBtn = document.getElementById('confirmarBtn');
  confirmarBtn.replaceWith(confirmarBtn.cloneNode(true)); 
  document.getElementById('confirmarBtn').addEventListener('click', () => {
    cerrarModal();   
    agregarEnvio(); 
    
  });
} 

function cerrarModal() {
  document.getElementById('modalConfirmacion').style.display = 'none';
  document.getElementById('modalValidacion').style.display = 'none';
}


function agregarEnvio() {

  const m_tipoEntrega = document.getElementById('m-tipoEntrega');
  const select_departamento = document.getElementById('select-departamento');
  const select_provincia = document.getElementById('select-provincia');
  const select_distrito = document.getElementById('select-distrito');
  const m_direccion = document.getElementById('m-direccion');
  const select_sucursal = document.getElementById('select-sucursal');

  // 2. Datos del paquete
  const m_tipoEmpaque = document.getElementById('m-tipoEmpaque');
  const m_tipoArticulo = document.getElementById('m-tipoArticulo');
  const m_valorEnvio = document.getElementById('m-valorEnvio');
  const m_peso = document.getElementById('m-peso');
  const m_largo = document.getElementById('m-largo');
  const m_ancho = document.getElementById('m-ancho');
  const m_alto = document.getElementById('m-alto');
  const m_folios = document.getElementById('m-folios');
  const m_descripcionArticulo = document.getElementById('m-descripcionArticulo');

  // 3. Datos del destinatario
  const m_tipoDocumento = document.getElementById('m-tipoDocumento');
  const m_nroDocumento = document.getElementById('m-nroDocumento');
  const m_celular = document.getElementById('m-celular');
  const m_razonSocial = document.getElementById('m-razonSocial');
  const m_contacto = document.getElementById('m-contacto');
  const m_nombres = document.getElementById('m-nombres');
  const m_apellidos = document.getElementById('m-apellidos');

  // 4. IDs y nombres de los <select>
  const tipoEntregaId = m_tipoEntrega.value;
  const tipoEntregaNombre = m_tipoEntrega.value
    ? m_tipoEntrega.selectedOptions[0].text
    : '';


  const tipoEmpaqueId = m_tipoEmpaque.value;
  const tipoEmpaqueNombre = m_tipoEmpaque.value
    ? m_tipoEmpaque.selectedOptions[0].text
    : '';
  const contenidoPaqueteId = m_tipoArticulo.value;
  const contenidoPaqueteNombre = m_tipoArticulo.value
    ? m_tipoArticulo.selectedOptions[0].text
    : '';
  const tipoDocumentoId = m_tipoDocumento.value;
  const tipoDocumentoNombre = m_tipoDocumento.value
    ? m_tipoDocumento.selectedOptions[0].text
    : '';

  const selectDepOrigen = document.getElementById('origen-departamento');
  const selectProvOrigen = document.getElementById('origen-provincia');
  const selectDistOrigen = document.getElementById('origen-distrito');


  const envio = {
    origen: {
      departamento: selectDepOrigen.value,
      provincia: selectProvOrigen.value,
      distrito: selectDistOrigen.value,
      sucursalOrigenId: document.getElementById('origen-sucursal-id').value || null
    },
    destino: {
      tipoEntregaId,
      tipoEntregaNombre,
      departamento: select_departamento.value,
      provincia: select_provincia.value,
      distrito: select_distrito.value,
      direccion: m_direccion.value || '',
      sucursalDestinoId: select_sucursal.value || null
    },
    paquete: {
      tipoEmpaqueId,
      tipoEmpaqueNombre,
      contenidoPaqueteId,
      contenidoPaqueteNombre,
      valorEnvio: parseFloat(m_valorEnvio.value) || 0,
      peso: parseFloat(m_peso.value) || 0,
      largo: parseFloat(m_largo.value) || 0,
      ancho: parseFloat(m_ancho.value) || 0,
      alto: parseFloat(m_alto.value) || 0,
      folios: m_folios.value
        ? parseInt(m_folios.value)
        : null,
      descripcion: m_descripcionArticulo.value || ''
    },
    destinatario: {
      tipoDocumento: tipoDocumentoId,
      tipoDocumentoNombre,
      nroDocumento: m_nroDocumento.value || '',
      celular: m_celular.value || '',
      razonSocial: m_razonSocial.value || '',
      contacto: m_contacto.value || '',
      nombres: m_nombres.value || '',
      apellidos: m_apellidos.value || ''
    }
  };

  let enviosActuales = [];
  try {
    const data = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (Array.isArray(data)) {
      enviosActuales = data;
    }
  } catch (e) {
    console.error("Error al parsear localStorage:", e);
  }

  // 7. Si editIndex >= 0: estamos editando, reemplazamos el índice; si no: agregamos
  if (editIndex >= 0) {
    enviosActuales[editIndex] = envio;
    editIndex = -1;   // restauramos a "no edición"
    const btn = document.getElementById('btn-guardar');
    if (btn) {
      btn.textContent = 'Agregar'; // volvemos a texto original
    }
  } else {
    enviosActuales.push(envio);
  }

  localStorage.setItem(STORAGE_KEY, JSON.stringify(enviosActuales));
  limpiarFormularioMasivo();
  actualizarTabla();
}




function editarEnvio(index) {
  const almacen = localStorage.getItem(STORAGE_KEY);
  const envios = almacen ? JSON.parse(almacen) : [];
  if (index < 0 || index >= envios.length) return;

  const envio = envios[index];

  const selectDepOrigen = document.getElementById('origen-departamento');
  const selectProvOrigen = document.getElementById('origen-provincia');
  const selectDistOrigen = document.getElementById('origen-distrito');

  selectDepOrigen.value = envio.origen.departamento;
  selectDepOrigen.dispatchEvent(new Event('change'));

  selectProvOrigen.value = envio.origen.provincia;
  selectProvOrigen.dispatchEvent(new Event('change'));


  selectDistOrigen.value = envio.origen.distrito;
  selectDistOrigen.dispatchEvent(new Event('change'));

  document.getElementById('origen-sucursal-id').value = envio.origen.sucursalOrigenId || '';


  const selectDepDest = document.getElementById('select-departamento');
  const selectProvDest = document.getElementById('select-provincia');
  const selectDistDest = document.getElementById('select-distrito');
  const selectSucDest = document.getElementById('select-sucursal');

  selectDepDest.value = envio.destino.departamento;
  selectDepDest.dispatchEvent(new Event('change'));

  selectProvDest.value = envio.destino.provincia;
  selectProvDest.dispatchEvent(new Event('change'));

  selectDistDest.value = envio.destino.distrito;
  selectDistDest.dispatchEvent(new Event('change'));


  selectSucDest.value = envio.destino.sucursalDestinoId || '';
  document.getElementById('m-tipoEntrega').value = envio.paquete.tipoEntregaId;
  document.getElementById('m-tipoEmpaque').value = envio.paquete.tipoEmpaqueId;
  document.getElementById('m-tipoArticulo').value = envio.paquete.contenidoPaqueteId;
  document.getElementById('m-valorEnvio').value = envio.paquete.valorEnvio;
  document.getElementById('m-peso').value = envio.paquete.peso;
  document.getElementById('m-largo').value = envio.paquete.largo;
  document.getElementById('m-ancho').value = envio.paquete.ancho;
  document.getElementById('m-alto').value = envio.paquete.alto;
  document.getElementById('m-folios').value = envio.paquete.folios || '';
  document.getElementById('m-descripcionArticulo').value = envio.paquete.descripcion || '';

  document.getElementById('m-tipoDocumento').value = envio.destinatario.tipoDocumento;
  document.getElementById('m-nroDocumento').value = envio.destinatario.nroDocumento;
  document.getElementById('m-celular').value = envio.destinatario.celular;
  document.getElementById('m-razonSocial').value = envio.destinatario.razonSocial || '';
  document.getElementById('m-contacto').value = envio.destinatario.contacto || '';
  document.getElementById('m-nombres').value = envio.destinatario.nombres || '';
  document.getElementById('m-apellidos').value = envio.destinatario.apellidos || '';


  editIndex = index;
  const btn = document.getElementById('btn-guardar');
  if (btn) {
    btn.textContent = 'Guardar cambios';
  }
}



function eliminarEnvio(index) {
  const almacen = localStorage.getItem(STORAGE_KEY);
  const envios = almacen ? JSON.parse(almacen) : [];
  if (index < 0 || index >= envios.length) return;

  envios.splice(index, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(envios));
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

    let nombreDest = '';
    if (destinatario.tipoDocumento === '2') {
      nombreDest = destinatario.razonSocial || '';
    } else {
      nombreDest = `${destinatario.nombres || ''} ${destinatario.apellidos || ''}`.trim();
    }

    let badgeClass = '';
    if (destino.tipoEntrega === '1') {
      badgeClass = 'badge-domicilio';
    } else if (destino.tipoEntrega === '2') {
      badgeClass = 'badge-agencia';
    } else {
      badgeClass = 'badge-domicilio';
    }

    html += `
      <tr>
        <td>${index + 1}</td>
        <td><span class="badge ${badgeClass}">${destino.tipoEntregaNombre}</span></td>
        <td>
          <div><strong>${nombreDest}</strong></div>
          <small style="color: #718096;">
            ${destinatario.tipoDocumentoNombre || ''}: ${destinatario.nroDocumento || ''}
          </small>
        </td>
        <td>
          <div>${destino.distrito || ''}</div>
          <small style="color: #718096;">
            ${destino.provincia || ''}, ${destino.departamento || ''}
          </small>
        </td>
        <td>
          <div>${paquete.descripcion || ''}</div>
          <small style="color: #718096;">
            ${paquete.contenidoPaqueteNombre || ''} -
            ${paquete.tipoEmpaqueNombre || ''}
          </small>
        </td>
        <td>
          <small>${paquete.largo || 0}x${paquete.ancho || 0}x${paquete.alto || 0} cm</small>
        </td>
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




function limpiarFormularioMasivo() {
  document.getElementById('m-tipoEntrega').value = '';
  document.getElementById('select-departamento').value = '';
  document.getElementById('select-provincia').value = '';
  document.getElementById('select-distrito').value = '';
  document.getElementById('m-direccion').value = '';
  document.getElementById('select-sucursal').value = '';

  document.getElementById('m-tipoEmpaque').value = '';
  document.getElementById('m-tipoArticulo').value = '';
  document.getElementById('m-valorEnvio').value = '';
  document.getElementById('m-peso').value = '';
  document.getElementById('m-largo').value = '';
  document.getElementById('m-ancho').value = '';
  document.getElementById('m-alto').value = '';
  document.getElementById('m-folios').value = '';
  document.getElementById('m-descripcionArticulo').value = '';

  document.getElementById('m-tipoDocumento').value = '';
  document.getElementById('m-nroDocumento').value = '';
  document.getElementById('m-celular').value = '';
  document.getElementById('m-razonSocial').value = '';
  document.getElementById('m-contacto').value = '';
  document.getElementById('m-nombres').value = '';
  document.getElementById('m-apellidos').value = '';

  document.getElementById('grupo-direccion').style.display = 'none';
  document.getElementById('grupo-tienda').style.display = 'none';
  document.getElementById('grupo-articulos').style.display = 'none';
  document.getElementById('grupo-folios').style.display = 'none';
  document.getElementById('campos-nombres').style.display = 'none';
  document.getElementById('campos-apellidos').style.display = 'none';
  document.getElementById('campo-razon-ruc').style.display = '';
  document.getElementById('campo-contacto-ruc').style.display = '';

  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
  document.querySelector('.tab-btn[data-tab="destino"]').classList.add('active');
  document.getElementById('tab-destino').classList.add('active');
}



function cerrarModal() {
  const modal = document.getElementById('modalConfirmacion');
  modal.style.display = 'none';
  const confirmarBtn = document.getElementById('confirmarBtn');
  confirmarBtn.replaceWith(confirmarBtn.cloneNode(true));
}

function eliminarTodo() {

  localStorage.removeItem(STORAGE_KEY);

  if (typeof renderizarEnvios === 'function') {
    renderizarEnvios([]);
  } else {
    const contenedorTabla = document.getElementById('tabla-envios-body');
    if (contenedorTabla) {
      contenedorTabla.innerHTML = '';
    }
  }

  editIndex = -1;
  const btn = document.getElementById('btn-guardar');
  if (btn) {
    btn.textContent = 'Guardar envío';
  }

  cerrarModal();
}


function mostrarModalEliminarTodo() {
  const modal = document.getElementById('modalConfirmacion');
  const mensajeParrafo = modal.querySelector('p');
  const confirmarBtn  = modal.querySelector('#confirmarBtn');

  mensajeParrafo.textContent = '¿Deseas ELIMINAR todos los envíos?';

  confirmarBtn.textContent = 'Sí, eliminar';

  confirmarBtn.replaceWith(confirmarBtn.cloneNode(true));
  const nuevoConfirmar = modal.querySelector('#confirmarBtn');
  nuevoConfirmar.addEventListener('click', eliminarTodoEnvios);

  modal.style.display = 'flex';
}
