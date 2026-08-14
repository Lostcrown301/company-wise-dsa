with open('scripts/import_dataset.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('`n', '\n')
with open('scripts/import_dataset.py', 'w', encoding='utf-8') as f:
    f.write(content)
