# mypy: disallow-untyped-defs
"""
based on a Java version:
 Based on original version written in BCPL by Dr Martin Richards
 in 1981 at Cambridge University Computer Laboratory, England
 and a C++ version derived from a Smalltalk version written by
 L Peter Deutsch.
 Java version:  Copyright (C) 1995 Sun Microsystems, Inc.
 Translation from C++, Mario Wolczko
 Outer loop added by Alex Jacoby

 Dec. 2020: Copy/pasted by Stefane Fermigier from
 https://github.com/mypyc/mypyc-benchmarks/blob/master/benchmarks/bm_richards.py
 + Py3k-ized and made compatible with our benchmark harness.
"""


from typing import List, Optional, Tuple
from typing_extensions import Final


ITERATIONS = 50
EXPECTED = (9297, 23246)


# Task IDs
I_IDLE: Final = 1
I_WORK: Final = 2
I_HANDLERA: Final = 3
I_HANDLERB: Final = 4
I_DEVA: Final = 5
I_DEVB: Final = 6

# Packet types
K_DEV: Final = 1000
K_WORK: Final = 1001

# Packet

BUFSIZE: Final = 4
BUFSIZE_RANGE: Final = range(BUFSIZE)


class Packet(object):
    def __init__(self, l: Optional["Packet"], i: int, k: int) -> None:
        self.link = l
        self.ident = i
        self.kind = k
        self.datum = 0
        self.data = [0] * BUFSIZE

    def append_to(self, lst: Optional["Packet"]) -> "Packet":
        self.link = None
        if lst is None:
            return self
        else:
            p = lst
            next = p.link
            while next is not None:
                p = next
                next = p.link
            p.link = self
            return lst


# Task Records


class TaskRec(object):
    pass


class DeviceTaskRec(TaskRec):
    def __init__(self) -> None:
        self.pending: Optional[Packet] = None


class IdleTaskRec(TaskRec):
    def __init__(self) -> None:
        self.control = 1
        self.count = 10000


class HandlerTaskRec(TaskRec):
    def __init__(self) -> None:
        self.work_in: Optional[Packet] = None
        self.device_in: Optional[Packet] = None

    def workInAdd(self, p: Packet) -> Packet:
        self.work_in = p.append_to(self.work_in)
        return self.work_in

    def deviceInAdd(self, p: Packet) -> Packet:
        self.device_in = p.append_to(self.device_in)
        return self.device_in


class WorkerTaskRec(TaskRec):
    def __init__(self) -> None:
        self.destination = I_HANDLERA
        self.count = 0


# Task


class TaskState(object):
    def __init__(self) -> None:
        self.packet_pending = True
        self.task_waiting = False
        self.task_holding = False

    def packetPending(self) -> "TaskState":
        self.packet_pending = True
        self.task_waiting = False
        self.task_holding = False
        return self

    def waiting(self) -> "TaskState":
        self.packet_pending = False
        self.task_waiting = True
        self.task_holding = False
        return self

    def running(self) -> "TaskState":
        self.packet_pending = False
        self.task_waiting = False
        self.task_holding = False
        return self

    def waitingWithPacket(self) -> "TaskState":
        self.packet_pending = True
        self.task_waiting = True
        self.task_holding = False
        return self

    def isPacketPending(self) -> bool:
        return self.packet_pending

    def isTaskWaiting(self) -> bool:
        return self.task_waiting

    def isTaskHolding(self) -> bool:
        return self.task_holding

    def isTaskHoldingOrWaiting(self) -> bool:
        return self.task_holding or (not self.packet_pending and self.task_waiting)

    def isWaitingWithPacket(self) -> bool:
        return self.packet_pending and self.task_waiting and not self.task_holding


TASKTABSIZE: Final = 10


class TaskWorkArea(object):
    def __init__(self) -> None:
        self.taskTab: List[Optional[Task]] = [None] * TASKTABSIZE

        self.taskList: Optional[Task] = None

        self.holdCount = 0
        self.qpktCount = 0


taskWorkArea: Final = TaskWorkArea()


class Task(TaskState):
    def __init__(
        self, i: int, p: int, w: Optional[Packet], initialState: TaskState, r: TaskRec
    ) -> None:
        self.link = taskWorkArea.taskList
        self.ident = i
        self.priority = p
        self.input = w

        self.packet_pending = initialState.isPacketPending()
        self.task_waiting = initialState.isTaskWaiting()
        self.task_holding = initialState.isTaskHolding()

        self.handle = r

        taskWorkArea.taskList = self
        taskWorkArea.taskTab[i] = self

    def fn(self, pkt: Optional[Packet], r: TaskRec) -> Optional["Task"]:
        raise NotImplementedError

    def addPacket(self, p: Packet, old: "Task") -> "Task":
        if self.input is None:
            self.input = p
            self.packet_pending = True
            if self.priority > old.priority:
                return self
        else:
            p.append_to(self.input)
        return old

    def runTask(self) -> Optional["Task"]:
        if self.isWaitingWithPacket():
            msg = self.input
            assert msg is not None
            self.input = msg.link
            if self.input is None:
                self.running()
            else:
                self.packetPending()
        else:
            msg = None

        return self.fn(msg, self.handle)

    def waitTask(self) -> "Task":
        self.task_waiting = True
        return self

    def hold(self) -> Optional["Task"]:
        taskWorkArea.holdCount += 1
        self.task_holding = True
        return self.link

    def release(self, i: int) -> "Task":
        t = self.findtcb(i)
        t.task_holding = False
        if t.priority > self.priority:
            return t
        else:
            return self

    def qpkt(self, pkt: Packet) -> "Task":
        t = self.findtcb(pkt.ident)
        taskWorkArea.qpktCount += 1
        pkt.link = None
        pkt.ident = self.ident
        return t.addPacket(pkt, self)

    def findtcb(self, id: int) -> "Task":
        t = taskWorkArea.taskTab[id]
        if t is None:
            raise Exception("Bad task id %d" % id)
        return t


