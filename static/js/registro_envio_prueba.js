const STORAGE_KEYS = {
  REMITENTE: 'envios_remitente',
  ORIGEN:    'envios_origen',
  REGISTROS: 'envios_masivos'
};
const SELECTORS = {
  remitente: '#seccion_remitente',
  origen:    '#seccion-origen',
  masiva:    '#seccion-masiva'
};


function save(key, obj) { localStorage.setItem(key, JSON.stringify(obj)); }
function load(key) { try { return JSON.parse(localStorage.getItem(key)); } catch { return null; } }

function saveRemitente() {
  const data = { 
    tipo:   document.getElementById('remitente-tipo-doc').value,
    numero: document.getElementById('remitente-numero-doc').value,
    telefono: document.getElementById('remitente-telefono').value,
    nombre:   document.getElementById('remitente-nombre').value,
    email:    document.getElementById('remitente-email').value
  };
  save(STORAGE_KEYS.REMITENTE, data);
}

function saveOrigen() {
  const dep = document.getElementById('origen-departamento').value;
  const prov= document.getElementById('origen-provincia').value;
  const dist= document.getElementById('origen-distrito').value;
  const suc = document.getElementById('origen-sucursal-id').value;
  save(STORAGE_KEYS.ORIGEN, { dep, prov, dist, suc });
}

function saveRegistros() { save(STORAGE_KEYS.REGISTROS, registros); }

function restoreState() {
  // 1) Restaurar datos del remitente
  const rem = load(STORAGE_KEYS.REMITENTE);
  if (rem) {
    document.getElementById('remitente-tipo-doc').value   = rem.tipo;
    document.getElementById('remitente-numero-doc').value = rem.numero;
    document.getElementById('remitente-telefono').value   = rem.telefono;
    document.getElementById('remitente-nombre').value     = rem.nombre;
    document.getElementById('remitente-email').value      = rem.email;
  }

  // 2) Restaurar datos del lugar de origen (pero NO lo bloqueamos aún)
  const ori = load(STORAGE_KEYS.ORIGEN);
  if (ori) {
    const depSel  = document.getElementById('origen-departamento');
    const provSel = document.getElementById('origen-provincia');
    const distSel = document.getElementById('origen-distrito');
    const sucId   = document.getElementById('origen-sucursal-id');

    depSel.value = ori.dep;

    // Cargar provincias y distritos en cascada
    cargarProvincias(ori.dep)
      .then(() => {
        provSel.value = ori.prov;
        return cargarDistritos(ori.prov);
      })
      .then(() => {
        distSel.value = ori.dist;
        sucId.value   = ori.suc;
        // <-- nota: no llamamos lockOrigen() aquí
      });
  }

  // 3) Restaurar registros y renderizar tabla
  const regs = load(STORAGE_KEYS.REGISTROS);
  if (Array.isArray(regs) && regs.length > 0) {
    registros = regs;
    renderTabla();
    // Solo ahora que hay envíos guardados bloqueamos el origen
    lockOrigen();
  }
}




//Teléfono
const regexTelefono = /^9\d{8}$/;
//documentos
const regexDNI = /^\d{8}$/;
const regexRUC = /^(10|20)\d{9}$/;
const regexPasaporte = /^[A-Z0-9]{6,12}$/i;
const regexCE = /^[A-Z0-9]{9,12}$/i;
//Nombre completo
const regexNombre = /^[\p{L} '-]{2,60}$/u;
//Correo
const regexEmail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
//Dirección
const regexDireccion = /^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑ\-,.#°º()]{5,100}$/;

const regexApellido = /^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:[ '\-][A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$/;

const regexRazonSocial = /^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ&\.\-,() ]{2,100}$/;

const regexPositivos = /^[0-9]+(?:\.[0-9]+)?$/;



const tipoDoc = document.getElementById('remitente-tipo-doc');
const numeroDoc = document.getElementById('remitente-numero-doc');
const mensajeDoc = document.getElementById('mensaje-validacion-numero');

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
    telefonoRemitente.style.borderColor = '#48bb78';
  } else {
    mensajeTelefono.style.display = 'block';
    mensajeTelefono.textContent = 'El teléfono debe comenzar con 9 y tener 9 dígitos.';
    telefonoRemitente.style.borderColor = '#fc8181';
  }
});

