# Run enumeration attempt parallelly
Personal project to run basic enumerations.

## Dependencies
Please do manually install the following tools or dependencies:
- nmap
- gobuster
- dirsearch
- default kali wordlists

## Usage
Change your directory to your target's documentation folder.

Move it to your /usr/local folder for ease of execution:
chmod +x parley.py; sudo cp parley.py /usr/local/bin/parley

Example: sudo parley -t example.com

## Disclaimer
Pip installation requires sudo e.g sudo pip install -r requirements.txt. This might be insecure. If there are other more secure methods, please do give feedback.