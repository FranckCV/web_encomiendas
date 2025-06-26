// ===========================
// CONFIGURACIÓN Y CONSTANTES
// ===========================
const CONFIG = {
  STORAGE_KEY: "envios_masivos",
  MIN_CM: 5,
  MAX_CM: 200,
  MAX_VOLUMEN: 1000000,
  MAX_VALOR: 50000, // Asumiendo un valor máximo
  REGEX: {
    telefono: /^9\d{8}$/,
    dni: /^\d{8}$/,
    ruc: /^(10|20)\d{9}$/,
    pasaporte: /^[A-Z0-9]{6,12}$/i,
    ce: /^[A-Z0-9]{9,12}$/i,
    nombre: /^[\p{L} '-]{2,60}$/u,
    email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    direccion: /^[a-zA-Z0-9\sáéíóúÁÉÍÓÚñÑ\-,.#°º()]{5,100}$/,
    apellido: /^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:[ '\-][A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$/,
    razonSocial: /^[A-Za-z0-9ÁÉÍÓÚáéíóúÑñ&\.\-,() ]{2,100}$/,
    positivos: /^[0-9]+(?:\.[0-9]+)?$/
  }
};

// Variables globales
let LISTA_ENVIOS = [];
let editIndex = -1;
let pasoActual = 1;
let origenSeleccionado = null;
let eventosRegistrados = { origen: false, destino: false };
let editingIndex = null;
window.registros = [];

// ===========================
// UTILIDADES GENERALES
// ===========================
class Utils {
  static showModal({ message = '', onConfirm = null, onCancel = null }) {
    const modal = document.getElementById('modalConfirmacion');
    const texto = modal.querySelector('p');
    const btnOk = modal.querySelector('.btn_acept');
    const btnCancel = modal.querySelector('.btn_cancel');

    texto.textContent = message;

    if (typeof onConfirm === 'function') {
      btnOk.style.display = 'inline-block';
      btnOk.textContent = 'Continuar';
      btnOk.onclick = () => { modal.style.display = 'none'; onConfirm(); };
      btnCancel.textContent = 'Cancelar';
    } else {
      btnOk.style.display = 'none';
      btnCancel.textContent = 'Entendido';
    }

    btnCancel.onclick = () => {
      modal.style.display = 'none';
      if (onCancel) onCancel();
    };

    modal.style.display = 'flex';
  }

  static showWarning(message, onConfirm) {
    this.showModal({ message, onConfirm });
  }

  static cerrarModal() {
    const modal = document.getElementById('modalConfirmacion');
    modal.style.display = 'none';
    const confirmarBtn = document.getElementById('confirmarBtn');
    confirmarBtn.replaceWith(confirmarBtn.cloneNode(true));
  }
}

// ===========================
// VALIDACIONES
// ===========================
class Validator {
  static getErrorElem(input, type = 'rango') {
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

  static showError(input, msg, type = 'rango') {
    let err = this.getErrorElem(input, type);
    err.textContent = msg;
    err.style.display = 'block';
    input.classList.add('manually-invalid')
  }

  static clearError(input, type = 'rango') {
    const err = this.getErrorElem(input, type);
    if (err) err.style.display = 'none';
    const otherType = type === 'rango' ? 'volumen' : 'rango';
    const otherErr = this.getErrorElem(input, otherType);
    if (!otherErr || otherErr.style.display === 'none') {
      // ╮（╯＿╰）╭
    }
    input.classList.remove('manually-invalid')
  }

  static validateDocument(tipo, valor) {
    const regex = CONFIG.REGEX;
    switch (tipo) {
      case '1': return { valid: regex.dni.test(valor), message: 'Debe tener 8 dígitos.' };
      case '2': return { valid: regex.ruc.test(valor), message: 'Debe comenzar con 10 o 20 y tener 11 dígitos.' };
      case '3': return { valid: regex.ce.test(valor), message: 'Debe tener 9-12 caracteres alfanuméricos.' };
      case '4': return { valid: regex.pasaporte.test(valor), message: 'Debe tener 6-12 caracteres alfanuméricos.' };
      default: return { valid: false, message: 'Seleccione tipo de documento.' };
    }
  }

  static validatePhone(telefono) {
    return CONFIG.REGEX.telefono.test(telefono);
  }

  static validateEmail(email) {
    return CONFIG.REGEX.email.test(email);
  }

  static validateName(nombre) {
    return CONFIG.REGEX.nombre.test(nombre);
  }

  static validateAddress(direccion) {
    return CONFIG.REGEX.direccion.test(direccion);
  }

  static validatePositiveNumber(value) {
    return CONFIG.REGEX.positivos.test(value);
  }

  static validateDimensions(largo, ancho, alto) {
    const values = [
      { name: "largo", value: largo },
      { name: "ancho", value: ancho },
      { name: "alto", value: alto }
    ];

    const invalidValues = values.filter(v =>
      isNaN(v.value) || v.value < CONFIG.MIN_CM || v.value > CONFIG.MAX_CM
    );

    if (invalidValues.length > 0) {
      const detalles = invalidValues.map(v =>
        `${v.name} (${v.value})`
      ).join(", ");

      return {
        valid: false,
        message: `Valores inválidos: ${detalles}. Deben estar entre ${CONFIG.MIN_CM} y ${CONFIG.MAX_CM} cm.`,
        invalidFields: invalidValues.map(v => v.name)
      };
    }

    const volumen = largo * ancho * alto;
    if (volumen > CONFIG.MAX_VOLUMEN) {
      return {
        valid: false,
        message: `Volumen excesivo: ${volumen.toLocaleString()} cm³ (> ${CONFIG.MAX_VOLUMEN.toLocaleString()} cm³).`
      };
    }

    return { valid: true };
  }


  static isCurrentTabComplete() {
    const panel = document.querySelector('.tab-panel.active');
    if (!panel) return false;

    const fields = panel.querySelectorAll('input, select, textarea');
    for (const f of fields) {
      if (f.offsetParent === null) continue;
      if (f.id === 'm-descripcionArticulo') continue;
      if (f.type === 'radio') continue;
      if (!f.value.trim()) return false;
    }

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

  static validarRequeridos() {
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
        campo.focus();
        return false;
      } else {
        campo.style.borderColor = '';
      }
    }

    return true;
  }
}

// ===========================
// GESTIÓN DE FORMULARIOS
// ===========================
class FormManager {
  static setupValidationListeners() {
    this.setupValueValidation();
    this.setupDimensionValidation();
    this.setupDocumentValidation();
    this.setupPhoneValidation();
    this.setupNameValidation();
    this.setupEmailValidation();
    this.setupAddressValidation();
    this.setupNumberFieldsValidation();
    this.setupPinInputs();
  }

  static setupValueValidation() {
    const valorInput = document.getElementById('m-valorEnvio');
    if (!valorInput) return;

    valorInput.addEventListener('input', () => {
      const raw = valorInput.value.trim();
      const val = parseFloat(raw);

      if (raw === '') {
        Validator.clearError(valorInput);
        return;
      }

      if (isNaN(val) || val <= 0) {
        Validator.showError(valorInput, 'El valor debe ser mayor que 0.');
        return;
      }

      if (val > CONFIG.MAX_VALOR) {
        Validator.showError(valorInput, `El valor no puede exceder S/ ${CONFIG.MAX_VALOR}.`);
        return;
      }

      Validator.clearError(valorInput);
    });
  }

  static setupDimensionValidation() {
    const inputsDim = {
      largo: document.getElementById('m-largo'),
      ancho: document.getElementById('m-ancho'),
      alto: document.getElementById('m-alto')
    };

    Object.values(inputsDim).forEach(input => {
      if (!input) return;

      Object.values(inputsDim).forEach(input => {
        input.addEventListener('input', () => {
          const largo = parseFloat(inputsDim.largo.value);
          const ancho = parseFloat(inputsDim.ancho.value);
          const alto = parseFloat(inputsDim.alto.value);

          const result = Validator.validateDimensions(largo, ancho, alto);

          Object.values(inputsDim).forEach(i => {
            Validator.clearError(i);
            Validator.clearError(i, 'volumen');
          });

          if (!result.valid) {
            if (result.invalidFields) {
              result.invalidFields.forEach(fieldName => {
                const fieldInput = inputsDim[fieldName];
                Validator.showError(
                  fieldInput,
                  `${fieldName} inválido: debe estar entre ${CONFIG.MIN_CM} y ${CONFIG.MAX_CM} cm.`
                );
              });
            } else {
              Object.values(inputsDim).forEach(i =>
                Validator.showError(i, result.message, 'volumen')
              );
            }
          }
        });
      });

    });
  }



  static setupDocumentValidation() {
    // Remitente
    const tipoDocRemitente = document.getElementById('remitente-tipo-doc');
    const numeroDocRemitente = document.getElementById('remitente-numero-doc');
    const mensajeDocRemitente = document.getElementById('mensaje-validacion-numero');

    if (numeroDocRemitente && tipoDocRemitente) {
      this.setupDocumentField(tipoDocRemitente, numeroDocRemitente, mensajeDocRemitente);
    }

    // Destinatario
    const tipoDocDestinatario = document.getElementById('m-tipoDocumento');
    const numeroDocDestinatario = document.getElementById('m-nroDocumento');
    const mensajeDocDestinatario = document.getElementById('mensaje-validacion-numero-dest');

    if (numeroDocDestinatario && tipoDocDestinatario) {
      this.setupDocumentField(tipoDocDestinatario, numeroDocDestinatario, mensajeDocDestinatario);
    }
  }

  static setupDocumentField(tipoSelect, numeroInput, mensajeElement) {
    numeroInput.addEventListener('input', () => {
      const tipo = tipoSelect.value;
      const valor = numeroInput.value.trim();
      const validation = Validator.validateDocument(tipo, valor);

      if (valor === '') {
        if (mensajeElement) mensajeElement.style.display = 'none';
        numeroInput.style.borderColor = '';
      } else if (validation.valid) {
        if (mensajeElement) mensajeElement.style.display = 'none';
        numeroInput.style.borderColor = '#48bb78';
      } else {
        if (mensajeElement) {
          mensajeElement.style.display = 'block';
          mensajeElement.textContent = validation.message;
        }
        numeroInput.style.borderColor = '#fc8181';
      }
    });

    tipoSelect.addEventListener('change', () => {
      const valorActual = numeroInput.value.trim();
      if (valorActual !== '') {
        numeroInput.dispatchEvent(new Event('input'));
      }
    });
  }

  static setupPhoneValidation() {
    // Teléfono remitente
    const telefonoRemitente = document.getElementById('remitente-telefono');
    const mensajeTelefono = document.getElementById('mensaje-validacion-telefono');

    if (telefonoRemitente) {
      this.setupPhoneField(telefonoRemitente, mensajeTelefono);
    }

    // Teléfono destinatario
    const telefonoDestinatario = document.getElementById('m-celular');
    const mensajeTelefonoDest = document.getElementById('mensaje-validacion-telefono-dest');

    if (telefonoDestinatario) {
      this.setupPhoneField(telefonoDestinatario, mensajeTelefonoDest);
    }
  }

  static setupPhoneField(input, messageElement) {
    input.addEventListener('input', () => {
      const telefono = input.value.trim();
      const valido = Validator.validatePhone(telefono);

      if (telefono === '') {
        if (messageElement) messageElement.style.display = 'none';
        input.style.borderColor = '';
      } else if (valido) {
        if (messageElement) messageElement.style.display = 'none';
        input.style.borderColor = '#48bb78';
      } else {
        if (messageElement) {
          messageElement.style.display = 'block';
          messageElement.textContent = 'El teléfono debe comenzar con 9 y tener 9 dígitos.';
        }
        input.style.borderColor = '#fc8181';
      }
    });
  }

  static setupNameValidation() {
    const nombreRemitente = document.getElementById('remitente-nombre');
    const mensajeNombre = document.getElementById('mensaje-validacion-nombre');

    if (nombreRemitente) {
      nombreRemitente.addEventListener('input', () => {
        const nombre = nombreRemitente.value.trim();
        const valido = Validator.validateName(nombre);

        if (nombre === '') {
          if (mensajeNombre) mensajeNombre.style.display = 'none';
          nombreRemitente.style.borderColor = '';
        } else if (valido) {
          if (mensajeNombre) mensajeNombre.style.display = 'none';
          nombreRemitente.style.borderColor = '#48bb78';
        } else {
          if (mensajeNombre) {
            mensajeNombre.style.display = 'block';
            mensajeNombre.textContent = 'Solo se permiten letras y espacios (mínimo 2 caracteres).';
          }
          nombreRemitente.style.borderColor = '#fc8181';
        }
      });
    }
  }

  static setupEmailValidation() {
    const emailRemitente = document.getElementById('remitente-email');
    const mensajeEmail = document.getElementById('mensaje-validacion-email');

    if (emailRemitente) {
      emailRemitente.addEventListener('input', () => {
        const email = emailRemitente.value.trim();
        const valido = Validator.validateEmail(email);

        if (email === '') {
          if (mensajeEmail) mensajeEmail.style.display = 'none';
          emailRemitente.style.borderColor = '';
        } else if (valido) {
          if (mensajeEmail) mensajeEmail.style.display = 'none';
          emailRemitente.style.borderColor = '#48bb78';
        } else {
          if (mensajeEmail) {
            mensajeEmail.style.display = 'block';
            mensajeEmail.textContent = 'Debe ingresar un correo válido (ej. usuario@dominio.com).';
          }
          emailRemitente.style.borderColor = '#fc8181';
        }
      });
    }
  }

  static setupAddressValidation() {
    const direccionDestinatario = document.getElementById('m-direccion');
    const mensajeDireccion = document.getElementById('mensaje-validacion-direccion');

    if (direccionDestinatario) {
      direccionDestinatario.addEventListener('input', () => {
        const direccion = direccionDestinatario.value.trim();
        const valido = Validator.validateAddress(direccion);

        if (direccion === '') {
          if (mensajeDireccion) mensajeDireccion.style.display = 'none';
          direccionDestinatario.style.borderColor = '';
        } else if (valido) {
          if (mensajeDireccion) mensajeDireccion.style.display = 'none';
          direccionDestinatario.style.borderColor = '#48bb78';
        } else {
          if (mensajeDireccion) {
            mensajeDireccion.style.display = 'block';
            mensajeDireccion.textContent = 'La dirección debe tener entre 5 y 100 caracteres válidos.';
          }
          direccionDestinatario.style.borderColor = '#fc8181';
        }
      });
    }
  }

  static setupNumberFieldsValidation() {
    document.querySelectorAll('input[type="number"]').forEach(input => {
      const errorMsg = document.createElement('span');
      errorMsg.style.color = '#fc8181';
      errorMsg.style.display = 'none';
      errorMsg.textContent = 'Sólo se permiten números enteros o decimales positivos.';
      input.insertAdjacentElement('afterend', errorMsg);

      input.addEventListener('input', () => {
        const val = input.value.trim();
        if (val === '' || Validator.validatePositiveNumber(val)) {
          input.style.borderColor = '';
          errorMsg.style.display = 'none';
        } else {
          input.style.borderColor = '#fc8181';
          errorMsg.style.display = 'block';
        }
      });

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
  }

static setupPinInputs() {
  const pinInputs = document.querySelectorAll('.pin-input');

  pinInputs.forEach((input, idx) => {
    input.addEventListener('input', e => {
      if (e.target.value.length > 1) e.target.value = e.target.value.slice(0, 1);

      if (e.target.value && idx < pinInputs.length - 1) {
        pinInputs[idx + 1].focus();
      }

      const valores = Array.from(pinInputs).map(i => i.value);
      if (valores.every(v => v.length === 1)) {
        const pin = valores.join('');
        console.log('PIN completo:', pin);

      }
    });

    input.addEventListener('keydown', e => {
      if (!/[0-9]/.test(e.key) && !['Backspace', 'Delete', 'Tab', 'Enter'].includes(e.key)) {
        e.preventDefault();
      }
    });

    input.addEventListener('paste', e => {
      e.preventDefault();
      const digits = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 4);
      digits.split('').forEach((d, i) => {
        if (pinInputs[i]) pinInputs[i].value = d;
      });
      pinInputs[digits.length - 1]?.dispatchEvent(new Event('input'));
    });
  });
}

  static clearForm(full = true) {
    const seccion = document.getElementById('seccion-masiva');
    if (!seccion) return;

    seccion.querySelectorAll('input, select, textarea').forEach(el => {
      if (el.type === 'radio') return;
      if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
        el.value = '';
      }
      if (el.tagName === 'SELECT') {
        el.selectedIndex = 0;
      }
    });

    document.querySelectorAll('input[name="modalidad_pago"]').forEach(r => r.checked = false);

    const recepcion = document.getElementById('m-tipoEntrega');
    if (recepcion) {
      recepcion.innerHTML = '<option disabled selected value="">Seleccione una modalidad de pago primero</option>';
    }

    if (full) {
      this.unlockOrigen();
    }
  }

  static lockOrigen() {
    document.querySelectorAll('#seccion-origen select').forEach(el => el.disabled = true);
  }

  static unlockOrigen() {
    document.querySelectorAll('#seccion-origen select').forEach(el => el.disabled = false);
  }
}

// ===========================
// GESTIÓN DE PESTAÑAS Y UI
// ===========================
class TabManager {
  static initTabs() {
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

  static updateNextTabHint() {
    const btns = Array.from(document.querySelectorAll('.tab-btn'));
    const activeIndex = btns.findIndex(b => b.classList.contains('active'));
    btns.forEach(b => b.classList.remove('pulse'));

    if (activeIndex >= 0 && Validator.isCurrentTabComplete()) {
      const next = btns[activeIndex + 1];
      if (next) next.classList.add('pulse');
    }
  }

  static setupTabHints() {
    document.querySelectorAll('.tabs-content .tab-panel').forEach(panel => {
      panel.addEventListener('input', this.updateNextTabHint, true);
      panel.addEventListener('change', this.updateNextTabHint, true);
    });

    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        this.updateNextTabHint();
      });
    });

    this.updateNextTabHint();
  }
}


