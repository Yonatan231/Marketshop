let cart = JSON.parse(localStorage.getItem('cart')) || [];
let coins = Number(localStorage.getItem('coins'));
if (!Number.isFinite(coins)) {
    coins = 100;
    localStorage.setItem('coins', coins);
}
let rouletteDiscount = Number(localStorage.getItem('rouletteDiscount')) || 0;
let rouletteLabel = localStorage.getItem('rouletteLabel') || '';
let orderCount = Number(localStorage.getItem('orderCount')) || 0;
let profileName = localStorage.getItem('profileName') || '';
let profileEmail = localStorage.getItem('profileEmail') || '';

const products = JSON.parse(document.getElementById('product-data').textContent || '[]');

// Normalize cart data from storage to avoid NaN when quantity is missing
cart = cart.map(item => ({
    ...item,
    quantity: Number.isFinite(item?.quantity) ? Number(item.quantity) : 1,
}));

function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    clearTimeout(window.toastTimeout);
    window.toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 1800);
}

// DOM elements
const screens = document.querySelectorAll('.screen');
const navBtns = document.querySelectorAll('.nav-btn');
const backBtns = document.querySelectorAll('.back-btn');

// Navigation
function showScreen(screenId) {
    screens.forEach(screen => screen.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
    navBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-screen="${screenId}"]`)?.classList.add('active');
    if (screenId === 'home') {
        loadProducts();
    }
    if (screenId === 'cart') {
        loadCart();
    }
    if (screenId === 'profile') {
        loadProfile();
    }
}

navBtns.forEach(btn => {
    btn.addEventListener('click', () => showScreen(btn.dataset.screen));
});

backBtns.forEach(btn => {
    btn.addEventListener('click', () => showScreen(btn.dataset.screen));
});

// Login
/*document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const loginInput = document.querySelector('#login-form input[type="text"]');
    const passwordInput = document.querySelector('#login-form input[type="password"]');
    const name = loginInput?.value.trim() || 'Invitada';
    profileName = name;
    profileEmail = loginInput?.value.trim() || '';
    localStorage.setItem('profileName', profileName);
    localStorage.setItem('profileEmail', profileEmail);
    showScreen('home');
    loadProducts();
});*/

// Load Products
function loadProducts() {
    const grid = document.getElementById('products-grid');
    grid.innerHTML = '';
    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h4>${product.name}</h4>
            <p>$${product.price - product.discount} <span class="discount">$${product.price}</span></p>
        `;
        card.addEventListener('click', () => showProductDetail(product));
        grid.appendChild(card);
    });
}

// Show Product Detail
function showProductDetail(product) {
    document.getElementById('product-image').src = product.image;
    document.getElementById('product-name').textContent = product.name;
    document.getElementById('product-price').textContent = `$${product.price - product.discount} (Antes $${product.price})`;
    document.getElementById('product-rating').textContent = '⭐'.repeat(product.rating);
    showScreen('product-detail');
}

// Add to Cart
document.getElementById('add-to-cart').addEventListener('click', () => {
    const name = document.getElementById('product-name').textContent;
    const product = products.find(p => p.name === name);
    if (!product) return;

    const existing = cart.find(item => item.id === product.id);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ ...product, quantity: 1 });
    }
    saveCart();
    showToast('Agregado al carrito');
    showScreen('home');
});

function calculateTotal() {
    return cart.reduce((sum, item) => {
        const price = Number(item.price) - Number(item.discount);
        const quantity = Number.isFinite(item.quantity) ? Number(item.quantity) : 1;
        return sum + price * quantity;
    }, 0);
}

function getCouponDiscount(total) {
    const coupon = document.getElementById('coupon').value.trim().toUpperCase();
    if (coupon === 'DESC10') {
        return total * 0.1;
    }
    return 0;
}

function getRouletteDiscount(total) {
    return total * (rouletteDiscount / 100);
}

// Load Cart
function loadCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Tu carrito está vacío.</p>';
    }

    cart.forEach(item => {
        const unitPrice = item.price - item.discount;
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        itemDiv.innerHTML = `
            <div class="cart-item-details">
                <div>
                    <strong>${item.name}</strong>
                    <p class="cart-item-price">$${unitPrice.toFixed(2)} x ${item.quantity}</p>
                </div>
                <div class="cart-item-controls">
                    <button onclick="changeQuantity(${item.id}, -1)">−</button>
                    <span>${item.quantity}</span>
                    <button onclick="changeQuantity(${item.id}, 1)">+</button>
                </div>
            </div>
            <div class="cart-item-actions">
                <span class="cart-item-total">$${(unitPrice * item.quantity).toFixed(2)}</span>
                <button class="remove-btn" onclick="removeFromCart(${item.id})">Eliminar</button>
            </div>
        `;
        cartItems.appendChild(itemDiv);
    });

    const subtotal = calculateTotal();
    const couponDiscount = getCouponDiscount(subtotal);
    const rouletteDiscountAmount = getRouletteDiscount(subtotal);
    const finalTotal = subtotal - couponDiscount - rouletteDiscountAmount;

    document.getElementById('total').textContent = finalTotal.toFixed(2);
    const discountInfo = document.getElementById('discount-info');
    discountInfo.textContent = couponDiscount > 0 ? `Descuento cupón aplicado: -$${couponDiscount.toFixed(2)}` : '';

    const rouletteInfo = document.getElementById('roulette-info');
    if (rouletteDiscount > 0) {
        rouletteInfo.textContent = `Descuento de ruleta: ${rouletteLabel} (-$${rouletteDiscountAmount.toFixed(2)})`;
    } else if (rouletteLabel) {
        rouletteInfo.textContent = rouletteLabel;
    } else {
        rouletteInfo.textContent = '';
    }
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

