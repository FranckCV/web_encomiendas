// static/js/cajas.js

document.addEventListener('DOMContentLoaded', async () => {
  // 1) Carga dinámica de datos desde Flask
  let productSizes = {};
  try {
    const res = await fetch('/api/cajas');
    if (!res.ok) throw new Error(`Satus ${res.status}`);
    productSizes = await res.json();
  } catch (e) {
    console.error('Error cargando /api/cajas:', e);
    return;
  }

  // 2) Referencias al DOM
  const decreaseBtn      = document.querySelector('.decrease');
  const increaseBtn      = document.querySelector('.increase');
  const qtyInput         = document.querySelector('.qty-input');
  const quantityLimit    = document.querySelector('.quantity-limit');
  const addToCartBtn     = document.querySelector('.btn-agregar');
  const productImage     = document.querySelector('.producto-imagen img');
  const priceElement     = document.querySelector('.precio');
  const dimensionsElement= document.querySelector('.producto-dimensiones');
  const discountItems    = document.querySelectorAll('.precio-volumen-item');
  const discountEls      = document.querySelectorAll('.precio-volumen-item .etiqueta-precio');
  const sizeBtns         = document.querySelectorAll('.size-btn');
  const maxQuantity      = 100;

  // 3) Estado inicial
const clavesOrdenadas = Object.keys(productSizes).sort((a,b) => {
  const orden = ['xxs', 'xs', 's', 'm', 'l'];
  return orden.indexOf(a) - orden.indexOf(b);
});
let currentSize = clavesOrdenadas[0];
  console.log(currentSize)
  let currentQuantity = 1;

  // 4) Funciones de UI y validaciones

  function updateProductInfo(size) {
    currentSize = size;
    const data = productSizes[size];
    // Imagen y texto
    productImage.src   = data.image;
    productImage.alt   = `Caja ${size.toUpperCase()}`;
    dimensionsElement.textContent = data.dimensions;
    // Descuentos
    const d25 = data.discounts[25] ?? data.price;
    const d50 = data.discounts[50] ?? d25;
    discountEls[0].textContent = `s/. ${d25.toFixed(2)}`;
    discountEls[1].textContent = `s/. ${d50.toFixed(2)}`;
    // Recálculo de precio y cantidad
    updateQuantity(currentQuantity);
  }

  function updatePrice() {
    const data = productSizes[currentSize];
    let price = data.price;
    if (currentQuantity >= 50 && data.discounts[50]) price = data.discounts[50];
    else if (currentQuantity >= 25 && data.discounts[25]) price = data.discounts[25];
    priceElement.textContent = price.toFixed(2);
    highlightDiscount();
  }

  function highlightDiscount() {
    discountItems.forEach(item => item.classList.remove('active-discount'));
    if (currentQuantity >= 50)      discountItems[1]?.classList.add('active-discount');
    else if (currentQuantity >= 25) discountItems[0]?.classList.add('active-discount');
  }

  function highlightLimit() {
    quantityLimit.classList.add('active');
    setTimeout(() => quantityLimit.classList.remove('active'), 1500);
  }

  function updateQuantity(val) {
    let n = parseInt(val, 10);
    if (isNaN(n) || n < 1) n = 1;
    else if (n > maxQuantity) {
      n = maxQuantity;
      highlightLimit();
    }
    currentQuantity = n;
    qtyInput.value    = n;
    decreaseBtn.disabled = n === 1;
    increaseBtn.disabled = n === maxQuantity;
    updatePrice();
  }

  // 5) Event listeners

  // Tamaño
  sizeBtns.forEach(btn =>
    btn.addEventListener('click', () => {
      sizeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateProductInfo(btn.textContent.toLowerCase());
    })
  );

  // Cantidad
  decreaseBtn.addEventListener('click', () => updateQuantity(currentQuantity - 1));
  increaseBtn.addEventListener('click', () => updateQuantity(currentQuantity + 1));
  qtyInput.addEventListener('change', () => updateQuantity(qtyInput.value));
  qtyInput.addEventListener('input',  () => updateQuantity(qtyInput.value));

  // Prevenir caracteres no numéricos y exceso
  qtyInput.addEventListener('keydown', e => {
    const k = e.keyCode;
    // teclas permitidas: editar, flechas, ctrl+c/x/v/a
    if (
      [8,9,13,27,46,35,36,37,39].includes(k) ||
      ((k === 65||k===67||k===86||k===88) && e.ctrlKey)
    ) return;
    // dígitos numéricos
    if ((e.shiftKey || k < 48 || k > 57) && (k < 96 || k > 105)) {
      e.preventDefault();
      return;
    }
    // simula nuevo valor y previene exceso
    const { value, selectionStart, selectionEnd } = qtyInput;
    const char = e.key;
    let next = value;
    if (selectionStart === selectionEnd) {
      next = value.slice(0, selectionStart) + char + value.slice(selectionEnd);
    }
    if (parseInt(next, 10) > maxQuantity) {
      e.preventDefault();
      highlightLimit();
    }
  });

  // Agregar al carrito
  addToCartBtn.addEventListener('click', () => {
    if (currentQuantity < 1 || currentQuantity > maxQuantity) {
      highlightLimit(); 
      return;
    }
    const data = productSizes[currentSize];
    let unitPrice = data.price;
    if (currentQuantity >= 50 && data.discounts[50]) unitPrice = data.discounts[50];
    else if (currentQuantity >= 25 && data.discounts[25]) unitPrice = data.discounts[25];
    const total = (unitPrice * currentQuantity).toFixed(2);
    alert(
      `Agregaste ${currentQuantity} × Caja ${currentSize.toUpperCase()} al carrito\n` +
      `Unitario: S/ ${unitPrice.toFixed(2)}\nTotal:  S/ ${total}`
    );
  });

  // 6) Inyección de estilos adicionales
  const style = document.createElement('style');
  style.textContent = `
    .precio-volumen-item.active-discount {
      border: 2px solid #1a3c5b;
      transform: scale(1.05);
      background-color: #e8f4f8;
      box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }`;
  document.head.appendChild(style);

  // Responsividad
  function adjustResponsiveness() {
    const det = document.querySelector('.producto-detalle');
    det.style.flexDirection = window.innerWidth <= 768 ? 'column' : 'row';
  }
  adjustResponsiveness();
  window.addEventListener('resize', adjustResponsiveness);

  // 7) Inicialización final
  updateProductInfo(currentSize);
  updateQuantity(currentQuantity);
});