# DeviceTask


class DeviceTask(Task):
    def fn(self, pkt: Optional[Packet], r: TaskRec) -> Optional[Task]:
        d = r
        assert isinstance(d, DeviceTaskRec)
        if pkt is None:
            pkt = d.pending
            if pkt is None:
                return self.waitTask()
            else:
                d.pending = None
                return self.qpkt(pkt)
        else:
            d.pending = pkt
            return self.hold()


class HandlerTask(Task):
    def fn(self, pkt: Optional[Packet], r: TaskRec) -> Optional[Task]:
        h = r
        assert isinstance(h, HandlerTaskRec)
        if pkt is not None:
            if pkt.kind == K_WORK:
                h.workInAdd(pkt)
            else:
                h.deviceInAdd(pkt)
        work = h.work_in
        if work is None:
            return self.waitTask()
        count = work.datum
        if count >= BUFSIZE:
            h.work_in = work.link
            return self.qpkt(work)

        dev = h.device_in
        if dev is None:
            return self.waitTask()

        h.device_in = dev.link
        dev.datum = work.data[count]
        work.datum = count + 1
        return self.qpkt(dev)


# IdleTask


class IdleTask(Task):
    def __init__(self, i: int, p: int, w: int, s: TaskState, r: IdleTaskRec) -> None:
        Task.__init__(self, i, 0, None, s, r)

    def fn(self, pkt: Optional[Packet], r: TaskRec) -> Optional[Task]:
        i = r
        assert isinstance(i, IdleTaskRec)
        i.count -= 1
        if i.count == 0:
            return self.hold()
        elif i.control & 1 == 0:
            i.control //= 2
            return self.release(I_DEVA)
        else:
            i.control = i.control // 2 ^ 0xD008
            return self.release(I_DEVB)


# WorkTask


A: Final = ord("A")


class WorkTask(Task):
    def fn(self, pkt: Optional[Packet], r: TaskRec) -> Optional[Task]:
        w = r
        assert isinstance(w, WorkerTaskRec)
        if pkt is None:
            return self.waitTask()

        if w.destination == I_HANDLERA:
            dest = I_HANDLERB
        else:
            dest = I_HANDLERA

        w.destination = dest
        pkt.ident = dest
        pkt.datum = 0

        for i in BUFSIZE_RANGE:  # xrange(BUFSIZE)
            w.count += 1
            if w.count > 26:
                w.count = 1
            pkt.data[i] = A + w.count - 1

        return self.qpkt(pkt)


def schedule() -> None:
    t = taskWorkArea.taskList
    while t is not None:
        if t.isTaskHoldingOrWaiting():
            t = t.link
        else:
            t = t.runTask()


def run() -> Tuple[int, int]:
    taskWorkArea.holdCount = 0
    taskWorkArea.qpktCount = 0

    IdleTask(I_IDLE, 1, 10000, TaskState().running(), IdleTaskRec())

    wkq: Optional[Packet] = Packet(None, 0, K_WORK)
    wkq = Packet(wkq, 0, K_WORK)
    WorkTask(I_WORK, 1000, wkq, TaskState().waitingWithPacket(), WorkerTaskRec())

    wkq = Packet(None, I_DEVA, K_DEV)
    wkq = Packet(wkq, I_DEVA, K_DEV)
    wkq = Packet(wkq, I_DEVA, K_DEV)
    HandlerTask(
        I_HANDLERA, 2000, wkq, TaskState().waitingWithPacket(), HandlerTaskRec()
    )

    wkq = Packet(None, I_DEVB, K_DEV)
    wkq = Packet(wkq, I_DEVB, K_DEV)
    wkq = Packet(wkq, I_DEVB, K_DEV)
    HandlerTask(
        I_HANDLERB, 3000, wkq, TaskState().waitingWithPacket(), HandlerTaskRec()
    )

    wkq = None
    DeviceTask(I_DEVA, 4000, wkq, TaskState().waiting(), DeviceTaskRec())
    DeviceTask(I_DEVB, 5000, wkq, TaskState().waiting(), DeviceTaskRec())

    schedule()

    return (taskWorkArea.holdCount, taskWorkArea.qpktCount)


def main(iterations):
    for i in range(iterations):
        result = run()
        assert result == EXPECTED


main(ITERATIONS)
