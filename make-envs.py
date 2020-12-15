#!/usr/bin/env python3

from plumbum import local
import config

for env in config.ENVS:
    print(env)

    name = env["name"]
    runner = env["runner"]
    deps = env.get("deps")

    local["python3.8"]["-m", "venv", "--copies", "--clear", f"envs/{name}"]()

    if deps:
        local[f"envs/{name}/bin/pip"]["install", deps]()
