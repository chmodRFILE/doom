#!/usr/bin/env python3
"""
Testskript für die Tool-Wrapper-Klasse
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from scripts.tools.tool_wrapper import ToolWrapper

def test_tool_wrapper():
    """Testet die Tool-Wrapper-Klasse"""
    print("Testing Tool Wrapper...")
    
    # Erstelle eine Instanz des Tool Wrappers
    wrapper = ToolWrapper()
    
    # Prüfe den Status der Tools
    print("\nTool Status:")
    status = wrapper.get_tool_status()
    for tool, available in status.items():
        print(f"  {tool}: {'✓' if available else '✗'}")
    
    # Teste nmap (nur mit einer einfachen Ziel-IP)
    print("\nTesting nmap scan...")
    result = wrapper.run_nmap_scan("127.0.0.1", "-sS -p 22,80,443", timeout=60)
    print(f"nmap Ergebnis: {result['success']}")
    
    # Teste nslookup
    print("\nTesting nslookup...")
    result = wrapper.run_nslookup("google.com")
    print(f"nslookup Ergebnis: {result['success']}")
    
    # Teste nping
    print("\nTesting nping...")
    result = wrapper.run_nping("127.0.0.1", "-c 1 -p 1000")
    print(f"nping Ergebnis: {result['success']}")
    
    print("\nTest abgeschlossen!")

if __name__ == "__main__":
    test_tool_wrapper()