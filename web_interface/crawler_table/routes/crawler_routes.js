// Crawler management routes with PHP-like functionality
import { Router } from 'express';
import { CrawlerModel } from '../models/crawler_model.js';

const router = Router();
const crawlerModel = new CrawlerModel();

// Get all crawlers
router.get('/crawlers', (req, res) => {
  try {
    const crawlers = crawlerModel.getAllCrawlers();
    res.json({
      success: true,
      data: crawlers,
      count: crawlers.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get active crawlers
router.get('/crawlers/active', (req, res) => {
  try {
    const crawlers = crawlerModel.getActiveCrawlers();
    res.json({
      success: true,
      data: crawlers,
      count: crawlers.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get crawler by ID
router.get('/crawlers/:id', (req, res) => {
  try {
    const { id } = req.params;
    const crawler = crawlerModel.getCrawlerById(id);
    
    if (!crawler) {
      return res.status(404).json({
        success: false,
        error: 'Crawler not found'
      });
    }
    
    res.json({
      success: true,
      data: crawler
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Add new crawler
router.post('/crawlers', (req, res) => {
  try {
    const { name, type, url, frequency, maxDepth, maxPages, priority, tags } = req.body;
    
    if (!name || !type || !url) {
      return res.status(400).json({
        success: false,
        error: 'Name, type, and URL are required'
      });
    }
    
    const newCrawler = crawlerModel.addCrawler({
      name,
      type,
      url,
      frequency,
      maxDepth,
      maxPages,
      priority,
      tags
    });
    
    res.status(201).json({
      success: true,
      data: newCrawler,
      message: 'Crawler created successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Update crawler
router.put('/crawlers/:id', (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    
    const updated = crawlerModel.updateCrawler(id, updates);
    
    if (!updated) {
      return res.status(404).json({
        success: false,
        error: 'Crawler not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Crawler updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Delete crawler
router.delete('/crawlers/:id', (req, res) => {
  try {
    const { id } = req.params;
    
    const deleted = crawlerModel.deleteCrawler(id);
    
    if (!deleted) {
      return res.status(404).json({
        success: false,
        error: 'Crawler not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Crawler deleted successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Start crawler
router.post('/crawlers/:id/start', (req, res) => {
  try {
    const { id } = req.params;
    
    const started = crawlerModel.startCrawler(id);
    
    if (!started) {
      return res.status(404).json({
        success: false,
        error: 'Crawler not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Crawler started successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Stop crawler
router.post('/crawlers/:id/stop', (req, res) => {
  try {
    const { id } = req.params;
    
    const stopped = crawlerModel.stopCrawler(id);
    
    if (!stopped) {
      return res.status(404).json({
        success: false,
        error: 'Crawler not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Crawler stopped successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get crawler stats
router.get('/crawlers/:id/stats', (req, res) => {
  try {
    const { id } = req.params;
    
    const stats = crawlerModel.getCrawlerStats(id);
    
    if (!stats) {
      return res.status(404).json({
        success: false,
        error: 'Crawler stats not found'
      });
    }
    
    res.json({
      success: true,
      data: stats
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Update crawler stats
router.put('/crawlers/:id/stats', (req, res) => {
  try {
    const { id } = req.params;
    const updates = req.body;
    
    const updated = crawlerModel.updateCrawlerStats(id, updates);
    
    if (!updated) {
      return res.status(404).json({
        success: false,
        error: 'Crawler stats not found'
      });
    }
    
    res.json({
      success: true,
      message: 'Crawler stats updated successfully'
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Get crawler queue
router.get('/crawlers/queue', (req, res) => {
  try {
    const queue = crawlerModel.getCrawlerQueue();
    res.json({
      success: true,
      data: queue,
      count: queue.length
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

export default router;