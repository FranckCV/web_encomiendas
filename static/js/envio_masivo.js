const LISTA_ENVIOS = [];

const { rutasTarifas } = window.CONFIG_ENVIO || {};

const STORAGE_KEY = "envios_masivos";

let editIndex = -1;
let pasoActual = 1;

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


const valorInput = document.getElementById('m-valorEnvio');

// Ajustamos showError / clearError para distinguir tipo de error
function showError(input, msg, type = 'rango') {
  let err = getErrorElem(input, type);
  err.textContent = msg;
  err.style.display = 'block';
  input.style.borderColor = '#fc8181';
}

function clearError(input, type = 'rango') {
  const err = getErrorElem(input, type);
  if (err) err.style.display = 'none';
  // solo limpiamos el borde si NO hay otro tipo de error visible
  const otherType = type === 'rango' ? 'volumen' : 'rango';
  const otherErr = getErrorElem(input, otherType);
  if (!otherErr || otherErr.style.display === 'none') {
    input.style.borderColor = '';
  }
}

valorInput.addEventListener('input', () => {
  const raw = valorInput.value.trim();
  const val = parseFloat(raw);

  if (raw === '') {
    clearError(valorInput);
    return;
  }

  if (isNaN(val) || val <= 0) {
    showError(valorInput, 'El valor debe ser mayor que 0.');
    return;
  }

  if (val > MAX_VALOR) {
    showError(valorInput, `El valor no puede exceder S/ ${MAX_VALOR}.`);
    return;
  }

  clearError(valorInput);
});


function getErrorElem(input, type) {
  const cls = `error-msg-${type}`;
  let err = input.parentNode.querySelector(`.${cls}`);
  if (!err) {
    err = document.createElement('small');
    err.className = cls;
    err.style.color = '#fc8181';
    input.insertAdjacentElement('afterend', err);
  }
  return err;
}

const MIN_CM = 5;
const MAX_CM = 200;
const MAX_VOLUMEN = 1000000; 

const inputsDim = {
  largo: document.getElementById('m-largo'),
  ancho: document.getElementById('m-ancho'),
  alto:  document.getElementById('m-alto')
};

Object.values(inputsDim).forEach(input => {
  input.addEventListener('input', () => {
    const val = parseFloat(input.value);

    // 1) Validación individual de rango
    if (isNaN(val) || val < MIN_CM || val > MAX_CM) {
      showError(input, `Debe ingresar un valor entre ${MIN_CM} y ${MAX_CM} cm.`);
      // Si individual falla, limpiamos mensajes de volumen en todos
      Object.values(inputsDim).forEach(i => {
        if (i !== input) clearError(i, 'volumen');
      });
      return;
    } else {
      clearError(input);
    }

    // 2) Solo si TODOS los campos están dentro de rango, validamos volumen
    const largo = parseFloat(inputsDim.largo.value);
    const ancho = parseFloat(inputsDim.ancho.value);
    const alto  = parseFloat(inputsDim.alto.value);

    if (
      !isNaN(largo) && largo >= MIN_CM && largo <= MAX_CM &&
      !isNaN(ancho) && ancho >= MIN_CM && ancho <= MAX_CM &&
      !isNaN(alto)  && alto  >= MIN_CM && alto  <= MAX_CM
    ) {
      const volumen = largo * ancho * alto;
      if (volumen > MAX_VOLUMEN) {
        const msg = `Volumen excesivo: ${volumen.toLocaleString()} cm³ (> ${MAX_VOLUMEN.toLocaleString()} cm³).`;
        // mostramos el error de volumen en **este** campo
        showError(input, msg, 'volumen');
      } else {
        // limpiamos solo los errores de volumen (no tocamos errores de rango)
        Object.values(inputsDim).forEach(i => clearError(i, 'volumen'));
      }
    }
  });
});



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
  if (mode === 'caja' || mode === 'sobre') {
    // deshabilita el select de tipo empaque
    const tipoEmpaque = document.getElementById('m-tipoEmpaque');
    tipoEmpaque.value = (mode === 'sobre' ? '2' : '1');  // 2 = folios, 1 = articulos
    tipoEmpaque.disabled = true;

    // forzamos la lógica de mostrar sólo folios o sólo artículos
    if (mode === 'sobre') {
      toggleFolios();
      document.getElementById('grupo-articulos').style.display = 'none';
    } else { // caja
      toggleArticulos();
      document.getElementById('grupo-folios').style.display = 'none';
    }

    // ocultar tabla de envíos y botón de agregar
    document.querySelector('.tabla-envios').style.display = 'none';
    document.querySelector('.btn-agregar').style.display = 'none';
  }

