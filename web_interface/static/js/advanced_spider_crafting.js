// Advanced Spider Crafting Table Funktionen

// API-Endpunkte
const API_BASE = '/api';

// Lade die Rezepte in die Tabelle
async function loadRecipes() {
    try {
        const response = await fetch(`${API_BASE}/crafting/recipes`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Fehler beim Laden der Rezepte');
        }
        
        const container = document.getElementById('recipes-container');
        if (!container) return;
        
        container.innerHTML = '';
        
        data.data.forEach(recipe => {
            const recipeElement = document.createElement('div');
            recipeElement.className = 'recipe-card';
            recipeElement.innerHTML = `
                <h3>${recipe.name}</h3>
                <div class="materials">
                    <strong>Materialien:</strong>
                    <ul>
                        ${recipe.ingredients.map(mat => `<li>${mat.item}: ${mat.quantity}</li>`).join('')}
                    </ul>
                </div>
                <div class="result">
                    <strong>Ergebnis:</strong> ${recipe.result.item} (${recipe.result.quantity})
                </div>
                <div class="time">
                    <strong>Bearbeitungszeit:</strong> ${recipe.craftingTime / 1000} Sekunden
                </div>
                ${recipe.requirements ? `
                <div class="requirements">
                    <strong>Anforderungen:</strong>
                    <ul>
                        ${Object.entries(recipe.requirements).map(([skill, level]) => `<li>${skill}: ${level}</li>`).join('')}
                    </ul>
                </div>
                ` : ''}
                <button onclick="craftRecipe('${recipe.id}')">Herstellen</button>
            `;
            container.appendChild(recipeElement);
        });
    } catch (error) {
        console.error('Fehler beim Laden der Rezepte:', error);
        showMessage('Fehler beim Laden der Rezepte', 'error');
    }
}

// Lade das Inventar
async function loadInventory() {
    try {
        const response = await fetch(`${API_BASE}/crafting/inventory`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Fehler beim Laden des Inventars');
        }
        
        const container = document.getElementById('inventory-items');
        if (!container) return;
        
        container.innerHTML = '';
        
        data.data.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'inventory-item';
            itemElement.innerHTML = `
                <span>${item.name}: ${item.quantity}</span>
            `;
            container.appendChild(itemElement);
        });
    } catch (error) {
        console.error('Fehler beim Laden des Inventars:', error);
        showMessage('Fehler beim Laden des Inventars', 'error');
    }
}

// Lade die erzeugten Spiders
async function loadSpiders() {
    try {
        const response = await fetch(`${API_BASE}/crafting/spiders`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Fehler beim Laden der Spiders');
        }
        
        const container = document.getElementById('spiders-container');
        if (!container) return;
        
        container.innerHTML = '';
        
        if (data.data.length === 0) {
            container.innerHTML = '<p>Keine Spiders erzeugt</p>';
            return;
        }
        
        data.data.forEach(spider => {
            const spiderElement = document.createElement('div');
            spiderElement.className = 'spider-card';
            spiderElement.innerHTML = `
                <h3>${spider.name}</h3>
                <div class="spider-type">Typ: ${spider.type}</div>
                <div class="spider-level">Level: ${spider.level}</div>
                <div class="spider-skills">
                    <strong>Fähigkeiten:</strong>
                    <ul>
                        ${Object.entries(spider.skills).map(([skill, level]) => `<li>${skill}: ${level}</li>`).join('')}
                    </ul>
                </div>
                <div class="spider-abilities">
                    <strong>Fähigkeiten:</strong>
                    <ul>
                        ${spider.abilities.map(ability => `<li>${ability}</li>`).join('')}
                    </ul>
                </div>
                <div class="spider-capabilities">
                    <strong>Kapazitäten:</strong>
                    <ul>
                        ${Object.entries(spider.getCapabilities()).map(([key, value]) => 
                            `<li>${key}: ${Array.isArray(value) ? value.join(', ') : value}</li>`
                        ).join('')}
                    </ul>
                </div>
            `;
            container.appendChild(spiderElement);
        });
    } catch (error) {
        console.error('Fehler beim Laden der Spiders:', error);
        showMessage('Fehler beim Laden der Spiders', 'error');
    }
}

// Lade Spieler-Fähigkeiten
async function loadPlayerSkills() {
    try {
        const response = await fetch(`${API_BASE}/crafting/player-skills`);
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Fehler beim Laden der Spieler-Fähigkeiten');
        }
        
        const container = document.getElementById('skills-container');
        if (!container) return;
        
        container.innerHTML = '';
        
        Object.entries(data.data).forEach(([skill, level]) => {
            const skillElement = document.createElement('div');
            skillElement.className = 'skill-item';
            skillElement.innerHTML = `
                <span>${skill}: ${level}</span>
                <button onclick="upgradePlayerSkill('${skill}')">Upgrade</button>
            `;
            container.appendChild(skillElement);
        });
    } catch (error) {
        console.error('Fehler beim Laden der Spieler-Fähigkeiten:', error);
        showMessage('Fehler beim Laden der Spieler-Fähigkeiten', 'error');
    }
}

// Herstellen eines Rezepts
async function craftRecipe(recipeId) {
    try {
        const response = await fetch(`${API_BASE}/crafting/craft`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                recipe_id: recipeId
            })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Fehler beim Herstellen des Rezepts');
        }
        
        // Aktualisiere die Anzeige
        loadInventory();
        loadRecipes();
        loadSpiders();
        showMessage(`Rezept erfolgreich hergestellt!`, 'success');
    } catch (error) {
        console.error('Fehler beim Herstellen des Rezepts:', error);
        showMessage('Fehler beim Herstellen des Rezepts', 'error');
    }
}

// Upgrade einer Spieler-Fähigkeit
async function upgradePlayerSkill(skillName) {
    try {
        const response = await fetch(`${API_BASE}/crafting/upgrade-skill`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                skill_name: skillName
            })
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Fehler beim Upgrade der Fähigkeit');
        }
        
        // Aktualisiere die Anzeige
        loadPlayerSkills();
        loadRecipes();
        showMessage(`Fähigkeit ${skillName} erfolgreich geupgraded!`, 'success');
    } catch (error) {
        console.error('Fehler beim Upgrade der Fähigkeit:', error);
        showMessage('Fehler beim Upgrade der Fähigkeit', 'error');
    }
}

// Inventar zurücksetzen
async function resetInventory() {
    try {
        const response = await fetch(`${API_BASE}/crafting/reset-inventory`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.error || 'Fehler beim Zurücksetzen des Inventars');
        }
        
        // Aktualisiere die Anzeige
        loadInventory();
        showMessage('Inventar erfolgreich zurückgesetzt!', 'success');
    } catch (error) {
        console.error('Fehler beim Zurücksetzen des Inventars:', error);
        showMessage('Fehler beim Zurücksetzen des Inventars', 'error');
    }
}

// Zeige eine Statusmeldung
function showMessage(message, type = 'info') {
    const messageElement = document.getElementById('status-message');
    if (messageElement) {
        messageElement.textContent = message;
        messageElement.className = `status-message ${type}`;
        
        // Automatisch nach 5 Sekunden verschwinden lassen
        setTimeout(() => {
            messageElement.textContent = '';
            messageElement.className = 'status-message';
        }, 5000);
    }
}

// Initialisiere die Seite
document.addEventListener('DOMContentLoaded', function() {
    loadRecipes();
    loadInventory();
    loadSpiders();
    loadPlayerSkills();
});