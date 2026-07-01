#!/usr/bin/env python3
"""Publish a new article to the LowSpecLab site.
Reads a topic from the ARTICLE_TOPIC env var, generates the article,
builds the site, and pushes to GitHub.
"""
import os, subprocess, sys, datetime

REPO_DIR = '/tmp/lowspelab'
TOPIC = os.environ.get('ARTICLE_TOPIC', '')
SLUG = os.environ.get('ARTICLE_SLUG', '')
CATEGORY = os.environ.get('ARTICLE_CATEGORY', 'Budget Gaming')
ARTICLE_BODY = os.environ.get('ARTICLE_BODY', '')

if not TOPIC or not SLUG or not ARTICLE_BODY:
    print('ERR: ARTICLE_TOPIC, ARTICLE_SLUG, and ARTICLE_BODY env vars required')
    sys.exit(1)

date = datetime.date.today().isoformat()
filepath = f'{REPO_DIR}/content/posts/{SLUG}.md'

with open(filepath, 'w') as f:
    f.write(f'---\ntitle: "{TOPIC}"\ndate: "{date}"\ncategory: "{CATEGORY}"\n---\n\n{ARTICLE_BODY}')

print(f'Written: {filepath}')
