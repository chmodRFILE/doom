// Crafting model for spider crafting table
export class CraftingModel {
  constructor() {
    this.recipes = [];
    this.inventory = [];
    this.craftingQueue = [];
    this.unlockedRecipes = new Set();
  }

  // Initialize with default recipes
  initDefaultRecipes() {
    const defaultRecipes = [
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
        description: 'Craft a spider web from string and spider eyes'
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
        description: 'Craft a spider leg piece'
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
        description: 'Create a poisonous spider variant'
      }
    ];

    this.recipes = defaultRecipes;
    // Unlock first recipe by default
    this.unlockedRecipes.add('spider_web_1');
  }

  // Get all recipes
  getAllRecipes() {
    return this.recipes;
  }

  // Get unlocked recipes
  getUnlockedRecipes() {
    return this.recipes.filter(recipe => this.unlockedRecipes.has(recipe.id));
  }

  // Unlock a recipe
  unlockRecipe(recipeId) {
    this.unlockedRecipes.add(recipeId);
    return true;
  }

  // Check if player can craft a recipe
  canCraft(recipeId, inventory) {
    const recipe = this.recipes.find(r => r.id === recipeId);
    if (!recipe) return false;

    // Check ingredients
    for (const ingredient of recipe.ingredients) {
      const item = inventory.find(i => i.name === ingredient.item);
      if (!item || item.quantity < ingredient.quantity) {
        return false;
      }
    }
    return true;
  }

  // Craft an item
  craftItem(recipeId, inventory) {
    const recipe = this.recipes.find(r => r.id === recipeId);
    if (!recipe) {
      return { success: false, error: 'Recipe not found' };
    }

    // Check if player can craft
    if (!this.canCraft(recipeId, inventory)) {
      return { success: false, error: 'Insufficient ingredients' };
    }

    // Deduct ingredients
    for (const ingredient of recipe.ingredients) {
      const item = inventory.find(i => i.name === ingredient.item);
      item.quantity -= ingredient.quantity;
    }

    // Add result
    const resultItem = inventory.find(i => i.name === recipe.result.item);
    if (resultItem) {
      resultItem.quantity += recipe.result.quantity;
    } else {
      inventory.push({ ...recipe.result });
    }

    return { 
      success: true, 
      recipe,
      result: recipe.result
    };
  }

  // Get inventory
  getInventory() {
    return this.inventory;
  }

  // Update inventory
  updateInventory(items) {
    this.inventory = items;
  }
}