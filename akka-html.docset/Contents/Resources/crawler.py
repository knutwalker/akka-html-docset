#!/usr/local/bin/python
# get stuff with wget -r -k -L  http://doc.akka.io/docs/akka/2.2.3/index.html

import sqlite3, re

from bs4 import BeautifulSoup
from collections import deque, defaultdict
from contextlib import contextmanager
from os.path import normpath, join, split
from urllib import quote


DB_PATH = u'docSet.dsidx'
DOC_PATH = u'Documents'
SEED_FILE = u'index.html'


@contextmanager
def db(db_path):
    db = sqlite3.connect(db_path)
    cur = db.cursor()

    try:
        cur.execute('DROP TABLE searchIndex;')
    except:
        pass

    cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
    cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    try:

        yield cur

    finally:
        db.commit()
        db.close()


def normalize_target(base, href):
    return normpath(join(split(base)[0], href))


def normalize_name(name, target):
    path = target.split(u'/')
    if len(path) > 1:
        path = path[0]
        suffix = u'(%s)' % path.title()
        if not name.endswith(suffix):
            name = name + u' ' + suffix

    return re.sub(u'\s+', ' ', name)


def get_file_name(target):
    return target.split(u'#')[0]


def analyze_link(tag, fname):
    name = tag.text.strip()
    if name:
        href = tag.attrs['href'].strip()

        target = normalize_target(fname, href)
        name = normalize_name(name, target)

        return target, name


def parse_page(path):
    sout = None
    with open(path) as page:
        soup = BeautifulSoup(page)

    return soup


def crawl_page(doc_path, fname):

    internal_links = lambda href: not href.startswith('http')
    link_classifier = {
        'class': u'reference',
        'href': internal_links
    }

    soup = parse_page(join(doc_path, fname))
    for tag in soup.find_all('a', link_classifier):
        analyzed = analyze_link(tag, fname)
        if analyzed:
            yield analyzed


def generate_index(doc_path, seed_file):
    seen = set([seed_file])
    queue = deque(seen)

    index = set()
    names_files = defaultdict(set)

    while queue:
        fname = queue.pop()
        for target, name in crawl_page(doc_path, fname):

            fpath = get_file_name(target)

            if fpath not in seen:
                queue.appendleft(fpath)
                seen.add(fpath)

            if target not in index:
                index.add(target)
                names_files[name].add(target)

    for name in sorted(names_files.iterkeys(), key=lambda s: s.lower()):
        for target in set(get_file_name(t) for t in names_files[name]):
            yield (name, target)



def save_row(cur, name, path):
    cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Guide', path))


def log(name, path):
    print u'name: %s, path: %s' % (name, path)


def crawl(cur, crawler, logger, saver):
    for name, path in crawler():
        logger(name, path)
        saver(cur, name, path)


def make_toc(doc_path, *toc_files):
    for toc_file in toc_files:
        soup = parse_page(join(doc_path, toc_file))
        for tag in soup.find_all('a', {'class': 'reference'}):
            analyzed = analyze_link(tag, toc_file)
            if analyzed:
                target, name = analyzed
                tag.attrs['name'] = '//apple_ref/cpp/Guide/%s' % quote(name.encode('utf-8'))

                classes = tag.attrs.get('class', [])
                if not 'dashAnchor' in classes:
                    classes.append('dashAnchor')

                tag.attrs['class'] = classes

        with open(join(doc_path, toc_file), 'wb') as fh:
            fh.write(soup.prettify().encode('utf-8'))


if __name__ == "__main__":
    import sys

    if '-h' in sys.argv:
        print 'usage: crawler.py [-d | -n] [-q | -s] [-h]'
        print '  -d | -n      dry run/no op'
        print '  -q | -s      quiet/silent'
        print '  -h           show help'
        sys.exit(-1)

    if u'-q' in sys.argv or u'-s' in sys.argv:
        logger = lambda a, b: None
    else:
        logger = log

    dry_run = False
    if '-d' in sys.argv or '-n' in sys.argv:
        storer = lambda a, b, c: None
        dry_run = True
    else:
        storer = save_row

    generator = lambda: generate_index(DOC_PATH, SEED_FILE)

    if dry_run:
        crawl(None, generator, logger, storer)
    else:
        with db(DB_PATH) as cur:
            crawl(cur, generator, logger, storer)
        make_toc(DOC_PATH, 'java.html', 'scala.html')
