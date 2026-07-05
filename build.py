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

def parse_table(lines, start_idx):
    """Parse a markdown table starting at start_idx. Returns (html, next_idx)."""
    if start_idx >= len(lines):
        return '', start_idx
    
    # Check if this line looks like a table header (contains | and not just ||)
    header_line = lines[start_idx].strip()
    if not ('|' in header_line and not header_line.startswith('||')):
        return '', start_idx
    
    # Need at least header + separator
    if start_idx + 1 >= len(lines):
        return '', start_idx
    
    separator_line = lines[start_idx + 1].strip()
    if not re.match(r'^[\|\-\s:]+$', separator_line):
        return '', start_idx
    
    # Parse header
    header_cells = [c.strip() for c in header_line.split('|') if c.strip() or c == '']
    # Remove empty first/last if present
    if header_cells and not header_cells[0]:
        header_cells = header_cells[1:]
    if header_cells and not header_cells[-1]:
        header_cells = header_cells[:-1]
    
    # Parse separator to determine alignment
    sep_cells = [c.strip() for c in separator_line.split('|') if c.strip() or c == '']
    if sep_cells and not sep_cells[0]:
        sep_cells = sep_cells[1:]
    if sep_cells and not sep_cells[-1]:
        sep_cells = sep_cells[:-1]
    
    alignments = []
    for sep in sep_cells:
        if sep.startswith(':') and sep.endswith(':'):
            alignments.append('center')
        elif sep.endswith(':'):
            alignments.append('right')
        else:
            alignments.append('left')
    
    # Pad alignments if needed
    while len(alignments) < len(header_cells):
        alignments.append('left')
    
    # Parse rows
    rows = [header_cells]
    idx = start_idx + 2
    while idx < len(lines):
        row_line = lines[idx].strip()
        if not ('|' in row_line):
            break
        if re.match(r'^[\|\-\s:]+$', row_line):  # another separator
            break
        row_cells = [c.strip() for c in row_line.split('|') if c.strip() or c == '']
        if row_cells and not row_cells[0]:
            row_cells = row_cells[1:]
        if row_cells and not row_cells[-1]:
            row_cells = row_cells[:-1]
        if len(row_cells) == len(header_cells):
            rows.append(row_cells)
        idx += 1
    
    if len(rows) < 2:
        return '', start_idx
    
    # Build HTML
    html_out = ['<table>']
    html_out.append('  <thead>')
    html_out.append('    <tr>')
    for i, cell in enumerate(rows[0]):
        align_attr = f' style="text-align: {alignments[i]};"' if i < len(alignments) else ''
        html_out.append(f'      <th{align_attr}>{inline_format(cell)}</th>')
    html_out.append('    </tr>')
    html_out.append('  </thead>')
    html_out.append('  <tbody>')
    for row in rows[1:]:
        html_out.append('    <tr>')
        for i, cell in enumerate(row):
            align_attr = f' style="text-align: {alignments[i]};"' if i < len(alignments) else ''
            html_out.append(f'      <td{align_attr}>{inline_format(cell)}</td>')
        html_out.append('    </tr>')
    html_out.append('  </tbody>')
    html_out.append('</table>')
    
    return '\n'.join(html_out), idx