const pinInputs = document.querySelectorAll('.pin-input');

pinInputs.forEach((input, idx) => {
  input.addEventListener('input', e => {
    // 1) Limita a un dígito
    if (e.target.value.length > 1) e.target.value = e.target.value.slice(0,1);
    // 2) Salta al siguiente
    if (e.target.value && idx < pinInputs.length-1) {
      pinInputs[idx+1].focus();
    }
    // 3) Si ya están todos llenos, guarda el PIN en tu variable
    const valores = Array.from(pinInputs).map(i => i.value);
    if (valores.every(v => v.length === 1)) {
      // Aquí tienes el PIN completo:
      const pin = valores.join('');
      console.log('PIN completo:', pin);
      // Por ejemplo, podrías almacenarlo en un campo hidden:
      document.getElementById('destino-sucursal-id').value = pin;
      // O directamente en tu objeto de formulario:
      // currentForm.pin = pin;
    }
  });

  // Previene teclas inválidas
  input.addEventListener('keydown', e => {
    if (!/[0-9]/.test(e.key) && !['Backspace','Delete','Tab','Enter'].includes(e.key)) {
      e.preventDefault();
    }
  });

  // Maneja pegado de hasta 4 dígitos
  input.addEventListener('paste', e => {
    e.preventDefault();
    const digits = e.clipboardData.getData('text').replace(/\D/g,'').slice(0,4);
    digits.split('').forEach((d,i) => {
      if (pinInputs[i]) pinInputs[i].value = d;
    });
    // Luego dispara de nuevo el input de la última casilla para activar el guardado
    pinInputs[digits.length-1]?.dispatchEvent(new Event('input'));
  });
});



  initTabs();
  mostrarCamposDestino();
  toggleFolios();
  toggleArticulos();
  mostrarCamposReceptor();

  let dep = document.getElementById('origen-departamento');

  dep.addEventListener('change', () => {
    cargarProvincias(dep.value);
  }
  );


  let prov = document.getElementById('origen-provincia');

  prov.addEventListener('change', () => {
    cargarDistritos(prov.value);

  });

  let dist = document.getElementById('origen-distrito');

  dist.addEventListener('change', () => {
    console.log(dep.value, prov.value, dist.value);
    cargarSucursales(dep.value, prov.value, dist.value);
  }
  );

  let suc = document.getElementById('origen-sucursal');

  suc.addEventListener('change', () => {
    console.log(suc.value)
    cargarDeparDestino(suc.value);
  }
  );


  let dep_destino = document.getElementById('select-departamento');

  dep_destino.addEventListener('change', () => {
    let codigo = document.getElementById('origen-sucursal').value;
    cargarProvDestino(dep_destino.value, codigo)
  })

  let prov_destino = document.getElementById('select-provincia')
  prov_destino.addEventListener('change', () => {
    let codigo = document.getElementById('origen-sucursal').value;
    cargarDistDestino(prov_destino.value, codigo)
  })

  let dist_destino = document.getElementById('select-distrito')
  dist_destino.addEventListener('change', () => {
    let codigo = document.getElementById('origen-sucursal').value;
    cargarSucDestino(dep_destino.value, prov_destino.value, dist_destino.value, codigo)
  })

  document
    .querySelectorAll('input[name="modalidad_pago"]')
    .forEach(radio => {
      radio.addEventListener('change', () => {
        if (radio.checked) {
          console.log(radio.value)
          cargarRecepcion(radio.value);
        }
      });
    });

