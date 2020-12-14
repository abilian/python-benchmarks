#!/usr/bin/env python3

from plumbum import local
import config

for env in config.ENVS:
    print(env)

    name = env["name"]
    runner = env["runner"]
    deps = env.get("deps")

    local["python3.8"]["-m", "venv", f"envs/{name}"]()

    if deps:
        local[f"envs/{name}/bin/pip"]["install", deps]()


# x = seashore.Executor(seashore.Shell())
#
# env = "cython"
# x.command(["python3.8", "-m", "venv", f"envs/{env}"]).batch()
# x.command(["python3.8", f"envs/{env}/pip", "install", "cython"]).batch()
#
# x.command(["python3.8", "-m", "venv", "envs/cythonplus"]).batch()
# x.command(["python3.8", "envs/cython/pip", "install", "cython"]).batch()
