// Spider Crafting System for Webserver

// Base crafting recipe class
export class CraftingRecipe {
  constructor(id, name, ingredients, result, craftingTime = 1000) {
    this.id = id;
    this.name = name;
    this.ingredients = ingredients; // Array of {item, quantity}
    this.result = result; // {item, quantity}
    this.craftingTime = craftingTime; // Time in milliseconds
    this.category = 'spider';
  }

  canCraft(inventory) {
    // Check if player has all required ingredients
    for (const ingredient of this.ingredients) {
      const item = inventory.find(i => i.name === ingredient.item);
      if (!item || item.quantity < ingredient.quantity) {
        return false;
      }
    }
    return true;
  }

  craft(inventory) {
    if (!this.canCraft(inventory)) {
      return { success: false, error: 'Insufficient ingredients' };
    }

    // Deduct ingredients from inventory
    for (const ingredient of this.ingredients) {
      const item = inventory.find(i => i.name === ingredient.item);
      item.quantity -= ingredient.quantity;
    }

    // Add result to inventory
    const resultItem = inventory.find(i => i.name === this.result.item);
    if (resultItem) {
      resultItem.quantity += this.result.quantity;
    } else {
      inventory.push({ ...this.result });
    }

    return { 
      success: true, 
      recipe: this,
      result: this.result
    };
  }
}

// Spider crafting recipes
export class SpiderCraftingRecipes {
  constructor() {
    this.recipes = new Map();
    this.initRecipes();
  }

  initRecipes() {
    // Basic spider crafting recipes
    const recipes = [
      // Spider Web Crafting
      new CraftingRecipe(
        'spider_web_1',
        'Spider Web',
        [
          { item: 'string', quantity: 4 },
          { item: 'spider_eye', quantity: 2 }
        ],
        { item: 'spider_web', quantity: 1 },
        2000
      ),

      // Spider Leg Crafting
      new CraftingRecipe(
        'spider_leg_1',
        'Spider Leg',
        [
          { item: 'spider_leg', quantity: 4 },
          { item: 'string', quantity: 1 }
        ],
        { item: 'spider_leg_piece', quantity: 1 },
        1500
      ),

      // Poisonous Spider Crafting
      new CraftingRecipe(
        'poison_spider_1',
        'Poisonous Spider',
        [
          { item: 'spider_eye', quantity: 3 },
          { item: 'poison', quantity: 2 },
          { item: 'string', quantity: 1 }
        ],
        { item: 'poisonous_spider', quantity: 1 },
        3000
      ),

      // Spider Armor Crafting
      new CraftingRecipe(
        'spider_armor_1',
        'Spider Armor',
        [
          { item: 'spider_leg', quantity: 8 },
          { item: 'spider_web', quantity: 4 },
          { item: 'leather', quantity: 2 }
        ],
        { item: 'spider_armor', quantity: 1 },
        5000
      ),

      // Spider Bow Crafting
      new CraftingRecipe(
        'spider_bow_1',
        'Spider Bow',
        [
          { item: 'spider_leg', quantity: 6 },
          { item: 'string', quantity: 3 },
          { item: 'wood', quantity: 4 }
        ],
        { item: 'spider_bow', quantity: 1 },
        4000
      ),

      // Spider Sword Crafting
      new CraftingRecipe(
        'spider_sword_1',
        'Spider Sword',
        [
          { item: 'spider_leg', quantity: 5 },
          { item: 'spider_eye', quantity: 2 },
          { item: 'iron_ingot', quantity: 3 }
        ],
        { item: 'spider_sword', quantity: 1 },
        4500
      ),

      // Spider Trap Crafting
      new CraftingRecipe(
        'spider_trap_1',
        'Spider Trap',
        [
          { item: 'spider_web', quantity: 3 },
          { item: 'wood', quantity: 2 },
          { item: 'stone', quantity: 2 }
        ],
        { item: 'spider_trap', quantity: 1 },
        3500
      )
    ];

    recipes.forEach(recipe => {
      this.recipes.set(recipe.id, recipe);
    });
  }

  getRecipe(id) {
    return this.recipes.get(id) || null;
  }

  getAllRecipes() {
    return Array.from(this.recipes.values());
  }

  getRecipesByCategory(category) {
    return Array.from(this.recipes.values()).filter(recipe => recipe.category === category);
  }

  searchRecipes(query) {
    const lowerQuery = query.toLowerCase();
    return Array.from(this.recipes.values()).filter(recipe => 
      recipe.name.toLowerCase().includes(lowerQuery) ||
      recipe.ingredients.some(ing => ing.item.toLowerCase().includes(lowerQuery)) ||
      recipe.result.item.toLowerCase().includes(lowerQuery)
    );
  }
}

// Crafting table class
export class CraftingTable {
  constructor() {
    this.recipes = new SpiderCraftingRecipes();
    this.inventory = [];
    this.craftingQueue = [];
  }

  // Add item to inventory
  addItem(itemName, quantity = 1) {
    const existingItem = this.inventory.find(i => i.name === itemName);
    if (existingItem) {
      existingItem.quantity += quantity;
    } else {
      this.inventory.push({ name: itemName, quantity });
    }
  }

  // Remove item from inventory
  removeItem(itemName, quantity = 1) {
    const item = this.inventory.find(i => i.name === itemName);
    if (item && item.quantity >= quantity) {
      item.quantity -= quantity;
      if (item.quantity <= 0) {
        this.inventory = this.inventory.filter(i => i.name !== itemName);
      }
      return true;
    }
    return false;
  }

  // Check if can craft recipe
  canCraft(recipeId) {
    const recipe = this.recipes.getRecipe(recipeId);
    if (!recipe) return false;
    
    return recipe.canCraft(this.inventory);
  }

  // Craft an item
  craftItem(recipeId) {
    const recipe = this.recipes.getRecipe(recipeId);
    if (!recipe) {
      return { success: false, error: 'Recipe not found' };
    }

    return recipe.craft(this.inventory);
  }

  // Get crafting queue status
  getCraftingQueue() {
    return this.craftingQueue;
  }

  // Add to crafting queue
  addToQueue(recipeId, quantity = 1) {
    const recipe = this.recipes.getRecipe(recipeId);
    if (!recipe) {
      return { success: false, error: 'Recipe not found' };
    }

    const item = {
      id: Date.now() + Math.random(),
      recipeId,
      recipe,
      quantity,
      startTime: Date.now(),
      status: 'queued'
    };

    this.craftingQueue.push(item);
    return { success: true, item };
  }

  // Get inventory
  getInventory() {
    return this.inventory;
  }

  // Get available recipes
  getAvailableRecipes() {
    return this.recipes.getAllRecipes().filter(recipe => recipe.canCraft(this.inventory));
  }
}

// Export singleton instance
export const spiderCraftingSystem = new CraftingTable();