// ===========================
// GESTIÓN DE UBICACIONES (API)
// ===========================
class LocationManager {
  static async cargarProvincias(depOrigen) {
    try {
      const response = await fetch('/api/provincia_origen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dep: depOrigen })
      });

      const data = await response.json();
      this.updateSelect('origen-provincia', data.data, 'provincia', 'Selecciona provincia');
      this.resetSelect('origen-distrito', 'Selecciona una provincia primero');
      this.resetSelect('origen-sucursal', 'Selecciona una provincia');
      this.resetDestinationSelects();
    } catch (error) {
      console.error('Error cargando provincias:', error);
    }
  }

  static async cargarDistritos(provOrigen) {
    try {
      const response = await fetch('/api/distrito_origen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prov: provOrigen })
      });

      const data = await response.json();
      this.updateSelect('origen-distrito', data.data, 'distrito', 'Seleccione un distrito');
      this.resetSelect('origen-sucursal', 'Selecciona un distrito primero');
      this.resetDestinationSelects();
    } catch (error) {
      console.error('Error cargando distritos:', error);
    }
  }

  static async cargarSucursales(dep_origen, prov_origen, dist_origen) {
    try {
      const response = await fetch('/api/sucursal_origen', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dep: dep_origen, prov: prov_origen, dist: dist_origen })
      });

      const data = await response.json();
      this.updateSelect('origen-sucursal', data.data, 'direccion', 'Selecciona una sucursal', 'id');
      this.resetDestinationSelects();
    } catch (error) {
      console.error('Error cargando sucursales:', error);
    }
  }

  static async cargarDeparDestino(id_origen) {
    try {
      const response = await fetch('/api/departamento_destino', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ suc_origen: id_origen })
      });

      const data = await response.json();
      this.updateSelect('select-departamento', data.data, 'departamento', 'Seleccione un departamento');
      this.resetSelect('select-provincia', 'Seleccione un lugar de origen primero');
      this.resetSelect('select-distrito', 'Seleccione un lugar de origen primero');
      this.resetSelect('select-sucursal', 'Seleccione un lugar de origen primero');
    } catch (error) {
      console.error('Error cargando departamentos destino:', error);
    }
  }

  static async cargarProvDestino(dep_origen, codigo) {
    try {
      const response = await fetch('/api/provincia_destino', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ dep: dep_origen, codigo })
      });

      const data = await response.json();
      this.updateSelect('select-provincia', data.data, 'provincia', 'Seleccione una provincia');
      this.resetSelect('select-distrito', 'Seleccione una provincia primero');
      this.resetSelect('select-sucursal', 'Seleccione una provincia primero');
    } catch (error) {
      console.error('Error cargando provincias destino:', error);
    }
  }

  static async cargarDistDestino(prov, codigo) {
    try {
      const response = await fetch('/api/distrito_destino', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prov, codigo })
      });

      const data = await response.json();
      this.updateSelect('select-distrito', data.data, 'distrito', 'Seleccione un distrito');
      this.resetSelect('select-sucursal', 'Seleccione un distrito primero');
    } catch (error) {
      console.error('Error cargando distritos destino:', error);
    }
  }

  static async cargarSucDestino(dep_destino, prov_destino, dist_destino, origen) {
    try {
      const response = await fetch('/api/sucursal_destino', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          cod_origen: origen,
          dep: dep_destino,
          prov: prov_destino,
          dist: dist_destino
        })
      });

      const data = await response.json();
      this.updateSelect('select-sucursal', data.data, 'direccion', 'Seleccione una sucursal', 'id');
    } catch (error) {
      console.error('Error cargando sucursales destino:', error);
    }
  }

  static async cargarRecepcion(modalidad) {
    if (!modalidad) return;

    try {
      const response = await fetch('/api/recepcion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ modalidad })
      });

      const data = await response.json();
      this.updateSelect('m-tipoEntrega', data.data, 'nombre', 'Seleccione un tipo de recepción', 'id');
    } catch (error) {
      console.error('Error cargando tipos de recepción:', error);
    }
  }

  static updateSelect(selectId, data, textField, placeholder, valueField = null) {
    const select = document.getElementById(selectId);
    if (!select) return;

    select.innerHTML = `<option disabled selected value="">${placeholder}</option>`;

    if (data && Array.isArray(data)) {
      data.forEach(item => {
        const value = valueField ? item[valueField] : item[textField];
        const text = item[textField];
        select.appendChild(new Option(text, value));
      });
    }
  }

  static resetSelect(selectId, placeholder) {
    const select = document.getElementById(selectId);
    if (select) {
      select.innerHTML = `<option disabled selected value="">${placeholder}</option>`;
    }
  }

  static resetDestinationSelects() {
    const selects = [
      { id: 'select-departamento', text: 'Seleccione un lugar de origen primero' },
      { id: 'select-provincia', text: 'Seleccione un lugar de origen primero' },
      { id: 'select-distrito', text: 'Seleccione un lugar de origen primero' },
      { id: 'select-sucursal', text: 'Seleccione un lugar de origen primero' }
    ];

    selects.forEach(({ id, text }) => this.resetSelect(id, text));
  }

  static setupLocationListeners() {
    const elements = {
      dep: document.getElementById('origen-departamento'),
      prov: document.getElementById('origen-provincia'),
      dist: document.getElementById('origen-distrito'),
      suc: document.getElementById('origen-sucursal'),
      depDestino: document.getElementById('select-departamento'),
      provDestino: document.getElementById('select-provincia'),
      distDestino: document.getElementById('select-distrito')
    };

    if (elements.dep) {
      elements.dep.addEventListener('change', () => {
        this.cargarProvincias(elements.dep.value);
      });
    }

    if (elements.prov) {
      elements.prov.addEventListener('change', () => {
        this.cargarDistritos(elements.prov.value);
      });
    }

    if (elements.dist) {
      elements.dist.addEventListener('change', () => {
        this.cargarSucursales(elements.dep.value, elements.prov.value, elements.dist.value);
      });
    }

    if (elements.suc) {
      elements.suc.addEventListener('change', () => {
        this.cargarDeparDestino(elements.suc.value);
      });
    }

    if (elements.depDestino) {
      elements.depDestino.addEventListener('change', () => {
        const codigo = document.getElementById('origen-sucursal').value;
        this.cargarProvDestino(elements.depDestino.value, codigo);
      });
    }

    if (elements.provDestino) {
      elements.provDestino.addEventListener('change', () => {
        const codigo = document.getElementById('origen-sucursal').value;
        this.cargarDistDestino(elements.provDestino.value, codigo);
      });
    }

    if (elements.distDestino) {
      elements.distDestino.addEventListener('change', () => {
        const codigo = document.getElementById('origen-sucursal').value;
        this.cargarSucDestino(
          elements.depDestino.value,
          elements.provDestino.value,
          elements.distDestino.value,
          codigo
        );
      });
    }

    // Modalidad de pago
    document.querySelectorAll('input[name="modalidad_pago"]').forEach(radio => {
      radio.addEventListener('change', () => {
        if (radio.checked) {
          this.cargarRecepcion(radio.value);
        }
      });
    });

    // Click en opciones de modalidad de pago
    document.querySelectorAll('#tab-modalidad-pago .campos-envio > div').forEach(option => {
      const radio = option.querySelector('input[type="radio"]');
      if (!radio) return;

      option.addEventListener('click', () => {
        radio.checked = true;
        radio.dispatchEvent(new Event('change', { bubbles: true }));
      });
    });
  }
}