const nombreRemitente = document.getElementById('remitente-nombre');
const mensajeNombre = document.getElementById('mensaje-validacion-nombre');

nombreRemitente.addEventListener('input', () => {
  const nombre = nombreRemitente.value.trim();
  const valido = regexNombre.test(nombre);

  if (nombre === '') {
    mensajeNombre.style.display = 'none';
    nombreRemitente.style.borderColor = '';
  } else if (valido) {
    mensajeNombre.style.display = 'none';
    nombreRemitente.style.borderColor = '#48bb78'; // verde
  } else {
    mensajeNombre.style.display = 'block';
    mensajeNombre.textContent = 'Solo se permiten letras y espacios (mínimo 2 caracteres).';
    nombreRemitente.style.borderColor = '#fc8181'; // rojo
  }
});


const emailRemitente = document.getElementById('remitente-email');
const mensajeEmail = document.getElementById('mensaje-validacion-email');

emailRemitente.addEventListener('input', () => {
  const email = emailRemitente.value.trim();
  const valido = regexEmail.test(email);

  if (email === '') {
    mensajeEmail.style.display = 'none';
    emailRemitente.style.borderColor = '';
  } else if (valido) {
    mensajeEmail.style.display = 'none';
    emailRemitente.style.borderColor = '#48bb78';
  } else {
    mensajeEmail.style.display = 'block';
    mensajeEmail.textContent = 'Debe ingresar un correo válido (ej. usuario@dominio.com).';
    emailRemitente.style.borderColor = '#fc8181';
  }
});

const direccionDestinatario = document.getElementById('m-direccion');
const mensajeDireccion = document.getElementById('mensaje-validacion-direccion');

direccionDestinatario.addEventListener('input', () => {
  const direccion = direccionDestinatario.value.trim();
  const valido = regexDireccion.test(direccion);

  if (direccion === '') {
    mensajeDireccion.style.display = 'none';
    direccionDestinatario.style.borderColor = '';
  } else if (valido) {
    mensajeDireccion.style.display = 'none';
    direccionDestinatario.style.borderColor = '#48bb78';
  } else {
    mensajeDireccion.style.display = 'block';
    mensajeDireccion.textContent = 'La dirección debe tener entre 5 y 100 caracteres válidos.';
    direccionDestinatario.style.borderColor = '#fc8181';
  }
});
const destTipoDoc = document.getElementById('m-tipoDocumento');
const destinatario_num_doc = document.getElementById('m-nroDocumento');
const mensajeDestinatarioNumDoc = document.getElementById('mensaje-validacion-numero-dest');

destinatario_num_doc.addEventListener('input', () => {
  const tipo = destTipoDoc.value;
  const valor = destinatario_num_doc.value.trim();

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
    mensajeDestinatarioNumDoc.style.display = 'none';
    destinatario_num_doc.style.borderColor = '';
  } else if (valido) {
    mensajeDestinatarioNumDoc.style.display = 'none';
    destinatario_num_doc.style.borderColor = '#48bb78';
  } else {
    mensajeDestinatarioNumDoc.style.display = 'block';
    mensajeDestinatarioNumDoc.textContent = mensaje;
    destinatario_num_doc.style.borderColor = '#fc8181';
  }
});

destTipoDoc.addEventListener('change', () => {
  const valorActual = numeroDoc.value.trim();
  if (valorActual !== '') {
    numeroDoc.dispatchEvent(new Event('input'));
  }
});


const m_celular = document.getElementById('m-celular');
const mensajeTelDest = document.getElementById('mensaje-validacion-telefono-dest');

m_celular.addEventListener('input', () => {
  const telefono = m_celular.value.trim();
  const valido = regexTelefono.test(telefono);

  if (telefono === '') {
    mensajeTelDest.style.display = 'none';
    m_celular.style.borderColor = '';
  } else if (valido) {
    mensajeTelDest.style.display = 'none';
    m_celular.style.borderColor = '#48bb78';
  } else {
    mensajeTelDest.style.display = 'block';
    mensajeTelDest.textContent = 'El teléfono debe comenzar con 9 y tener 9 dígitos.';
    m_celular.style.borderColor = '#fc8181';
  }
});

