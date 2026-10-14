// Simple search and indexing system for webserver

// In-memory search index
class SearchIndex {
  constructor() {
    this.index = new Map();
    this.documents = [];
  }

  // Add document to index
  addDocument(id, title, content, tags = []) {
    const doc = {
      id,
      title,
      content,
      tags,
      timestamp: new Date()
    };

    this.documents.push(doc);
    
    // Index words from title and content
    const text = `${title} ${content}`.toLowerCase();
    const words = text.split(/\s+/).filter(word => word.length > 2);
    
    words.forEach(word => {
      if (!this.index.has(word)) {
        this.index.set(word, []);
      }
      this.index.get(word).push(id);
    });
  }

  // Search for documents
  search(query) {
    const terms = query.toLowerCase().split(/\s+/).filter(term => term.length > 2);
    
    if (terms.length === 0) {
      return [];
    }

    // Find documents containing all terms
    let results = null;
    
    terms.forEach(term => {
      const docIds = this.index.get(term) || [];
      
      if (results === null) {
        results = new Set(docIds);
      } else {
        results = new Set([...results].filter(id => docIds.includes(id)));
      }
    });

    // Return matching documents
    return Array.from(results)
      .map(id => this.documents.find(doc => doc.id === id))
      .filter(Boolean)
      .sort((a, b) => {
        // Simple scoring based on relevance
        const scoreA = this.calculateScore(a, query);
        const scoreB = this.calculateScore(b, query);
        return scoreB - scoreA;
      });
  }

  // Calculate relevance score
  calculateScore(doc, query) {
    let score = 0;
    const terms = query.toLowerCase().split(/\s+/);
    
    // Check title match
    if (doc.title.toLowerCase().includes(query.toLowerCase())) {
      score += 10;
    }
    
    // Check content match
    const content = doc.content.toLowerCase();
    terms.forEach(term => {
      if (content.includes(term)) {
        score += 5;
      }
    });
    
    return score;
  }

  // Get all documents
  getAllDocuments() {
    return this.documents;
  }
}

// Main search engine class
export class SearchEngine {
  constructor() {
    this.index = new SearchIndex();
    this.isInitialized = true;
  }

  // Initialize the search engine
  async initialize() {
    console.log('Simple search engine initialized');
    return true;
  }

  // Index Doom-related content
  indexDoomContent(content) {
    if (!content || !content.title || !content.content) {
      return { success: false, error: 'Invalid content format' };
    }

    try {
      const id = `doc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      // Extract tags from content
      let tags = [];
      if (content.tags && Array.isArray(content.tags)) {
        tags = content.tags;
      } else if (content.content) {
        // Simple tag extraction based on common Doom terms
        const doomTerms = ['weapon', 'monster', 'map', 'level', 'doom', 'heretic', 'hexen'];
        tags = doomTerms.filter(term => 
          content.content.toLowerCase().includes(term) || 
          content.title.toLowerCase().includes(term)
        );
      }

      this.index.addDocument(id, content.title, content.content, tags);
      
      return { success: true, message: 'Content indexed successfully' };
    } catch (error) {
      console.error('Error indexing content:', error);
      return { success: false, error: error.message };
    }
  }

  // Search through indexed content
  search(query) {
    if (!query || typeof query !== 'string') {
      return { success: false, error: 'Invalid search query' };
    }

    try {
      const results = this.index.search(query);
      return { 
        success: true, 
        results,
        total: results.length
      };
    } catch (error) {
      console.error('Search error:', error);
      return { success: false, error: error.message };
    }
  }

  // Get search suggestions
  getSuggestions(query) {
    if (!query || query.length < 2) {
      return { 
        success: true, 
        suggestions: [],
        query
      };
    }

    const suggestions = [
      `Doom ${query}`,
      `${query} weapon`,
      `${query} tutorial`,
      `How to ${query} in Doom`,
      `${query} strategy`,
      `Best ${query} in Doom`
    ];

    return { 
      success: true, 
      suggestions,
      query
    };
  }

  // Get all indexed documents (for debugging)
  getAllDocuments() {
    return this.index.getAllDocuments();
  }
}

// Export singleton instance
export const searchEngine = new SearchEngine();

// Initialize on startup
searchEngine.initialize().catch(console.error);