// ===========================
// GESTIÓN DE ENVÍOS
// ===========================

class ShippingManager {
  
  // Método principal para recoger datos del formulario actual
  static collectFormData() {
    const getValue = (id) => {
      const element = document.getElementById(id);
      return element ? element.value.trim() : '';
    };

    const getCheckedRadio = (name) => {
      const radio = document.querySelector(`input[name="${name}"]:checked`);
      return radio ? radio.value : '';
    };

    // Recopilar datos del registro individual
    const registro = {
      clave: Array.from(document.querySelectorAll('.pin-input')).map(i => i.value || '').join(''),
      valorEnvio: parseFloat(getValue('m-valorEnvio')) || 0,
      peso: parseFloat(getValue('m-peso')) || 0,
      alto: parseFloat(getValue('m-alto')) || 0,
      largo: parseFloat(getValue('m-largo')) || 0,
      ancho: parseFloat(getValue('m-ancho')) || 0,
      tarifa: 0, // Se calculará en el backend
      tipoEmpaqueId: parseInt(getValue('m-tipoEmpaque')) || null,
      tipoArticuloId: parseInt(getValue('m-tipoArticulo')) || null,
      tipoEntregaId: parseInt(getValue('m-tipoEntrega')) || null,
      estado_pago: "P", // Por defecto pendiente
      modalidadPago: getCheckedRadio('modalidad_pago'),
      destino: {
        sucursal_destino: parseInt(getValue('select-sucursal')) || null
      },
      destinatario: {
        nombres: getValue('m-nombres'),
        apellidos: getValue('m-apellidos'),
        tipo_doc_destinatario: parseInt(getValue('m-tipoDocumento')) || null,
        num_doc_destinatario: getValue('m-nroDocumento'),
        num_tel_destinatario: getValue('m-celular')
      }
    };

    // Campos adicionales según el tipo de empaque
    if (parseInt(getValue('m-tipoEmpaque')) === 2) {
      // Es sobre (folios)
      registro.cantidad_folios = parseInt(getValue('m-folios')) || null;
    }

    // Campo adicional según el tipo de entrega
    if (parseInt(getValue('m-tipoEntrega')) === 2) {
      // Es entrega a domicilio
      registro.direccion_destinatario = getValue('m-direccion');
    }

    // Campos adicionales para RUC (tipo documento 2)
    if (parseInt(getValue('m-tipoDocumento')) === 2) {
      registro.destinatario.razon_social = getValue('m-razonSocial');
      registro.destinatario.contacto = getValue('m-contacto');
      // Para RUC, usar razón social como nombre
      registro.destinatario.nombres = getValue('m-razonSocial');
      registro.destinatario.apellidos = ''; // Vacío para RUC
    }

    // Determinar el modo correcto
    let modoEnvio = 'masivo'; // Por defecto
    if (typeof mode !== 'undefined' && (mode === 'caja' || mode === 'sobre')) {
      modoEnvio = 'individual';
    }

    // Estructura principal del payload
    const formData = {
      modo: modoEnvio,
      origen: {
        sucursal_origen: parseInt(getValue('origen-sucursal')) || null
      },
      remitente: {
        nombre_remitente: getValue('remitente-nombre'),
        correo_remitente: getValue('remitente-email'),
        num_tel_remitente: getValue('remitente-telefono'),
        num_doc_remitente: getValue('remitente-numero-doc'),
        tipo_doc_remitente: parseInt(getValue('remitente-tipo-doc')) || null
      },
      registros: [registro]
    };

    console.log('Datos recolectados del formulario:', formData);
    return formData;
  }