function attachNumberFieldsValidation() {
  const regexPositivos = /^[0-9]+(?:\.[0-9]+)?$/;

  document.querySelectorAll('input[type="number"]').forEach(input => {
    const errorMsg = document.createElement('span');
    errorMsg.style.color = '#fc8181';
    errorMsg.style.display = 'none';
    errorMsg.textContent = 'Sólo se permiten números enteros o decimales positivos.';
    input.insertAdjacentElement('afterend', errorMsg);

    input.addEventListener('input', () => {
      const val = input.value.trim();
      if (val === '' || regexPositivos.test(val)) {
        input.style.borderColor = '';
        errorMsg.style.display = 'none';
      } else {
        input.style.borderColor = '#fc8181';
        errorMsg.style.display = 'block';
      }
    });
  });
}



/*************************************************************************************************+ */
document.addEventListener("DOMContentLoaded", function () {

  initTabs();
  mostrarCamposDestino();
  toggleFolios();
  toggleArticulos();
  mostrarCamposReceptor();
  restoreState();

  let dep = document.getElementById('origen-departamento');

  dep.addEventListener('change', () => {
    cargarProvincias(dep.value);
    saveOrigen(); 
  }
  );


  let prov = document.getElementById('origen-provincia');

  prov.addEventListener('change', () => {
    cargarDistritos(prov.value);
    saveOrigen(); 

  });

  let dist = document.getElementById('origen-distrito');

  let dep_destino = document.getElementById('select-departamento');

  dist.addEventListener('change', () => {
    cargarDeparDestino(dep.value, prov.value, dist.value);
    saveOrigen(); 
  }
  );


  dep_destino.addEventListener('change', () => {
    let codigo = document.getElementById('origen-sucursal-id').value;
    cargarProvDestino(dep_destino.value, codigo)
  })

  let prov_destino = document.getElementById('select-provincia')
  prov_destino.addEventListener('change', () => {
    let codigo = document.getElementById('origen-sucursal-id').value;
    cargarDistDestino(prov_destino.value, codigo)
  })

  let dist_destino = document.getElementById('select-distrito')
  dist_destino.addEventListener('change', () => {
    let codigo = document.getElementById('origen-sucursal-id').value;
    cargarSucDestino(dep_destino.value, prov_destino.value, dist_destino.value, codigo)
  })

  document
    .querySelectorAll('input[name="modalidad_pago"]')
    .forEach(radio => {
      radio.addEventListener('change', () => {
        if (radio.checked) {
          cargarRecepcion(radio.value);
        }
      });
    });


  document
    .querySelectorAll('.campos-envio > div')
    .forEach(option => {
      const radio = option.querySelector('input');

      option.addEventListener('click', () => {
        radio.checked = true;
        radio.dispatchEvent(new Event('change'));


      });
    });

  attachNumberFieldsValidation();

  document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('keydown', e => {
      if (['+', '-', 'e', 'E'].includes(e.key)) {
        e.preventDefault();
      }
    });
    input.addEventListener('paste', e => {
      const paste = (e.clipboardData || window.clipboardData).getData('text');
      if (/[+\-eE]/.test(paste)) {
        e.preventDefault();
      }
    });



  });

  renderTabla();


});

let origenSeleccionado = null;
let eventosRegistrados = {
  origen: false,
  destino: false
};




