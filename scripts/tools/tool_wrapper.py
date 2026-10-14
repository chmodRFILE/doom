import subprocess
import os
import json
from typing import Dict, List, Optional, Union

class ToolWrapper:
    """Wrapper-Klasse für Shell-Tools wie nmap, nslookup, nping und proxychains4"""
    
    def __init__(self, tools_dir: str = "scripts/tools"):
        self.tools_dir = tools_dir
        self.tools = {
            'nmap': '/usr/bin/nmap',
            'nslookup': '/usr/bin/nslookup',
            'nping': '/usr/bin/nping',
            'proxychains4': '/usr/bin/proxychains4'
        }
        
        # Sicherstellen, dass das Verzeichnis existiert
        os.makedirs(tools_dir, exist_ok=True)
    
    def run_nmap_scan(self, target: str, options: str = "-sS", timeout: int = 300) -> Dict:
        """
        Führt einen nmap-Scan durch
        
        Args:
            target (str): Ziel-IP oder Hostname
            options (str): Nmap-Optionen
            timeout (int): Timeout in Sekunden
            
        Returns:
            Dict mit Scan-Ergebnissen
        """
        try:
            cmd = [self.tools['nmap'], options, '-oN', f'{self.tools_dir}/nmap_scan_{target}.txt', target]
            
            # Ausführung mit Timeout
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': True,
                'command': ' '.join(cmd),
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'output_file': f'{self.tools_dir}/nmap_scan_{target}.txt'
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Timeout beim Ausführen von nmap',
                'command': ' '.join(cmd)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': ' '.join(cmd)
            }
    
    def run_nslookup(self, domain: str, server: Optional[str] = None) -> Dict:
        """
        Führt nslookup durch
        
        Args:
            domain (str): Domain-Name
            server (str, optional): DNS-Server
            
        Returns:
            Dict mit nslookup-Ergebnissen
        """
        try:
            cmd = [self.tools['nslookup'], domain]
            if server:
                cmd.append(server)
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': True,
                'command': ' '.join(cmd),
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': ' '.join(cmd)
            }
    
    def run_nping(self, target: str, options: str = "-c 1", timeout: int = 60) -> Dict:
        """
        Führt nping durch
        
        Args:
            target (str): Ziel-IP
            options (str): nping-Optionen
            timeout (int): Timeout in Sekunden
            
        Returns:
            Dict mit nping-Ergebnissen
        """
        try:
            cmd = [self.tools['nping'], options, target]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': True,
                'command': ' '.join(cmd),
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': ' '.join(cmd)
            }
    
    def run_with_proxychains(self, command: List[str], proxy_config: str = "/etc/proxychains/proxychains.conf") -> Dict:
        """
        Führt einen Befehl mit proxychains4 aus
        
        Args:
            command (List[str]): Kommando als Liste
            proxy_config (str): Pfad zur Proxychains-Konfiguration
            
        Returns:
            Dict mit Ergebnissen
        """
        try:
            # Erstelle das proxychains-Kommando
            cmd = [self.tools['proxychains4'], '-f', proxy_config] + command
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120  # 2 Minuten Timeout
            )
            
            return {
                'success': True,
                'command': ' '.join(cmd),
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'command': ' '.join(cmd)
            }
    
    def get_tool_status(self) -> Dict[str, bool]:
        """
        Überprüft den Status aller Tools
        
        Returns:
            Dict mit Tool-Status
        """
        status = {}
        for tool_name, tool_path in self.tools.items():
            status[tool_name] = os.path.exists(tool_path)
        
        return status
    
    def create_scan_script(self, target: str, scan_type: str = "full") -> str:
        """
        Erstellt ein Shell-Skript für einen Scan
        
        Args:
            target (str): Ziel-IP oder Hostname
            scan_type (str): Art des Scans
            
        Returns:
            Pfad zum erstellten Skript
        """
        script_content = f"""#!/bin/bash
# Auto-generated nmap scan script for {target}

echo "Starting nmap scan for {target}"
nmap -sS -p- -T4 {target} -oN scan_{target}.txt

if [ $? -eq 0 ]; then
    echo "Scan completed successfully"
else
    echo "Scan failed"
fi
"""
        
        script_path = f"{self.tools_dir}/scan_{target}_{scan_type}.sh"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Rechte setzen
        os.chmod(script_path, 0o755)
        
        return script_path

# Beispiel für die Verwendung
if __name__ == "__main__":
    wrapper = ToolWrapper()
    
    # Status der Tools prüfen
    print("Tool Status:", wrapper.get_tool_status())
    
    # Beispiel für nmap-Scan
    result = wrapper.run_nmap_scan("127.0.0.1")
    print("nmap Ergebnis:", json.dumps(result, indent=2))