  // Método para envíos masivos
  static collectMassiveFormData() {
    // Para envíos masivos, usar los datos del primer registro para remitente y origen
    const primerRegistro = window.registros && window.registros.length > 0 ? window.registros[0] : null;
    
    if (!primerRegistro) {
      throw new Error('No hay registros para procesar');
    }

    // Convertir registros al formato correcto
    const registrosFormateados = window.registros.map(envio => {
      const registro = {
        clave: envio.clave || '',
        valorEnvio: parseFloat(envio.valorEnvio) || 0,
        peso: parseFloat(envio.peso) || 0,
        alto: parseFloat(envio.alto) || 0,
        largo: parseFloat(envio.largo) || 0,
        ancho: parseFloat(envio.ancho) || 0,
        tarifa: 0, // Se calculará en el backend
        tipoEmpaqueId: parseInt(envio.tipoEmpaqueId) || null,
        tipoArticuloId: parseInt(envio.tipoArticuloId) || null,
        tipoEntregaId: parseInt(envio.tipoEntregaId) || null,
        estado_pago: "P",
        modalidadPago: envio.modalidadPago,
        destino: {
          sucursal_destino: parseInt(envio.destino?.sucursal_destino) || null
        },
        destinatario: {
          nombres: envio.destinatario?.nombres || '',
          apellidos: envio.destinatario?.apellidos || '',
          tipo_doc_destinatario: parseInt(envio.destinatario?.tipo_doc_destinatario) || null,
          num_doc_destinatario: envio.destinatario?.num_doc_destinatario || '',
          num_tel_destinatario: envio.destinatario?.num_tel_destinatario || ''
        }
      };

      // Campos condicionales
      if (parseInt(envio.tipoEmpaqueId) === 2) {
        registro.cantidad_folios = parseInt(envio.folios) || null;
      }

      if (parseInt(envio.tipoEntregaId) === 2) {
        registro.direccion_destinatario = envio.destino?.direccion || '';
      }

      if (parseInt(envio.destinatario?.tipo_doc_destinatario) === 2) {
        registro.destinatario.razon_social = envio.destinatario?.razon_social || '';
        registro.destinatario.contacto = envio.destinatario?.contacto || '';
        registro.destinatario.nombres = envio.destinatario?.razon_social || '';
        registro.destinatario.apellidos = '';
      }

      return registro;
    });

    const formData = {
      modo: 'masivo', // Los envíos masivos siempre son modo "masivo"
      origen: {
        sucursal_origen: parseInt(primerRegistro.origen?.sucursal_origen) || null
      },
      remitente: {
        nombre_remitente: primerRegistro.remitente?.nombre_remitente || '',
        correo_remitente: primerRegistro.remitente?.correo_remitente || '',
        num_tel_remitente: primerRegistro.remitente?.num_tel_remitente || '',
        num_doc_remitente: primerRegistro.remitente?.num_doc_remitente || '',
        tipo_doc_remitente: parseInt(primerRegistro.remitente?.tipo_doc_remitente) || null
      },
      registros: registrosFormateados
    };

    return formData;
  }

