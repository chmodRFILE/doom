// Advanced Spider Crafting System for Webserver

// Base crafting recipe class
export class CraftingRecipe {
  constructor(id, name, ingredients, result, craftingTime = 1000, requirements = {}) {
    this.id = id;
    this.name = name;
    this.ingredients = ingredients; // Array of {item, quantity}
    this.result = result; // {item, quantity}
    this.craftingTime = craftingTime; // Time in milliseconds
    this.category = 'spider';
    this.requirements = requirements; // Additional requirements like skills, level, etc.
  }

  canCraft(inventory, playerSkills = {}) {
    // Check if player has all required ingredients
    for (const ingredient of this.ingredients) {
      const item = inventory.find(i => i.name === ingredient.item);
      if (!item || item.quantity < ingredient.quantity) {
        return false;
      }
    }

    // Check additional requirements
    for (const [skill, requiredLevel] of Object.entries(this.requirements)) {
      if ((playerSkills[skill] || 0) < requiredLevel) {
        return false;
      }
    }
    
    return true;
  }

  craft(inventory) {
    if (!this.canCraft(inventory)) {
      return { success: false, error: 'Insufficient ingredients or requirements' };
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

// Spider class with enhanced capabilities
export class AdvancedSpider {
  constructor(id, name, type, level = 1, skills = {}, abilities = []) {
    this.id = id;
    this.name = name;
    this.type = type; // basic, advanced, specialized
    this.level = level;
    this.skills = skills; // {scraping: 5, analysis: 3, proxy: 2}
    this.abilities = abilities; // List of special abilities
    this.maxInventory = 100;
    this.currentInventory = [];
    this.craftingQueue = [];
  }

  addSkill(skillName, level) {
    this.skills[skillName] = level;
  }

  addAbility(ability) {
    this.abilities.push(ability);
  }

  getCraftingRequirements() {
    return {
      skills: this.skills,
      level: this.level
    };
  }

  // Get spider's effective capabilities based on skills and abilities
  getCapabilities() {
    const capabilities = {
      level: this.level,
      type: this.type,
      skills: { ...this.skills },
      abilities: [...this.abilities],
      maxInventory: this.maxInventory
    };

    // Calculate effective capabilities based on skills
    if (this.skills.scraping) {
      capabilities.effectiveScraping = Math.floor(this.skills.scraping * 1.5);
    }
    
    if (this.skills.proxy) {
      capabilities.effectiveProxy = Math.floor(this.skills.proxy * 2);
    }

    return capabilities;
  }
}

// Spider crafting recipes with enhanced features
export class AdvancedSpiderCraftingRecipes {
  constructor() {
    this.recipes = new Map();
    this.initRecipes();
  }

  initRecipes() {
    // Basic spider crafting recipes
    const recipes = [
      // Enhanced Spider Web Crafting
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

      // Advanced Spider Armor Crafting
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
      ),

      // Advanced Spider Crafting (requires higher skills)
      new CraftingRecipe(
        'advanced_spider_1',
        'Advanced Spider',
        [
          { item: 'spider_leg', quantity: 10 },
          { item: 'spider_eye', quantity: 5 },
          { item: 'steel_ingot', quantity: 3 }
        ],
        { item: 'advanced_spider', quantity: 1 },
        6000,
        { scraping: 3, proxy: 2 }
      ),

      // Specialized Data Extraction Spider
      new CraftingRecipe(
        'data_spider_1',
        'Data Extraction Spider',
        [
          { item: 'spider_web', quantity: 5 },
          { item: 'electronic_parts', quantity: 4 },
          { item: 'processor_chip', quantity: 2 }
        ],
        { item: 'data_extraction_spider', quantity: 1 },
        8000,
        { scraping: 5, analysis: 3 }
      ),

      // Proxy Rotation Spider
      new CraftingRecipe(
        'proxy_spider_1',
        'Proxy Rotation Spider',
        [
          { item: 'spider_leg', quantity: 8 },
          { item: 'network_cable', quantity: 3 },
          { item: 'router', quantity: 1 }
        ],
        { item: 'proxy_rotation_spider', quantity: 1 },
        7000,
        { proxy: 4, networking: 2 }
      ),

      // Multi-Stage Spider
      new CraftingRecipe(
        'multi_stage_spider_1',
        'Multi-Stage Spider',
        [
          { item: 'spider_web', quantity: 8 },
          { item: 'spider_leg', quantity: 12 },
          { item: 'advanced_circuit', quantity: 3 }
        ],
        { item: 'multi_stage_spider', quantity: 1 },
        10000,
        { scraping: 6, proxy: 4, analysis: 5 }
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

// Advanced crafting table class
export class AdvancedCraftingTable {
  constructor() {
    this.recipes = new AdvancedSpiderCraftingRecipes();
    this.inventory = [];
    this.spiders = []; // Collection of created spiders
    this.craftingQueue = [];
    this.playerSkills = {
      scraping: 1,
      analysis: 1,
      proxy: 1,
      networking: 1
    };
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
    
    return recipe.canCraft(this.inventory, this.playerSkills);
  }

  // Craft an item (can be a spider or other item)
  craftItem(recipeId) {
    const recipe = this.recipes.getRecipe(recipeId);
    if (!recipe) {
      return { success: false, error: 'Recipe not found' };
    }

    // Check if we can craft
    if (!recipe.canCraft(this.inventory, this.playerSkills)) {
      return { success: false, error: 'Insufficient ingredients or requirements' };
    }

    // Deduct ingredients from inventory
    for (const ingredient of recipe.ingredients) {
      const item = this.inventory.find(i => i.name === ingredient.item);
      if (item) {
        item.quantity -= ingredient.quantity;
        if (item.quantity <= 0) {
          this.inventory = this.inventory.filter(i => i.name !== ingredient.item);
        }
      }
    }

    // Create result
    const resultItem = recipe.result.item;
    
    // If it's a spider, create an AdvancedSpider instance
    if (resultItem.includes('spider')) {
      const spider = new AdvancedSpider(
        `${resultItem}_${Date.now()}`,
        recipe.name,
        this.getSpiderType(resultItem),
        1,
        { ...this.playerSkills }
      );
      
      // Add special abilities based on the spider type
      if (resultItem.includes('data_extraction')) {
        spider.addAbility('Data Extraction');
        spider.addSkill('analysis', 3);
      } else if (resultItem.includes('proxy_rotation')) {
        spider.addAbility('Proxy Rotation');
        spider.addSkill('proxy', 4);
      } else if (resultItem.includes('multi_stage')) {
        spider.addAbility('Multi-Stage Processing');
        spider.addSkill('scraping', 6);
      }
      
      this.spiders.push(spider);
      return { 
        success: true, 
        recipe: recipe,
        result: { type: 'spider', spider: spider }
      };
    } else {
      // Regular item crafting
      const existingItem = this.inventory.find(i => i.name === resultItem);
      if (existingItem) {
        existingItem.quantity += recipe.result.quantity;
      } else {
        this.inventory.push({ ...recipe.result });
      }
      
      return { 
        success: true, 
        recipe: recipe,
        result: { type: 'item', item: resultItem }
      };
    }
  }

  // Get spider type based on item name
  getSpiderType(itemName) {
    if (itemName.includes('advanced')) return 'advanced';
    if (itemName.includes('data_extraction')) return 'specialized';
    if (itemName.includes('proxy_rotation')) return 'specialized';
    if (itemName.includes('multi_stage')) return 'specialized';
    return 'basic';
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
    return this.recipes.getAllRecipes().filter(recipe => recipe.canCraft(this.inventory, this.playerSkills));
  }

  // Get all spiders
  getAllSpiders() {
    return this.spiders;
  }

  // Get spider capabilities for display
  getSpiderCapabilities(spiderId) {
    const spider = this.spiders.find(s => s.id === spiderId);
    if (spider) {
      return spider.getCapabilities();
    }
    return null;
  }

  // Upgrade a spider's skills
  upgradeSpiderSkill(spiderId, skillName, amount = 1) {
    const spider = this.spiders.find(s => s.id === spiderId);
    if (spider) {
      if (!spider.skills[skillName]) {
        spider.skills[skillName] = 0;
      }
      spider.skills[skillName] += amount;
      return { success: true, spider: spider };
    }
    return { success: false, error: 'Spider not found' };
  }

  // Get player skills
  getPlayerSkills() {
    return this.playerSkills;
  }

  // Upgrade player skills
  upgradePlayerSkill(skillName, amount = 1) {
    if (!this.playerSkills[skillName]) {
      this.playerSkills[skillName] = 0;
    }
    this.playerSkills[skillName] += amount;
    return { success: true, skills: this.playerSkills };
  }
}

// Export singleton instance
export const advancedSpiderCraftingSystem = new AdvancedCraftingTable();