document
  .querySelectorAll('#tab-modalidad-pago .campos-envio > div')
  .forEach(option => {
    const radio = option.querySelector('input[type="radio"]');
    if (!radio) return;
    option.addEventListener('click', () => {
      // Si ya estaba checked, no cambia el estado,
      // pero forzamos el change igualmente y hacemos bubbling:
      radio.checked = true;
      radio.dispatchEvent(new Event('change', { bubbles: true }));
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
      let sucursalSelect = document.getElementById('origen-sucursal');
      sucursalSelect.innerHTML = '<option disabled selected value="">Selecciona una provincia</option>';

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
      let sucursalSelect = document.getElementById('origen-sucursal');
      sucursalSelect.innerHTML = '<option disabled selected value="">Selecciona una distrito primero</option>';

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



function cargarSucursales(dep_origen,prov_origen,dist_origen) {

    dict_ubigeo = {
    'dep': dep_origen,
    'prov': prov_origen,//Un solo elemento, se debe poner en formato de diccionario
    'dist': dist_origen
  }

  ruta = '/api/sucursal_origen'
  fetch(ruta, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dict_ubigeo)
  })
    .then(res => res.json())
    .then(diccionario => {
      let sucursalSelect = document.getElementById('origen-sucursal');
      sucursalSelect.innerHTML = '<option disabled selected value="">Selecciona una sucursal</option>';

      lista = diccionario.data;
      lista.forEach(suc => sucursalSelect.append(new Option(suc.direccion, suc.id)));


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


function cargarDeparDestino(id_origen) {
  dict_ubigeo = {'suc_origen':id_origen}

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

      departamentosSelect.innerHTML = '<option disabled selected value="">Seleccione un departamento</option>';
      provinciasSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      distritosSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';
      sucursalSelect.innerHTML = '<option disabled selected value="">Seleccione un lugar de origen primero </option>';


      lista_departamentos = diccionario.data;


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
      lista.forEach(suc => sucursalSelect.append(new Option(suc.direccion, suc.id)));
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

  if (tipo === '2') {
    grupoDir.style.display = 'flex';
  } else if (tipo === '1') {
    grupoDir.style.display = 'none';
  } else {
    grupoDir.style.display = 'none';
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
  console.log('oaa');
  console.log(modalidad);
  
  if (modalidad == '') {
    console.log(modalidad)
    return false
  }
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

  // 1) Campos de texto / selects / textareas
  const fields = panel.querySelectorAll('input, select, textarea');
  for (const f of fields) {
    if (f.offsetParent === null) continue;          // ocultos
    if (f.id === 'm-descripcionArticulo') continue; // opcional
    if (f.type === 'radio') continue;               // los validamos por grupos
    if (!f.value.trim()) return false;
  }

  // 2) Validar dinámicamente **todos** los grupos de radios de esta pestaña
  const radios = panel.querySelectorAll('input[type="radio"]');
  const byName = {};
  radios.forEach(r => {
    if (r.name) byName[r.name] = true;
  });
  for (const name in byName) {
    const group = panel.querySelectorAll(`input[type="radio"][name="${name}"]`);
    if (group.length && !Array.from(group).some(r => r.checked)) {
      return false;
    }
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



window.registros = [];
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
    btnOk.textContent = 'Continuar';
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
      `<td>${r.valorEnvio}</td>` +
      `<td>${r.peso}</td>` +
      `<td>${r.largo} cm x ${r.ancho} cm x ${r.alto} cm</td>` +
      `<td>${r.destinatario.nombre_destinatario}</td>` +
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


  // const nombreDestinatario = document.getElementById('m-tipoDocumento').value === '2'
  //   ? document.getElementById('m-razonSocial').value
  //   : document.getElementById('m-nombres').value + ' ' + document.getElementById('m-apellidos').value;
  return {
    modo : mode,
    remitente :{
      tipo_doc_remitente : document.getElementById('remitente-tipo-doc').value,
      num_doc_remitente : document.getElementById('remitente-numero-doc').value,
      num_tel_remitente : document.getElementById('remitente-telefono').value,
      nombre_remitente : document.getElementById('remitente-nombre').value,
        correo_remitente : document.getElementById('remitente-email').value,

    },
    origen:{
      departamento_origen : document.getElementById('origen-departamento').value,
      provincia_origen : document.getElementById('origen-distrito').value,
      distrito_origen : document.getElementById('origen-distrito').value,
      sucursal_origen : document.getElementById('origen-sucursal').value
    },
    tipoEntrega: document.querySelector(`#m-tipoEntrega option[value="${document.querySelector('#m-tipoEntrega').value}"]`).textContent,
    tipoEntregaId:document.getElementById('m-tipoEntrega').value,
    destino: {
      departamento: document.getElementById('select-departamento').value,
      provincia: document.getElementById('select-provincia').value,
      distrito: document.getElementById('select-distrito').value,
      sucursal_destino : document.getElementById('select-sucursal').value

    },
    tipoEmpaque: document.querySelector(`#m-tipoEmpaque option[value="${document.querySelector('#m-tipoEmpaque').value}"]`).textContent,
    tipoEmpaqueId: document.getElementById('m-tipoEmpaque').value,
    tipoArticulo: document.querySelector(`#m-tipoArticulo option[value="${document.querySelector('#m-tipoArticulo').value}"]`).textContent,
    tipoArticuloId: document.getElementById('m-tipoArticulo').value,
    folios: document.getElementById('m-folios').value,
    valorEnvio: document.getElementById('m-valorEnvio').value,
    peso: document.getElementById('m-peso').value,
    largo: document.getElementById('m-largo').value,
    ancho: document.getElementById('m-ancho').value,
    alto: document.getElementById('m-alto').value,
    destinatario :{
      tipo_doc_destinatario : document.getElementById('m-tipoDocumento').value,
      num_doc_destinatario : document.getElementById('m-nroDocumento').value,
      num_tel_destinatario : document.getElementById('m-celular').value,
      nombre_destinatario : document.getElementById('m-tipoDocumento').value === '2'
      ? document.getElementById('m-razonSocial').value
    : document.getElementById('m-nombres').value + ' ' + document.getElementById('m-apellidos').value

    },
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

function validateEnvio() {
  // Recorre cada pestaña
  const panels = document.querySelectorAll('.tabs-content .tab-panel');
  for (const panel of panels) {
    // 1) Validar inputs, selects y textareas
    const fields = panel.querySelectorAll('input, select, textarea');
    for (const f of fields) {
      if (f.offsetParent === null) continue;            // campo oculto
      if (f.id === 'm-descripcionArticulo') continue;   // opcional
      if (f.type === 'radio') continue;                 // radios los validamos después
      if (!f.value.trim()) {
        return false;
      }
    }
   
//    Buscamos todos los radios con required, agrupamos por name
  const requiredRadios = Array.from(
    document.querySelectorAll('.tab-panel input[type="radio"][required]')
  );
  const names = [...new Set(requiredRadios.map(r => r.name))];
  for (const name of names) {
    const grupo = document.querySelectorAll(`input[name="${name}"]`);
    if (!Array.from(grupo).some(r => r.checked)) {
      return false;
    }
  }


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
    window.registros[editingIndex] = envio;
    editingIndex = null;
  } else{
  window.registros.push(envio);
  }     
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
    if (el.type === 'radio') return;     // <-- saltamos los radios
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.value = '';
    }
    if (el.tagName === 'SELECT') {
      el.selectedIndex = 0;
    }
  });

  document
    .querySelectorAll('input[name="modalidad_pago"]')
    .forEach(r => r.checked = false);

  const recepcion = document.getElementById('m-tipoEntrega');
  if (recepcion) {
    recepcion.innerHTML = '<option disabled selected value="">Seleccione una modalidad de pago primero</option>';
  }

  if (full) {
    unlockOrigen();
  }
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
btnAdd.addEventListener('click', e => {
  e.preventDefault();  
  if (!validateEnvio()) {
    showModal({ message: 'Complete todos los campos visibles' });
    return;
  }
  showModal({
    message: '¿Agregar este envío?',
    onConfirm: guardarRegistro
  });
});

// Cancelar edición
document.querySelector('.btn-limpiar').addEventListener('click', e => {
  e.preventDefault();

  // 1) Seleccionamos todos los campos relevantes de la sección masiva
  const fields = Array.from(
    document.querySelectorAll(
      '#seccion-masiva input, #seccion-masiva select, #seccion-masiva textarea'
    )
  );

  // 2) Comprobamos si alguno está no vacío (ignoramos placeholders)
  const anyFilled = fields.some(f => f.value && f.value.trim() !== '');

  if (!anyFilled) {
    // 3a) Si ningún campo tiene valor, aviso
    showModal({ message: 'No hay campos para limpiar.' });
  } else {
    // 3b) Si hay al menos uno, cancelamos edición / limpiamos
    cancelEdit();
  }
});

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
    // Si no hay registros, aviso de que debe haber al menos uno
    showModal({ message: 'No hay registros para exportar.' });
  } else {
    // Si hay registros, procedemos a exportar
    exportXLSX();
  }
});

// Ocultar botón de “cancelar edición” hasta que se entre en modo edición
const btnCancelEdit = document.querySelector('.btn-cancel-edit');
if (btnCancelEdit) btnCancelEdit.style.display = 'none';



function exportXLSX() {
  // 1. Tomar los envíos del array global
  if (!registros || registros.length === 0) {
    return showModal({ message: 'No hay envíos para exportar.' });
  }

  // 2. Transformar cada envío en una fila plana
  const data = registros.map(e => ({
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

  // 3. Crear worksheet y workbook con SheetJS
  const ws = XLSX.utils.json_to_sheet(data);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'Envíos Masivos');

  // 4. Disparar la descarga
  XLSX.writeFile(wb, 'envios_masivos.xlsx');
}



// document.addEventListener('DOMContentLoaded', () => {
//   const btn = document.getElementById('btn-continuar');

//   btn.addEventListener('click', async () => {
//     // 1) comprueba que haya al menos un envío registrado
//     if (!window.registros || registros.length === 0) {
//       return showModal({ message: 'Agrega al menos un envío antes de continuar.' });
//     }

//     try {
//       // 2) envía el JSON y fuerza application/json
//       const resp = await fetch('/resumen_envio', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ registros })
//       });

//       if (!resp.ok) {
//         const txt = await resp.text();
//         throw new Error(`(${resp.status}) ${txt}`);
//       }

//       // 3) recibe el HTML renderizado y lo pinta
//       const html = await resp.text();
//       document.open();
//       document.write(html);
//       document.close();

//     } catch (err) {
//       console.error(err);
//       showModal({ message: 'No fue posible generar el resumen: ' + err.message });
//     }
//   });
// });
document.querySelector(".btn-agregar").addEventListener("click", function () {
  const claveInputs = document.querySelectorAll(".pin-input");
  const clave = Array.from(claveInputs).map(input => input.value).join("");

  // if (clave.length !== 4 || clave.includes("")) {
  //   alert("Ingrese una clave de 4 dígitos.");
  //   return;
  // }

  const envio = {
    clave,
    valorEnvio: parseFloat(document.getElementById("m-valorEnvio").value),
    peso: parseFloat(document.getElementById("m-peso").value),
    largo: parseFloat(document.getElementById("m-largo").value),
    ancho: parseFloat(document.getElementById("m-ancho").value),
    alto: parseFloat(document.getElementById("m-alto").value),
    descripcion: document.getElementById("m-descripcionArticulo").value || "",
    // tarifa: 0, // esta función la debes definir tú
    telefono_destinatario: document.getElementById("m-celular").value,
    tipo_doc_destinatario: parseInt(document.getElementById("m-tipoDocumento").value),
    tipo_empaqueid: parseInt(document.getElementById("m-tipoEmpaque").value),
    contenido_paqueteid: parseInt(document.getElementById("m-tipoArticulo").value),
    tipo_recepcionid: parseInt(document.getElementById("m-tipoEntrega").value),
    destino: {
      num_doc_destinatario: document.getElementById("m-nroDocumento").value,
      sucursal_destino: parseInt(document.getElementById("select-sucursal").value)
    },
    origen: {
      sucursal_origen: parseInt(document.getElementById("origen-sucursal").value)
    }
  };

  LISTA_ENVIOS.push(envio);
  actualizarTablaEnvios(); // opcional para mostrar en pantalla
  limpiarCampos(); // opcional para limpiar los inputs
  console.log("Envíos registrados:", LISTA_ENVIOS);
});

function limpiarCampos() {
  const ids = [
    "m-valorEnvio", "m-peso", "m-largo", "m-ancho", "m-alto", "m-descripcionArticulo",
    "m-nroDocumento", "m-celular", "m-nombres", "m-apellidos"
  ];
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = "";
  });

  document.querySelectorAll(".pin-input").forEach(input => input.value = "");
}

document.getElementById("btn-continuar").addEventListener("click", async function () {
  try {
    const remitente = {
      tipo_doc_remitente: document.getElementById("remitente-tipo-doc").value,
      num_doc_remitente: document.getElementById("remitente-numero-doc").value,
      num_tel_remitente: document.getElementById("remitente-telefono").value,
      nombre_remitente: document.getElementById("remitente-nombre").value,
      correo: document.getElementById("remitente-email").value
    };

    const modalidad_pago = document.querySelector("input[name='modalidad_pago']:checked")?.value || null;

    const tipo_comprobante = 1; // O puedes obtenerlo de algún select/radio adicional si existe

    // Envíos agregados (asumimos que los fuiste acumulando en JS)
    const envios = window.LISTA_ENVIOS || []; // si usas una lista JS interna

    // if (envios.length === 0) {
    //   alert("Debe agregar al menos un envío.");
    //   return;
    // }

    const resumenEnvios = {
      remitente,
      modalidad_pago,
      tipo_comprobante,
      envios
    };

    const response = await fetch("/generar_comprobante", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(resumenEnvios)
    });

    const data = await response.json();
    if (data.ok) {
      alert("Comprobante registrado exitosamente");
      // window.location.href = `/ver_comprobante/${data.serie}`;
    } else {
      alert("Error al registrar comprobante.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error inesperado.");
  }
    try {
      // 2) envía el JSON y fuerza application/json
      const resp = await fetch('/resumen_envio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ registros })
      });

      if (!resp.ok) {
        const txt = await resp.text();
        throw new Error(`(${resp.status}) ${txt}`);
      }

      // 3) recibe el HTML renderizado y lo pinta
      const html = await resp.text();
      document.open();
      document.write(html);
      document.close();

    } catch (err) {
      console.error(err);
      showModal({ message: 'No fue posible generar el resumen: ' + err.message });
    }
    
  });


//  agregado ahora ......
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

function agregarEnvio() {
  const m_tipoEntrega = document.getElementById('m-tipoEntrega');
  const select_departamento = document.getElementById('select-departamento');
  const select_provincia = document.getElementById('select-provincia');
  const select_distrito = document.getElementById('select-distrito');
  const m_direccion = document.getElementById('m-direccion');
  const select_sucursal = document.getElementById('select-sucursal');

  const m_tipoEmpaque = document.getElementById('m-tipoEmpaque');
  const m_tipoArticulo = document.getElementById('m-tipoArticulo');
  const m_valorEnvio = document.getElementById('m-valorEnvio');
  const m_peso = document.getElementById('m-peso');
  const m_largo = document.getElementById('m-largo');
  const m_ancho = document.getElementById('m-ancho');
  const m_alto = document.getElementById('m-alto');
  const m_folios = document.getElementById('m-folios');
  const m_descripcionArticulo = document.getElementById('m-descripcionArticulo');

  const m_tipoDocumento = document.getElementById('m-tipoDocumento');
  const m_nroDocumento = document.getElementById('m-nroDocumento');
  const m_celular = document.getElementById('m-celular');
  const m_razonSocial = document.getElementById('m-razonSocial');
  const m_contacto = document.getElementById('m-contacto');
  const m_nombres = document.getElementById('m-nombres');
  const m_apellidos = document.getElementById('m-apellidos');

  const campoCodigo = document.getElementById('remitente-codigo');

  const tipoEntregaId = m_tipoEntrega.value;
  const tipoEntregaNombre = m_tipoEntrega.selectedOptions[0]?.text || '';

  const tipoEmpaqueId = m_tipoEmpaque.value;
  const tipoEmpaqueNombre = m_tipoEmpaque.selectedOptions[0]?.text || '';
  const contenidoPaqueteId = m_tipoArticulo.value;
  const contenidoPaqueteNombre = m_tipoArticulo.selectedOptions[0]?.text || '';
  const tipoDocumentoId = m_tipoDocumento.value;
  const tipoDocumentoNombre = m_tipoDocumento.selectedOptions[0]?.text || '';

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
      folios: m_folios.value ? parseInt(m_folios.value) : null,
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
    },
    codigo: campoCodigo.value.trim() || null
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

  if (editIndex >= 0) {
    enviosActuales[editIndex] = envio;
    editIndex = -1;
    const btn = document.getElementById('btn-guardar');
    if (btn) {
      btn.textContent = 'Agregar';
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



function recolectarDatosEnvio() {
  return {
    tipo_documento_origen: document.getElementById('remitente-tipo-doc').value || null,
    dni_origen: document.getElementById('remitente-numero-doc').value.trim(),
    cel_origen: document.getElementById('remitente-telefono').value.trim(),
    nombre_remitente: document.getElementById('remitente-nombre').value.trim(),
    email: document.getElementById('remitente-email').value.trim(),
    id_origen: document.getElementById('origen-sucursal-id').value,
    tipo_recepcion: document.getElementById('m-tipoEntrega').value || null,

    cod_seguridad: document.getElementById('remitente-codigo').value.trim(),

    id_destino: document.getElementById('destino-sucursal-id').value || null,
    id_empaque: document.getElementById('m-tipoEmpaque').value,
    valor_paquete: document.getElementById('m-valorEnvio').value,
    peso: document.getElementById('m-peso').value,
    largo: document.getElementById('m-largo').value,
    ancho: document.getElementById('m-ancho').value,
    alto: document.getElementById('m-alto').value,
    descripcion: document.getElementById('m-descripcionArticulo').value.trim(),

    tipo_documento_destino: document.getElementById('m-tipoDocumento').value,
    dni_destino: document.getElementById('m-nroDocumento').value.trim(),
    cel_destino: document.getElementById('m-celular').value.trim(),
    nombre_destinatario: (
      document.getElementById('m-razonSocial').value.trim() ||
      (document.getElementById('m-nombres').value.trim() + ' ' + document.getElementById('m-apellidos').value.trim())
    ),
    contacto_destino: document.getElementById('m-contacto').value.trim(),
    distrito_origen: document.getElementById('origen-distrito').value,
    distrito_destino_sucursal: document.getElementById('select-distrito').value,
    direccion_destino: document.getElementById('m-direccion').value.trim(),

    folios: document.getElementById('m-folios').value ? parseInt(document.getElementById('m-folios').value) : null,
    tipo_articulo: document.getElementById('m-tipoArticulo').value,


  };




}



document.getElementById('btn-continuar').addEventListener('click', () => {
 // agregarEnvio();
  const datos = recolectarDatosEnvio();

  fetch("/guardar_datos_envio", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(datos)
  })
    .then(res => res.json())
    .then(data => {
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else {
        alert("Error al redirigir");
      }
    })
    .catch(err => {
      console.error("Error en el envío:", err);
    });

});

