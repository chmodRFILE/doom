// Main crafting table application with PHP-like functionality
import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'static')));
app.use(express.urlencoded({ extended: true }));

// Simulate PHP-like functionality with JavaScript classes
class SpiderCraftingFramework {
    constructor() {
        this.inventory = [];
        this.recipes = [];
        this.unlockedRecipes = new Set();
        this.craftingHistory = [];
        this.sessionId = this.generateSessionId();
        this.init();
    }

    // Generate session ID (like PHP session_id())
    generateSessionId() {
        return 'spider_craft_' + Math.random().toString(36).substr(2, 9);
    }

    init() {
        this.loadDefaultRecipes();
        this.loadInventory();
    }

    loadDefaultRecipes() {
        // Simulate loading from database or config file (like PHP includes)
        this.recipes = [
            {
                id: 'spider_web_1',
                name: 'Spider Web',
                ingredients: [
                    { item: 'string', quantity: 4 },
                    { item: 'spider_eye', quantity: 2 }
                ],
                result: { item: 'spider_web', quantity: 1 },
                craftingTime: 2000,
                category: 'spider',
                description: 'Craft a spider web from string and spider eyes',
                difficulty: 'Easy'
            },
            {
                id: 'spider_leg_1',
                name: 'Spider Leg',
                ingredients: [
                    { item: 'spider_leg', quantity: 4 },
                    { item: 'string', quantity: 1 }
                ],
                result: { item: 'spider_leg_piece', quantity: 1 },
                craftingTime: 1500,
                category: 'spider',
                description: 'Craft a spider leg piece',
                difficulty: 'Easy'
            },
            {
                id: 'poison_spider_1',
                name: 'Poisonous Spider',
                ingredients: [
                    { item: 'spider_eye', quantity: 3 },
                    { item: 'poison', quantity: 2 },
                    { item: 'string', quantity: 1 }
                ],
                result: { item: 'poisonous_spider', quantity: 1 },
                craftingTime: 3000,
                category: 'spider',
                description: 'Create a poisonous spider variant',
                difficulty: 'Medium'
            },
            {
                id: 'spider_armor_1',
                name: 'Spider Armor',
                ingredients: [
                    { item: 'spider_leg', quantity: 8 },
                    { item: 'spider_web', quantity: 4 },
                    { item: 'leather', quantity: 2 }
                ],
                result: { item: 'spider_armor', quantity: 1 },
                craftingTime: 5000,
                category: 'spider',
                description: 'Craft spider armor from spider parts',
                difficulty: 'Hard'
            },
            {
                id: 'spider_bow_1',
                name: 'Spider Bow',
                ingredients: [
                    { item: 'spider_leg', quantity: 6 },
                    { item: 'string', quantity: 3 },
                    { item: 'wood', quantity: 4 }
                ],
                result: { item: 'spider_bow', quantity: 1 },
                craftingTime: 4000,
                category: 'spider',
                description: 'Craft a powerful spider bow',
                difficulty: 'Hard'
            }
        ];

        // Unlock first recipe by default
        this.unlockedRecipes.add('spider_web_1');
    }

    loadInventory() {
        // Simulate loading from database or session (like PHP $_SESSION)
        this.inventory = [
            { name: 'string', quantity: 10 },
            { name: 'spider_eye', quantity: 5 },
            { name: 'spider_leg', quantity: 8 },
            { name: 'wood', quantity: 3 }
        ];
    }

    // PHP-like function to check if user can craft
    canCraft(recipeId) {
        const recipe = this.recipes.find(r => r.id === recipeId);
        if (!recipe) return false;

        for (const ingredient of recipe.ingredients) {
            const item = this.inventory.find(i => i.name === ingredient.item);
            if (!item || item.quantity < ingredient.quantity) {
                return false;
            }
        }
        return true;
    }

