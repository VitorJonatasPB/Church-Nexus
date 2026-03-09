import os
import shutil

base_dir = r"c:\Users\Vitor.Paiva\Documents\Programacao\Python\projetos\meu_projeto"

# Delete files
files_to_delete = ['test_pagamentos.py', 'test_pagamentos2.py', 'seed_eventos.py']
for f in files_to_delete:
    path = os.path.join(base_dir, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {f}")

# Create directories
backend_dir = os.path.join(base_dir, 'backend')
frontend_dir = os.path.join(base_dir, 'frontend')

os.makedirs(backend_dir, exist_ok=True)
os.makedirs(frontend_dir, exist_ok=True)
print("Created folders")

# Move to frontend
frontend_items = ['templates', 'static']
for item in frontend_items:
    src = os.path.join(base_dir, item)
    dst = os.path.join(frontend_dir, item)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {item} to frontend")

# Move to backend
backend_items = ['apps', 'core', 'config', 'manage.py', 'requirements.txt', 'db.sqlite3']
for item in backend_items:
    src = os.path.join(base_dir, item)
    dst = os.path.join(backend_dir, item)
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {item} to backend")

print("Reorganization complete")
