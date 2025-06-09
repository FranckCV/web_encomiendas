// ===== SISTEMA DE ENVÍOS MASIVOS =====
class EnviosMasivos {
    constructor() {
        this.envios = [];
        this.origenBloqueado = false;
        this.editandoEnvio = null;
        this.tabActual = 'destino';
        this.ubicaciones = {};
        this.rutasDisponibles = {};
        this.tarifasRuta = {};
        
        this.init();
    }

    init() {
        this.cargarDatosIniciales();
        this.configurarEventListeners();
        this.configurarTabs();
        this.actualizarEstadisticas();
        this.poblarDepartamentosOrigen();
    }

    // ===== CONFIGURACIÓN INICIAL =====
    cargarDatosIniciales() {
        // Cargar configuración desde el backend
        this.config = window.CONFIG_ENVIO || {};
        
        // Procesar rutas disponibles
        this.rutasDisponibles = this.config.rutasTarifas || {};
        this.tarifasRuta = this.config.tarifas || {};
        
        console.log('Datos cargados:', this.config);
    }

    // ===== CONFIGURACIÓN DE EVENT LISTENERS =====
    configurarEventListeners() {
        // Datos del remitente
        this.configurarValidacionRemitente();
        
        // Lugar de origen
        this.configurarSeleccionOrigen();
        
        // Formulario de encomiendas
        this.configurarFormularioEncomienda();
        
        // Botones de acción
        this.configurarBotonesAccion();
        
        // Validación en tiempo real
        this.configurarValidacionTiempoReal();
    }

    configurarValidacionRemitente() {
        const campos = [
            'remitente-tipo-doc',
            'remitente-numero-doc', 
            'remitente-telefono',
            'remitente-nombre',
            'remitente-email'
        ];

        campos.forEach(campo => {
            const elemento = document.getElementById(campo);
            if (elemento) {
                elemento.addEventListener('blur', () => this.validarCampoRemitente(campo));
                elemento.addEventListener('input', () => this.limpiarMensajeError(campo));
            }
        });
    }

    configurarSeleccionOrigen() {
        // Departamento origen
        document.getElementById('origen-departamento').addEventListener('change', (e) => {
            this.cargarProvinciasOrigen();
            this.limpiarSeleccionDestino();
        });

        // Provincia origen  
        document.getElementById('origen-provincia').addEventListener('change', (e) => {
            this.cargarDistritosOrigen();
        });

        // Distrito origen
        document.getElementById('origen-distrito').addEventListener('change', (e) => {
            this.validarOrigenCompleto();
            this.habilitarSeleccionDestino();
        });
    }

    configurarFormularioEncomienda() {
        // Tipo de recepción
        document.getElementById('m-tipoEntrega').addEventListener('change', (e) => {
            this.mostrarCamposDestino();
            this.validarTab('destino');
        });

        // Destino
        document.getElementById('select-departamento').addEventListener('change', (e) => {
            this.cargarProvinciasDestino();
            this.validarTab('destino');
        });

        document.getElementById('select-provincia').addEventListener('change', (e) => {
            this.cargarDistritosDestino();
            this.validarTab('destino');
        });

        document.getElementById('select-distrito').addEventListener('change', (e) => {
            this.cargarSucursalesDestino();
            this.validarTab('destino');
        });

        // Tipo de empaque
        document.getElementById('m-tipoEmpaque').addEventListener('change', (e) => {
            this.toggleFolios();
            this.toggleArticulos();
            this.validarTab('paquete');
        });

        // Tipo de documento destinatario
        document.getElementById('m-tipoDocumento').addEventListener('change', (e) => {
            this.mostrarCamposReceptor();
            this.validarTab('destinatario');
        });

        // Campos de dimensiones y peso
        ['m-peso', 'm-largo', 'm-ancho', 'm-alto', 'm-valorEnvio'].forEach(campo => {
            const elemento = document.getElementById(campo);
            if (elemento) {
                elemento.addEventListener('input', () => {
                    this.validarTab('paquete');
                });
            }
        });
    }

    configurarBotonesAccion() {
        // Botón agregar envío
        document.querySelector('.btn-agregar').addEventListener('click', () => {
            this.mostrarModalConfirmacion();
        });

        // Botón limpiar formulario
        document.querySelector('.btn-limpiar').addEventListener('click', () => {
            this.limpiarFormularioMasivo();
        });

        // Botón continuar
        document.getElementById('btn-continuar').addEventListener('click', () => {
            this.continuarProceso();
        });

        // Modal confirmación
        document.getElementById('confirmarBtn').addEventListener('click', () => {
            this.confirmarAgregarEnvio();
        });
    }