def md_to_html(md):
    """Minimal markdown → HTML with table support."""
    lines = md.split('\n')
    out = []
    in_list = False
    in_code = False
    code_buf = []
    list_type = 'ul'  # 'ul' or 'ol'
    in_blockquote = False
    blockquote_buf = []
    
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        
        # Code blocks
        if stripped.startswith('```'):
            if in_code:
                out.append(f'<pre><code>{html.escape(chr(10).join(code_buf))}</code></pre>')
                code_buf = []
                in_code = False
            else:
                if in_list:
                    out.append(f'</{list_type}>')
                    in_list = False
                in_code = True
            idx += 1
            continue
        if in_code:
            code_buf.append(line)
            idx += 1
            continue
        
        # Tables
        table_html, next_idx = parse_table(lines, idx)
        if table_html:
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            out.append(table_html)
            idx = next_idx
            continue
        
        # Headers
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            lvl = len(m.group(1))
            txt = inline_format(m.group(2))
            out.append(f'<h{lvl}>{txt}</h{lvl}>')
            idx += 1
            continue
        
        # Horizontal rule
        if re.match(r'^---+\s*$', stripped):
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            out.append('<hr>')
            idx += 1
            continue
        
        # Blockquote
        m = re.match(r'^>\s+(.*)', line)
        if m:
            if in_list:
                out.append(f'</{list_type}>')
                in_list = False
            if not in_blockquote:
                out.append('<blockquote>')
                in_blockquote = True
            out.append(f'  <p>{inline_format(m.group(1))}</p>')
            idx += 1
            continue
        elif in_blockquote and not stripped:
            # Empty line inside blockquote - continue it
            idx += 1
            continue
        elif in_blockquote and not stripped.startswith('>'):
            out.append('</blockquote>')
            in_blockquote = False
            continue
        
        # Unordered list
        m = re.match(r'^[-\*]\s+(.*)', line)
        if m:
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            if not in_list:
                out.append('<ul>')
                in_list = True
                list_type = 'ul'
            elif list_type != 'ul':
                out.append('</ol>')
                out.append('<ul>')
                list_type = 'ul'
            out.append(f'<li>{inline_format(m.group(1))}</li>')
            idx += 1
            continue
        
        # Ordered list
        m = re.match(r'^\d+\.\s+(.*)', line)
        if m:
            if in_blockquote:
                out.append('</blockquote>')
                in_blockquote = False
            if not in_list:
                out.append('<ol>')
                in_list = True
                list_type = 'ol'
            elif list_type != 'ol':
                out.append('</ul>')
                out.append('<ol>')
                list_type = 'ol'
            out.append(f'<li>{inline_format(m.group(1))}</li>')
            idx += 1
            continue
        
        # List continuation (indented content under list item)
        if in_list and (line.startswith('  ') or line.startswith('\t')):
            # Continuation of previous list item - just add as text
            if out and out[-1].startswith('<li>'):
                # Replace closing </li> with continued content
                prev = out.pop()
                if prev.endswith('</li>'):
                    prev = prev[:-5]  # remove </li>
                out.append(f'{prev}\n{inline_format(stripped)}</li>')
            idx += 1
            continue
        
        if in_list and not stripped:
            # Empty line in list - keep list open
            idx += 1
            continue
        
        if in_list:
            out.append(f'</{list_type}>')
            in_list = False
        
        # Paragraphs
        if not stripped:
            idx += 1
            continue
        
        out.append(f'<p>{inline_format(stripped)}</p>')
        idx += 1
    
    # Close any open blocks
    if in_code and code_buf:
        out.append(f'<pre><code>{html.escape(chr(10).join(code_buf))}</code></pre>')
    if in_list:
        out.append(f'</{list_type}>')
    if in_blockquote:
        out.append('</blockquote>')
    
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
    # Italic *text* (but not bold)
    text = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', text)
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

def json_escape(s):
    """Escape a string for safe inclusion in JSON string values."""
    # Unescape HTML entities first for clean text
    import html as _html
    s = _html.unescape(str(s))
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', ' ')
    s = s.replace('\r', ' ')
    s = s.replace('\t', ' ')
    return s

# ── Build ─────────────────────────────────────────────────────────────────────

def load_config(path='config.yaml'):
    with open(path) as f:
        return yaml.safe_load(f)

BASE_PATH = ''  # Org user page serves at root — no subpath

def collect_posts(content_dir='content/posts'):
    posts = []
    for fname in sorted(os.listdir(content_dir)):
        if not fname.endswith('.md'):
            continue
        with open(os.path.join(content_dir, fname)) as f:
            meta, body = parse_frontmatter(f.read())
        meta['slug'] = fname.replace('.md', '')
        meta['body_html'] = md_to_html(body)
        # Excerpt: first paragraph from rendered HTML
        excerpt_html = md_to_html(body[:500])
        # Strip tags for excerpt
        excerpt_text = re.sub(r'<[^>]+>', '', excerpt_html)[:250] + '…'
        meta['excerpt'] = excerpt_text
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
    hero = ''
    
    posts_html = '<ul class="post-list">\n'
    for p in posts:
        posts_html += f'''<li>
        <h2><a href="{BASE_PATH}/posts/{p['slug']}/">{p.get('title', 'Untitled')}</a></h2>
        <div class="post-meta">{p.get('date', '')}</div>
        <div class="post-excerpt">{p.get('excerpt', '')}</div>
        </li>\n'''
    posts_html += '</ul>'
    
    index_html = render_template(index_tmpl, posts=posts_html)
    full = render_template(base, site_name=site['name'], site_tagline=site['tagline'],
                           site_description=site['description'], content=index_html,
                           site_url=site['url'], page_title=site['name'],
                           base_path=BASE_PATH, hero=hero)
    
    with open(f'{out_dir}/index.html', 'w') as f:
        f.write(full)
    
    # ── Individual posts ──
    for p in posts:
        date_iso = str(p.get('date', ''))
        page_url = f"{site['url']}{BASE_PATH}/posts/{p['slug']}/"

        post_content = render_template(post_tmpl,
                                       title=p.get('title', 'Untitled'),
                                       date=p.get('date', ''),
                                       date_iso=date_iso,
                                       page_url=page_url,
                                       excerpt=json_escape(p.get('excerpt', '')),
                                       title_json=json_escape(p.get('title', 'Untitled')),
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