- Boletas de venta para carrito
- Validaciones de campos de crud
- Pasarela de pago en parte administrativa
- En el registro de la encomienda, si recarga la página aunque no haya hecho nada, sale estás seguro de recargar? 
- Campos con autocompletado, se toma como que nunca tocaste el campo y te pide "completa todos los campos"
- Por paquete: rótulo , boleta o factura , guía de remisión


En el registro también yo le quité el botón de editar, no sé si creen que sí debemos incluirlo
Creo que debemos agregar un boolean que sea enSucursal
Hay dos casos 
- Que cuando el remitente vaya a dejarlo a sucursal, tenga que pagar 
- Y que cuando el remitente vaya a dejarlo en sucursal ya esté pagado
Entonces, en una se debe mostrar la interfaz de pago y cambiar el estado, y en otra ya no, simplemente un cambio de estado
