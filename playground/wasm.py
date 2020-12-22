#!/usr/bin/env python
from devtools import debug
from ppci.lang.python import python_to_wasm

prog = open("playground/mandelbrot-wasm.py").read()

r = python_to_wasm(prog)
debug(r)
debug(r.to_string())

open("playground/mandelbrot.wasm", "w").write(r.to_string())
