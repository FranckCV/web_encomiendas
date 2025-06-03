document.addEventListener('DOMContentLoaded', async () => {
  let productos = {};
  try {
    const res = await fetch('/api/articulos');
    if (!res.ok) throw new Error(`Status ${res.status}`);
    productos = await res.json();
  } catch (e) {
    console.error('Error cargando /api/articulos:', e);
    return;
  }

  const decreaseBtn = document.querySelector('.qty-btn.decrease');
  const increaseBtn = document.querySelector('.qty-btn.increase');
  const qtyInput = document.querySelector('.qty-input');
  const quantityLimit = document.querySelector('.quantity-limit');
  const addToCartBtn = document.querySelector('.btn-agregar');
  const productImage = document.getElementById('producto-img');
  const priceElement = document.getElementById('precio');
  const dimensionsElement = document.getElementById('producto-dimensiones');
  const discountContainer = document.getElementById('precios-volumen');
  const sizeOptions = document.getElementById('size-options');
  const titulo = document.getElementById('producto-titulo');
  const thumbsContainer = document.getElementById('thumbs-container');

  const keys = Object.keys(productos);
  if (keys.length === 0) return;
  let currentKey = keys[0];
  let currentQuantity = 1;

  function updateDiscountCards(descuentos) {
    discountContainer.innerHTML = '';
    if (!descuentos || descuentos.length === 0) {
      discountContainer.innerHTML = '<p>No hay descuentos disponibles.</p>';
      return;
    }
    descuentos.forEach(desc => {
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

  function updateProductInfo(key) {
    currentKey = key;
    const data = productos[key];
    if (!data) return;

    productImage.src = data.image;
    productImage.alt = data.name_product || '';
    dimensionsElement.textContent = data.dimensions || '';
    titulo.textContent = data.name_product || '';

    // Tamaños si existen (adapta según tu estructura)
    if (data.tamanios && data.tamanios.length > 0) {
      sizeOptions.innerHTML = '';
      sizeOptions.style.display = 'flex';
      data.tamanios.forEach(t => {
        const btn = document.createElement('button');
        btn.classList.add('size-btn');
        btn.textContent = t;
        btn.dataset.size = t;
        btn.addEventListener('click', () => {
          document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          updatePrice();
        });
        sizeOptions.appendChild(btn);
      });
      sizeOptions.firstChild.classList.add('active');
    } else {
      sizeOptions.style.display = 'none';
      sizeOptions.innerHTML = '';
    }

    currentQuantity = 1;
    qtyInput.value = 1;
    quantityLimit.textContent = `Máximo: ${data.stock || 100} unidades`;

    updateDiscountCards(data.discounts);
    updatePrice();
  }

  function updatePrice() {
    const data = productos[currentKey];
    if (!data) return;

    let price = data.price;
    let bestDiscountPrice = null;
    let bestVolume = 0;

    if (data.discounts && data.discounts.length > 0) {
      data.discounts.forEach(desc => {
        const match = desc.name.match(/\d+/);
        if (!match) return;
        const volumen = parseInt(match[0], 10);
        if (currentQuantity >= volumen && volumen > bestVolume) {
          bestVolume = volumen;
          bestDiscountPrice = desc.value;
        }
      });
    }

    if (bestDiscountPrice !== null) price = bestDiscountPrice;

    const totalPrice = price * currentQuantity;
    priceElement.textContent = totalPrice.toFixed(2);

    // Resaltar descuento aplicado
    const discountItems = discountContainer.querySelectorAll('.precio-volumen-item');
    discountItems.forEach(item => item.classList.remove('active-discount'));
    if (bestVolume > 0 && discountItems.length) {
      for (let i = 0; i < data.discounts.length; i++) {
        if (data.discounts[i].value === bestDiscountPrice) {
          discountItems[i].classList.add('active-discount');
          break;
        }
      }
    }
  }

  function updateQuantity(val) {
    let n = parseInt(val, 10);
    if (isNaN(n) || n < 1) n = 1;
    else if (n > (productos[currentKey].stock || 100)) {
      n = productos[currentKey].stock || 100;
      quantityLimit.classList.add('active');
      setTimeout(() => quantityLimit.classList.remove('active'), 1500);
    }
    currentQuantity = n;
    qtyInput.value = n;
    decreaseBtn.disabled = n === 1;
    increaseBtn.disabled = n === (productos[currentKey].stock || 100);
    updatePrice();
  }

  function renderThumbnails() {
    if (!thumbsContainer) return;
    thumbsContainer.innerHTML = '';

    keys.forEach(key => {
      const prod = productos[key];
      const thumb = document.createElement('div');
      thumb.classList.add('thumb-item');
      if (key === currentKey) thumb.classList.add('active');

      thumb.innerHTML = `
        <img src="${prod.image}" alt="${prod.name_product}">
        <p>${prod.name_product}</p>
      `;

      thumb.addEventListener('click', () => {
        updateProductInfo(key);
        document.querySelectorAll('.thumb-item').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
      });

      thumbsContainer.appendChild(thumb);
    });
  }

  decreaseBtn.addEventListener('click', () => updateQuantity(currentQuantity - 1));
  increaseBtn.addEventListener('click', () => updateQuantity(currentQuantity + 1));
  qtyInput.addEventListener('change', () => updateQuantity(qtyInput.value));
  qtyInput.addEventListener('input', () => updateQuantity(qtyInput.value));

  qtyInput.addEventListener('keydown', e => {
    const allowedKeys = [8,9,13,27,46,35,36,37,39];
    if (
      allowedKeys.includes(e.keyCode) ||
      ([65,67,86,88].includes(e.keyCode) && e.ctrlKey)
    ) return;
    if ((e.shiftKey || e.keyCode < 48 || e.keyCode > 57) && (e.keyCode < 96 || e.keyCode > 105)) {
      e.preventDefault();
      return;
    }
    const {value, selectionStart, selectionEnd} = qtyInput;
    const char = e.key;
    let next = value;
    if (selectionStart === selectionEnd) {
      next = value.slice(0, selectionStart) + char + value.slice(selectionEnd);
    }
    if (parseInt(next, 10) > (productos[currentKey].stock || 100)) {
      e.preventDefault();
      quantityLimit.classList.add('active');
      setTimeout(() => quantityLimit.classList.remove('active'), 1500);
    }
  });

  addToCartBtn.addEventListener('click', () => {
    if (currentQuantity < 1 || currentQuantity > (productos[currentKey].stock || 100)) {
      quantityLimit.classList.add('active');
      setTimeout(() => quantityLimit.classList.remove('active'), 1500);
      return;
    }
    const data = productos[currentKey];
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

    const producto = {
      size: currentKey,
      quantity: currentQuantity,
      unitPrice: unitPrice,
      totalPrice: parseFloat(total),
      name: data.name_product,
      image: data.image,
    };

    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const index = carrito.findIndex(item => item.size === producto.size && item.name === producto.name);
    if (index !== -1) {
      carrito[index].quantity += producto.quantity;
      carrito[index].totalPrice = carrito[index].unitPrice * carrito[index].quantity;
    } else {
      carrito.push(producto);
    }
    localStorage.setItem('carrito', JSON.stringify(carrito));

    alert(
      `Agregaste ${producto.quantity} × ${producto.name} al carrito\nUnitario: S/ ${producto.unitPrice.toFixed(2)}\nTotal: S/ ${producto.totalPrice.toFixed(2)}`
    );
  });

  // Agregar estilos para descuentos activos
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

  // Inicializar todo
  updateProductInfo(currentKey);
  renderThumbnails();
  updateQuantity(currentQuantity);
});
