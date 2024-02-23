from meters import (
    ResourceMeter,
    ResourceUsage,
    metered,
)


def test_resourceusage():
    res = ResourceUsage()
    assert res.cpu >= 0
    assert res.mem > 0

    res = ResourceUsage(123.0, 10 * 1024**2)
    assert res.cpu == 123.0
    assert res.mem == 10 * 1024**2
    assert (
        str(res)
        == "CPU time: 123 s (2 minutes 3 seconds), memory: 10485760 bytes (10 MiB)"
    )


def test_resourcemeter():
    meter = ResourceMeter()
    start = meter.start
    start_cpu = meter.start_cpu
    assert meter.elapsed == 0.0
    assert meter.elapsed_cpu == 0.0
    assert meter.mem > 0

    meter.update()
    assert meter.start == start
    assert meter.start_cpu == start_cpu
    assert meter.elapsed > 0
    assert meter.elapsed_cpu > 0
    assert meter.mem > 0

    meter.update(reset=True)
    assert meter.start > start
    assert meter.start_cpu > start_cpu
    assert meter.elapsed == 0.0
    assert meter.elapsed_cpu == 0.0
    assert meter.mem > 0


def test_resourcemeter_named():
    name = "MyMeter"
    meter = ResourceMeter(name)
    assert str(meter).startswith(f"{name}: ")


def test_resourcemeter_contextmgr(capsys):
    with ResourceMeter() as meter:
        pass
    capture = capsys.readouterr()
    assert capture.out == f"{meter!s}\n"


def test_metered(capsys):
    @metered
    def myfunc(x):
        return x + 42

    res = myfunc(1)
    capture = capsys.readouterr()
    assert res == 43
    assert capture.out.startswith("myfunc: wall time:")

    @metered("test")
    def myfunc2():
        return True

    res = myfunc2()
    capture = capsys.readouterr()
    assert res is True
    assert capture.out.startswith("test: wall time:")

    outs = []

    @metered(out=(lambda x: outs.append(x)))
    def myfunc3(foo=None):
        return foo

    res = myfunc3(foo="bar")
    capture = capsys.readouterr()
    assert res == "bar"
    assert not capture.out
    assert len(outs) == 1
    assert outs[0].startswith("myfunc3: wall time:")

    @metered(return_meter=True)
    def myfunc4(*args):
        return len(args)

    meter, res = myfunc4(1, 2, 3)
    capture = capsys.readouterr()
    assert res == 3
    assert isinstance(meter, ResourceMeter)
    assert capture.out == f"{meter!s}\n"
