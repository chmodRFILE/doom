#!/usr/bin/env python3
"""
Debug script to check the ImprovedDoomCrawler constructor
"""

import inspect
from crawler.improved_doom_crawler import ImprovedDoomCrawler

def check_crawler_constructor():
    print("Checking ImprovedDoomCrawler constructor:")
    
    # Get the signature of the constructor
    sig = inspect.signature(ImprovedDoomCrawler.__init__)
    print(f"Constructor signature: {sig}")
    
    # Get parameters
    params = list(sig.parameters.keys())
    print(f"Parameters: {params}")

if __name__ == "__main__":
    check_crawler_constructor()