function cargarProvincias(depOrigen) {

  dict_dep = { 'dep': depOrigen }
  ruta = '/api/provincia_origen'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_dep)
  })
    .then(res => res.json())
    .then(diccionario => {
      let provinciasSelect = document.getElementById('origen-provincia');
      let distritosSelect = document.getElementById('origen-distrito');
      provinciasSelect.innerHTML = '<option disabled selected value="">Selecciona provincia</option>';
      distritosSelect.innerHTML = '<option disabled selected value="">Selecciona una provincia primero</option>';

      lista_provincia = diccionario.data;
      lista_provincia.forEach(prov => provinciasSelect.append(new Option(prov.provincia, prov.provincia)));


      let departamentoDestinoSelect = document.getElementById('select-departamento');
      let provinciaDestinoSelect = document.getElementById('select-provincia');
      let distritoDestinoSelect = document.getElementById('select-distrito');
      let sucursalDestinoSelect = document.getElementById('select-sucursal');

      departamentoDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero</option>';
      provinciaDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      distritoDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      sucursalDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
    }
    );
}

function cargarDistritos(provOrigen) {
  dict_prov = { 'prov': provOrigen } //Un solo elemento, se debe poner en formato de diccionario
  ruta = '/api/distrito_origen'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_prov)
  })
    .then(res => res.json())
    .then(diccionario => {
      let distritosSelect = document.getElementById('origen-distrito');
      distritosSelect.innerHTML = '<option disabled selected value="">Seleccione un distrito</option>';

      lista_distritos = diccionario.data;
      lista_distritos.forEach(dist => distritosSelect.append(new Option(dist.distrito, dist.distrito)));

      let departamentoDestinoSelect = document.getElementById('select-departamento');
      let provinciaDestinoSelect = document.getElementById('select-provincia');
      let distritoDestinoSelect = document.getElementById('select-distrito');
      let sucursalDestinoSelect = document.getElementById('select-sucursal');

      departamentoDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero</option>';
      provinciaDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      distritoDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      sucursalDestinoSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';

    })
}



function cargarDeparDestino(dep_origen, prov_origen, dist_origen) {
  dict_ubigeo = {
    'dep': dep_origen,
    'prov': prov_origen,//Un solo elemento, se debe poner en formato de diccionario
    'dist': dist_origen
  }

  ruta = '/api/departamento_destino'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_ubigeo)
  })
    .then(res => res.json())
    .then(diccionario => {
      let departamentosSelect = document.getElementById('select-departamento');
      let provinciasSelect = document.getElementById('select-provincia');
      let distritosSelect = document.getElementById('select-distrito');
      let sucursalSelect = document.getElementById('select-sucursal');
      let codigo_origen = document.getElementById('origen-sucursal-id');

      departamentosSelect.innerHTML = '<option disabled selected value="">Seleccione un departamento</option>';
      provinciasSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      distritosSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      sucursalSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';


      lista_departamentos = diccionario.data;

      codigo_origen.value = diccionario.codigo;

      lista_departamentos.forEach(dep => departamentosSelect.append(new Option(dep.departamento, dep.departamento)));

    })
}

function cargarProvDestino(dep_origen, codigo) {
  dict_ubigeo = {
    'dep': dep_origen,
    'codigo': codigo
  }
  ruta = '/api/provincia_destino'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_ubigeo)
  })
    .then(res => res.json())
    .then(diccionario => {
      let provinciasSelect = document.getElementById('select-provincia');
      let distritosSelect = document.getElementById('select-distrito');
      let sucursalSelect = document.getElementById('select-sucursal');


      provinciasSelect.innerHTML = '<option disabled selected value="">Seleccione una provincia</option>';
      distritosSelect.innerHTML = '<option disabled selected value="">Seleccione una provincia primero</option>';
      sucursalSelect.innerHTML = '<option disabled selected value="">Seleccione una provincia primero</option>';


      lista = diccionario.data;
      lista.forEach(prov => provinciasSelect.append(new Option(prov.provincia, prov.provincia)));
    })
}

function cargarDistDestino(prov, codigo) {
  dict_ubigeo = {
    'prov': prov,
    'codigo': codigo
  }
  ruta = '/api/distrito_destino'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_ubigeo)
  })
    .then(res => res.json())
    .then(diccionario => {
      let distritosSelect = document.getElementById('select-distrito');
      const sucursalSelect = document.getElementById('select-sucursal');


      distritosSelect.innerHTML = '<option disabled selected value="">Seleccione un distrito</option>';
      sucursalSelect.innerHTML = '<option disabled selected value="">Seleccione un distrito primero</option>';


      lista = diccionario.data;
      lista.forEach(dist => distritosSelect.append(new Option(dist.distrito, dist.distrito)));
    })
}


