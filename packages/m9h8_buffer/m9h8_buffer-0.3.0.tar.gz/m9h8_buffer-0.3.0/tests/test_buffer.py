from buffer import Buffer


def test_append():
    temp = []
    b = Buffer(size=3, callback=temp.append)

    b.append(0)
    assert temp == []
    b.append(1)
    assert temp == []
    b.append(2)
    assert temp == [0, 1, 2]
    b.append(3)
    assert temp == [0, 1, 2]
    b.flush()
    assert temp == [0, 1, 2, 3]


def test_extend():
    temp = []
    b = Buffer(size=3, callback=temp.append)

    b.extend(range(2))
    assert temp == []

    b.extend(range(3))
    assert temp == [0, 1, 0]

    b.flush()
    assert temp == [0, 1, 0, 1, 2]
