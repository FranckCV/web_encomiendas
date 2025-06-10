document.addEventListener('DOMContentLoaded', async () => {
  let productSizes = {};
  try {
    const res = await fetch('/api/cajas');
    if (!res.ok) throw new Error(`Status ${res.status}`);
    productSizes = await res.json();
  } catch (e) {
    console.error('Error cargando /api/cajas:', e);
    return;
  }

  const decreaseBtn = document.querySelector('.decrease');
  const increaseBtn = document.querySelector('.increase');
  const qtyInput = document.querySelector('.qty-input');
  const quantityLimit = document.querySelector('.quantity-limit');
  const addToCartBtn = document.querySelector('.btn-agregar');
  const productImage = document.querySelector('.producto-imagen img');
  const priceElement = document.querySelector('.precio');
  const dimensionsElement = document.querySelector('.producto-dimensiones');
  const discountContainer = document.querySelector('.precios-volumen');
  const sizeBtns = document.querySelectorAll('.size-btn');
  const titulo = document.querySelector('.producto-titulo');

  const maxQuantity = 100;
  const orderSizes = ['xxs', 'xs', 's', 'm', 'l'];

  const clavesOrdenadas = Object.keys(productSizes).sort(
    (a, b) => orderSizes.indexOf(a) - orderSizes.indexOf(b)
  );
  let currentSize = clavesOrdenadas[0];
  let currentQuantity = 1;

  function updateDiscountCards(discounts) {
    discountContainer.innerHTML = '';
    if (!discounts || discounts.length === 0) {
      discountContainer.innerHTML = '<p>No hay descuentos disponibles.</p>';
      return;
    }
    discounts.forEach((desc) => {
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
    console.log(data.image);
    productImage.alt = `Caja ${size.toUpperCase()}`;
    dimensionsElement.textContent = data.dimensions || '';

    titulo.textContent = data.name_product || '';

    updateDiscountCards(data.discounts);
    updateQuantity(currentQuantity);
  }

  function updatePrice() {
    const data = productSizes[currentSize];
    if (!data) return;

    if (data.discounts && data.discounts.length > 0) {
      data.discounts.sort((a, b) => {
        const volA = parseInt(a.name.match(/\d+/)?.[0] || '0', 10);
        const volB = parseInt(b.name.match(/\d+/)?.[0] || '0', 10);
        return volA - volB;
      });
    }

    let unitPrice = data.price;
    let bestDiscountPrice = null;
    let bestVolume = 0;

    if (data.discounts && data.discounts.length > 0) {
      data.discounts.forEach((desc) => {
        const match = desc.name.match(/\d+/);
        if (!match) return;
        const volumen = parseInt(match[0], 10);
        if (currentQuantity >= volumen && volumen > bestVolume) {
          bestVolume = volumen;
          bestDiscountPrice = desc.value;
        }
      });
    }

    if (bestDiscountPrice !== null) unitPrice = bestDiscountPrice;

    const totalPrice = unitPrice * currentQuantity;

    priceElement.textContent = totalPrice.toFixed(2);

    highlightDiscount();
  }

  function highlightDiscount() {
    const discountItems = discountContainer.querySelectorAll('.precio-volumen-item');
    discountItems.forEach((item) => item.classList.remove('active-discount'));

    if (!productSizes[currentSize]?.discounts?.length) return;

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

  sizeBtns.forEach((btn, i) => {
    btn.dataset.size = orderSizes[i];
    btn.addEventListener('click', () => {
      sizeBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      updateProductInfo(btn.dataset.size);
    });
  });

  decreaseBtn.addEventListener('click', () => updateQuantity(currentQuantity - 1));
  increaseBtn.addEventListener('click', () => updateQuantity(currentQuantity + 1));
  qtyInput.addEventListener('change', () => updateQuantity(qtyInput.value));
  qtyInput.addEventListener('input', () => updateQuantity(qtyInput.value));

  qtyInput.addEventListener('keydown', (e) => {
    const allowedKeys = [8, 9, 13, 27, 46, 35, 36, 37, 39];
    if (
      allowedKeys.includes(e.keyCode) ||
      ([65, 67, 86, 88].includes(e.keyCode) && e.ctrlKey)
    )
      return;
    if ((e.shiftKey || e.keyCode < 48 || e.keyCode > 57) && (e.keyCode < 96 || e.keyCode > 105)) {
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
    if (!data) return;

    let unitPrice = data.price;

    if (data.discounts && data.discounts.length > 0) {
      let bestDiscountPrice = null;
      let bestVolume = 0;

      data.discounts.forEach((desc) => {
        const match = desc.name.match(/\d+/);
        if (!match) return;
        const volumen = parseInt(match[0], 10);
        if (currentQuantity >= volumen && volumen > bestVolume) {
          bestVolume = volumen;
          bestDiscountPrice = desc.value;
        }
      });

      if (bestDiscountPrice !== null && bestDiscountPrice < unitPrice) {
        unitPrice = bestDiscountPrice;
      }
    }

    const total = (unitPrice * currentQuantity).toFixed(2);

    let precio_unitario_1 = data.price;
    let precio_unitario_2 = null;
    let cantidad_precio_unitario_2 = null;
    let precio_unitario_3 = null;
    let cantidad_precio_unitario_3 = null;

    // Obtener precios y cantidades desde los descuentos (ordenados)
    if (data.discounts && data.discounts.length > 0) {
      const ordenados = [...data.discounts].sort((a, b) => {
        const volA = parseInt(a.name.match(/\d+/)?.[0] || '0', 10);
        const volB = parseInt(b.name.match(/\d+/)?.[0] || '0', 10);
        return volA - volB;
      });

      if (ordenados.length > 0) {
        precio_unitario_2 = ordenados[0].value;
        cantidad_precio_unitario_2 = parseInt(ordenados[0].name.match(/\d+/)?.[0] || '0', 10);
      }
      if (ordenados.length > 1) {
        precio_unitario_3 = ordenados[1].value;
        cantidad_precio_unitario_3 = parseInt(ordenados[1].name.match(/\d+/)?.[0] || '0', 10);
      }
    }

    const producto = {
      id: data.id,
      size: currentSize,
      quantity: currentQuantity,
      unitPrice: unitPrice,
      // subtotal: unitPrice * currentQuantity,
      // totalPrice: parseFloat(total),
      name: data.name_product,
      image: data.image.split('/').pop(),
      originalPrice: precio_unitario_1,
      discount: precio_unitario_1 - unitPrice,
      precio_unitario_1,
      precio_unitario_2,
      cantidad_precio_unitario_2,
      precio_unitario_3,
      cantidad_precio_unitario_3
      // description: 'aeaaaa'
    };


    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const index = carrito.findIndex((item) => item.size === producto.size);
    if (index !== -1) {
      carrito[index].quantity += producto.quantity;
      carrito[index].totalPrice = carrito[index].unitPrice * carrito[index].quantity;
    } else {
      carrito.push(producto);
    }
    localStorage.setItem('carrito', JSON.stringify(carrito));

    alert(
      `Agregaste ${producto.quantity} × Caja ${producto.size.toUpperCase()} al carrito\nUnitario: S/ ${producto.unitPrice.toFixed(
        2
      )}\nTotal: S/ ${producto.totalPrice.toFixed(2)}`
    );
  });

  const style = document.createElement('style');
  style.textContent = `
    .precio-volumen-item.active-discount {
      border: 2px solid #1a3c5b;
      transform: scale(1.05);
      background-color: #e8f4f8;
      box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }`;
  document.head.appendChild(style);

  function adjustResponsiveness() {
    const det = document.querySelector('.producto-detalle');
    det.style.flexDirection = window.innerWidth <= 768 ? 'column' : 'row';
  }
  adjustResponsiveness();
  window.addEventListener('resize', adjustResponsiveness);

  updateProductInfo(currentSize);
  updateQuantity(currentQuantity);
});
