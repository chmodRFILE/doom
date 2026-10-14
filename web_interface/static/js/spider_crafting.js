// Spider Crafting Table Funktionen

// Verfügbare Rezepte für Spiders
const spiderRecipes = [
    {
        id: 1,
        name: "Basic Spider",
        description: "Ein einfacher Spiderspawner",
        materials: [
            { item: "Web", quantity: 5 },
            { item: "Carapace", quantity: 2 }
        ],
        result: { item: "Spider", quantity: 1 },
        time: 30
    },
    {
        id: 2,
        name: "Speed Spider",
        description: "Ein schneller Spiderspawner",
        materials: [
            { item: "Web", quantity: 8 },
            { item: "Carapace", quantity: 3 },
            { item: "Speed Potion", quantity: 1 }
        ],
        result: { item: "Speed Spider", quantity: 1 },
        time: 60
    },
    {
        id: 3,
        name: "Poison Spider",
        description: "Ein giftiger Spiderspawner",
        materials: [
            { item: "Web", quantity: 10 },
            { item: "Carapace", quantity: 4 },
            { item: "Poison Extract", quantity: 2 }
        ],
        result: { item: "Poison Spider", quantity: 1 },
        time: 90
    },
    {
        id: 4,
        name: "Armored Spider",
        description: "Ein gepanzerter Spiderspawner",
        materials: [
            { item: "Web", quantity: 15 },
            { item: "Carapace", quantity: 6 },
            { item: "Iron Ingot", quantity: 3 }
        ],
        result: { item: "Armored Spider", quantity: 1 },
        time: 120
    },
    {
        id: 5,
        name: "Giant Spider",
        description: "Ein riesiger Spiderspawner",
        materials: [
            { item: "Web", quantity: 20 },
            { item: "Carapace", quantity: 8 },
            { item: "Giant Essence", quantity: 1 }
        ],
        result: { item: "Giant Spider", quantity: 1 },
        time: 180
    }
];

// Verfügbares Inventar
let inventory = [
    { item: "Web", quantity: 50 },
    { item: "Carapace", quantity: 30 },
    { item: "Speed Potion", quantity: 5 },
    { item: "Poison Extract", quantity: 8 },
    { item: "Iron Ingot", quantity: 12 },
    { item: "Giant Essence", quantity: 2 }
];

// Lade die Rezepte in die Tabelle
function loadRecipes() {
    const container = document.getElementById('recipes-container');
    
    if (!container) return;
    
    container.innerHTML = '';
    
    spiderRecipes.forEach(recipe => {
        const recipeElement = document.createElement('div');
        recipeElement.className = 'recipe-card';
        recipeElement.innerHTML = `
            <h3>${recipe.name}</h3>
            <p class="description">${recipe.description}</p>
            <div class="materials">
                <strong>Materialien:</strong>
                <ul>
                    ${recipe.materials.map(mat => `<li>${mat.item}: ${mat.quantity}</li>`).join('')}
                </ul>
            </div>
            <div class="result">
                <strong>Ergebnis:</strong> ${recipe.result.item} (${recipe.result.quantity})
            </div>
            <div class="time">
                <strong>Bearbeitungszeit:</strong> ${recipe.time} Sekunden
            </div>
            <button onclick="craftRecipe(${recipe.id})">Herstellen</button>
        `;
        container.appendChild(recipeElement);
    });
}

// Lade das Inventar
function loadInventory() {
    const container = document.getElementById('inventory-items');
    
    if (!container) return;
    
    container.innerHTML = '';
    
    inventory.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'inventory-item';
        itemElement.innerHTML = `
            <span>${item.item}: ${item.quantity}</span>
        `;
        container.appendChild(itemElement);
    });
}

// Herstellen eines Rezepts
function craftRecipe(recipeId) {
    const recipe = spiderRecipes.find(r => r.id === recipeId);
    
    if (!recipe) {
        showMessage('Rezept nicht gefunden!', 'error');
        return;
    }
    
    // Prüfe, ob genügend Materialien vorhanden sind
    const hasMaterials = recipe.materials.every(material => {
        const inventoryItem = inventory.find(item => item.item === material.item);
        return inventoryItem && inventoryItem.quantity >= material.quantity;
    });
    
    if (!hasMaterials) {
        showMessage('Nicht genügend Materialien!', 'error');
        return;
    }
    
    // Verbrauche Materialien
    recipe.materials.forEach(material => {
        const inventoryItem = inventory.find(item => item.item === material.item);
        if (inventoryItem) {
            inventoryItem.quantity -= material.quantity;
        }
    });
    
    // Füge Ergebnis hinzu
    const resultItem = inventory.find(item => item.item === recipe.result.item);
    if (resultItem) {
        resultItem.quantity += recipe.result.quantity;
    } else {
        inventory.push({ item: recipe.result.item, quantity: recipe.result.quantity });
    }
    
    // Aktualisiere die Anzeige
    loadInventory();
    showMessage(`Rezept ${recipe.name} erfolgreich hergestellt!`, 'success');
}

// Alle Rezepte herstellen
function craftAllRecipes() {
    showMessage('Alle Rezepte werden hergestellt...', 'info');
    
    // In diesem Beispiel: Herstellung aller Rezepte mit genügend Materialien
    spiderRecipes.forEach(recipe => {
        const hasMaterials = recipe.materials.every(material => {
            const inventoryItem = inventory.find(item => item.item === material.item);
            return inventoryItem && inventoryItem.quantity >= material.quantity;
        });
        
        if (hasMaterials) {
            // Verbrauche Materialien
            recipe.materials.forEach(material => {
                const inventoryItem = inventory.find(item => item.item === material.item);
                if (inventoryItem) {
                    inventoryItem.quantity -= material.quantity;
                }
            });
            
            // Füge Ergebnis hinzu
            const resultItem = inventory.find(item => item.item === recipe.result.item);
            if (resultItem) {
                resultItem.quantity += recipe.result.quantity;
            } else {
                inventory.push({ item: recipe.result.item, quantity: recipe.result.quantity });
            }
        }
    });
    
    loadInventory();
    showMessage('Alle Rezepte hergestellt!', 'success');
}

// Inventar zurücksetzen
function resetInventory() {
    if (confirm('Möchtest du wirklich das Inventar zurücksetzen?')) {
        inventory = [
            { item: "Web", quantity: 50 },
            { item: "Carapace", quantity: 30 },
            { item: "Speed Potion", quantity: 5 },
            { item: "Poison Extract", quantity: 8 },
            { item: "Iron Ingot", quantity: 12 },
            { item: "Giant Essence", quantity: 2 }
        ];
        loadInventory();
        showMessage('Inventar zurückgesetzt!', 'success');
    }
}

// Statusmeldung anzeigen
function showMessage(message, type) {
    const statusElement = document.getElementById('status-message');
    
    if (!statusElement) return;
    
    statusElement.textContent = message;
    statusElement.className = `status-message ${type}`;
    
    // Lösche die Nachricht nach 3 Sekunden
    setTimeout(() => {
        statusElement.textContent = '';
        statusElement.className = 'status-message';
    }, 3000);
}