async function searchLaptops(query) {
    const response = await fetch(`/api/laptops/search?q=${encodeURIComponent(query)}`);
    const laptops = await response.json();
    updateLaptopList(laptops);
}

async function filterLaptops(filters) {
    const queryParams = new URLSearchParams(filters);
    const response = await fetch(`/api/laptops/filter?${queryParams}`);
    const laptops = await response.json();
    updateLaptopList(laptops);
}

async function getLaptopStats() {
    const response = await fetch('/api/laptops/stats');
    const stats = await response.json();
    updateStats(stats);
}

function updateLaptopList(laptops) {
    const container = document.querySelector('.laptop-grid');
    container.innerHTML = laptops.map(laptop => `
        <div class="laptop-card">
            <h2>${laptop.name}</h2>
            <p class="brand">${laptop.brand}</p>
            <p class="price">$${laptop.price}</p>
            <div class="specs">
                <h3>Specifications:</h3>
                <ul>
                    ${Object.entries(laptop.specs).map(([key, value]) => 
                        `<li><strong>${key}:</strong> ${value}</li>`
                    ).join('')}
                </ul>
            </div>
        </div>
    `).join('');
}

function updateStats(stats) {
    const statsContainer = document.querySelector('.stats-container');
    if (statsContainer) {
        statsContainer.innerHTML = stats.map(stat => `
            <div class="stat-card">
                <h3>${stat._id}</h3>
                <p>Count: ${stat.count}</p>
                <p>Average Price: $${stat.avg_price.toFixed(2)}</p>
                <p>Price Range: $${stat.min_price} - $${stat.max_price}</p>
            </div>
        `).join('');
    }
} 