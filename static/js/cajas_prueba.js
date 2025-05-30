document.addEventListener('DOMContentLoaded', async () => {
  // 1) Carga dinámica de datos desde Flask
  let productSizes = {};
  try {
    const res = await fetch('/api/cajas');
    if (!res.ok) throw new Error(`Status ${res.status}`);
    productSizes = await res.json();
  } catch (e) {
    console.error('Error cargando /api/cajas:', e);
    return;
  }

  // 2) Referencias al DOM
  const decreaseBtn       = document.querySelector('.decrease');
  const increaseBtn       = document.querySelector('.increase');
  const qtyInput          = document.querySelector('.qty-input');
  const quantityLimit     = document.querySelector('.quantity-limit');
  const addToCartBtn      = document.querySelector('.btn-agregar');
  const productImage      = document.querySelector('.producto-imagen img');
  const priceElement      = document.querySelector('.precio');
  const dimensionsElement = document.querySelector('.producto-dimensiones');
  const discountContainer = document.getElementById('discount-container'); // nuevo contenedor
  const sizeBtns          = document.querySelectorAll('.size-btn');
  const titulo          = document.querySelector('.producto-titulo');

  const maxQuantity       = 100;

  // 3) Estado inicial
  const orderSizes = ['xxs', 'xs', 's', 'm', 'l'];
  const clavesOrdenadas = Object.keys(productSizes).sort((a,b) => orderSizes.indexOf(a) - orderSizes.indexOf(b));
  let currentSize = clavesOrdenadas[0];
  let currentQuantity = 1;

  // 4) Funciones UI

  // Genera las tarjetas de descuento dinámicamente
  function updateDiscountCards(discounts) {
    discountContainer.innerHTML = ''; // limpio el contenedor

    if (!discounts || discounts.length === 0) {
      discountContainer.innerHTML = '<p>No hay descuentos disponibles.</p>';
      return;
    }

    discounts.forEach(desc => {
      const div = document.createElement('div');
      div.classList.add('precio-volumen-item');

      const priceSpan = document.createElement('span');
      priceSpan.classList.add('etiqueta-precio');
      priceSpan.textContent = `s/. ${desc.value.toFixed(2)}`;

      const nameSpan = document.createElement('span');
      nameSpan.classList.add('etiqueta-cantidad');
      nameSpan.textContent = desc.name;

      div.appendChild(priceSpan);
      div.appendChild(nameSpan);
      discountContainer.appendChild(div);
    });
  }

  function updateProductInfo(size) {
    currentSize = size;
    const data = productSizes[size];
    if (!data) return;

    productImage.src = data.image;
    productImage.alt = `Caja ${size.toUpperCase()}`;
    dimensionsElement.textContent = data.dimensions || '';

    // Actualizamos el precio base
    titulo.textContent = data.name_product || '';
    priceElement.textContent = data.price.toFixed(2);

    // Actualizamos las tarjetas de descuento
    updateDiscountCards(data.discounts);

    // Actualizamos la cantidad y precio
    updateQuantity(currentQuantity);
  }

  function updatePrice() {
    const data = productSizes[currentSize];
    let price = data.price;

    if (currentQuantity < 1) price = data.price;

    if (data.discounts && data.discounts.length > 0) {
      // Buscamos el descuento válido según cantidad, asumimos descuentos ordenados por volumen mínimo ascendente
      // O buscamos el mayor descuento aplicable
      let bestDiscountPrice = null;

      data.discounts.forEach(desc => {
        // Extraer el número del nombre para detectar volumen, ejemplo: "Descuento Volumen 25"
        const match = desc.name.match(/\d+/);
        if (!match) return; // si no hay número, no cuenta
        const volumen = parseInt(match[0], 10);
        if (currentQuantity >= volumen) {
          if (bestDiscountPrice === null || desc.value < bestDiscountPrice) {
            bestDiscountPrice = desc.value;
          }
        }
      });

      if (bestDiscountPrice !== null) price = bestDiscountPrice;
    }

    priceElement.textContent = price.toFixed(2);
    highlightDiscount();
  }

  function highlightDiscount() {
    const discountItems = discountContainer.querySelectorAll('.precio-volumen-item');
    discountItems.forEach(item => item.classList.remove('active-discount'));

    if (!productSizes[currentSize]?.discounts?.length) return;

    // Activa la tarjeta del descuento vigente (el mayor volumen menor o igual a currentQuantity)
    let activeIndex = -1;
    let maxVolumen = 0;
    productSizes[currentSize].discounts.forEach((desc, idx) => {
      const match = desc.name.match(/\d+/);
      if (!match) return;
      const volumen = parseInt(match[0], 10);
      if (currentQuantity >= volumen && volumen > maxVolumen) {
        maxVolumen = volumen;
        activeIndex = idx;
      }
    });

    if (activeIndex >= 0 && discountItems[activeIndex]) {
      discountItems[activeIndex].classList.add('active-discount');
    }
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
    qtyInput.value = n;
    decreaseBtn.disabled = n === 1;
    increaseBtn.disabled = n === maxQuantity;
    updatePrice();
  }

  // 5) Event listeners

  sizeBtns.forEach(btn =>
    btn.addEventListener('click', () => {
      sizeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateProductInfo(btn.dataset.size);
    })
  );

  decreaseBtn.addEventListener('click', () => updateQuantity(currentQuantity - 1));
  increaseBtn.addEventListener('click', () => updateQuantity(currentQuantity + 1));
  qtyInput.addEventListener('change', () => updateQuantity(qtyInput.value));
  qtyInput.addEventListener('input', () => updateQuantity(qtyInput.value));

  qtyInput.addEventListener('keydown', e => {
    const k = e.keyCode;
    if (
      [8,9,13,27,46,35,36,37,39].includes(k) ||
      ((k === 65||k===67||k===86||k===88) && e.ctrlKey)
    ) return;
    if ((e.shiftKey || k < 48 || k > 57) && (k < 96 || k > 105)) {
      e.preventDefault();
      return;
    }
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

  addToCartBtn.addEventListener('click', () => {
    if (currentQuantity < 1 || currentQuantity > maxQuantity) {
      highlightLimit();
      return;
    }
    const data = productSizes[currentSize];
    let unitPrice = data.price;

    if (data.discounts && data.discounts.length > 0) {
      let bestDiscountPrice = null;

      data.discounts.forEach(desc => {
        const match = desc.name.match(/\d+/);
        if (!match) return;
        const volumen = parseInt(match[0], 10);
        if (currentQuantity >= volumen) {
          if (bestDiscountPrice === null || desc.value < bestDiscountPrice) {
            bestDiscountPrice = desc.value;
          }
        }
      });

      if (bestDiscountPrice !== null) unitPrice = bestDiscountPrice;
    }

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
