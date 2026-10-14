// Main crawler management application with PHP-like functionality
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
class CrawlerManagementFramework {
    constructor() {
        this.crawlers = [];
        this.crawlerStats = new Map();
        this.crawlerQueue = [];
        this.sessionId = this.generateSessionId();
        this.init();
    }

    // Generate session ID (like PHP session_id())
    generateSessionId() {
        return 'crawler_mgt_' + Math.random().toString(36).substr(2, 9);
    }

    init() {
        this.loadDefaultCrawlers();
    }

    loadDefaultCrawlers() {
        // Simulate loading from database or config file (like PHP includes)
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

    // PHP-like function to check if crawler exists
    getCrawlerById(id) {
        return this.crawlers.find(c => c.id === id);
    }

    // PHP-like function to get all crawlers
    getAllCrawlers() {
        return Array.from(this.crawlers);
    }

    // PHP-like function to get active crawlers
    getActiveCrawlers() {
        return this.crawlers.filter(crawler => crawler.status === 'active');
    }

    // PHP-like function to add crawler
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

    // PHP-like function to update crawler
    updateCrawler(id, updates) {
        const index = this.crawlers.findIndex(c => c.id === id);
        if (index !== -1) {
            this.crawlers[index] = { ...this.crawlers[index], ...updates };
            return true;
        }
        return false;
    }

    // PHP-like function to delete crawler
    deleteCrawler(id) {
        const index = this.crawlers.findIndex(c => c.id === id);
        if (index !== -1) {
            this.crawlers.splice(index, 1);
            this.crawlerStats.delete(id);
            return true;
        }
        return false;
    }

    // PHP-like function to start crawler
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

    // PHP-like function to stop crawler
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

    // PHP-like function to get crawler stats
    getCrawlerStats(id) {
        return this.crawlerStats.get(id) || null;
    }

    // PHP-like function to update crawler stats
    updateCrawlerStats(id, updates) {
        const stats = this.crawlerStats.get(id);
        if (stats) {
            Object.assign(stats, updates);
            return true;
        }
        return false;
    }

    // PHP-like session management
    getSessionId() {
        return this.sessionId;
    }

    // PHP-like function to get crawler queue
    getCrawlerQueue() {
        return this.crawlerQueue;
    }

    // PHP-like function to add to queue
    addToQueue(crawlerId) {
        this.crawlerQueue.push({
            id: crawlerId,
            addedAt: new Date(),
            status: 'queued'
        });
    }

    // PHP-like function to remove from queue
    removeFromQueue(crawlerId) {
        const index = this.crawlerQueue.findIndex(item => item.id === crawlerId);
        if (index !== -1) {
            this.crawlerQueue.splice(index, 1);
            return true;
        }
        return false;
    }
}

// Create global crawler management framework instance (like PHP global variables)
const crawlerManagementFramework = new CrawlerManagementFramework();

// Routes - Simulating PHP-style routing
app.get('/crawler', (req, res) => {
    // PHP-like $_GET handling
    const { action = 'view' } = req.query;
    
    // Set response headers like PHP
    res.setHeader('Content-Type', 'text/html');
    res.setHeader('X-Powered-By', 'Doom Web Framework');
    
    // Simulate PHP include for template
    const templatePath = path.join(__dirname, 'templates', 'crawler_table.html');
    
    fs.readFile(templatePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).send('Template not found');
        }
        
        // PHP-like variable replacement
        let html = data;
        html = html.replace('{{session_id}}', crawlerManagementFramework.getSessionId());
        html = html.replace('{{crawler_count}}', crawlerManagementFramework.crawlers.length);
        html = html.replace('{{active_crawlers}}', crawlerManagementFramework.getActiveCrawlers().length);
        
        res.send(html);
    });
});

// PHP-like API endpoints
app.get('/crawler/crawlers', (req, res) => {
    // Simulate PHP $_GET and JSON response
    const { active } = req.query;
    
    let crawlers = crawlerManagementFramework.getAllCrawlers();
    if (active === 'true') {
        crawlers = crawlerManagementFramework.getActiveCrawlers();
    }
    
    res.json({
        success: true,
        session_id: crawlerManagementFramework.getSessionId(),
        crawlers: crawlers,
        count: crawlers.length
    });
});

app.post('/crawler/crawlers', (req, res) => {
    // PHP-like $_POST handling
    const { name, type, url, frequency, maxDepth, maxPages, priority, tags } = req.body;
    
    if (!name || !type || !url) {
        return res.status(400).json({
            success: false,
            error: 'Name, type, and URL are required'
        });
    }
    
    const newCrawler = crawlerManagementFramework.addCrawler({
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
});

app.put('/crawler/crawlers/:id', (req, res) => {
    // PHP-like $_POST handling for updates
    const { id } = req.params;
    const updates = req.body;
    
    const updated = crawlerManagementFramework.updateCrawler(id, updates);
    
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
});

app.delete('/crawler/crawlers/:id', (req, res) => {
    // PHP-like $_POST handling for deletion
    const { id } = req.params;
    
    const deleted = crawlerManagementFramework.deleteCrawler(id);
    
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
});

app.post('/crawler/crawlers/:id/start', (req, res) => {
    // PHP-like $_POST handling for starting crawler
    const { id } = req.params;
    
    const started = crawlerManagementFramework.startCrawler(id);
    
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
});

app.post('/crawler/crawlers/:id/stop', (req, res) => {
    // PHP-like $_POST handling for stopping crawler
    const { id } = req.params;
    
    const stopped = crawlerManagementFramework.stopCrawler(id);
    
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
});

app.get('/crawler/crawlers/:id/stats', (req, res) => {
    // PHP-like $_GET handling for stats
    const { id } = req.params;
    
    const stats = crawlerManagementFramework.getCrawlerStats(id);
    
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
});

// PHP-like file upload handling (simplified)
app.post('/crawler/upload', (req, res) => {
    // Simulate PHP $_FILES handling
    res.json({
        success: true,
        message: 'File uploaded successfully',
        session_id: crawlerManagementFramework.getSessionId()
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