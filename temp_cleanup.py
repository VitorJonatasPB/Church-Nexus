import os
import subprocess

out = subprocess.check_output(['git', 'ls-files']).decode('utf-8')
files = out.splitlines()

to_remove = []
for f in files:
    if '__pycache__' in f or f.startswith('media/') or f.startswith('.vscode/') or f.startswith('venv/') or f.startswith('inspirações/'):
        to_remove.append(f)

if to_remove:
    # Run git rm --cached in chunks to avoid command line length limits
    chunk_size = 50
    for i in range(0, len(to_remove), chunk_size):
        chunk = to_remove[i:i + chunk_size]
        subprocess.call(['git', 'rm', '--cached'] + chunk)
    
    print(f"Removed {len(to_remove)} files from git tracking.")
else:
    print("No files to remove.")
