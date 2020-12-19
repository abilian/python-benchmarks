#!/usr/bin/env python

from __future__ import annotations

import contextlib
import glob
import os
import pathlib
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import fire as fire

import config

PATH = os.environ["PATH"]
DEBUG = False


class Runner:
    name: str
    extension: str
    interpreter: str
    variants: List[Dict[str, Any]] = ()

    def match(self, source_name):
        return source_name.endswith(f".{self.extension}")

    def run_all(self, source_path):
        self.prepare_sandbox(source_path)
        if self.variants:
            for variant in self.variants:
                run = Run(self, source_path, variant=variant)
                self.run(run)

        else:
            run = Run(self, source_path)
            self.run(run)

    def prepare_sandbox(self, source_path):
        shutil.rmtree("sandbox")
        os.mkdir("sandbox")
        shutil.copy(source_path, "sandbox")

        # Temps hack
        m = re.match(r".*/([a-z0-9]+)/[^/]*\.([a-z0-9]+)", source_path)
        name = m.group(1)
        ext = m.group(2)
        shutil.copy(source_path, f"sandbox/{name}.{ext}")

    def compile(self, run: Run):
        cmd = self.compile_cmd(run)
        if not cmd:
            return

        p = subprocess.run(cmd, cwd="sandbox", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if p.returncode != 0:
            run.error = "Compile error"

    def compile_cmd(self, run: Run) -> List[str]:
        return []

    def run(self, run: Run) -> None:
        self.compile(run)
        cmd = self.run_cmd(run)
        run.run(cmd)

    def run_cmd(self, run: Run) -> List[str]:
        """Default run command.

        Can be overridden in subclass.
        """
        variant = run.variant
        if variant and "interpreter" in variant:
            interpreter = variant["interpreter"]
        else:
            interpreter = self.interpreter

        cmd = [interpreter, run.source_name]
        if run.args:
            cmd += run.args.split(" ")

        return cmd


@dataclass
class Run:
    runner: Runner
    source_path: str
    variant: Optional[Dict] = None
    start_time: float = 0
    end_time: float = 0
    returncode: int = 0
    error: str = ""

    @property
    def prog_name(self) -> str:
        return pathlib.Path(self.source_path).parent.name

    @property
    def source_name(self) -> str:
        return pathlib.Path(self.source_path).name

    @property
    def variant_name(self) -> str:
        if not self.variant:
            return self.runner.interpreter
        if "virtualenv" in self.variant:
            return self.variant["virtualenv"]
        if "interpreter" in self.variant:
            return self.variant["interpreter"]
        return "???"

    @property
    def virtualenv(self) -> str:
        if self.variant and "virtualenv" in self.variant:
            return self.variant["virtualenv"]
        return ""

    @property
    def args(self) -> str:
        source_dir = pathlib.Path(self.source_path).parent
        args_txt = source_dir / "args.txt"
        if args_txt.exists():
            return args_txt.open().read().strip()
        else:
            return ""

    def run(self, cmd):
        if self.error:
            self.report()
            return

        self.start_time = time.time()

        error = ""
        if self.virtualenv:
            cmd[0] = f"{os.getcwd()}/envs/{self.virtualenv}/bin/{cmd[0]}"
            if DEBUG:
                print(" ".join(cmd))
            try:
                p = subprocess.run(
                    cmd,
                    cwd="sandbox",
                    # env=env,
                    capture_output=True,
                )
                self.returncode = p.returncode
                if DEBUG:
                    print("Output")
                    print(p.stdout)
                    print("Error")
                    print(p.stderr)
            except FileNotFoundError:
                error = "N/A"

        else:
            if DEBUG:
                print(" ".join(cmd))
            try:
                p = subprocess.run(
                    cmd, cwd="sandbox", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                self.returncode = p.returncode
            except FileNotFoundError:
                error = "N/A"

        if error:
            self.error = error
            self.returncode = -1
        elif self.returncode != 0:
            self.error = "Error"
        self.end_time = time.time()
        self.report()

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time

    def report(self):
        if self.error == "N/A":
            return

        if self.error:
            duration = self.error
        else:
            duration = f"{self.duration:3.3f}"

        print(
            f"{self.source_name:<20} "
            f"{(self.runner.name + '/' + self.variant_name):<20} "
            f"{duration}"
        )


class PyRunner(Runner):
    name = "Python"
    extension = "py"
    variants = [
        {
            "interpreter": "python3.7",
            "virtualenv": "python3.7",
        },
        {
            "interpreter": "python3.8",
            "virtualenv": "python3.8",
        },
        {
            "interpreter": "python3.9",
            "virtualenv": "python3.9",
        },
        {
            "interpreter": "python",
            "virtualenv": "py3.8-conda",
        },
        {
            "interpreter": "python",
            "virtualenv": "pyjion",
        },
        {
            "interpreter": "python",
            "virtualenv": "pypy3",
        },
        {
            "interpreter": "python",
            "virtualenv": "pyston",
        },
    ]


class LuaRunner(Runner):
    name = "Lua"
    extension = "lua"
    variants = [
        {"interpreter": "lua"},
        {"interpreter": "luajit"},
    ]


class JSRunner(Runner):
    name = "JavaScript"
    extension = "js"
    variants = [
        {"interpreter": "node"},
        {"interpreter": "deno"},
        {"interpreter": "duk"},
    ]

    # FIXME: hack
    def run_cmd(self, run: Run) -> List[str]:
        variant = run.variant
        interpreter = variant["interpreter"]
        if interpreter == "deno":
            cmd = [interpreter, "run", run.source_name]
        else:
            cmd = [interpreter, run.source_name]

        if run.args:
            cmd += run.args.split(" ")

        return cmd

class RubyRunner(Runner):
    name = "Ruby"
    extension = "rb"
    interpreter = "ruby"
    variants = [
        {"interpreter": "ruby"},
        {"interpreter": "jruby"},
    ]


class PhpRunner(Runner):
    name = "PHP"
    extension = "php"
    interpreter = "php"


class CythonRunner(Runner):
    name = "Cython"
    extension = "pyx"
    variants = [
        {
            "virtualenv": "cython",
        },
        {
            "virtualenv": "cython-dev",
        },
        {
            "virtualenv": "cython-plus",
        },
    ]

    def compile_cmd(self, run: Run):
        executable = f"{os.getcwd()}/envs/{run.virtualenv}/bin/cythonize"
        return [executable, "-3", "-bi", run.source_name]

    def run_cmd(self, run: Run) -> List[str]:
        return ["python3", "-c", f"import {run.prog_name}", run.args]


class MypycRunner(Runner):
    name = "Mypyc"
    extension = "py"
    variants = [
        {
            "virtualenv": "python3.7",
        },
        {
            "virtualenv": "python3.8",
        },
        # Doesn't work, currently
        # {
        #     "virtualenv": "python3.9",
        # },
    ]

    def compile_cmd(self, run: Run):
        executable = f"{os.getcwd()}/envs/{run.virtualenv}/bin/mypyc"
        return [executable, f"{run.prog_name}.py"]

    def run_cmd(self, run: Run) -> List[str]:
        return ["python3", "-c", f"import {run.prog_name}", run.args]


class CRunner(Runner):
    name = "C"
    extension = "c"
    interpreter = "gcc"

    def compile_cmd(self, run: Run):
        return ["gcc", "-O", run.source_name]

    def run_cmd(self, run: Run) -> List[str]:
        return ["./a.out", run.args]


def all_runners():
    def is_runner_subclass(v):
        if not type(v) == type:
            return False
        if v is Runner:
            return False
        if not issubclass(v, Runner):
            return False
        return True

    result = [r() for r in globals().values() if is_runner_subclass(r)]
    return sorted(result, key=lambda x: x.name)


def run_all(prog_name):
    runners = all_runners()

    for source_path in sorted(glob.glob(f"programs/{prog_name}/{prog_name}*")):
        for runner in runners:
            if not runner.match(source_path):
                continue

            runner.run_all(source_path)


@contextlib.contextmanager
def chdir(dirname=None):
    curdir = os.getcwd()
    try:
        if dirname is not None:
            os.chdir(dirname)
        yield
    finally:
        os.chdir(curdir)


def main(verbose=False, program=""):
    global DEBUG
    DEBUG = verbose

    pathlib.Path("sandbox").mkdir(exist_ok=True)

    for program_dir in sorted(glob.glob("programs/*")):
        prog_name = program_dir.split("/")[1]

        if prog_name in config.SKIP_PROGRAMS:
            continue
        if program and prog_name != program:
            continue

        title = f"Running benchmarks for {prog_name}"
        print(title)
        print("=" * len(title))
        print()
        run_all(prog_name)

        print()


if __name__ == "__main__":
    fire.Fire(main)