  // CORREGIDO: Mejor manejo de errores y múltiples formas de encontrar el texto
  static getModalidadPagoTexto(value) {
    if (!value) return 'No especificado';

    const radio = document.querySelector(`input[name="modalidad_pago"][value="${value}"]`);
    if (!radio) return value;

    // Buscar el texto en múltiples formas posibles
    const container = radio.closest('div') || radio.parentElement;
    
    // Intentar diferentes selectores para encontrar el texto
    const textElement = 
      container.querySelector('label[for="' + radio.id + '"]') ||  // Label específico
      container.querySelector('label') ||                          // Cualquier label
      container.querySelector('.payment-text') ||                 // Clase específica
      container.querySelector('span') ||                          // Span
      radio.nextElementSibling ||                                 // Elemento siguiente
      container;                                                  // Container mismo

    if (textElement && textElement.textContent) {
      const texto = textElement.textContent.trim();
      // Filtrar texto que no sea útil (como solo números o símbolos)
      return texto && texto !== value ? texto : value;
    }

    return value;
  }

  // Método para guardar registro en window.registros
  static guardarRegistro() {
    if (!this.validateEnvio()) {
      Utils.showModal({ message: 'Complete todos los campos visibles' });
      return;
    }

    const getValue = (id) => {
      const element = document.getElementById(id);
      return element ? element.value.trim() : '';
    };

    const getCheckedRadio = (name) => {
      const radio = document.querySelector(`input[name="${name}"]:checked`);
      return radio ? radio.value : '';
    };

    const modalidadPagoValue = getCheckedRadio('modalidad_pago');
    const modalidadPagoTexto = this.getModalidadPagoTexto(modalidadPagoValue);

    // Crear el registro en el formato correcto para window.registros
    const registro = {
      clave: Array.from(document.querySelectorAll('.pin-input')).map(i => i.value || '').join(''),
      valorEnvio: parseFloat(getValue('m-valorEnvio')) || 0,
      peso: parseFloat(getValue('m-peso')) || 0,
      alto: parseFloat(getValue('m-alto')) || 0,
      largo: parseFloat(getValue('m-largo')) || 0,
      ancho: parseFloat(getValue('m-ancho')) || 0,
      tipoEmpaqueId: parseInt(getValue('m-tipoEmpaque')) || null,
      tipoArticuloId: parseInt(getValue('m-tipoArticulo')) || null,
      tipoEntregaId: parseInt(getValue('m-tipoEntrega')) || null,
      modalidadPago: modalidadPagoValue,
      modalidadPagoTexto: modalidadPagoTexto, 
      
      folios: getValue('m-folios') ? parseInt(getValue('m-folios')) : null,
      
      tipoEntrega: this.getSelectText('m-tipoEntrega'),
      tipoEmpaque: this.getSelectText('m-tipoEmpaque'),
      tipoArticulo: this.getSelectText('m-tipoArticulo'),
      
      origen: {
        sucursal_origen: parseInt(getValue('origen-sucursal')) || null,
        departamento_origen: this.getSelectText('origen-departamento'), 
        provincia_origen: this.getSelectText('origen-provincia'),       
        distrito_origen: this.getSelectText('origen-distrito')         
      },
      
      destino: {
        sucursal_destino: parseInt(getValue('select-sucursal')) || null,
        departamento: this.getSelectText('select-departamento'),        
        provincia: this.getSelectText('select-provincia'),              
        distrito: this.getSelectText('select-distrito'),               
        direccion: getValue('m-direccion') || null
      },
      
      destinatario: {
        nombres: getValue('m-nombres'),
        apellidos: getValue('m-apellidos'),
        tipo_doc_destinatario: parseInt(getValue('m-tipoDocumento')) || null,
        num_doc_destinatario: getValue('m-nroDocumento'),
        num_tel_destinatario: getValue('m-celular'),
        razon_social: getValue('m-razonSocial'),
        contacto: getValue('m-contacto'),
        // Para compatibilidad con la tabla
        nombre_destinatario: this.getDestinatarioName()
      },
      
      remitente: {
        nombre_remitente: getValue('remitente-nombre'),
        correo_remitente: getValue('remitente-email'),
        num_tel_remitente: getValue('remitente-telefono'),
        num_doc_remitente: getValue('remitente-numero-doc'),
        tipo_doc_remitente: parseInt(getValue('remitente-tipo-doc')) || null
      }
    };

    if (editingIndex !== null) {
      window.registros[editingIndex] = registro;
      editingIndex = null;
    } else {
      window.registros.push(registro);
    }

    TableManager.renderTabla();
    FormManager.clearForm(false);
    FormManager.lockOrigen();
  }

  // Método para obtener texto de select
  static getSelectText(selectId) {
    const select = document.getElementById(selectId);
    return select?.selectedOptions[0]?.textContent?.trim() || '';
  }

  // Método para obtener nombre del destinatario
  static getDestinatarioName() {
    const tipoDoc = document.getElementById('m-tipoDocumento')?.value;
    if (tipoDoc === '2') {
      return document.getElementById('m-razonSocial')?.value || '';
    } else {
      const nombres = document.getElementById('m-nombres')?.value || '';
      const apellidos = document.getElementById('m-apellidos')?.value || '';
      return `${nombres} ${apellidos}`.trim();
    }
  }

  // Método principal para enviar datos
  static async enviarDatosResumen() {
    try {
      // Determinar si es envío individual o masivo
      const btnAdd = document.querySelector('.btn-agregar');
      const isIndividualShipment = btnAdd && window.getComputedStyle(btnAdd).display === 'none';
      
      // También verificar si el mode es 'caja' o 'sobre' (siempre individual)
      const isModeIndividual = typeof mode !== 'undefined' && (mode === 'caja' || mode === 'sobre');

      let datosParaEnviar;

      if (isIndividualShipment || isModeIndividual) {
        console.log('Procesando envío individual...');

        // Validar formulario antes de continuar
        if (!this.validateEnvio()) {
          Utils.showModal({ message: 'Complete todos los campos visibles antes de continuar.' });
          return;
        }

        // Usar el método corregido para envío individual
        datosParaEnviar = this.collectFormData();
      } else {
        // Envío masivo
        if (!window.registros || window.registros.length === 0) {
          Utils.showModal({ message: 'Agrega al menos un envío antes de continuar.' });
          return;
        }

        // Usar el método para envíos masivos
        datosParaEnviar = this.collectMassiveFormData();
      }

      console.log('Datos finales para enviar:', datosParaEnviar); // AGREGADO: Log para debugging

      // Crear form para envío
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = '/resumen_envio_prueba';
      form.style.display = 'none';

      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'payload';
      input.value = JSON.stringify(datosParaEnviar);
      form.appendChild(input);

      document.body.appendChild(form);
      form.submit();

    } catch (err) {
      console.error("Error en el envío:", err);
      Utils.showModal({ message: "Error al procesar el envío: " + err.message });
    }
  }

  // CORREGIDO: Validación mejorada de radio buttons
  static validateEnvio() {
    function isHidden(el) {
      while (el) {
        if (el.style && el.style.display === 'none') {
          return true;
        }
        el = el.parentElement;
      }
      return false;
    }

    const panels = document.querySelectorAll('.tabs-content .tab-panel');

    for (const panel of panels) {
      const selectAndTextInputs = panel.querySelectorAll('select, input[type="text"], input[type="number"]');

      for (const f of selectAndTextInputs) {
        if (f.id === 'm-descripcionArticulo') continue;
        if (isHidden(f)) continue;
        
        if (!f.value.trim()) {
          console.warn('Campo vacío encontrado:', f.id || f.name);
          return false;
        }
      }

      // CORREGIDO: Mejor validación de radio buttons
      const radioGroups = {};
      panel.querySelectorAll('input[type="radio"]').forEach(radio => {
        if (radio.name && !isHidden(radio)) {
          radioGroups[radio.name] = radioGroups[radio.name] || [];
          radioGroups[radio.name].push(radio);
        }
      });

      for (const [groupName, radios] of Object.entries(radioGroups)) {
        if (radios.length > 0 && !radios.some(r => r.checked)) {
          console.warn(`Grupo de radio "${groupName}" sin selección`);
          return false;
        }
      }
    }

    return true;
  }

