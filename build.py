#!/usr/bin/env python3
"""Minimal static site generator for LowSpecLab.
Reads markdown from content/, renders via templates/, outputs to docs/ (GitHub Pages source).
Zero external dependencies — stdlib only.
"""

import os
import sys
import yaml
import re
import html
import pathlib
from datetime import datetime
from collections import defaultdict

# ── Markdown-to-HTML (minimal, no deps) ──────────────────────────────────────

def parse_frontmatter(text):
    """Split YAML frontmatter from markdown body."""
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
            return meta, body
    return {}, text

def md_to_html(md):
    """Minimal markdown → HTML. Good enough for articles, not a full MD parser."""
    lines = md.split('\n')
    out = []
    in_list = False
    in_code = False
    code_buf = []

    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if in_code:
                out.append(f'<pre><code>{html.escape(chr(10).join(code_buf))}</code></pre>')
                code_buf = []
                in_code = False
            else:
                if in_list:
                    out.append('</ul>')
                    in_list = False
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue

        # Headers
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            if in_list:
                out.append('</ul>')
                in_list = False
            lvl = len(m.group(1))
            txt = inline_format(m.group(2))
            out.append(f'<h{lvl}>{txt}</h{lvl}>')
            continue

        # Horizontal rule
        if re.match(r'^---+\s*$', line.strip()):
            out.append('<hr>')
            continue

        # Unordered list
        m = re.match(r'^[\-\*]\s+(.*)', line)
        if m:
            if not in_list:
                out.append('<ul>')
                in_list = True
            out.append(f'<li>{inline_format(m.group(1))}</li>')
            continue

        # Ordered list
        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            if not in_list:
                out.append('<ol>')
                in_list = True
            out.append(f'<li>{inline_format(m.group(1))}</li>')
            continue

        if in_list:
            out.append('</ul>')
            in_list = False

        # Paragraphs
        stripped = line.strip()
        if not stripped:
            continue
        out.append(f'<p>{inline_format(stripped)}</p>')

    if in_code and code_buf:
        out.append(f'<pre><code>{html.escape(chr(10).join(code_buf))}</code></pre>')
    if in_list:
        out.append('</ul>')

    return '\n'.join(out)

def inline_format(text):
    """Inline formatting: bold, italic, code, links, images."""
    text = html.escape(text)
    # Images ![alt](src)
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" loading="lazy">', text)
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    # Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Inline code `text`
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

# ── Template rendering ────────────────────────────────────────────────────────

def load_template(name, template_dir='templates'):
    path = os.path.join(template_dir, f'{name}.html')
    with open(path) as f:
        return f.read()

def render_template(tmpl, **kwargs):
    for key, val in kwargs.items():
        # Triple braces = unescaped (for HTML content)
        tmpl = tmpl.replace(f'{{{{{{ {key} }}}}}}', str(val))
        # Double braces = regular replacement
        tmpl = tmpl.replace(f'{{{{ {key} }}}}', str(val))
    return tmpl

# ── Build ─────────────────────────────────────────────────────────────────────

def load_config(path='config.yaml'):
    with open(path) as f:
        return yaml.safe_load(f)

BASE_PATH = '/lowspelab.github.io'  # GitHub project page subpath

def collect_posts(content_dir='content/posts'):
    posts = []
    for fname in sorted(os.listdir(content_dir)):
        if not fname.endswith('.md'):
            continue
        with open(os.path.join(content_dir, fname)) as f:
            meta, body = parse_frontmatter(f.read())
        meta['slug'] = fname.replace('.md', '')
        meta['body_html'] = md_to_html(body)
        meta['excerpt'] = md_to_html(body[:300]).replace('<p>', '').replace('</p>', '')[:250] + '…'
        posts.append(meta)
    posts.sort(key=lambda p: p.get('date', ''), reverse=True)
    return posts