    // PHP-like crafting function
    craftItem(recipeId, inventory = null) {
        if (inventory) {
            this.inventory = inventory;
        }

        const recipe = this.recipes.find(r => r.id === recipeId);
        if (!recipe) {
            return { success: false, error: 'Recipe not found' };
        }

        if (!this.canCraft(recipeId)) {
            return { success: false, error: 'Insufficient ingredients' };
        }

        // Deduct ingredients
        for (const ingredient of recipe.ingredients) {
            const item = this.inventory.find(i => i.name === ingredient.item);
            item.quantity -= ingredient.quantity;
        }

        // Add result
        const resultItem = this.inventory.find(i => i.name === recipe.result.item);
        if (resultItem) {
            resultItem.quantity += recipe.result.quantity;
        } else {
            this.inventory.push({ ...recipe.result });
        }

        // Log crafting history
        this.craftingHistory.push({
            recipeId: recipe.id,
            timestamp: new Date(),
            result: recipe.result
        });

        return { 
            success: true, 
            recipe,
            result: recipe.result,
            inventory: this.inventory
        };
    }

    // PHP-like session management
    getSessionId() {
        return this.sessionId;
    }

    // PHP-like function to get all recipes
    getAllRecipes() {
        return Array.from(this.recipes);
    }

    // PHP-like function to get unlocked recipes
    getUnlockedRecipes() {
        return this.recipes.filter(recipe => this.unlockedRecipes.has(recipe.id));
    }

    // PHP-like function to unlock recipe
    unlockRecipe(recipeId) {
        this.unlockedRecipes.add(recipeId);
        return true;
    }
}

// Create global crafting framework instance (like PHP global variables)
const spiderCraftingFramework = new SpiderCraftingFramework();

// Routes - Simulating PHP-style routing
app.get('/crafting-table', (req, res) => {
    // PHP-like $_GET handling
    const { action = 'view' } = req.query;
    
    // Set response headers like PHP
    res.setHeader('Content-Type', 'text/html');
    res.setHeader('X-Powered-By', 'Doom Web Framework');
    
    // Simulate PHP include for template
    const templatePath = path.join(__dirname, 'templates', 'spider_crafting_frame.html');
    
    fs.readFile(templatePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Template not found');
        }
        
        // PHP-like variable replacement
        let html = data;
        html = html.replace('{{session_id}}', spiderCraftingFramework.getSessionId());
        html = html.replace('{{recipe_count}}', spiderCraftingFramework.recipes.length);
        html = html.replace('{{inventory_count}}', spiderCraftingFramework.inventory.length);
        
        res.send(html);
    });
});

// PHP-like API endpoints
app.get('/crafting/api/recipes', (req, res) => {
    // Simulate PHP $_GET and JSON response
    const unlockedOnly = req.query.unlocked === 'true';
    
    let recipes = spiderCraftingFramework.getAllRecipes();
    if (unlockedOnly) {
        recipes = spiderCraftingFramework.getUnlockedRecipes();
    }
    
    res.json({
        success: true,
        session_id: spiderCraftingFramework.getSessionId(),
        recipes: recipes,
        count: recipes.length
    });
});

app.post('/crafting/api/craft', (req, res) => {
    // PHP-like $_POST handling
    const { recipeId, inventory } = req.body;
    
    if (!recipeId) {
        return res.status(400).json({
            success: false,
            error: 'Recipe ID is required'
        });
    }
    
    const result = spiderCraftingFramework.craftItem(recipeId, inventory);
    
    if (result.success) {
        res.json({
            success: true,
            message: 'Crafting successful',
            result: result.result,
            inventory: result.inventory
        });
    } else {
        res.status(400).json({
            success: false,
            error: result.error
        });
    }
});

app.post('/crafting/api/unlock', (req, res) => {
    // PHP-like $_POST handling
    const { recipeId } = req.body;
    
    if (!recipeId) {
        return res.status(400).json({
            success: false,
            error: 'Recipe ID is required'
        });
    }

    const unlocked = spiderCraftingFramework.unlockRecipe(recipeId);
    
    res.json({
        success: true,
        message: 'Recipe unlocked',
        unlocked: unlocked
    });
});

// PHP-like file upload handling (simplified)
app.post('/crafting/api/upload', (req, res) => {
    // Simulate PHP $_FILES handling
    res.json({
        success: true,
        message: 'File uploaded successfully',
        session_id: spiderCraftingFramework.getSessionId()
    });
});

// PHP-like error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({
        success: false,
        error: 'Internal server error'
    });
});

export default app;