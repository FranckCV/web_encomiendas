from controladores.bd import sql_select_fetchone, sql_select_fetchall, sql_execute

def obtener_salida_completa(salida_id):
    """
    Obtiene todos los datos de una salida para editarla
    """
    try:
        # 1. Obtener datos básicos de la salida
        sql_salida = """
        SELECT 
            s.id,
            s.fecha,
            s.hora,
            s.recojo,
            s.entrega,
            s.estado,
            s.unidadid,
            s.destino_final_id,
            s.conductor_principal,
            s.origen_inicio_id,
            u.placa as vehiculo_placa,
            u.capacidad as vehiculo_capacidad,
            so.abreviatura as origen_nombre,
            so.latitud as origen_lat,
            so.longitud as origen_lng,
            sd.abreviatura as destino_nombre,
            sd.latitud as destino_lat,
            sd.longitud as destino_lng
        FROM salida s
        INNER JOIN unidad u ON s.unidadid = u.id
        INNER JOIN sucursal so ON s.origen_inicio_id = so.id
        INNER JOIN sucursal sd ON s.destino_final_id = sd.id
        WHERE s.id = %s
        """
        
        salida = sql_select_fetchone(sql_salida, (salida_id,))
        
        # ✅ VERIFICAR SI HAY ERROR DE BD
        if isinstance(salida, Exception):
            print(f"Error en consulta de salida: {salida}")
            return None
            
        if not salida:
            print(f"No se encontró salida con ID: {salida_id}")
            return None
        
        # 2. Obtener empleados asignados
        sql_empleados = """
        SELECT 
            e.id,
            e.nombre,
            e.apellidos,
            e.correo,
            e.n_documento
        FROM empleado_salida es
        INNER JOIN empleado e ON es.empleadoid = e.id
        WHERE es.salidaid = %s
        """
        
        empleados = sql_select_fetchall(sql_empleados, (salida_id,))
        
        # ✅ VERIFICAR ERRORES Y USAR LISTA VACÍA SI HAY PROBLEMAS
        if isinstance(empleados, Exception):
            print(f"Error en consulta de empleados: {empleados}")
            empleados = []
        elif not empleados:
            empleados = []
        
        # 3. Obtener escalas
        sql_escalas = """
        SELECT 
            s.id,
            s.abreviatura,
            s.direccion,
            s.latitud,
            s.longitud,
            u.distrito,
            u.provincia,
            s.teléfono as telefono,
            s.horario_l_v as horario,
            CONCAT(s.abreviatura, ' - ', s.direccion, ' / ', u.distrito, ' - ', u.provincia) as nombre
        FROM escala es
        INNER JOIN sucursal s ON es.sucursalid = s.id
        INNER JOIN ubigeo u ON s.ubigeocodigo = u.codigo
        WHERE es.salidaid = %s
        ORDER BY es.sucursalid
        """
        
        escalas = sql_select_fetchall(sql_escalas, (salida_id,))
        
        # ✅ VERIFICAR ERRORES
        if isinstance(escalas, Exception):
            print(f"Error en consulta de escalas: {escalas}")
            escalas = []
        elif not escalas:
            escalas = []
        
        # 4. Obtener paquetes asignados
        sql_paquetes = """
        SELECT 
            p.tracking,
            p.peso,
            p.valor,
            p.descripcion,
            p.nombres_contacto_destinatario,
            p.apellidos_razon_destinatario,
            p.direccion_destinatario,
            p.telefono_destinatario,
            cp.nombre as contenido,
            te.id_sucursal_origen,
            p.sucursal_destino_id
        FROM paquete p
        LEFT JOIN contenido_paquete cp ON p.contenido_paqueteid = cp.id
        LEFT JOIN transaccion_encomienda te ON p.transaccion_encomienda_num_serie = te.num_serie
        WHERE p.salidaid = %s
        """
        
        paquetes = sql_select_fetchall(sql_paquetes, (salida_id,))
        
        # ✅ VERIFICAR ERRORES
        if isinstance(paquetes, Exception):
            print(f"Error en consulta de paquetes: {paquetes}")
            paquetes = []
        elif not paquetes:
            paquetes = []
        
        # 6. Estructurar datos para el frontend
        salida_data = {
            'id': salida['id'],
            'fecha': salida['fecha'].strftime('%Y-%m-%d') if salida['fecha'] else '',
            'hora': str(salida['hora']) if salida['hora'] else '',
            'recojo': bool(salida['recojo']) if salida['recojo'] is not None else False,
            'entrega': bool(salida['entrega']) if salida['entrega'] is not None else False,
            'estado': salida['estado'] or '',
            
            # Origen y destino
            'origen': {
                'id': int(salida['origen_inicio_id']) if salida['origen_inicio_id'] else 0,
                'nombre': str(salida['origen_nombre']) if salida['origen_nombre'] else '',
                'lat': float(salida['origen_lat']) if salida['origen_lat'] else 0,
                'lng': float(salida['origen_lng']) if salida['origen_lng'] else 0
            },
            'destino': {
                'id': int(salida['destino_final_id']) if salida['destino_final_id'] else 0,
                'nombre': str(salida['destino_nombre']) if salida['destino_nombre'] else '',
                'lat': float(salida['destino_lat']) if salida['destino_lat'] else 0,
                'lng': float(salida['destino_lng']) if salida['destino_lng'] else 0
            },
            
            # Vehículo
            'vehiculo': {
                'id': int(salida['unidadid']) if salida['unidadid'] else 0,
                'placa': str(salida['vehiculo_placa']) if salida['vehiculo_placa'] else '',
                'capacidad': float(salida['vehiculo_capacidad']) if salida['vehiculo_capacidad'] else 0
            },
            
            # Personal asignado
            'empleados': [
                {
                    'id': int(emp['id']),
                    'nombre': f"{emp['nombre'] or ''} {emp['apellidos'] or ''}".strip(),
                    'correo': str(emp['correo']) if emp['correo'] else '',
                    'documento': str(emp['n_documento']) if emp['n_documento'] else ''
                }
                for emp in empleados
            ],
            
            # Escalas
            'escalas': [
                {
                    'id': int(escala['id']),
                    'nombre': str(escala['nombre']) if escala['nombre'] else '',
                    'direccion': str(escala['direccion']) if escala['direccion'] else '',
                    'lat': float(escala['latitud']) if escala['latitud'] else 0,
                    'lng': float(escala['longitud']) if escala['longitud'] else 0,
                    'distrito': str(escala['distrito']) if escala['distrito'] else '',
                    'provincia': str(escala['provincia']) if escala['provincia'] else '',
                    'telefono': str(escala['telefono']) if escala['telefono'] else '',
                    'horario': str(escala['horario']) if escala['horario'] else ''
                }
                for escala in escalas
            ],
            
            # Paquetes
            'paquetes': [
                {
                    'tracking': str(paq['tracking']) if paq['tracking'] else '',
                    'peso': float(paq['peso']) if paq['peso'] else 0,
                    'valor': float(paq['valor']) if paq['valor'] else 0,
                    'descripcion': str(paq['descripcion']) if paq['descripcion'] else '',
                    'contenido': str(paq['contenido']) if paq['contenido'] else 'Sin especificar',
                    'destinatario': f"{paq['nombres_contacto_destinatario'] or ''} {paq['apellidos_razon_destinatario'] or ''}".strip(),
                    'origen_id': int(paq['id_sucursal_origen']) if paq['id_sucursal_origen'] else 0,
                    'destino_id': int(paq['sucursal_destino_id']) if paq['sucursal_destino_id'] else 0
                }
                for paq in paquetes
            ]
        }
        
        return salida_data
        
    except Exception as e:
        print(f"Error al obtener salida completa: {str(e)}")
        return None

