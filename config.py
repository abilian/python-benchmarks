ENVS = [
    # Regular Python
    {
        "python": "python3.7",
    },
    {
        "python": "python3.8",
    },
    {
        "python": "python3.9",
    },
    # {
    #     "python": "python3.10",
    # },
    #
    # Accelerated Python
    #
    # {
    #     "name": "python3.8-conda",
    #     "python": "python3.8",
    #     "command": "conda create -p envs/python3.8-conda -y",
    # },
    {
        "name": "python3.8-numba",
        "python": "python3.8",
        "deps": "numba",
    },
    {
        "name": "pyjion",
        "python": "python3.9",
        "deps": "pyjion",
    },
    # {
    #     "name": "graalpython",
    #     "python": "graalpython",
    # },
    {
        "name": "pypy3",
        "python": "pypy3",
    },
    # Cython
    {
        "name": "cython",
        "runner": "Cython",
        "deps": "cython",
    },
    {
        "name": "cython-dev",
        "runner": "Cython",
        "deps": "git+https://github.com/cython/cython.git",
    },
    {
        "name": "cython-plus",
        "runner": "Cython",
        "deps": "git+https://github.com/abilian/cythonplus.git",
    },
    # Mypyc
    {
        "name": "mypyc",
        "runner": "Mypyc",
        "deps": "mypy",
    },
]

SKIP_PROGRAMS = {"knucleotide"}
