from hilo import HiLo, Roll

def test_roll():
    game = HiLo(quantity=100, unit='karma')
    game.roll('user-1')
    game.roll('user-2')

    assert len(game.rolls) == 2

def test_finalize():
    game = HiLo(quantity=100, unit='karma')
    game.add_roll(Roll('user-1', 10))
    game.add_roll(Roll('user-2', 100))

    (win, lose) = game.finalize()

    assert win.user_id == 'user-1'
    assert lose.user_id == 'user-2'
    assert win.value == 10
    assert lose.value == 100