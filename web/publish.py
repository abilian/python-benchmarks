#!/usr/bin/env python

import os


result_txt = open("result.txt").read()

index_html = open("index.html.tpl").read().format(RESULT_TXT=result_txt)

open("index.html", "w").write(index_html)