  // Métodos auxiliares para compatibilidad
  // static startEdit(idx) {
  //   editingIndex = idx;
  //   this.fillFormData(window.registros[idx]);
  //   document.querySelectorAll('#seccion-origen select').forEach(el => el.disabled = true);
  //   const btnCancelEdit = document.querySelector('.btn-cancel-edit');
  //   if (btnCancelEdit) btnCancelEdit.style.display = 'inline-block';
  // }

  static cancelEdit() {
    editingIndex = null;
    FormManager.clearForm(true);
    TabManager.updateNextTabHint();
    const btnCancelEdit = document.querySelector('.btn-cancel-edit');
    if (btnCancelEdit) btnCancelEdit.style.display = 'none';
  }

  static fillFormData(r) {
    console.log('Llenando formulario con:', r);
    // TODO: Implementar llenado de formulario para edición
    // Esta función debería llenar todos los campos del formulario con los datos del registro
  }

  static limpiarCampos() {
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

  // Métodos legacy para compatibilidad
  static async continuarProceso() {
    return this.enviarDatosResumen();
  }

  static async enviarDatos() {
    return this.enviarDatosResumen();
  }

  static recolectarDatosEnvio() {
    // Método legacy - mantener por compatibilidad
    return this.collectFormData();
  }
}

// ===========================
// GESTIÓN DE TABLA
// ===========================
class TableManager {
static renderTabla() {
  const container = document.getElementById('tableContent');
  const totalEnvios = document.getElementById('totalEnvios');
  const pesoTotal = document.getElementById('pesoTotal');
  const valorTotal = document.getElementById('valorTotal');
  
  if (!container) return;

  if (window.registros.length === 0) {
    container.innerHTML = '<div class="empty-state"><p>No hay envíos registrados aún</p><p>Comienza agregando tu primer envío</p></div>';
    
    // Actualizar totales a cero
    if (totalEnvios) totalEnvios.textContent = '0';
    if (pesoTotal) pesoTotal.textContent = '0';
    if (valorTotal) valorTotal.textContent = '0.00';
    return;
  }

  let sumaPeso = 0;
  let sumaValor = 0;

  let html = '<div style="overflow-x: auto;"><table><thead><tr>' +
    '<th>#</th><th>Recepción</th><th>Destino</th><th>Paquete</th>' +
    '<th>Valor</th><th>Peso</th><th>Dimensiones</th>' +
    '<th>Destinatario</th><th>Modalidad pago</th><th>Clave</th><th>Acciones</th>' +
    '</tr></thead><tbody>';

  window.registros.forEach((r, i) => {
    // Extraer valores seguros
    const tipoEntrega = r.tipoEntrega || 'N/A';
    const departamento = r.destino?.departamento || 'N/A';
    const provincia = r.destino?.provincia || 'N/A';
    const distrito = r.destino?.distrito || 'N/A';
    const valorEnvio = parseFloat(r.valorEnvio) || 0;
    const peso = parseFloat(r.peso) || 0;
    const largo = r.largo || 0;
    const ancho = r.ancho || 0;
    const alto = r.alto || 0;
    const nombreDestinatario = r.destinatario?.nombre_destinatario || 'N/A';
    const modalidadPago = r.modalidadPagoTexto || 'N/A';
    const clave = r.clave || '';

    // Acumular totales
    sumaPeso += peso;
    sumaValor += valorEnvio;

    // Determinar el tipo de paquete
    let tipoPaquete = '';
    if (parseInt(r.tipoEmpaqueId) === 2) {
      tipoPaquete = `${r.folios || 0} folios`;
    } else {
      tipoPaquete = `${r.tipoEmpaque || 'Paquete'} - ${r.tipoArticulo || 'Artículo'}`;
    }

    html += `<tr>` +
      `<td>${i + 1}</td>` +
      `<td>${tipoEntrega}</td>` +
      `<td>` +
        `<div>${distrito}</div>` +
        `<small>${provincia}, ${departamento}</small>` +
      `</td>` +
      `<td>` +
        `<div>${tipoPaquete}</div>` +
        `<small>${r.descripcion || ''}</small>` +
      `</td>` +
      `<td><strong>S/ ${valorEnvio.toFixed(2)}</strong></td>` +
      `<td>${peso} kg</td>` +
      `<td><small>${largo}x${ancho}x${alto} cm</small></td>` +
      `<td>` +
        `<div><strong>${nombreDestinatario}</strong></div>` +
        `<small>${r.destinatario?.tipo_doc_destinatario === 2 ? 'RUC' : 'DNI'}: ${r.destinatario?.num_doc_destinatario || ''}</small>` +
      `</td>` +
      `<td>${modalidadPago}</td>` +
      `<td>${clave}</td>` +
      `<td>` +
      ` <div class="btn-actions">` +
      `<button class="btn-small btn-edit" data-index="${i}" title="Editar"><i class="fa fa-edit"></i></button>` +
      `<button class="btn-small btn-delete" data-index="${i}" title="Eliminar"><i class="fa fa-trash"></i></button>` +
      `</div>` +
      `</td></tr>`;
  });

  html += '</tbody></table></div>';
  container.innerHTML = html;

  // Actualizar totales
  if (totalEnvios) totalEnvios.textContent = window.registros.length;
  if (pesoTotal) pesoTotal.textContent = sumaPeso.toFixed(2);
  if (valorTotal) valorTotal.textContent = sumaValor.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  // Adjuntar eventos de la tabla
  this.attachTableActions();
}


  static attachTableActions() {
    document.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = +btn.dataset.index;
        Utils.showModal({
          message: '¿Eliminar este envío?',
          onConfirm: () => {
            window.registros.splice(idx, 1);
            this.renderTabla();
          }
        });
      });
    });

    document.querySelectorAll('.btn-edit').forEach(btn => {
      btn.addEventListener('click', () => {
        const idx = +btn.dataset.index;
        const warning = () => ShippingManager.startEdit(idx);

        if (window.registros.length > 1) {
          Utils.showWarning('Al editar se eliminarán registros con origen diferente. ¿Continuar?', warning);
        } else {
          warning();
        }
      });
    });
  }


}

// ===========================
// GESTIÓN DE EXPORT
// ===========================
class ExportManager {
static exportXLSX() {
  if (!window.registros || window.registros.length === 0) {
    return Utils.showModal({ message: 'No hay envíos para exportar.' });
  }

  const data = window.registros.map(e => ({
    'Modalidad de Pago': e.modalidadPago || '',
    'Tipo de Entrega': e.tipoEntrega || '',
    'Depto. Destino': e.destino?.departamento || '',
    'Provincia Destino': e.destino?.provincia || '',
    'Distrito Destino': e.destino?.distrito || '',
    'Tipo de Empaque': e.tipoEmpaque || '',
    'Tipo de Contenido': e.tipoArticulo || '',
    '# Folios': e.folios || '',
    'Valor (S/)': e.valorEnvio || 0,
    'Peso (kg)': e.peso || 0,
    'Largo (cm)': e.largo || 0,
    'Ancho (cm)': e.ancho || 0,
    'Alto (cm)': e.alto || 0,
    'Destinatario': e.destinatario?.nombre_destinatario || '',
    'Clave de seguridad': e.clave || ''
  }));

  // Si XLSX está disponible globalmente
  if (typeof XLSX !== 'undefined') {
    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Envíos Masivos');
    XLSX.writeFile(wb, 'envios_masivos.xlsx');
  } else {
    console.error('XLSX library not available');
    Utils.showModal({ message: 'Error: Biblioteca de exportación no disponible.' });
  }
}
}

// ===========================
// GESTIÓN DE CAMPOS DINÁMICOS
// ===========================
class FieldManager {
  static mostrarCamposDestino() {
    const tipo = document.getElementById('m-tipoEntrega')?.value;
    const grupoDir = document.getElementById('grupo-direccion');

    if (grupoDir) {
      grupoDir.style.display = (tipo === '2') ? 'flex' : 'none';
    }
  }

