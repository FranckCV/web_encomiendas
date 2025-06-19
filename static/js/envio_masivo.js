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
          const hiddenField = document.getElementById('destino-sucursal-id');
          if (hiddenField) hiddenField.value = pin;
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
  static collectFormData() {
    // Función auxiliar para obtener valores seguros
    const getValue = (id) => {
      const element = document.getElementById(id);
      return element ? element.value.trim() : '';
    };

    const getSelectText = (id) => {
      const select = document.getElementById(id);
      return select?.selectedOptions[0]?.textContent?.trim() || '';
    };

    const getCheckedRadio = (name) => {
      const radio = document.querySelector(`input[name="${name}"]:checked`);
      return radio ? radio.value : '';
    };

    // Recolectar datos con validación
    const formData = {
      modo: typeof mode !== 'undefined' ? mode : null,
      remitente: {
        tipo_doc_remitente: getValue('remitente-tipo-doc'),
        num_doc_remitente: getValue('remitente-numero-doc'),
        num_tel_remitente: getValue('remitente-telefono'),
        nombre_remitente: getValue('remitente-nombre'),
        correo_remitente: getValue('remitente-email'),
      },
      origen: {
        departamento_origen: getValue('origen-departamento'),
        provincia_origen: getValue('origen-provincia'),
        distrito_origen: getValue('origen-distrito'),
        sucursal_origen: getValue('origen-sucursal')
      },
      tipoEntrega: getSelectText('m-tipoEntrega'),
      tipoEntregaId: getValue('m-tipoEntrega'),
      destino: {
        departamento: getValue('select-departamento'),
        provincia: getValue('select-provincia'),
        distrito: getValue('select-distrito'),
        sucursal_destino: getValue('select-sucursal'),
        direccion: getValue('m-direccion') // Agregar dirección si es domicilio
      },
      tipoEmpaque: getSelectText('m-tipoEmpaque'),
      tipoEmpaqueId: getValue('m-tipoEmpaque'),
      tipoArticulo: getSelectText('m-tipoArticulo'),
      tipoArticuloId: getValue('m-tipoArticulo'),
      folios: getValue('m-folios') || null,
      valorEnvio: parseFloat(getValue('m-valorEnvio')) || 0,
      peso: parseFloat(getValue('m-peso')) || 0,
      largo: parseFloat(getValue('m-largo')) || 0,
      ancho: parseFloat(getValue('m-ancho')) || 0,
      alto: parseFloat(getValue('m-alto')) || 0,
      descripcion: getValue('m-descripcionArticulo'),
      destinatario: {
        tipo_doc_destinatario: getValue('m-tipoDocumento'),
        num_doc_destinatario: getValue('m-nroDocumento'),
        num_tel_destinatario: getValue('m-celular'),
        nombre_destinatario: this.getDestinatarioName(),
        razon_social: getValue('m-razonSocial'),
        contacto: getValue('m-contacto'),
        nombres: getValue('m-nombres'),
        apellidos: getValue('m-apellidos')
      },
      modalidadPago: getCheckedRadio('modalidad_pago'),
      clave: Array.from(document.querySelectorAll('.pin-input')).map(i => i.value || '').join('')
    };

    // Validar que los campos críticos no estén vacíos
    const requiredFields = [
      'tipoEntregaId', 'tipoEmpaqueId', 'valorEnvio', 'peso',
      'largo', 'ancho', 'alto', 'modalidadPago'
    ];

    for (let field of requiredFields) {
      if (!formData[field] && formData[field] !== 0) {
        console.warn(`Campo requerido vacío: ${field}`);
      }
    }

    console.log('Datos recolectados del formulario:', formData);
    return formData;
  }

  static getSelectText(selectId) {
    const select = document.getElementById(selectId);
    return select?.selectedOptions[0]?.textContent || '';
  }

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

  static recolectarDatosEnvio() {
    return {
      tipo_documento_origen: document.getElementById('remitente-tipo-doc')?.value || null,
      dni_origen: document.getElementById('remitente-numero-doc')?.value.trim(),
      cel_origen: document.getElementById('remitente-telefono')?.value.trim(),
      nombre_remitente: document.getElementById('remitente-nombre')?.value.trim(),
      email: document.getElementById('remitente-email')?.value.trim(),
      id_origen: document.getElementById('origen-sucursal-id')?.value,
      tipo_recepcion: document.getElementById('m-tipoEntrega')?.value || null,
      cod_seguridad: document.getElementById('remitente-codigo')?.value.trim(),
      id_destino: document.getElementById('destino-sucursal-id')?.value || null,
      id_empaque: document.getElementById('m-tipoEmpaque')?.value,
      valor_paquete: document.getElementById('m-valorEnvio')?.value,
      peso: document.getElementById('m-peso')?.value,
      largo: document.getElementById('m-largo')?.value,
      ancho: document.getElementById('m-ancho')?.value,
      alto: document.getElementById('m-alto')?.value,
      descripcion: document.getElementById('m-descripcionArticulo')?.value.trim(),
      tipo_documento_destino: document.getElementById('m-tipoDocumento')?.value,
      dni_destino: document.getElementById('m-nroDocumento')?.value.trim(),
      cel_destino: document.getElementById('m-celular')?.value.trim(),
      nombre_destinatario: this.getDestinatarioName(),
      contacto_destino: document.getElementById('m-contacto')?.value.trim(),
      distrito_origen: document.getElementById('origen-distrito')?.value,
      distrito_destino_sucursal: document.getElementById('select-distrito')?.value,
      direccion_destino: document.getElementById('m-direccion')?.value.trim(),
      folios: document.getElementById('m-folios')?.value ?
        parseInt(document.getElementById('m-folios').value) : null,
      tipo_articulo: document.getElementById('m-tipoArticulo')?.value,
    };
  }

  static guardarRegistro() {
    if (!this.validateEnvio()) {
      Utils.showModal({ message: 'Complete todos los campos visibles' });
      return;
    }

    const envio = this.collectFormData();

    if (editingIndex !== null) {
      window.registros[editingIndex] = envio;
      editingIndex = null;
    } else {
      window.registros.push(envio);
    }

    TableManager.renderTabla();
    FormManager.clearForm(false);
    FormManager.lockOrigen();
  }


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
    console.log('Total de paneles:', panels.length);

    for (const panel of panels) {
      console.group(`Panel: ${panel.id}`);

      const selectAndTextInputs = panel.querySelectorAll('select, input[type="text"], input[type="number"]');
      console.log(`Campos encontrados: ${selectAndTextInputs.length}`);

      const fieldDetails = [];

      for (const f of selectAndTextInputs) {
        if (f.id === 'm-descripcionArticulo') continue;
        if (isHidden(f)) continue;
        const fieldInfo = {
          id: f.id || f.name,
          type: f.tagName.toLowerCase() === 'select' ? 'select' : f.type,
          value: f.value.trim(),
          valid: !!f.value.trim()
        };

        fieldDetails.push(fieldInfo);

        if (!fieldInfo.valid) {
          console.warn(`Campo inválido: ${fieldInfo.id}`);
          console.log('Detalles del campo:', fieldInfo);
          console.groupEnd();
          return false;
        }
      }

      console.log('Detalles de campos:', fieldDetails);

      const requiredRadios = Array.from(
        panel.querySelectorAll('input[type="radio"][required]')
      );

      const radioGroups = [...new Set(requiredRadios.map(r => r.name))];

      console.log('Grupos de Radio Requeridos:', radioGroups);

      for (const name of radioGroups) {
        const grupo = panel.querySelectorAll(`input[name="${name}"]`);

        const radioGroupInfo = {
          name: name,
          totalRadios: grupo.length,
          checkedRadios: Array.from(grupo).filter(r => r.checked),
          isValid: Array.from(grupo).some(r => r.checked)
        };

        console.log('Grupo de Radio:', radioGroupInfo);

        if (grupo.length > 0 && !radioGroupInfo.isValid) {
          console.warn(`Grupo de Radio "${name}" sin selección`);
          console.groupEnd();
          return false;
        }
      }

      console.log('Validación de panel: ÉXITO');
      console.groupEnd();
    }

    return true;
  }

  static startEdit(idx) {
    editingIndex = idx;
    this.fillFormData(window.registros[idx]);
    document.querySelectorAll('#seccion-origen select').forEach(el => el.disabled = true);
    const btnCancelEdit = document.querySelector('.btn-cancel-edit');
    if (btnCancelEdit) btnCancelEdit.style.display = 'inline-block';
  }

  static cancelEdit() {
    editingIndex = null;
    FormManager.clearForm(true);
    TabManager.updateNextTabHint();
    const btnCancelEdit = document.querySelector('.btn-cancel-edit');
    if (btnCancelEdit) btnCancelEdit.style.display = 'none';
  }

  static fillFormData(r) {
    // Implementar llenado de formulario basado en los datos del registro
    // Esta función necesitaría ser adaptada según la estructura exacta de tus datos
    console.log('Llenando formulario con:', r);
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

  static async enviarDatosResumen() {
    try {
      // Si es envío individual, recolectar datos del formulario actual
      const btnAdd = document.querySelector('.btn-agregar');
      const isIndividualShipment = btnAdd && window.getComputedStyle(btnAdd).display === 'none';

      let datosParaEnviar;

      if (isIndividualShipment) {
        console.log('Procesando envío individual...');

        // Validar formulario antes de continuar
        if (!this.validateEnvio()) {
          Utils.showModal({ message: 'Complete todos los campos visibles antes de continuar.' });
          return;
        }

        // Recoger datos del formulario actual
        const envioIndividual = this.collectFormData();
        datosParaEnviar = {
          envios: [envioIndividual],
          remitente: envioIndividual.remitente,
          modalidad_pago: envioIndividual.modalidadPago,
          tipo_envio: 'individual'
        };
      } else {
        // Envío masivo - usar registros existentes
        if (!window.registros || window.registros.length === 0) {
          Utils.showModal({ message: 'Agrega al menos un envío antes de continuar.' });
          return;
        }

        datosParaEnviar = {
          envios: window.registros,
          remitente: window.registros[0]?.remitente || {},
          modalidad_pago: window.registros[0]?.modalidadPago || '',
          tipo_envio: 'masivo'
        };
      }
      // Crear un form "invisible"
      const form = document.createElement('form');
      form.method = 'POST';
      form.action = '/resumen_envio_prueba';
      form.style.display = 'none';

      // Meter el JSON en un input oculto
      const input = document.createElement('input');
      input.type = 'hidden';
      input.name = 'payload';
      input.value = JSON.stringify(datosParaEnviar);
      form.appendChild(input);

      document.body.appendChild(form);

      // Enviar el form → navega a /resumen_envio_prueba
      form.submit();
    } catch (err) {
      console.error("Error en el envío:", err);
      Utils.showModal({ message: "Error al procesar el envío: " + err.message });
    }
  }

  // Mantener el método anterior para compatibilidad, pero que use el nuevo
  static async continuarProceso() {
    return this.enviarDatosResumen();
  }

  static async enviarDatos() {
    return this.enviarDatosResumen();
  }
}
// ===========================
// GESTIÓN DE TABLA
// ===========================
class TableManager {
  static renderTabla() {
    const container = document.getElementById('tableContent');
    if (!container) return;

    if (window.registros.length === 0) {
      container.innerHTML = '<div class="empty-state"><p>No hay envíos registrados aún</p><p>Comienza agregando tu primer envío</p></div>';
      return;
    }

    let html = '<table><thead><tr>' +
      '<th>#</th><th>Recepción</th><th>Destino</th><th>Paquete</th>' +
      '<th>Valor</th><th>Peso</th><th>Dimensiones</th>' +
      '<th>Destinatario</th><th>Modalidad pago</th><th>Clave</th><th>Acciones</th>' +
      '</tr></thead><tbody>';

    window.registros.forEach((r, i) => {
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

  static actualizarTabla() {
    const tableContent = document.getElementById('tableContent');
    const totalEnvios = document.getElementById('totalEnvios');
    const pesoTotal = document.getElementById('pesoTotal');
    const valorTotal = document.getElementById('valorTotal');

    if (!tableContent) return;

    const stored = localStorage.getItem(CONFIG.STORAGE_KEY);
    const envios = stored ? JSON.parse(stored) : [];

    if (envios.length === 0) {
      tableContent.innerHTML = `
        <div class="empty-state">
          <p>No hay envíos registrados aún</p>
          <p>Comienza agregando tu primer envío</p>
        </div>
      `;
      if (totalEnvios) totalEnvios.textContent = '0';
      if (pesoTotal) pesoTotal.textContent = '0';
      if (valorTotal) valorTotal.textContent = '0.00';
      return;
    }

    let sumaPeso = 0;
    let sumaValor = 0;

    let html = `
      <div style="overflow-x: auto;">
        <table>
          <thead>
            <tr>
              <th>#</th><th>Tipo</th><th>Destinatario</th><th>Destino</th>
              <th>Descripción</th><th>Dimensiones</th><th>Peso</th><th>Valor</th><th>Acciones</th>
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

      html += `
        <tr>
          <td>${index + 1}</td>
          <td><span class="badge">${destino.tipoEntregaNombre}</span></td>
          <td>
            <div><strong>${nombreDest}</strong></div>
            <small>${destinatario.tipoDocumentoNombre || ''}: ${destinatario.nroDocumento || ''}</small>
          </td>
          <td>
            <div>${destino.distrito || ''}</div>
            <small>${destino.provincia || ''}, ${destino.departamento || ''}</small>
          </td>
          <td>
            <div>${paquete.descripcion || ''}</div>
            <small>${paquete.contenidoPaqueteNombre || ''} - ${paquete.tipoEmpaqueNombre || ''}</small>
          </td>
          <td><small>${paquete.largo || 0}x${paquete.ancho || 0}x${paquete.alto || 0} cm</small></td>
          <td>${paquete.peso || 0} kg</td>
          <td><strong>S/ ${(parseFloat(paquete.valorEnvio) || 0).toFixed(2)}</strong></td>
          <td>
            <div class="btn-actions">
              <button class="btn-small btn-editar" onclick="editarEnvio(${index})"><i class="fa fa-edit"></i></button>
              <button class="btn-small btn-eliminar" onclick="eliminarEnvio(${index})"><i class="fa fa-trash"></i></button>
            </div>
          </td>
        </tr>
      `;
    });

    html += `</tbody></table></div>`;
    tableContent.innerHTML = html;

    if (totalEnvios) totalEnvios.textContent = envios.length;
    if (pesoTotal) pesoTotal.textContent = sumaPeso.toFixed(2);
    if (valorTotal) valorTotal.textContent = sumaValor.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
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
      'Destinatario': e.destinatario.nombre_destinatario,
      'Clave de seguridad': e.clave
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
      if (elementos.camposRazon) elementos.camposRazon.style.display = 'flex';
      if (elementos.camposContacto) elementos.camposContacto.style.display = 'flex';
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
  static init() {
    this.setupModeSpecificBehavior();
    this.setupEventListeners();
    this.initializeComponents();
    this.setupButtonEvents();
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
          await ShippingManager.enviarDatosResumen();
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