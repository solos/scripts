#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile
from lxml import etree

CHARACTERS = '''`"=:'-_^~*#+<>,.!@'''
SYMBOLS = dict(enumerate(CHARACTERS))

rst = []


def xmind2rst(filename):
    global rst
    try:
        content = zipfile.ZipFile(filename).read('content.xml')
    except Exception, e:
        print e
        return
    try:
        root = etree.fromstring(content)
    except Exception, e:
        print e
    traverse(root, 0)
    title = rst[-1][0]
    lines = []
    for i, symbol in rst[0:-1]:
        c = i.encode('utf8')
        s = len(c) * symbol
        line = '%s\n%s' % (c, s)
        lines.append(line)
    content = '\n'.join(lines)
    return title, content


def traverse(node, depth):
    global rst
    symbol = SYMBOLS[depth]
    for i in node.getchildren():
        if i.tag == '{urn:xmind:xmap:xmlns:content:2.0}title':
            if i.text is not None:
                rst.append((i.text, symbol))
        if i.getchildren():
            traverse(i, depth+1)


if __name__ == '__main__':
    title, content = xmind2rst('历代经济变革得失.xmind')
    open('%s.rst' % title, 'w').write(content)
