import tomd
import os

with open('./sass.html', 'r', encoding='utf-8', errors='ignore') as f:
    # print(f.read())
    html = f.read()
    md = tomd.Tomd(html).markdown
    print(md)
    with open('./sass.md', 'w', encoding='utf-8') as f:
        f.write(md + '\n')