    configurarValidacionTiempoReal() {
        // Validar campos conforme se llenan
        const todosLosCampos = [
            // Destino
            'm-tipoEntrega', 'select-departamento', 'select-provincia', 'select-distrito',
            // Paquete  
            'm-tipoEmpaque', 'm-valorEnvio', 'm-peso', 'm-largo', 'm-ancho', 'm-alto',
            // Destinatario
            'm-tipoDocumento', 'm-nroDocumento', 'm-celular'
        ];

        todosLosCampos.forEach(campo => {
            const elemento = document.getElementById(campo);
            if (elemento) {
                elemento.addEventListener('input', () => {
                    this.validarProgresoPestanas();
                });
                elemento.addEventListener('change', () => {
                    this.validarProgresoPestanas();
                });
            }
        });
    }

    // ===== CONFIGURACIÓN DE PESTAÑAS =====
    configurarTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const tabName = e.target.dataset.tab;
                this.cambiarTab(tabName);
            });
        });
    }

    cambiarTab(tabName) {
        // Remover clase active de todos los tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });

        // Activar el tab seleccionado
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        document.getElementById(`tab-${tabName}`).classList.add('active');

        this.tabActual = tabName;
    }

    // ===== MANEJO DE UBICACIONES ORIGEN =====
    poblarDepartamentosOrigen() {
        const departamentos = this.extraerDepartamentos();
        this.llenarSelect('origen-departamento', departamentos, 'Seleccionar departamento...');
    }

    extraerDepartamentos() {
        const departamentos = new Set();
        Object.keys(this.rutasDisponibles).forEach(origen => {
            const [dep] = origen.split('|');
            departamentos.add(dep);
        });
        return Array.from(departamentos).sort().map((dep, index) => [index, dep]);
    }

    cargarProvinciasOrigen() {
        const departamento = this.obtenerTextoSelect('origen-departamento');
        if (!departamento) return;

        const provincias = this.extraerProvincias(departamento);
        this.llenarSelect('origen-provincia', provincias, 'Seleccionar provincia...');
        document.getElementById('origen-provincia').disabled = false;
        this.limpiarSelect('origen-distrito');
    }

    cargarDistritosOrigen() {
        const departamento = this.obtenerTextoSelect('origen-departamento');
        const provincia = this.obtenerTextoSelect('origen-provincia');
        if (!departamento || !provincia) return;

        const distritos = this.extraerDistritos(departamento, provincia);
        this.llenarSelect('origen-distrito', distritos, 'Seleccionar distrito...');
        document.getElementById('origen-distrito').disabled = false;
    }

    extraerProvincias(departamento) {
        const provincias = new Set();
        Object.keys(this.rutasDisponibles).forEach(origen => {
            const [dep, prov] = origen.split('|');
            if (dep === departamento) {
                provincias.add(prov);
            }
        });
        return Array.from(provincias).sort().map((prov, index) => [index, prov]);
    }

    extraerDistritos(departamento, provincia) {
        const distritos = new Set();
        Object.keys(this.rutasDisponibles).forEach(origen => {
            const [dep, prov, dist] = origen.split('|');
            if (dep === departamento && prov === provincia) {
                distritos.add(dist);
            }
        });
        return Array.from(distritos).sort().map((dist, index) => [index, dist]);
    }

    // ===== MANEJO DE UBICACIONES DESTINO =====
    habilitarSeleccionDestino() {
        const origenKey = this.construirClaveOrigen();
        if (!origenKey || !this.rutasDisponibles[origenKey]) {
            return;
        }

        const destinosDisponibles = this.rutasDisponibles[origenKey];
        const departamentosDestino = this.extraerDepartamentosDestino(destinosDisponibles);
        
        this.llenarSelect('select-departamento', departamentosDestino, 'Seleccionar departamento...');
        document.getElementById('select-departamento').disabled = false;
    }

    construirClaveOrigen() {
        const dep = this.obtenerTextoSelect('origen-departamento');
        const prov = this.obtenerTextoSelect('origen-provincia');
        const dist = this.obtenerTextoSelect('origen-distrito');
        
        if (dep && prov && dist) {
            return `${dep}|${prov}|${dist}`;
        }
        return null;
    }

    extraerDepartamentosDestino(destinos) {
        const departamentos = new Set();
        destinos.forEach(destino => {
            departamentos.add(destino.departamento);
        });
        return Array.from(departamentos).sort().map((dep, index) => [index, dep]);
    }

    cargarProvinciasDestino() {
        const departamentoDestino = this.obtenerTextoSelect('select-departamento');
        if (!departamentoDestino) return;

        const origenKey = this.construirClaveOrigen();
        const destinosDisponibles = this.rutasDisponibles[origenKey] || [];
        
        const provinciasDestino = this.extraerProvinciasDestino(destinosDisponibles, departamentoDestino);
        this.llenarSelect('select-provincia', provinciasDestino, 'Seleccionar provincia...');
        document.getElementById('select-provincia').disabled = false;
        this.limpiarSelect('select-distrito');
    }

    extraerProvinciasDestino(destinos, departamento) {
        const provincias = new Set();
        destinos.forEach(destino => {
            if (destino.departamento === departamento) {
                provincias.add(destino.provincia);
            }
        });
        return Array.from(provincias).sort().map((prov, index) => [index, prov]);
    }

    cargarDistritosDestino() {
        const departamentoDestino = this.obtenerTextoSelect('select-departamento');
        const provinciaDestino = this.obtenerTextoSelect('select-provincia');
        if (!departamentoDestino || !provinciaDestino) return;

        const origenKey = this.construirClaveOrigen();
        const destinosDisponibles = this.rutasDisponibles[origenKey] || [];
        
        const distritosDestino = this.extraerDistritosDestino(destinosDisponibles, departamentoDestino, provinciaDestino);
        this.llenarSelect('select-distrito', distritosDestino, 'Seleccionar distrito...');
        document.getElementById('select-distrito').disabled = false;
    }

    extraerDistritosDestino(destinos, departamento, provincia) {
        const distritos = [];
        destinos.forEach(destino => {
            if (destino.departamento === departamento && destino.provincia === provincia) {
                distritos.push([destino.id, destino.distrito]);
            }
        });
        return distritos.sort((a, b) => a[1].localeCompare(b[1]));
    }

    cargarSucursalesDestino() {
        const tipoEntrega = document.getElementById('m-tipoEntrega').value;
        if (tipoEntrega !== '2') return; // Solo para agencia

        const distritoDestinoId = document.getElementById('select-distrito').value;
        if (!distritoDestinoId) return;

        const origenKey = this.construirClaveOrigen();
        const destinosDisponibles = this.rutasDisponibles[origenKey] || [];
        
        const sucursalesDestino = destinosDisponibles.filter(destino => 
            destino.id == distritoDestinoId
        );

        if (sucursalesDestino.length > 0) {
            const sucursalSelect = document.getElementById('select-sucursal');
            sucursalSelect.innerHTML = '';
            
            sucursalesDestino.forEach(destino => {
                const option = document.createElement('option');
                option.value = destino.id;
                option.textContent = destino.direccion || `Sucursal ${destino.distrito}`;
                sucursalSelect.appendChild(option);
            });
            
            sucursalSelect.disabled = false;
        }
    }

    limpiarSeleccionDestino() {
        this.limpiarSelect('select-departamento');
        this.limpiarSelect('select-provincia'); 
        this.limpiarSelect('select-distrito');
        this.limpiarSelect('select-sucursal');
    }

    // ===== VALIDACIÓN DE ORIGEN =====
    validarOrigenCompleto() {
        const departamento = this.obtenerTextoSelect('origen-departamento');
        const provincia = this.obtenerTextoSelect('origen-provincia');
        const distrito = this.obtenerTextoSelect('origen-distrito');

        if (departamento && provincia && distrito) {
            this.bloquearOrigen();
        }
    }

    bloquearOrigen() {
        document.getElementById('origen-departamento').disabled = true;
        document.getElementById('origen-provincia').disabled = true;
        document.getElementById('origen-distrito').disabled = true;
        
        this.origenBloqueado = true;
        this.mostrarBotonEditarOrigen();
    }

    mostrarBotonEditarOrigen() {
        // Buscar si ya existe el botón
        let btnEditar = document.querySelector('.btn-editar-origen');
        if (!btnEditar) {
            // Encontrar el botón existente de editar en acciones_origen
            const accionesOrigen = document.querySelector('.acciones_origen');
            const btnExistente = accionesOrigen ? accionesOrigen.querySelector('.btn_update') : null;
            
            if (btnExistente) {
                btnExistente.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.editarOrigen();
                });
                btnExistente.classList.add('btn-editar-origen');
            }
        }
    }

    editarOrigen() {
        const mensaje = "Si modifica el lugar de origen, se eliminarán todos los envíos ya registrados cuyos destinos no sean válidos para este nuevo origen. ¿Deseas continuar?";
        
        if (confirm(mensaje)) {
            this.desbloquearOrigen();
        }
    }

    desbloquearOrigen() {
        document.getElementById('origen-departamento').disabled = false;
        document.getElementById('origen-provincia').disabled = false;
        document.getElementById('origen-distrito').disabled = false;
        
        this.origenBloqueado = false;
        
        // Limpiar envíos que ya no sean válidos
        this.validarEnviosExistentes();
    }

    validarEnviosExistentes() {
        const origenKey = this.construirClaveOrigen();
        if (!origenKey) return;

        this.envios = this.envios.filter(envio => {
            const destinosDisponibles = this.rutasDisponibles[origenKey] || [];
            return destinosDisponibles.some(destino => destino.id == envio.destinoId);
        });
        
        this.renderizarTablaEnvios();
        this.actualizarEstadisticas();
    }

    // ===== MOSTRAR/OCULTAR CAMPOS =====
    mostrarCamposDestino() {
        const tipoEntrega = document.getElementById('m-tipoEntrega').value;
        const grupoDireccion = document.getElementById('grupo-direccion');
        const grupoTienda = document.getElementById('grupo-tienda');
        
        if (tipoEntrega === '1') { // Domicilio
            grupoDireccion.style.display = 'block';
            grupoTienda.style.display = 'none';
            document.getElementById('m-direccion').required = true;
            document.getElementById('select-sucursal').required = false;
        } else if (tipoEntrega === '2') { // Agencia
            grupoDireccion.style.display = 'none';
            grupoTienda.style.display = 'block';
            document.getElementById('m-direccion').required = false;
            document.getElementById('select-sucursal').required = true;
        } else {
            grupoDireccion.style.display = 'none';
            grupoTienda.style.display = 'none';
        }
    }

    toggleFolios() {
        const tipoEmpaque = document.getElementById('m-tipoEmpaque').value;
        const grupoFolios = document.getElementById('grupo-folios');
        
        if (tipoEmpaque === '1') { // Documento
            grupoFolios.style.display = 'block';
            document.getElementById('m-folios').required = true;
        } else {
            grupoFolios.style.display = 'none';
            document.getElementById('m-folios').required = false;
        }
    }

    toggleArticulos() {
        const tipoEmpaque = document.getElementById('m-tipoEmpaque').value;
        const grupoArticulos = document.getElementById('grupo-articulos');
        
        if (tipoEmpaque === '2') { // Mercancía
            grupoArticulos.style.display = 'block';
            document.getElementById('m-tipoArticulo').required = true;
        } else {
            grupoArticulos.style.display = 'none';
            document.getElementById('m-tipoArticulo').required = false;
        }
    }

    mostrarCamposReceptor() {
        const tipoDoc = document.getElementById('m-tipoDocumento').value;
        const camposNombres = document.getElementById('campos-nombres');
        const camposApellidos = document.getElementById('campos-apellidos');
        const campoRazon = document.getElementById('campo-razon-ruc');
        const campoContacto = document.getElementById('campo-contacto-ruc');
        
        if (tipoDoc === '3') { // RUC
            camposNombres.style.display = 'none';
            camposApellidos.style.display = 'none';
            campoRazon.style.display = 'block';
            campoContacto.style.display = 'block';
            
            document.getElementById('m-nombres').required = false;
            document.getElementById('m-apellidos').required = false;
            document.getElementById('m-razonSocial').required = true;
            document.getElementById('m-contacto').required = true;
        } else {
            camposNombres.style.display = 'block';
            camposApellidos.style.display = 'block';
            campoRazon.style.display = 'none';
            campoContacto.style.display = 'none';
            
            document.getElementById('m-nombres').required = true;
            document.getElementById('m-apellidos').required = true;
            document.getElementById('m-razonSocial').required = false;
            document.getElementById('m-contacto').required = false;
        }
    }

    // ===== VALIDACIÓN DE PESTAÑAS =====
    validarTab(tabName) {
        let valido = false;
        
        switch(tabName) {
            case 'destino':
                valido = this.validarTabDestino();
                break;
            case 'paquete':
                valido = this.validarTabPaquete();
                break;
            case 'destinatario':
                valido = this.validarTabDestinatario();
                break;
        }
        
        this.marcarTabComoCompletado(tabName, valido);
        return valido;
    }

    validarTabDestino() {
        const tipoEntrega = document.getElementById('m-tipoEntrega').value;
        const departamento = document.getElementById('select-departamento').value;
        const provincia = document.getElementById('select-provincia').value;
        const distrito = document.getElementById('select-distrito').value;
        
        let camposRequeridos = [tipoEntrega, departamento, provincia, distrito];
        
        if (tipoEntrega === '1') { // Domicilio
            const direccion = document.getElementById('m-direccion').value.trim();
            camposRequeridos.push(direccion);
        } else if (tipoEntrega === '2') { // Agencia
            const sucursal = document.getElementById('select-sucursal').value;
            camposRequeridos.push(sucursal);
        }
        
        return camposRequeridos.every(campo => campo !== '' && campo !== null);
    }

    validarTabPaquete() {
        const tipoEmpaque = document.getElementById('m-tipoEmpaque').value;
        const valor = document.getElementById('m-valorEnvio').value;
        const peso = document.getElementById('m-peso').value;
        const largo = document.getElementById('m-largo').value;
        const ancho = document.getElementById('m-ancho').value;
        const alto = document.getElementById('m-alto').value;
        
        let camposRequeridos = [tipoEmpaque, valor, peso, largo, ancho, alto];
        
        if (tipoEmpaque === '1') { // Documento
            const folios = document.getElementById('m-folios').value;
            camposRequeridos.push(folios);
        } else if (tipoEmpaque === '2') { // Mercancía
            const articulo = document.getElementById('m-tipoArticulo').value;
            camposRequeridos.push(articulo);
        }
        
        return camposRequeridos.every(campo => campo !== '' && campo !== null);
    }

    validarTabDestinatario() {
        const tipoDoc = document.getElementById('m-tipoDocumento').value;
        const nroDoc = document.getElementById('m-nroDocumento').value.trim();
        const celular = document.getElementById('m-celular').value.trim();
        
        let camposRequeridos = [tipoDoc, nroDoc, celular];
        
        if (tipoDoc === '3') { // RUC
            const razon = document.getElementById('m-razonSocial').value.trim();
            const contacto = document.getElementById('m-contacto').value.trim();
            camposRequeridos.push(razon, contacto);
        } else {
            const nombres = document.getElementById('m-nombres').value.trim();
            const apellidos = document.getElementById('m-apellidos').value.trim();
            camposRequeridos.push(nombres, apellidos);
        }
        
        return camposRequeridos.every(campo => campo !== '' && campo !== null);
    }

    marcarTabComoCompletado(tabName, completado) {
        const tabBtn = document.querySelector(`[data-tab="${tabName}"]`);
        
        if (completado) {
            tabBtn.classList.add('completed');
            this.animarSiguienteTab(tabName);
        } else {
            tabBtn.classList.remove('completed');
        }
    }

    animarSiguienteTab(tabActual) {
        const tabs = ['destino', 'paquete', 'destinatario'];
        const indiceActual = tabs.indexOf(tabActual);
        
        if (indiceActual < tabs.length - 1) {
            const siguienteTab = tabs[indiceActual + 1];
            const siguienteBtn = document.querySelector(`[data-tab="${siguienteTab}"]`);
            siguienteBtn.classList.add('next-available');
            
            setTimeout(() => {
                siguienteBtn.classList.remove('next-available');
            }, 3000);
        } else {
            // Último tab completado - animar botón agregar
            this.animarBotonAgregar();
        }
    }

    animarBotonAgregar() {
        const btnAgregar = document.querySelector('.btn-agregar');
        if (btnAgregar) {
            btnAgregar.classList.add('btn-add-bounce');
            
            setTimeout(() => {
                btnAgregar.classList.remove('btn-add-bounce');
            }, 3000);
        }
    }

    validarProgresoPestanas() {
        const tabs = ['destino', 'paquete', 'destinatario'];
        tabs.forEach(tab => this.validarTab(tab));
    }

    // ===== GESTIÓN DE ENVÍOS =====
    mostrarModalConfirmacion() {
        if (!this.validarFormularioCompleto()) {
            document.getElementById('modalValidacion').style.display = 'flex';
            return;
        }
        
        document.getElementById('modalConfirmacion').style.display = 'flex';
    }

    validarFormularioCompleto() {
        return this.validarTab('destino') && 
               this.validarTab('paquete') && 
               this.validarTab('destinatario');
    }

    confirmarAgregarEnvio() {
        const datosEnvio = this.recopilarDatosEnvio();
        
        if (this.editandoEnvio !== null) {
            this.envios[this.editandoEnvio] = datosEnvio;
            this.editandoEnvio = null;
        } else {
            this.envios.push(datosEnvio);
        }
        
        this.renderizarTablaEnvios();
        this.actualizarEstadisticas();
        this.limpiarFormularioMasivo();
        this.cerrarModal();
    }

    recopilarDatosEnvio() {
        const tipoDoc = document.getElementById('m-tipoDocumento').value;
        const tipoEntrega = document.getElementById('m-tipoEntrega').value;
        
        return {
            // Destino
            tipoRecepcion: this.obtenerTextoSelect('m-tipoEntrega'),
            tipoRecepcionId: tipoEntrega,
            departamento: this.obtenerTextoSelect('select-departamento'),
            provincia: this.obtenerTextoSelect('select-provincia'),
            distrito: this.obtenerTextoSelect('select-distrito'),
            destinoId: document.getElementById('select-distrito').value,
            direccion: tipoEntrega === '1' ? document.getElementById('m-direccion').value : '',
            sucursal: tipoEntrega === '2' ? this.obtenerTextoSelect('select-sucursal') : '',
            sucursalId: tipoEntrega === '2' ? document.getElementById('select-sucursal').value : '',
            
            // Paquete
            tipoEmpaque: this.obtenerTextoSelect('m-tipoEmpaque'),
            tipoEmpaqueId: document.getElementById('m-tipoEmpaque').value,
            valor: parseFloat(document.getElementById('m-valorEnvio').value),
            peso: parseFloat(document.getElementById('m-peso').value),
            largo: parseFloat(document.getElementById('m-largo').value),
            ancho: parseFloat(document.getElementById('m-ancho').value),
            alto: parseFloat(document.getElementById('m-alto').value),
            descripcion: document.getElementById('m-descripcionArticulo').value || '',
            folios: document.getElementById('m-folios').value || '',
            articulo: this.obtenerTextoSelect('m-tipoArticulo') || '',
            articuloId: document.getElementById('m-tipoArticulo').value || '',
            
            // Destinatario
            tipoDocumento: this.obtenerTextoSelect('m-tipoDocumento'),
            tipoDocumentoId: tipoDoc,
            nroDocumento: document.getElementById('m-nroDocumento').value,
            celular: document.getElementById('m-celular').value,
            nombres: tipoDoc === '3' ? '' : document.getElementById('m-nombres').value,
            apellidos: tipoDoc === '3' ? '' : document.getElementById('m-apellidos').value,
            razonSocial: tipoDoc === '3' ? document.getElementById('m-razonSocial').value : '',
            contacto: tipoDoc === '3' ? document.getElementById('m-contacto').value : '',
            
            // Calculados
            destinatario: this.construirNombreDestinatario(tipoDoc),
            destino: `${this.obtenerTextoSelect('select-distrito')} - ${this.obtenerTextoSelect('select-provincia')} - ${this.obtenerTextoSelect('select-departamento')}`,
            dimensiones: `${document.getElementById('m-largo').value} × ${document.getElementById('m-ancho').value} × ${document.getElementById('m-alto').value} cm`,
            
            // Tarifa
            tarifa: this.calcularTarifa()
        };
    }

    calcularTarifa() {
        const origenKey = this.construirClaveOrigen();
        const destinoId = document.getElementById('select-distrito').value;
        
        if (origenKey && destinoId) {
            const destinos = this.rutasDisponibles[origenKey] || [];
            const destino = destinos.find(d => d.id == destinoId);
            return destino ? destino.tarifa : 0;
        }
        return 0;
    }

    construirNombreDestinatario(tipoDoc) {
        if (tipoDoc === '3') { // RUC
            return document.getElementById('m-razonSocial').value;
        } else {
            const nombres = document.getElementById('m-nombres').value;
            const apellidos = document.getElementById('m-apellidos').value;
            return `${nombres} ${apellidos}`;
        }
    }

    obtenerTextoSelect(selectId) {
        const select = document.getElementById(selectId);
        return select.options[select.selectedIndex]?.text || '';
    }

    // ===== RENDERIZADO DE TABLA =====
    renderizarTablaEnvios() {
        const tableContent = document.getElementById('tableContent');
        
        if (this.envios.length === 0) {
            tableContent.innerHTML = `
                <div class="empty-state">
                    <p>No hay envíos registrados aún</p>
                    <p>Comienza agregando tu primer envío</p>
                </div>
            `;
            return;
        }
        
        let tablaHTML = `
            <table class="table-envios">
                <thead>
                    <tr>
                        <th>Tipo Recepción</th>
                        <th>Destinatario</th>
                        <th>Destino</th>
                        <th>Dirección/Sucursal</th>
                        <th>Descripción</th>
                        <th>Dimensiones</th>
                        <th>Peso (kg)</th>
                        <th>Valor (S/)</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        this.envios.forEach((envio, index) => {
            tablaHTML += `
                <tr>
                    <td>${envio.tipoRecepcion}</td>
                    <td>${envio.destinatario}</td>
                    <td>${envio.destino}</td>
                    <td>${envio.direccion || envio.sucursal}</td>
                    <td>${envio.descripcion}</td>
                    <td>${envio.dimensiones}</td>
                    <td>${envio.peso}</td>
                    <td>${envio.valor.toFixed(2)}</td>
                    <td class="action-buttons">
                        <button class="btn-icon btn-edit" onclick="enviosMasivos.editarEnvio(${index})" title="Editar">
                            ✎
                        </button>
                        <button class="btn-icon btn-delete" onclick="enviosMasivos.eliminarEnvio(${index})" title="Eliminar">
                            🗑️
                        </button>
                    </td>
                </tr>
            `;
        });
        
        tablaHTML += '</tbody></table>';
        tableContent.innerHTML = tablaHTML;
    }

    editarEnvio(index) {
        this.editandoEnvio = index;
        const envio = this.envios[index];
        
        // Llenar formulario con datos del envío
        this.llenarFormularioConEnvio(envio);
        
        // Ir a la primera pestaña
        this.cambiarTab('destino');
    }

    llenarFormularioConEnvio(envio) {
        // Destino
        document.getElementById('m-tipoEntrega').value = envio.tipoRecepcionId;
        this.mostrarCamposDestino();
        
        // Cargar ubicaciones del destino
        this.seleccionarUbicacionDestino(envio.departamento, envio.provincia, envio.distrito);
        
        if (envio.direccion) {
            document.getElementById('m-direccion').value = envio.direccion;
        }
        
        // Paquete
        document.getElementById('m-tipoEmpaque').value = envio.tipoEmpaqueId;
        document.getElementById('m-valorEnvio').value = envio.valor;
        document.getElementById('m-peso').value = envio.peso;
        document.getElementById('m-largo').value = envio.largo;
        document.getElementById('m-ancho').value = envio.ancho;
        document.getElementById('m-alto').value = envio.alto;
        document.getElementById('m-descripcionArticulo').value = envio.descripcion;
        
        this.toggleFolios();
        this.toggleArticulos();
        
        if (envio.folios) {
            document.getElementById('m-folios').value = envio.folios;
        }
        if (envio.articuloId) {
            document.getElementById('m-tipoArticulo').value = envio.articuloId;
        }
        
        // Destinatario
        document.getElementById('m-tipoDocumento').value = envio.tipoDocumentoId;
        document.getElementById('m-nroDocumento').value = envio.nroDocumento;
        document.getElementById('m-celular').value = envio.celular;
        
        this.mostrarCamposReceptor();
        
        if (envio.nombres) {
            document.getElementById('m-nombres').value = envio.nombres;
            document.getElementById('m-apellidos').value = envio.apellidos;
        } else {
            document.getElementById('m-razonSocial').value = envio.razonSocial;
            document.getElementById('m-contacto').value = envio.contacto;
        }
    }

    seleccionarUbicacionDestino(departamento, provincia, distrito) {
        // Esta función debería seleccionar las ubicaciones en los selects
        // Por ahora, solo establecemos el valor del distrito si coincide
        const distritoSelect = document.getElementById('select-distrito');
        for (let option of distritoSelect.options) {
            if (option.text === distrito) {
                distritoSelect.value = option.value;
                break;
            }
        }
    }

    eliminarEnvio(index) {
        if (confirm('¿Estás seguro de eliminar este envío?')) {
            this.envios.splice(index, 1);
            this.renderizarTablaEnvios();
            this.actualizarEstadisticas();
        }
    }

    // ===== ESTADÍSTICAS =====
    actualizarEstadisticas() {
        const totalEnvios = this.envios.length;
        const pesoTotal = this.envios.reduce((total, envio) => total + envio.peso, 0);
        
        document.getElementById('totalEnvios').textContent = totalEnvios;
        document.getElementById('pesoTotal').textContent = pesoTotal.toFixed(2);
    }

    // ===== UTILIDADES =====
    llenarSelect(selectId, opciones, placeholder = '') {
        const select = document.getElementById(selectId);
        if (!select) return;
        
        select.innerHTML = '';
        
        if (placeholder) {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = placeholder;
            option.disabled = true;
            option.selected = true;
            select.appendChild(option);
        }
        
        opciones.forEach(opcion => {
            const option = document.createElement('option');
            option.value = opcion[0];
            option.textContent = opcion[1];
            select.appendChild(option);
        });
    }

    limpiarSelect(selectId) {
        const select = document.getElementById(selectId);
        if (select) {
            select.innerHTML = '<option value="" disabled selected>Seleccionar...</option>';
            select.disabled = true;
        }
    }

    limpiarFormularioMasivo() {
        // Limpiar todos los campos del formulario de encomienda
        const campos = [
            'm-tipoEntrega', 'select-departamento', 'select-provincia', 'select-distrito',
            'm-direccion', 'select-sucursal', 'm-tipoEmpaque', 'm-valorEnvio', 'm-peso',
            'm-largo', 'm-ancho', 'm-alto', 'm-descripcionArticulo', 'm-folios',
            'm-tipoArticulo', 'm-tipoDocumento', 'm-nroDocumento', 'm-celular',
            'm-nombres', 'm-apellidos', 'm-razonSocial', 'm-contacto'
        ];
        
        campos.forEach(campo => {
            const elemento = document.getElementById(campo);
            if (elemento) {
                if (elemento.tagName === 'SELECT') {
                    elemento.selectedIndex = 0;
                } else {
                    elemento.value = '';
                }
            }
        });
        
        // Ocultar campos dinámicos
        document.getElementById('grupo-direccion').style.display = 'none';
        document.getElementById('grupo-tienda').style.display = 'none';
        document.getElementById('grupo-folios').style.display = 'none';
        document.getElementById('grupo-articulos').style.display = 'none';
        document.getElementById('campos-nombres').style.display = 'none';
        document.getElementById('campos-apellidos').style.display = 'none';
        document.getElementById('campo-razon-ruc').style.display = 'block';
        document.getElementById('campo-contacto-ruc').style.display = 'block';
        
        // Resetear pestañas
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('completed', 'next-available');
        });
        
        this.cambiarTab('destino');
        this.editandoEnvio = null;
        
        // Limpiar selects de destino
        this.limpiarSeleccionDestino();
    }

    cerrarModal() {
        document.getElementById('modalConfirmacion').style.display = 'none';
        document.getElementById('modalValidacion').style.display = 'none';
    }

    eliminarTodo() {
        if (this.envios.length === 0) {
            alert('No hay envíos para eliminar');
            return;
        }
        
        if (confirm('¿Estás seguro de eliminar todos los envíos registrados?')) {
            this.envios = [];
            this.renderizarTablaEnvios();
            this.actualizarEstadisticas();
        }
    }

    continuarProceso() {
        if (this.envios.length === 0) {
            alert('Debe agregar al menos un envío para continuar');
            return;
        }
        
        // Preparar datos para envío
        const datosCompletos = {
            remitente: this.obtenerDatosRemitente(),
            origen: this.obtenerDatosOrigen(),
            envios: this.envios
        };
        
        console.log('Datos para procesar:', datosCompletos);
        
        // Aquí puedes enviar los datos al servidor
        // fetch('/procesar_envios_masivos', {...})
        
        alert('Continuando al siguiente paso...');
    }

    obtenerDatosRemitente() {
        return {
            tipoDocumento: document.getElementById('remitente-tipo-doc').value,
            numeroDocumento: document.getElementById('remitente-numero-doc').value,
            telefono: document.getElementById('remitente-telefono').value,
            nombre: document.getElementById('remitente-nombre').value,
            email: document.getElementById('remitente-email').value
        };
    }

    obtenerDatosOrigen() {
        return {
            departamento: this.obtenerTextoSelect('origen-departamento'),
            provincia: this.obtenerTextoSelect('origen-provincia'),
            distrito: this.obtenerTextoSelect('origen-distrito'),
            clave: this.construirClaveOrigen()
        };
    }

    // ===== VALIDACIÓN DE CAMPOS =====
    validarCampoRemitente(campo) {
        const elemento = document.getElementById(campo);
        const valor = elemento.value.trim();
        
        let esValido = true;
        let mensaje = '';
        
        switch(campo) {
            case 'remitente-numero-doc':
                const tipoDoc = document.getElementById('remitente-tipo-doc').value;
                if (tipoDoc === '1' && valor.length !== 8) { // DNI
                    esValido = false;
                    mensaje = 'El DNI debe tener 8 dígitos';
                } else if (tipoDoc === '3' && valor.length !== 11) { // RUC
                    esValido = false;
                    mensaje = 'El RUC debe tener 11 dígitos';
                }
                break;
            case 'remitente-telefono':
                if (valor.length !== 9) {
                    esValido = false;
                    mensaje = 'El teléfono debe tener 9 dígitos';
                }
                break;
            case 'remitente-email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(valor)) {
                    esValido = false;
                    mensaje = 'Ingrese un email válido';
                }
                break;
        }
        
        this.mostrarMensajeValidacion(campo, mensaje, !esValido);
        return esValido;
    }

    mostrarMensajeValidacion(campo, mensaje, mostrar) {
        const mensajeId = `mensaje-validacion-${campo.split('-').pop()}`;
        const elementoMensaje = document.getElementById(mensajeId);
        
        if (elementoMensaje) {
            elementoMensaje.textContent = mensaje;
            elementoMensaje.style.display = mostrar ? 'block' : 'none';
        }
    }

    limpiarMensajeError(campo) {
        this.mostrarMensajeValidacion(campo, '', false);
    }

    mostrarError(mensaje) {
        alert(mensaje);
    }

    exportarExcel() {
        if (this.envios.length === 0) {
            alert('No hay datos para exportar');
            return;
        }
        
        console.log('Exportando a Excel...', this.envios);
        alert('Funcionalidad de exportación a Excel por implementar');
    }
}

// ===== FUNCIONES GLOBALES =====
function mostrarCamposDestino() {
    enviosMasivos.mostrarCamposDestino();
}

function toggleFolios() {
    enviosMasivos.toggleFolios();
}

function toggleArticulos() {
    enviosMasivos.toggleArticulos();
}

function mostrarCamposReceptor() {
    enviosMasivos.mostrarCamposReceptor();
}

function mostrarModalConfirmacion() {
    enviosMasivos.mostrarModalConfirmacion();
}

function limpiarFormularioMasivo() {
    enviosMasivos.limpiarFormularioMasivo();
}

function cerrarModal() {
    enviosMasivos.cerrarModal();
}

function eliminarTodo() {
    enviosMasivos.eliminarTodo();
}

function exportarExcel() {
    enviosMasivos.exportarExcel();
}

// ===== INICIALIZACIÓN =====
let enviosMasivos;

document.addEventListener('DOMContentLoaded', function() {
    enviosMasivos = new EnviosMasivos();
});