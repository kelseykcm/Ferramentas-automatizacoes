import nmap
import argparse
import logging
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class StealthScanner:
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports
        self.scanner = nmap.PortScanner()
        self.args = '-sS -f -Pn -n -T3 -sV'

    def run_scan(self):
        try:
            logger.info(f"Starting stealth scan on {self.target} (Ports: {self.ports})")
            self.scanner.scan(self.target, self.ports, arguments=self.args)
            return self.scanner
        except nmap.PortScannerError as e:
            logger.error(f"Nmap error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        return None

    def generate_report(self, scanner):
        filename = f"scan_report_{self.target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w') as f:
                f.write(f"Scan Report for {self.target}\n")
                f.write(f"Date: {datetime.now()}\n")
                f.write("-"*30 + "\n")
                for host in scanner.all_hosts():
                    f.write(f"Host: {host} ({scanner[host].state()})\n")
                    for proto in scanner[host].all_protocols():
                        ports = scanner[host][proto].keys()
                        for port in sorted(ports):
                            state = scanner[host][proto][port]['state']
                            service = scanner[host][proto][port].get('name', 'unknown')
                            f.write(f"Port: {port}\tState: {state}\tService: {service}\n")
            logger.info(f"Report saved to {filename}")
        except IOError as e:
            logger.error(f"Failed to write report: {e}")

def main():
    parser = argparse.ArgumentParser(description="Professional Stealth Nmap Scanner")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range (e.g., 20-10000)")
    args = parser.parse_args()

    scanner_obj = StealthScanner(args.target, args.ports)
    try:
        results = scanner_obj.run_scan()
        if results:
            scanner_obj.generate_report(results)
    except KeyboardInterrupt:
        logger.warning("Scan interrupted by user. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()