def build_site():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    cfg = load_config()
    site = cfg['site']
    
    posts = collect_posts()
    
    out_dir = 'docs'
    os.makedirs(f'{out_dir}/posts', exist_ok=True)
    os.makedirs(f'{out_dir}/css', exist_ok=True)
    os.makedirs(f'{out_dir}/images', exist_ok=True)
    
    # Load templates
    base = load_template('base')
    index_tmpl = load_template('index')
    post_tmpl = load_template('post')
    
    # ── Index page ──
    hero = f'''<section class="hero">
        <h1>{site['name']}</h1>
        <p>{site['tagline']}</p>
    </section>'''
    
    posts_html = '<section id="guides" class="posts-grid">\n'
    for p in posts[:12]:
        posts_html += f'''<article class="post-card">
        <h2><a href="{BASE_PATH}/posts/{p['slug']}/">{p.get('title', 'Untitled')}</a></h2>
        <time datetime="{p.get('date', '')}">{p.get('date', '')}</time>
        <p>{p.get('excerpt', '')}</p>
        </article>\n'''
    posts_html += '</section>'
    
    index_html = render_template(index_tmpl, posts=posts_html)
    full = render_template(base, site_name=site['name'], site_tagline=site['tagline'],
                           site_description=site['description'], content=index_html,
                           site_url=site['url'], page_title=site['name'],
                           base_path=BASE_PATH, hero=hero)
    
    with open(f'{out_dir}/index.html', 'w') as f:
        f.write(full)
    
    # ── Individual posts ──
    for p in posts:
        post_content = render_template(post_tmpl,
                                       title=p.get('title', 'Untitled'),
                                       date=p.get('date', ''),
                                       category=p.get('category', ''),
                                       body=p['body_html'],
                                       site_name=site['name'],
                                       site_url=site['url'])
        full = render_template(base, site_name=site['name'], site_tagline=site['tagline'],
                               site_description=site['description'], content=post_content,
                               site_url=site['url'],
                               page_title=f"{p.get('title', '')} — {site['name']}",
                               base_path=BASE_PATH, hero='')
        
        post_dir = f'{out_dir}/posts/{p["slug"]}'
        os.makedirs(post_dir, exist_ok=True)
        with open(f'{post_dir}/index.html', 'w') as f:
            f.write(full)
    
    # ── Sitemap ──
    site_url = site['url'] + BASE_PATH
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{site_url}/</loc><changefreq>weekly</changefreq></url>\n'
    for p in posts:
        sitemap += f'  <url><loc>{site_url}/posts/{p["slug"]}/</loc></url>\n'
    sitemap += '</urlset>'
    with open(f'{out_dir}/sitemap.xml', 'w') as f:
        f.write(sitemap)
    
    # ── RSS ──
    rss = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{site['name']}</title>
<link>{site_url}</link>
<description>{site['description']}</description>
<atom:link href="{site_url}/feed.xml" rel="self" type="application/rss+xml"/>
'''
    for p in posts[:20]:
        rss += f'''<item>
<title>{html.escape(p.get('title', ''))}</title>
<link>{site_url}/posts/{p['slug']}/</link>
<description>{html.escape(p.get('excerpt', ''))}</description>
<pubDate>{p.get('date', '')}</pubDate>
</item>\n'''
    rss += '</channel></rss>'
    with open(f'{out_dir}/feed.xml', 'w') as f:
        f.write(rss)
    
    # ── Copy static assets ──
    import shutil
    if os.path.exists('static/css'):
        shutil.copytree('static/css', f'{out_dir}/css', dirs_exist_ok=True)
    if os.path.exists('static/images'):
        shutil.copytree('static/images', f'{out_dir}/images', dirs_exist_ok=True)
    
    print(f'Built {len(posts)} posts to {out_dir}/')
    print(f'Sitemap: {out_dir}/sitemap.xml')
    print(f'RSS: {out_dir}/feed.xml')

if __name__ == '__main__':
    build_site()
