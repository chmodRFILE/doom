// Crawler management model with classes
export class CrawlerModel {
  constructor() {
    this.crawlers = [];
    this.crawlerStats = new Map();
    this.crawlerQueue = [];
    this.initDefaultCrawlers();
  }

  // Initialize default crawlers
  initDefaultCrawlers() {
    this.crawlers = [
      {
        id: 'crawler_001',
        name: 'Web Spider',
        type: 'web',
        status: 'active',
        url: 'https://example.com',
        frequency: '30s',
        lastRun: new Date(),
        nextRun: new Date(Date.now() + 30000),
        maxDepth: 5,
        maxPages: 100,
        priority: 'high',
        tags: ['web', 'general'],
        config: {
          userAgent: 'WebSpider/1.0',
          timeout: 5000,
          retries: 3
        }
      },
      {
        id: 'crawler_002',
        name: 'Image Spider',
        type: 'image',
        status: 'active',
        url: 'https://images.example.com',
        frequency: '60s',
        lastRun: new Date(),
        nextRun: new Date(Date.now() + 60000),
        maxDepth: 3,
        maxPages: 50,
        priority: 'medium',
        tags: ['image', 'media'],
        config: {
          userAgent: 'ImageSpider/1.0',
          timeout: 10000,
          retries: 2
        }
      },
      {
        id: 'crawler_003',
        name: 'API Spider',
        type: 'api',
        status: 'inactive',
        url: 'https://api.example.com',
        frequency: '120s',
        lastRun: new Date(),
        nextRun: new Date(Date.now() + 120000),
        maxDepth: 1,
        maxPages: 10,
        priority: 'low',
        tags: ['api', 'data'],
        config: {
          userAgent: 'APISpider/1.0',
          timeout: 3000,
          retries: 1
        }
      }
    ];

    // Initialize stats for each crawler
    this.crawlers.forEach(crawler => {
      this.crawlerStats.set(crawler.id, {
        pagesCrawled: 0,
        errors: 0,
        successRate: 100,
        lastSuccess: null,
        totalRuntime: 0,
        averageResponseTime: 0
      });
    });
  }

  // Get all crawlers
  getAllCrawlers() {
    return this.crawlers;
  }

  // Get active crawlers
  getActiveCrawlers() {
    return this.crawlers.filter(crawler => crawler.status === 'active');
  }

  // Get crawler by ID
  getCrawlerById(id) {
    return this.crawlers.find(crawler => crawler.id === id);
  }

  // Add new crawler
  addCrawler(crawlerData) {
    const newCrawler = {
      id: `crawler_${Date.now()}`,
      ...crawlerData,
      status: 'active',
      lastRun: null,
      nextRun: new Date(),
      createdAt: new Date()
    };

    this.crawlers.push(newCrawler);
    
    // Initialize stats
    this.crawlerStats.set(newCrawler.id, {
      pagesCrawled: 0,
      errors: 0,
      successRate: 100,
      lastSuccess: null,
      totalRuntime: 0,
      averageResponseTime: 0
    });

    return newCrawler;
  }

  // Update crawler
  updateCrawler(id, updates) {
    const index = this.crawlers.findIndex(c => c.id === id);
    if (index !== -1) {
      this.crawlers[index] = { ...this.crawlers[index], ...updates };
      return true;
    }
    return false;
  }

  // Delete crawler
  deleteCrawler(id) {
    const index = this.crawlers.findIndex(c => c.id === id);
    if (index !== -1) {
      this.crawlers.splice(index, 1);
      this.crawlerStats.delete(id);
      return true;
    }
    return false;
  }

  // Start crawler
  startCrawler(id) {
    const crawler = this.getCrawlerById(id);
    if (crawler) {
      crawler.status = 'running';
      crawler.lastRun = new Date();
      // Update next run time
      const frequencyMs = this.parseFrequency(crawler.frequency);
      crawler.nextRun = new Date(Date.now() + frequencyMs);
      
      // Update stats
      const stats = this.crawlerStats.get(id);
      if (stats) {
        stats.lastSuccess = new Date();
      }
      
      return true;
    }
    return false;
  }

  // Stop crawler
  stopCrawler(id) {
    const crawler = this.getCrawlerById(id);
    if (crawler) {
      crawler.status = 'inactive';
      return true;
    }
    return false;
  }

  // Parse frequency string to milliseconds
  parseFrequency(frequency) {
    if (!frequency) return 30000; // Default 30 seconds
    
    const unit = frequency.slice(-1);
    const value = parseInt(frequency);
    
    switch (unit) {
      case 's': return value * 1000;
      case 'm': return value * 60000;
      case 'h': return value * 3600000;
      default: return 30000;
    }
  }

  // Get crawler stats
  getCrawlerStats(id) {
    return this.crawlerStats.get(id) || null;
  }

  // Update crawler stats
  updateCrawlerStats(id, updates) {
    const stats = this.crawlerStats.get(id);
    if (stats) {
      Object.assign(stats, updates);
      return true;
    }
    return false;
  }

  // Get crawler queue
  getCrawlerQueue() {
    return this.crawlerQueue;
  }

  // Add to queue
  addToQueue(crawlerId) {
    this.crawlerQueue.push({
      id: crawlerId,
      addedAt: new Date(),
      status: 'queued'
    });
  }

  // Remove from queue
  removeFromQueue(crawlerId) {
    const index = this.crawlerQueue.findIndex(item => item.id === crawlerId);
    if (index !== -1) {
      this.crawlerQueue.splice(index, 1);
      return true;
    }
    return false;
  }
}