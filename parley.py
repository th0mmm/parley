#!/usr/bin/python3
import sys
from art import tprint
import argparse
import subprocess as sp
import os
from threading import Thread
from IPy import IP
from ping3 import ping

class executeTask:
    def __init__(self, target):
        self.ip = target
        # Check target directory
        if os.path.isdir(f"parley_result/{self.ip}"):
            pass
        else:
            sp.call(["mkdir", f"parley_result/{self.ip}"])
    
    def nmap(self):
        # Initiate nmap folder
        if os.path.isdir(f"parley_result/{self.ip}/nmap"):
            pass
        else:
            sp.call(["mkdir", f"parley_result/{self.ip}/nmap"])
        # Run nmap basic scan
        print("Nmap is currently running.")
        try:
            sp.run(["nmap", "-sS", f"{self.ip}", "-oN", f"parley_result/{self.ip}/nmap/result_nmap.txt"], capture_output=False, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        except:
            print("Error has occurred during nmap. Please re-run the script.")


    def subdomainEnum(self):
        # Initiate subdomain_enum folder
        if os.path.isdir(f"parley_result/{self.ip}/subdomain_enum"):
            pass
        else:
            sp.call(["mkdir", f"parley_result/{self.ip}/subdomain_enum"])
        # Run subdomain basic scan
        try:
            IP(self.ip)
        except:
            print("Subdomain enumeration is running.")
            try:
                sp.run(["gobuster", "vhost", "-u", f"{self.ip}", "-w", "/usr/share/wordlists/amass/subdomains-top1mil-110000.txt", "-q", "--append-domain", "-k", "-t", "70", "-o", f"parley_result/{self.ip}/subdomain_enum/result_subdomain_enum.txt"], capture_output=False, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            except:
                print("Error has occurred during subdomain enumeration. Please re-run the script.")
        else:  
            print("Unable to run subdomain enumeration. Target is not in domain name form.")

    def dirbusting(self):
        # Initiate dirbusting folder
        if os.path.isdir(f"parley_result/{self.ip}/dirbusting"):
            pass
        else:
            sp.call(["mkdir", f"parley_result/{self.ip}/dirbusting"])
        # Run dirbusting basic scan
        print("Directory busting is currently running.")
        current_directory = sp.check_output(["pwd"]).decode().strip()
        try:
            sp.run(["dirsearch", "-u", f"{self.ip}", "-w", "/usr/share/dirb/wordlists/big.txt", "-o", f"{current_directory}/parley_result/{self.ip}/dirbusting/result_dirbusting.txt", "-t", "70"], capture_output=False, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        except:
            print("Error has occurred during directory busting. Please re-run the script.")
    
    def executeThread(self):
        nmapT = Thread(target=self.nmap)
        subdomainT = Thread(target=self.subdomainEnum)
        dirbustingT = Thread(target=self.dirbusting)
        nmapT.start()
        subdomainT.start()
        dirbustingT.start()
        nmapT.join()
        print("Nmap is done processing.")
        subdomainT.join()
        print("Subdomain enumeration is done processing.")
        dirbustingT.join()
        print("Directory busting is done processing.")
        print("Basic enumeration is done.")


def checkDirectory():
    if os.path.isdir("parley_result"):
        pass
    else:
        sp.call(["mkdir","parley_result"])

def checkTarget(target, force):
    response_time = ping(target)
    if force:
        pass
    elif response_time is False:
        print(f"{target} is not a valid IP. Exiting ...")
        sys.exit()
    elif response_time is None:
        print(f"{target} is down or not responding to ping. Exiting ...")
        sys.exit()
    else:
        print(f"{target} is responding to ping. Executing ...\n")

def main():
    helpParser = argparse.ArgumentParser(description="Enumeration Paralelly")
    helpParser.add_argument("-t", "--target", help="Target to enumerate in domain name form.", required=True)
    helpParser.add_argument('--force', action='store_true', help='Force the script if the target is not responding to ICMP packets')
    tprint("Parley")
    helpArgs = helpParser.parse_args()

    if len(sys.argv) < 1:
        helpArgs.print_help()
        sys.exit()
    if sys.argv[2].startswith("http://") or sys.argv[2].startswith("https://"):
        print("Put only the domain name or IP")
        sys.exit()
    if os.geteuid() != 0:
        print("Please run the script as root or by using sudo")
        sys.exit()
    target = sys.argv[2]

    # Check if target is alive or not.
    checkTarget(target, helpArgs.force)
    # Check if parley directory exist, if it doesn't, create one.
    checkDirectory()

    run = executeTask(target)
    run.executeThread()

if __name__ == "__main__":
    main()
else:
    print("Parley version 0.1")