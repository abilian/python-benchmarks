# The Computer Language Benchmarks Game
# http://benchmarksgame.alioth.debian.org/
#
# contributed by Daniel Nanz 2008-03-11

# Coroutines via enhanced generators
# 2to3

import sys
import itertools


def main(n=int(sys.argv[1]), n_threads=503, cycle=itertools.cycle):
    def worker(worker_id):

        n = 1
        while True:
            if n > 0:
                n = yield (n - 1)
            else:
                print(worker_id)
                raise StopIteration

    threadRing = [worker(w) for w in range(1, n_threads + 1)]
    for t in threadRing:
        foo = next(t)  # start exec. gen. funcs
    sendFuncRing = [t.send for t in threadRing]  # speed...
    for send in cycle(sendFuncRing):
        try:
            n = send(n)
        except StopIteration:
            break


main()