  static toggleFolios() {
    const tipo = document.getElementById('m-tipoEmpaque')?.value;
    const grupoFolios = document.getElementById('grupo-folios');

    if (grupoFolios) {
      grupoFolios.style.display = (tipo === '2') ? 'flex' : 'none';
      const input = grupoFolios.querySelector('input');
      if (input) input.setAttribute('required', '');
    }
  }

  static toggleArticulos() {
    const tipo = document.getElementById('m-tipoEmpaque')?.value;
    const grupoArticulos = document.getElementById('grupo-articulos');

    if (grupoArticulos) {
      grupoArticulos.style.display = (tipo === '1') ? 'flex' : 'none';
      const select = grupoArticulos.querySelector('select');
      if (select) select.setAttribute('required', '');
    }
  }

  static mostrarCamposReceptor() {
    const tipo = document.getElementById('m-tipoDocumento')?.value;
    console.log(tipo)
    const elementos = {
      camposRazon: document.getElementById('campo-razon-ruc'),
      camposContacto: document.getElementById('campo-contacto-ruc'),
      camposNombres: document.getElementById('campos-nombres'),
      camposApellidos: document.getElementById('campos-apellidos'),
      razon: document.getElementById('m-razonSocial'),
      contacto: document.getElementById('m-contacto'),
      nombres: document.getElementById('m-nombres'),
      apellidos: document.getElementById('m-apellidos')
    };

    // Ocultar todos primero
    Object.values(elementos).forEach(el => {
      if (el && el.style) el.style.display = 'none';
      if (el && el.required !== undefined) el.required = false;
    });

    if (tipo == '2') {
      // RUC - mostrar razón social y contacto
      if (elementos.camposRazon) {
        elementos.camposRazon.style.display = 'flex';
        elementos.razon.style.display = 'flex';
      }
      if (elementos.camposContacto) {
        elementos.camposContacto.style.display = 'flex';
        elementos.contacto.style.display = 'flex';
      }
      if (elementos.razon) elementos.razon.required = true;
      if (elementos.contacto) elementos.contacto.required = true;
    } else if (tipo && tipo !== '') {
      // Otros documentos - mostrar nombres y apellidos
      if (elementos.camposNombres) {
        elementos.camposNombres.style.display = 'flex';
        elementos.nombres.style.display = 'flex';
        elementos.nombres.required = true;
      }
      if (elementos.camposApellidos) {
        elementos.camposApellidos.style.display = 'flex';
        elementos.apellidos.style.display = 'flex';
        elementos.apellidos.required = true;
      }
    }
  }
}

// ===========================
// INICIALIZACIÓN Y EVENTOS
// ===========================
class AppInitializer {
  static reloadConfirmed = false;
  static init() {
    this.setupModeSpecificBehavior();
    this.setupEventListeners();
    this.initializeComponents();
    this.setupButtonEvents();
    this.setupBeforeUnloadWarning();
    // FormManager.limpiarAlRecargar();
  }

  static setupModeSpecificBehavior() {
    if (typeof mode !== 'undefined' && (mode === 'caja' || mode === 'sobre')) {
      const tipoEmpaque = document.getElementById('m-tipoEmpaque');
      if (tipoEmpaque) {
        tipoEmpaque.value = (mode === 'sobre' ? '2' : '1');
        tipoEmpaque.disabled = true;

        if (mode === 'sobre') {
          FieldManager.toggleFolios();
          const grupoArticulos = document.getElementById('grupo-articulos');
          if (grupoArticulos) grupoArticulos.style.display = 'none';
        } else {
          FieldManager.toggleArticulos();
          const grupoFolios = document.getElementById('grupo-folios');
          if (grupoFolios) grupoFolios.style.display = 'none';
        }

        const tablaEnvios = document.querySelector('.tabla-envios');
        const btnAgregar = document.querySelector('.btn-agregar');
        if (tablaEnvios) tablaEnvios.style.display = 'none';
        if (btnAgregar) btnAgregar.style.display = 'none';
      }
    }
  }
  static hasFilledAll() {
    const masiva = this.hasFilledFields('seccion-masiva');
    const remitente = this.hasFilledFields('seccion_remitente');
    const origen = this.hasFilledFields('seccion-origen');
    return masiva || remitente || origen;
  }

  static hasFilledFields(seccion) {
    const seccionMasiva = document.getElementById(seccion);
    if (!seccionMasiva) return false;

    const fields = seccionMasiva.querySelectorAll('input, select, textarea');

    return Array.from(fields).some(field => {
      if (field.type === 'radio') {
        return field.checked;
      }
      return field.value && field.value.trim() !== '';
    });
  }


  static setupBeforeUnloadWarning() {
  // Variable para controlar si estamos en proceso de continuar
  let continuandoProceso = false;

  // Para TODOS los intentos de salir/recargar (incluyendo botón del navegador)
  window.addEventListener('beforeunload', (e) => {
    if (this.reloadConfirmed || continuandoProceso) {
      return;
    }

    if (this.hasFilledAll()) {
      const message = '¿Estás seguro de que quieres salir? Perderás todo el progreso actual.';
      e.preventDefault();
      e.returnValue = message;
      return message;
    }
  });

  // Detectar teclas de recarga (F5 o Ctrl+R) - mantener separado
  document.addEventListener('keydown', (e) => {
    if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
      if (this.hasFilledAll()) {
        e.preventDefault();
        this.showReloadConfirmation();
      }
    }
  });

  // Agregar listener al botón continuar para marcar que estamos continuando
  const btnContinuar = document.getElementById('btn-continuar');
  if (btnContinuar) {
    btnContinuar.addEventListener('click', () => {
      continuandoProceso = true;
    });
  }
}
  

  static showReloadConfirmation() {
    Utils.showModal({
      message: '¿Estás seguro de que quieres recargar la página? Perderás todo el progreso actual.',
      onConfirm: () => {
        // Si confirma, recargar la página
        this.reloadConfirmed = true;
        window.location.reload();
      },
      onCancel: () => {
        // No hacer nada, mantener la página
        console.log('Recarga cancelada por el usuario');
      }
    });
  }

  static setupEventListeners() {
    // Listeners de campos dinámicos
    const tipoEntrega = document.getElementById('m-tipoEntrega');
    if (tipoEntrega) {
      tipoEntrega.addEventListener('change', FieldManager.mostrarCamposDestino);
    }

    const tipoEmpaque = document.getElementById('m-tipoEmpaque');
    if (tipoEmpaque) {
      tipoEmpaque.addEventListener('change', () => {
        FieldManager.toggleFolios();
        FieldManager.toggleArticulos();
      });
    }

    const tipoDocumento = document.getElementById('m-tipoDocumento');
    if (tipoDocumento) {
      tipoDocumento.addEventListener('change', FieldManager.mostrarCamposReceptor);
    }
  }

  static initializeComponents() {
    TabManager.initTabs();
    TabManager.setupTabHints();
    FormManager.setupValidationListeners();
    LocationManager.setupLocationListeners();

    // Inicializar campos dinámicos
    FieldManager.mostrarCamposDestino();
    FieldManager.toggleFolios();
    FieldManager.toggleArticulos();
    FieldManager.mostrarCamposReceptor();

    // Renderizar tabla inicial
    TableManager.renderTabla();
  }