window.changeQuantity = function(id, delta) {
    const item = cart.find(product => product.id === id);
    if (!item) return;
    item.quantity += delta;
    if (item.quantity < 1) {
        removeFromCart(id);
        return;
    }
    saveCart();
    loadCart();
};

window.removeFromCart = function(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
    loadCart();
};

// Apply Coupon
document.getElementById('apply-coupon').addEventListener('click', () => {
    const coupon = document.getElementById('coupon').value.trim().toUpperCase();
    if (coupon === 'DESC10') {
        loadCart();
        showToast('Cupón aplicado');
    } else {
        showToast('Cupón inválido');
    }
});

// Checkout
document.getElementById('checkout').addEventListener('click', () => {
    if (cart.length === 0) {
        showToast('Tu carrito está vacío');
        return;
    }

    const subtotal = calculateTotal();
    const discount = getCouponDiscount(subtotal);
    const finalTotal = subtotal - discount;

    orderCount += 1;
    localStorage.setItem('orderCount', orderCount);
    cart = [];
    saveCart();
    loadCart();
    document.getElementById('coupon').value = '';
    showToast(`Pago procesado: $${finalTotal.toFixed(2)}`);
    showScreen('home');
});

// Rewards
document.getElementById('coins').textContent = coins;

document.getElementById('logout').addEventListener('click', () => {
    localStorage.removeItem('profileName');
    localStorage.removeItem('profileEmail');
    showScreen('login');
});

document.getElementById('daily-checkin').addEventListener('click', () => {
    const today = new Date().toDateString();
    const lastCheckin = localStorage.getItem('lastCheckin');
    if (lastCheckin !== today) {
        coins += 10;
        localStorage.setItem('coins', coins);
        localStorage.setItem('lastCheckin', today);
        document.getElementById('coins').textContent = coins;
        alert('¡10 monedas obtenidas!');
    } else {
        alert('Ya hiciste check-in hoy');
    }
});

function loadProfile() {
    document.getElementById('profile-name').textContent = profileName || 'Invitada';
    document.getElementById('profile-email').textContent = profileEmail || 'Usuario anónimo';
    document.getElementById('profile-coins').textContent = coins;
    document.getElementById('profile-orders').textContent = orderCount;
    document.getElementById('profile-discount').textContent = rouletteLabel || 'Sin descuento';
}

const rouletteWheel = document.getElementById('roulette-wheel');
const rouletteOverlay = document.getElementById('roulette-overlay');
const segmentLabels = Array.from(document.querySelectorAll('.segment span'));
const spinRouletteButton = document.getElementById('spin-roulette');

document.getElementById('spin-roulette').addEventListener('click', () => {
    if (coins < 5) {
        showToast('No tienes suficientes monedas');
        return;
    }

    coins -= 5;
    localStorage.setItem('coins', coins);
    document.getElementById('coins').textContent = coins;

    const prizes = [
        { label: '10% Descuento', value: 10 },
        { label: '25% Descuento', value: 25 },
        { label: '50% Descuento', value: 50 },
        { label: '75% Descuento', value: 75 },
        { label: 'Envío Gratis', value: 0 },
        { label: 'Nada', value: 0 },
    ];
    const prizeIndex = Math.floor(Math.random() * prizes.length);
    const prize = prizes[prizeIndex];

    spinRouletteButton.disabled = true;
    rouletteWheel.style.transition = 'transform 2.2s ease-out';
    rouletteOverlay.style.transition = 'transform 2.2s ease-out';
    const segmentAngle = 30 + prizeIndex * 60;
    const targetAngle = (360 - segmentAngle) % 360;
    const spinAngle = 360 * 6 + targetAngle;
    rouletteWheel.style.transform = `rotate(${spinAngle}deg)`;
    rouletteOverlay.style.transform = `rotate(${spinAngle}deg)`;
    segmentLabels.forEach(span => {
        span.style.transition = 'transform 2.2s ease-out';
        span.style.transform = `rotate(${-spinAngle}deg)`;
    });

    setTimeout(() => {
        rouletteDiscount = prize.value;
        rouletteLabel = prize.label;
        localStorage.setItem('rouletteDiscount', rouletteDiscount);
        localStorage.setItem('rouletteLabel', rouletteLabel);
        document.getElementById('roulette-result').textContent = `Ganaste: ${prize.label}`;
        loadCart();
        spinRouletteButton.disabled = false;
        showToast(`Obtuviste ${prize.label}`);
    }, 2300);
});

// Initial load
loadProducts();