def actualizar_salida_completa(salida_id, datos):
    """
    Actualiza todos los datos de una salida
    """
    try:
        # 1. Actualizar datos básicos de la salida
        sql_update_salida = """
        UPDATE salida SET
            fecha = %s,
            hora = %s,
            unidadid = %s,
            destino_final_id = %s,
            origen_inicio_id = %s
        WHERE id = %s
        """
        
        resultado = sql_execute(sql_update_salida, (
            datos['fecha'],
            datos['hora'],
            datos['vehiculo']['id'],
            datos['vehiculo']['destino_final_id'],
            datos['vehiculo']['origen_inicio_id'],
            salida_id
        ))
        
        # ✅ VERIFICAR ERRORES EN LA ACTUALIZACIÓN
        if isinstance(resultado, Exception):
            return {
                'success': False,
                'mensaje': f'Error al actualizar salida: {str(resultado)}'
            }
        
        # 2. Eliminar empleados actuales y agregar los nuevos
        sql_delete_empleados = "DELETE FROM empleado_salida WHERE salidaid = %s"
        resultado = sql_execute(sql_delete_empleados, (salida_id,))
        
        if isinstance(resultado, Exception):
            print(f"Error eliminando empleados: {resultado}")
        
        if datos.get('empleados'):
            sql_insert_empleado = "INSERT INTO empleado_salida (salidaid, empleadoid) VALUES (%s, %s)"
            for empleado_id in datos['empleados']:
                resultado = sql_execute(sql_insert_empleado, (salida_id, empleado_id))
                if isinstance(resultado, Exception):
                    print(f"Error insertando empleado {empleado_id}: {resultado}")
        
        # 3. Eliminar escalas actuales y agregar las nuevas
        sql_delete_escalas = "DELETE FROM escala WHERE salidaid = %s"
        resultado = sql_execute(sql_delete_escalas, (salida_id,))
        
        if isinstance(resultado, Exception):
            print(f"Error eliminando escalas: {resultado}")
        
        if datos.get('escalas'):
            sql_insert_escala = "INSERT INTO escala (salidaid, sucursalid) VALUES (%s, %s)"
            for escala_id in datos['escalas']:
                resultado = sql_execute(sql_insert_escala, (salida_id, escala_id))
                if isinstance(resultado, Exception):
                    print(f"Error insertando escala {escala_id}: {resultado}")
        
        # 4. Actualizar paquetes (quitar asignación actual y asignar nuevos)
        sql_update_paquetes_old = "UPDATE paquete SET salidaid = NULL WHERE salidaid = %s"
        resultado = sql_execute(sql_update_paquetes_old, (salida_id,))
        
        if isinstance(resultado, Exception):
            print(f"Error limpiando paquetes: {resultado}")
        
        if datos.get('paquetes'):
            sql_update_paquete = "UPDATE paquete SET salidaid = %s WHERE tracking = %s"
            for paquete in datos['paquetes']:
                resultado = sql_execute(sql_update_paquete, (salida_id, paquete['tracking']))
                if isinstance(resultado, Exception):
                    print(f"Error asignando paquete {paquete['tracking']}: {resultado}")
        
        return {
            'success': True,
            'mensaje': 'Salida actualizada correctamente'
        }
        
    except Exception as e:
        print(f"Error al actualizar salida: {str(e)}")
        return {
            'success': False,
            'mensaje': f'Error al actualizar: {str(e)}'
        }

