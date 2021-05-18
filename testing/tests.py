def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

def test_sum_tuple():
    assert sum((1, 2, 3)) == 6, "Should be 6"

def test_everything():
    test_sum()
    test_sum_tuple()
    print("Everything passed")


test_everything()