function cargarSucDestino(dep_destino, prov_destino, dist_destino, origen) {
  dict_ubigeo = {
    'cod_origen': origen,
    'dep': dep_destino,
    'prov': prov_destino,//Un solo elemento, se debe poner en formato de diccionario
    'dist': dist_destino

  }
  ruta = '/api/sucursal_destino'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_ubigeo)
  })
    .then(res => res.json())
    .then(diccionario => {
      const sucursalSelect = document.getElementById('select-sucursal');

      sucursalSelect.innerHTML = '<option disabled selected value="">Seleccione una sucursal </option>';


      lista = diccionario.data;
      lista.forEach(suc => sucursalSelect.append(new Option(suc.direccion, suc.direccion)));
    })
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

function toggleFolios() { //Funciona bien
  const tipo = document.getElementById('m-tipoEmpaque').value;
  const grupoFolios = document.getElementById('grupo-folios');
  grupoFolios.style.display = (tipo === '2') ? 'flex' : 'none';
  grupoFolios.querySelector('input').setAttribute('required', '');

}

function toggleArticulos() { //Funciona bien 
  const tipo = document.getElementById('m-tipoEmpaque').value;
  const grupoArticulos = document.getElementById('grupo-articulos');
  grupoArticulos.style.display = (tipo === '1') ? 'flex' : 'none';
  grupoArticulos.querySelector('select').setAttribute('required', '');
}

function mostrarCamposReceptor() { //Funciona bien
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

function cargarRecepcion(modalidad) {
  dict_modalidad = { 'modalidad': modalidad };
  ruta = '/api/recepcion'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_modalidad)
  })
    .then(res => res.json())
    .then(diccionario => {

      const recepcion = document.getElementById('m-tipoEntrega');

      recepcion.innerHTML = '<option disabled selected value="">Seleccione un tipo de recepción</option>';

      lista = diccionario.data;
      lista.forEach(rep => recepcion.append(new Option(rep.nombre, rep.id)));
    })
}









function mostrarModalEliminarTodo() {
  const modal = document.getElementById('modalConfirmacion');
  const mensajeParrafo = modal.querySelector('p');
  const confirmarBtn = modal.querySelector('#confirmarBtn');

  mensajeParrafo.textContent = '¿Deseas ELIMINAR todos los envíos?';

  confirmarBtn.textContent = 'Sí, eliminar';

  confirmarBtn.replaceWith(confirmarBtn.cloneNode(true));
  const nuevoConfirmar = modal.querySelector('#confirmarBtn');
  nuevoConfirmar.addEventListener('click', eliminarTodoEnvios);

  modal.style.display = 'flex';
}





function isCurrentTabComplete() {
  const panel = document.querySelector('.tab-panel.active');
  if (!panel) return false;

  // 1) Recorremos todos los inputs, selects y textareas visibles
  const fields = panel.querySelectorAll('input, select, textarea');
  for (const f of fields) {
    // saltamos los que están ocultos
    if (f.offsetParent === null) continue;
    // saltamos la descripción (es opcional)
    if (f.id === 'm-descripcionArticulo') continue;
    // saltamos los radios individuales; validaremos el grupo al final
    if (f.type === 'radio') continue;

    // para todo lo demás, pedimos que no esté vacío
    if (!f.value.trim()) {
      return false;
    }
  }

  // 2) Si en este panel hay un grupo de radios (modalidad de pago),
  //    validamos que al menos uno esté chequeado.
  const radios = panel.querySelectorAll('input[type="radio"][name="modalidad_pago"]');
  if (radios.length) {
    const anyChecked = Array.from(radios).some(r => r.checked);
    if (!anyChecked) return false;
  }

  return true;
}


