ENVS = [
    # Regular Python
    {
        "python": "python3.7",
    },
    {
        "python": "python3.8",
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
