// Products data
const products = [
    { id: 1, name: 'Labial Mate Premium', price: 25, discount: 10, image: 'https://via.placeholder.com/150?text=Labial', category: 'maquillaje', rating: 5 },
    { id: 2, name: 'Base Líquida Nude', price: 40, discount: 15, image: 'https://via.placeholder.com/150?text=Base', category: 'maquillaje', rating: 4 },
    { id: 3, name: 'Sombras de Ojos Palette', price: 35, discount: 20, image: 'https://via.placeholder.com/150?text=Sombras', category: 'maquillaje', rating: 5 },
    { id: 4, name: 'Tacones Elegantes', price: 80, discount: 25, image: 'https://via.placeholder.com/150?text=Tacones', category: 'zapatos', rating: 4 },
    { id: 5, name: 'Sneakers Blancos', price: 60, discount: 10, image: 'https://via.placeholder.com/150?text=Sneakers', category: 'zapatos', rating: 5 },
    { id: 6, name: 'Botas de Cuero', price: 100, discount: 30, image: 'https://via.placeholder.com/150?text=Botas', category: 'zapatos', rating: 4 }
];

let cart = JSON.parse(localStorage.getItem('cart')) || [];
let coins = parseInt(localStorage.getItem('coins')) || 0;

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
    cart.push(product);
    localStorage.setItem('cart', JSON.stringify(cart));
    alert('Producto agregado al carrito');
    showScreen('home');
});

// Load Cart
function loadCart() {
    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    let total = 0;
    cart.forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        itemDiv.innerHTML = `
            <span>${item.name}</span>
            <span>$${item.price - item.discount}</span>
            <button onclick="removeFromCart(${index})">Eliminar</button>
        `;
        cartItems.appendChild(itemDiv);
        total += item.price - item.discount;
    });
    document.getElementById('total').textContent = total;
}

// Remove from Cart
function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    loadCart();
}

// Apply Coupon
document.getElementById('apply-coupon').addEventListener('click', () => {
    const coupon = document.getElementById('coupon').value;
    if (coupon === 'DESC10') {
        const total = parseFloat(document.getElementById('total').textContent);
        document.getElementById('total').textContent = (total * 0.9).toFixed(2);
        alert('Cupón aplicado: 10% descuento');
    } else {
        alert('Cupón inválido');
    }
});

// Checkout
document.getElementById('checkout').addEventListener('click', () => {
    alert('Procediendo al pago...');
});

// Rewards
document.getElementById('coins').textContent = coins;

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

document.getElementById('spin-roulette').addEventListener('click', () => {
    if (coins >= 5) {
        coins -= 5;
        localStorage.setItem('coins', coins);
        document.getElementById('coins').textContent = coins;
        const prizes = ['10% Descuento', 'Envío Gratis', 'Producto Gratis', 'Nada'];
        const prize = prizes[Math.floor(Math.random() * prizes.length)];
        document.getElementById('roulette-result').textContent = `Ganaste: ${prize}`;
    } else {
        alert('No tienes suficientes monedas');
    }
});

// Initial load
if (document.getElementById('home').classList.contains('active')) {
    loadProducts();
}