// Marca o desmarca la animación en el siguiente botón
function updateNextTabHint() {
  const btns = Array.from(document.querySelectorAll('.tab-btn'));
  const activeIndex = btns.findIndex(b => b.classList.contains('active'));
  // quitamos pulsos anteriores
  btns.forEach(b => b.classList.remove('pulse'));

  if (activeIndex >= 0 && isCurrentTabComplete()) {
    const next = btns[activeIndex + 1];
    if (next) next.classList.add('pulse');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Cada vez que cambie un campo dentro de un panel activo:
  document.querySelectorAll('.tabs-content .tab-panel').forEach(panel => {
    panel.addEventListener('input', updateNextTabHint, true);
    panel.addEventListener('change', updateNextTabHint, true);
  });

  // Al cambiar de pestaña, recalculamos y borramos animaciones
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      // delega la clase active como ya tienes...
      updateNextTabHint();
    });
  });

  // Al cargar la página, revisamos si hay que animar
  updateNextTabHint();
});



let registros = [];
let editingIndex = null;

// Modales reutilizables
function showModal({ message = '', onConfirm = null, onCancel = null }) {
  const modal = document.getElementById('modalConfirmacion');
  const texto = modal.querySelector('p');
  const btnOk = modal.querySelector('.btn_acept');
  const btnCancel = modal.querySelector('.btn_cancel');

  texto.textContent = message;

  if (typeof onConfirm === 'function') {
    // Modo confirmación
    btnOk.style.display = 'inline-block';
    btnOk.textContent = 'Sí, agregar';
    btnOk.onclick = () => { modal.style.display = 'none'; onConfirm(); };
    btnCancel.textContent = 'Cancelar';
  } else {
    // Modo sólo aviso
    btnOk.style.display = 'none';
    btnCancel.textContent = 'Entendido';
  }

  btnCancel.onclick = () => {
    modal.style.display = 'none';
    if (onCancel) onCancel();
  };

  modal.style.display = 'flex';
}

function showWarning(message, onConfirm) {
  showModal({ message, onConfirm });
}

function renderTabla() {
  const container = document.getElementById('tableContent');
  if (registros.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No hay envíos registrados aún</p><p>Comienza agregando tu primer envío</p></div>';
    return;
  }
  let html = '<table><thead><tr>' +
    '<th>#</th><th>Recepción</th><th>Destino</th><th>Paquete</th>' +
    '<th>Valor</th><th>Peso</th><th>Dimensiones</th>' +
    '<th>Destinatario</th><th>Modalidad pago</th><th>Clave</th><th>Acciones</th>' +
    '</tr></thead><tbody>';
  registros.forEach((r, i) => {
    html += `<tr>` +
      `<td>${i + 1}</td>` +
      `<td>${r.tipoEntrega}</td>` +
      `<td>${r.destino.departamento}/${r.destino.provincia}/${r.destino.distrito}</td>` +
      `<td>${r.tipoEmpaque === '2' ? r.folios + ' folios' : r.tipoEmpaque + ' - ' + r.tipoArticulo}</td>` +
      `<td>s/ ${r.valorEnvio}</td>` +
      `<td>${r.peso} kg</td>` +
      `<td>${r.largo} cm x ${r.ancho} cm x ${r.alto} cm</td>` +
      `<td>${r.destinatario}</td>` +
      `<td>${r.modalidadPago}</td>` +
      `<td>${r.clave}</td>` +
      `<td>` +
      ` <div class="btn-actions">` +
      `<button class="btn-small btn-edit" data-index="${i}"><i class="fa fa-edit"></i></button>` +
      `<button class="btn-small btn-delete" data-index="${i}"><i class="fa fa-trash"></i></button>` +
      `</div>` +
      `</td></tr>`;
  });
  html += '</tbody></table>';
  container.innerHTML = html;
  attachTableActions();
  saveRegistros();
}

function attachTableActions() {
  document.querySelectorAll('.btn-delete').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = +btn.dataset.index;
      showModal({ message: '¿Eliminar este envío?', onConfirm: () => { registros.splice(idx, 1); renderTabla(); } });
    });
  });
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', () => {
      const idx = +btn.dataset.index;
      const warning = () => startEdit(idx);
      registros.length > 1
        ? showWarning('Al editar se eliminarán registros con origen diferente. Continuar?', warning)
        : warning();
    });
  });
}

