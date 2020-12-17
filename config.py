ENVS = [
    # Regular Python
    {
        "python": "python3.7",
    },
    {
        "python": "python3.8",
    },
    {
        "python": "python3.7",
    },
    {
        "python": "python3.8",
        "command": "conda create -p envs/py38-conda -y",
    },
    # {
    #     "python": "python3.9",
    # },
    # {
    #     "python": "python3.10",
    # },
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
]

SKIP_PROGRAMS = {"knucleotides"}
