#!/usr/bin/env python
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import glob
from jinja2 import FileSystemLoader, Environment

env = Environment(loader=FileSystemLoader(searchpath='.'),
                  trim_blocks=False, lstrip_blocks=True)

for fn in glob.glob('*.md'):
    name, _ = fn.split(os.extsep)
    tmpl = env.get_template(fn)
    md = tmpl.render()
    out_fn = os.path.join('../{}/README.md'.format(name))
    with open(out_fn, 'w') as f:
        f.write(md)