static setupButtonEvents() {
  // Botón agregar
  const btnAdd = document.querySelector('.btn-agregar');
  if (btnAdd) {
    btnAdd.addEventListener('click', e => {
      e.preventDefault();
      if (!ShippingManager.validateEnvio()) {
        Utils.showModal({ message: 'Complete todos los campos visibles' });
        return;
      }
      Utils.showModal({
        message: '¿Agregar este envío?',
        onConfirm: () => ShippingManager.guardarRegistro()
      });
    });
  }

  // Botón limpiar
  const btnLimpiar = document.querySelector('.btn-limpiar');
  if (btnLimpiar) {
    btnLimpiar.addEventListener('click', e => {
      e.preventDefault();

      const fields = Array.from(
        document.querySelectorAll('#seccion-masiva input, #seccion-masiva select, #seccion-masiva textarea')
      );

      const anyFilled = fields.some(f => f.value && f.value.trim() !== '');

      if (!anyFilled) {
        Utils.showModal({ message: 'No hay campos para limpiar.' });
      } else {
        ShippingManager.cancelEdit();
      }
    });
  }

  // Botón limpiar todos
  const btnLimpiarTodos = document.querySelector('.btn-limpiar-todos');
  if (btnLimpiarTodos) {
    btnLimpiarTodos.addEventListener('click', () => {
      if (window.registros.length === 0) {
        Utils.showModal({ message: 'No hay registros para eliminar.' });
      } else {
        Utils.showModal({
          message: '¿Eliminar todos los registros?',
          onConfirm: () => {
            window.registros = [];
            TableManager.renderTabla();
            FormManager.unlockOrigen();
          }
        });
      }
    });
  }

  // Botón exportar
  const btnExportar = document.querySelector('.btn-exportar');
  if (btnExportar) {
    btnExportar.addEventListener('click', () => {
      if (window.registros.length === 0) {
        Utils.showModal({ message: 'No hay registros para exportar.' });
      } else {
        ExportManager.exportXLSX();
      }
    });
  }

  // Botón continuar
  const btnContinuar = document.getElementById('btn-continuar');
  if (btnContinuar) {
    btnContinuar.addEventListener('click', async (e) => {
      e.preventDefault();
      
      // Validación existente
      const selectsOrigen = document.querySelectorAll('#seccion-origen select');
      const camposRemitente = document.querySelectorAll('#seccion_remitente select, #seccion_remitente input');

      function destacarCampo(element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        element.style.transition = 'transform 0.3s ease';
        element.style.transform = 'scale(1.05)';
        setTimeout(() => {
          element.style.transform = '';
        }, 900);
      }

      let primerInvalido = null;

      for (const select of selectsOrigen) {
        if (select.value === '') {
          primerInvalido = select;
          break;
        }
      }

      if (!primerInvalido) {
        for (const campo of camposRemitente) {
          if (!campo.matches(':user-valid')) {
            primerInvalido = campo;
            break;
          }
        }
      }

      if (!primerInvalido) {
        // CONFIRMACIÓN AGREGADA - Mostrar modal de confirmación
        Utils.showModal({
          message: '¿Desea continuar con el proceso de envío?',
          onConfirm: async () => {
            // Marcar que estamos continuando para evitar beforeunload
            AppInitializer.reloadConfirmed = true;
            await ShippingManager.enviarDatosResumen();
          }
        });
      } else {
        setTimeout(() => {
          destacarCampo(primerInvalido);
          setTimeout(() => {
            Utils.showModal({ message: 'Complete todos los campos necesarios.' });
          }, 1600)
        }, 500)
      }
    });
  }

  // Botón cancelar edición
  const btnCancelEdit = document.querySelector('.btn-cancel-edit');
  if (btnCancelEdit) {
    btnCancelEdit.style.display = 'none';
    btnCancelEdit.addEventListener('click', () => {
      ShippingManager.cancelEdit();
    });
  }
}


}

// ===========================
// FUNCIONES LEGACY (para compatibilidad)
// ===========================

// Funciones globales mantenidas para compatibilidad con HTML existente
function mostrarCamposDestino() {
  FieldManager.mostrarCamposDestino();
}

function toggleFolios() {
  FieldManager.toggleFolios();
}

function toggleArticulos() {
  FieldManager.toggleArticulos();
}

function mostrarCamposReceptor() {
  FieldManager.mostrarCamposReceptor();
}

function cargarProvincias(depOrigen) {
  return LocationManager.cargarProvincias(depOrigen);
}

function cargarDistritos(provOrigen) {
  return LocationManager.cargarDistritos(provOrigen);
}

function cargarSucursales(dep_origen, prov_origen, dist_origen) {
  return LocationManager.cargarSucursales(dep_origen, prov_origen, dist_origen);
}

function cargarDeparDestino(id_origen) {
  return LocationManager.cargarDeparDestino(id_origen);
}

function cargarProvDestino(dep_origen, codigo) {
  return LocationManager.cargarProvDestino(dep_origen, codigo);
}

function cargarDistDestino(prov, codigo) {
  return LocationManager.cargarDistDestino(prov, codigo);
}

function cargarSucDestino(dep_destino, prov_destino, dist_destino, origen) {
  return LocationManager.cargarSucDestino(dep_destino, prov_destino, dist_destino, origen);
}

function cargarRecepcion(modalidad) {
  return LocationManager.cargarRecepcion(modalidad);
}

function renderTabla() {
  TableManager.renderTabla();
}

function exportXLSX() {
  ExportManager.exportXLSX();
}

function mostrarModalConfirmacion() {
  if (!Validator.validarRequeridos()) {
    const modalValidacion = document.getElementById('modalValidacion');
    if (modalValidacion) modalValidacion.style.display = 'flex';
    return;
  }

  const modalConfirmacion = document.getElementById('modalConfirmacion');
  if (modalConfirmacion) modalConfirmacion.style.display = 'flex';

  const confirmarBtn = document.getElementById('confirmarBtn');
  if (confirmarBtn) {
    confirmarBtn.replaceWith(confirmarBtn.cloneNode(true));
    document.getElementById('confirmarBtn').addEventListener('click', () => {
      Utils.cerrarModal();
      agregarEnvio();
    });
  }
}

function agregarEnvio() {
  // Implementación de agregar envío usando las nuevas clases
  const envio = ShippingManager.collectFormData();

  // Agregar a LISTA_ENVIOS para compatibilidad
  LISTA_ENVIOS.push(envio);

  // También agregar a registros
  if (!window.registros) window.registros = [];
  window.registros.push(envio);

  TableManager.actualizarTabla();
  ShippingManager.limpiarCampos();

  console.log("Envío agregado:", envio);
}

function editarEnvio(index) {
  ShippingManager.startEdit(index);
}

function eliminarEnvio(index) {
  Utils.showModal({
    message: '¿Eliminar este envío?',
    onConfirm: () => {
      // Eliminar de ambas listas para compatibilidad
      if (LISTA_ENVIOS[index]) LISTA_ENVIOS.splice(index, 1);
      if (window.registros[index]) window.registros.splice(index, 1);

      TableManager.actualizarTabla();
      TableManager.renderTabla();
    }
  });
}

function limpiarFormularioMasivo() {
  FormManager.clearForm();
}

function cerrarModal() {
  Utils.cerrarModal();
}

function eliminarTodo() {
  localStorage.removeItem(CONFIG.STORAGE_KEY);
  LISTA_ENVIOS = [];
  window.registros = [];

  TableManager.actualizarTabla();
  TableManager.renderTabla();

  editIndex = -1;
  const btn = document.getElementById('btn-guardar');
  if (btn) btn.textContent = 'Guardar envío';

  Utils.cerrarModal();
}

function mostrarModalEliminarTodo() {
  Utils.showModal({
    message: '¿Deseas ELIMINAR todos los envíos?',
    onConfirm: eliminarTodo
  });
}

function verificarAceptar() {
  const btnAceptar = document.getElementById('btn-agregar');
  if (btnAceptar) {
    const estilo = window.getComputedStyle(btnAceptar);
    if (estilo.display === 'none') {
      ShippingManager.guardarRegistro();
    } else {
      console.log('El elemento no está oculto');
    }
  }
}

function recolectarDatosEnvio() {
  return ShippingManager.recolectarDatosEnvio();
}

// ===========================
// INICIALIZACIÓN DE LA APLICACIÓN
// ===========================

// Event listener principal para inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
  console.log('Inicializando aplicación de envíos...');

  try {
    AppInitializer.init();
    console.log('Aplicación inicializada correctamente');
  } catch (error) {
    console.error('Error al inicializar la aplicación:', error);
  }
});

// Exportar clases principales para uso externo si es necesario
window.ShippingApp = {
  CONFIG,
  Utils,
  Validator,
  FormManager,
  TabManager,
  LocationManager,
  ShippingManager,
  TableManager,
  ExportManager,
  FieldManager,
  AppInitializer
};