// Recolección y llenado de datos
function collectFormData() {
  const destinatario = document.getElementById('m-tipoDocumento').value === '2'
    ? document.getElementById('m-razonSocial').value
    : document.getElementById('m-nombres').value + ' ' + document.getElementById('m-apellidos').value;
  return {
    tipoEntrega: document.querySelector(`#m-tipoEntrega option[value="${document.querySelector('#m-tipoEntrega').value}"]`).textContent,
    destino: {
      departamento: document.getElementById('select-departamento').value,
      provincia: document.getElementById('select-provincia').value,
      distrito: document.getElementById('select-distrito').value
    },
    tipoEmpaque: document.querySelector(`#m-tipoEmpaque option[value="${document.querySelector('#m-tipoEmpaque').value}"]`).value,
    tipoArticulo: document.querySelector(`#m-tipoArticulo option[value="${document.querySelector('#m-tipoArticulo').value}"]`).value,
    folios: document.getElementById('m-folios').value,
    valorEnvio: document.getElementById('m-valorEnvio').value,
    peso: document.getElementById('m-peso').value,
    largo: document.getElementById('m-largo').value,
    ancho: document.getElementById('m-ancho').value,
    alto: document.getElementById('m-alto').value,
    destinatario,
    modalidadPago: document.querySelector('input[name="modalidad_pago"]:checked').value,
    clave: Array.from(document.querySelectorAll('.pin-input')).map(i => i.value).join('')
  };
}

function fillFormData(r) {
  // Pestaña Destino
  document.getElementById('m-tipoEntrega').value = r.tipoEntrega;
  mostrarCamposDestino();
  document.getElementById('select-departamento').value = r.destino.departamento;
  cargarProvDestino(r.destino.departamento, document.getElementById('origen-sucursal-id').value)
    .then(() => document.getElementById('select-provincia').value = r.destino.provincia)
    .then(() => cargarDistDestino(r.destino.provincia, document.getElementById('origen-sucursal-id').value))
    .then(() => document.getElementById('select-distrito').value = r.destino.distrito);

  // Pestaña Paquete
  document.getElementById('m-tipoEmpaque').value = r.tipoEmpaque;
  toggleFolios(); toggleArticulos();
  document.getElementById('m-tipoArticulo').value = r.tipoArticulo;
  document.getElementById('m-folios').value = r.folios;
  document.getElementById('m-valorEnvio').value = r.valorEnvio;
  document.getElementById('m-peso').value = r.peso;
  document.getElementById('m-largo').value = r.largo;
  document.getElementById('m-ancho').value = r.ancho;
  document.getElementById('m-alto').value = r.alto;

  // Pestaña Destinatario
  document.getElementById('m-tipoDocumento').value = r.tipoDocumento;
  mostrarCamposReceptor();
  if (r.tipoDocumento === '2') {
    document.getElementById('m-razonSocial').value = r.destinatario;
  } else {
    const parts = r.destinatario.split(' ');
    document.getElementById('m-nombres').value = parts[0] || '';
    document.getElementById('m-apellidos').value = parts.slice(1).join(' ') || '';
  }

  // Pestaña Modalidad y Clave
  document.querySelector(`input[name="modalidad_pago"][value="${r.modalidadPago}"]`).checked = true;
  document.querySelectorAll('.pin-input').forEach((inp, idx) => inp.value = r.clave[idx] || '');
}

// Validación de campos visibles
function validateEnvio() {
  const panel = document.querySelector('.tab-panel.active');
  const fields = panel.querySelectorAll('input, select, textarea');
  for (const f of fields) {
    if (f.offsetParent === null || f.id === 'm-descripcionArticulo') continue;
    if (!f.value.trim()) return false;
  }
  return true;
}

// Agregar o editar envío
function guardarRegistro() {
  if (!validateEnvio()) {
    showModal({ message: 'Complete todos los campos visibles' });
    return;
  }
  const envio = collectFormData();
  if (editingIndex !== null) {
    registros[editingIndex] = envio;
    editingIndex = null;
  } else registros.push(envio);
  renderTabla();
  clearForm(false);
  lockOrigen();
}