def verificar_salida_existe(salida_id):
    """
    Verifica si una salida existe
    """
    try:
        sql = "SELECT id FROM salida WHERE id = %s"
        resultado = sql_select_fetchone(sql, (salida_id,))
        
        if isinstance(resultado, Exception):
            print(f"Error verificando salida: {resultado}")
            return False
            
        return resultado is not None
    except Exception as e:
        print(f"Error al verificar salida: {str(e)}")
        return False

def obtener_vehiculos_para_edicion(salida_id):
    """
    Obtiene todos los vehículos disponibles incluyendo el de la salida actual
    """
    try:
        # Primero obtener el vehículo de la salida actual
        sql_vehiculo_actual = """
        SELECT 
            s.unidadid,
            CONCAT(tu.nombre, ' ', m.nombre, ' - ', u.placa) AS nombre_unidad,
            u.capacidad,
            SUM(COALESCE(p.peso, 0)) AS capacidad_usada
        FROM salida s
        INNER JOIN unidad u ON s.unidadid = u.id
        INNER JOIN modelo m ON m.id = u.modeloid
        INNER JOIN tipo_unidad tu ON tu.id = m.tipo_unidadid
        LEFT JOIN paquete p ON p.salidaid = s.id
        WHERE s.id = %s
        GROUP BY s.unidadid, tu.nombre, m.nombre, u.placa, u.capacidad
        """
        
        vehiculo_actual = sql_select_fetchone(sql_vehiculo_actual, (salida_id,))
        
        # Luego obtener todos los demás vehículos disponibles
        sql_otros_vehiculos = """
        SELECT 
            u.id as unidadid,
            CONCAT(tu.nombre, ' ', m.nombre, ' - ', u.placa) AS nombre_unidad,
            u.capacidad,
            COALESCE(capacidad_usada.peso_total, 0) AS capacidad_usada
        FROM unidad u
        INNER JOIN modelo m ON m.id = u.modeloid
        INNER JOIN tipo_unidad tu ON tu.id = m.tipo_unidadid
        LEFT JOIN (
            SELECT 
                s.unidadid,
                SUM(COALESCE(p.peso, 0)) AS peso_total
            FROM salida s 
            LEFT JOIN paquete p ON p.salidaid = s.id
            WHERE 
                s.estado IN ('P', 'T') 
                AND s.fecha BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 2 DAY)
                AND s.id != %s  -- Excluir la salida actual
            GROUP BY s.unidadid
        ) capacidad_usada ON capacidad_usada.unidadid = u.id
        WHERE u.estado = 'D' AND u.id != (
            SELECT unidadid FROM salida WHERE id = %s
        )
        ORDER BY nombre_unidad
        """
        
        otros_vehiculos = sql_select_fetchall(sql_otros_vehiculos, (salida_id, salida_id))
        
        # Combinar resultados
        vehiculos = []
        
        # Agregar el vehículo actual primero
        if vehiculo_actual and not isinstance(vehiculo_actual, Exception):
            vehiculos.append(vehiculo_actual)
        
        # Agregar los demás vehículos
        if otros_vehiculos and not isinstance(otros_vehiculos, Exception):
            vehiculos.extend(otros_vehiculos)
        
        print(f"✅ Obtenidos {len(vehiculos)} vehículos para edición de salida {salida_id}")
        
        return vehiculos
        
    except Exception as e:
        print(f"Error al obtener vehículos para edición: {str(e)}")
        return []