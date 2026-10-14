// Crafting routes for spider crafting table
import { Router } from 'express';
import { CraftingModel } from '../models/crafting_model.js';

const router = Router();
const craftingModel = new CraftingModel();

// Initialize default recipes
craftingModel.initDefaultRecipes();

// Get all available recipes
router.get('/recipes', (req, res) => {
  try {
    const recipes = craftingModel.getUnlockedRecipes();
    res.json({
      success: true,
      recipes: recipes
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get inventory
router.get('/inventory', (req, res) => {
  try {
    const inventory = craftingModel.getInventory();
    res.json({
      success: true,
      inventory: inventory
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Craft an item
router.post('/craft', (req, res) => {
  try {
    const { recipeId, inventory } = req.body;
    
    if (!recipeId) {
      return res.status(400).json({
        success: false,
        error: 'Recipe ID is required'
      });
    }

    // Update inventory in model
    craftingModel.updateInventory(inventory || []);
    
    const result = craftingModel.craftItem(recipeId, craftingModel.getInventory());
    
    if (result.success) {
      res.json({
        success: true,
        message: 'Crafting successful',
        result: result.result,
        inventory: craftingModel.getInventory()
      });
    } else {
      res.status(400).json({
        success: false,
        error: result.error
      });
    }
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Unlock a recipe
router.post('/unlock', (req, res) => {
  try {
    const { recipeId } = req.body;
    
    if (!recipeId) {
      return res.status(400).json({
        success: false,
        error: 'Recipe ID is required'
      });
    }

    const unlocked = craftingModel.unlockRecipe(recipeId);
    
    res.json({
      success: true,
      message: 'Recipe unlocked',
      unlocked: unlocked
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Check if can craft
router.post('/can-craft', (req, res) => {
  try {
    const { recipeId, inventory } = req.body;
    
    if (!recipeId) {
      return res.status(400).json({
        success: false,
        error: 'Recipe ID is required'
      });
    }

    const canCraft = craftingModel.canCraft(recipeId, inventory || []);
    
    res.json({
      success: true,
      canCraft: canCraft
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;