function startEdit(idx) {
  editingIndex = idx;
  fillFormData(registros[idx]);
  document.querySelectorAll('#seccion-origen select').forEach(el => el.disabled = true);
  document.querySelector('.btn-cancel-edit').style.display = 'inline-block';
}

function cancelEdit() {
  editingIndex = null;
  clearForm(true);
  updateNextTabHint();
}

function clearForm(full = true) {
  const seccion = document.getElementById('seccion-masiva');
  if (!seccion) return;

  seccion.querySelectorAll('input, select, textarea').forEach(el => {
    if (el.id === 'origen-sucursal-id' || el.id === 'destino-sucursal-id') {
      return;
    }
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.value = '';
    }
    if (el.tagName === 'SELECT') {
      el.selectedIndex = 0;
    }
  });
}


function lockOrigen() {
  // Deshabilita los selects de origen para evitar cambios
  document.querySelectorAll('#seccion-origen select').forEach(el => el.disabled = true);
}

function unlockOrigen() {
  // Reactiva los selects de origen para permitir cambios
  document.querySelectorAll('#seccion-origen select').forEach(el => el.disabled = false);
}


const btnAdd = document.querySelector('.btn-agregar');
btnAdd.addEventListener('click', () => {
  if (!validateEnvio()) {
    // Si hay campos visibles vacíos, mostrar aviso
    showModal({ message: 'Complete todos los campos visibles' });
  } else {
    // Si todo está bien, pedir confirmación antes de guardar
    showModal({ message: '¿Agregar este envío?', onConfirm: guardarRegistro });
  }
});

// Cancelar edición
document.querySelector('.btn-limpiar').addEventListener('click', cancelEdit);

// Eliminar todos los registros
document.querySelector('.btn-limpiar-todos').addEventListener('click', () => {
  if (registros.length === 0) {
    // No hay nada que eliminar
    showModal({ message: 'No hay registros para eliminar.' });
  } else {
    // Sí hay registros, pedimos confirmación
    showModal({
      message: '¿Eliminar todos los registros?',
      onConfirm: () => {
        registros = [];
        renderTabla();
        unlockOrigen();
      }
    });
  }
});

document.querySelector('.btn-exportar').addEventListener('click', () => {
  if (registros.length === 0) {
    showModal({ message: 'No hay registros para exportar.' });
  } else {
    exportXLSX();
  }
});

function exportXLSX() {
  // 1. Recuperar envíos desde localStorage usando tu clave
  const registrosJson = localStorage.getItem(STORAGE_KEYS.REGISTROS);
  const envios = registrosJson ? JSON.parse(registrosJson) : [];
  if (envios.length === 0) {
    return alert('No hay envíos para exportar');
  }

  // 2. Transformar cada envío en una fila plana
  const data = envios.map(e => ({
    'Modalidad de Pago': e.modalidadPago,
    'Tipo de Entrega': e.tipoEntrega,
    'Depto. Destino': e.destino.departamento,
    'Provincia Destino': e.destino.provincia,
    'Distrito Destino': e.destino.distrito,
    'Tipo de Empaque': e.tipoEmpaque,
    'Tipo de Contenido': e.tipoArticulo || '',
    '# Folios': e.folios || '',
    'Valor (S/)': e.valorEnvio,
    'Peso (kg)': e.peso,
    'Largo (cm)': e.largo,
    'Ancho (cm)': e.ancho,
    'Alto (cm)': e.alto,
    'Destinatario': e.destinatario,
    'Clave de seguridad': e.clave
  }));

  // 3. Crear worksheet y workbook
  const ws = XLSX.utils.json_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Envíos Masivos');

  // 4. Descargar archivo
  XLSX.writeFile(wb, 'envios_masivos.xlsx');
}

// Asociar al botón Exportar
document.querySelector('.btn-exportar')
        .addEventListener('click', exportXLSX);


const btnCancelEdit = document.querySelector('.btn-cancel-edit');
if (btnCancelEdit) btnCancelEdit.style.display = 'none';

