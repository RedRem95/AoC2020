from test.test_numpy import NUMPY_INSTALLED

if NUMPY_INSTALLED:
    def test_common():
        from AoC.misc import common
        s1 = {1, 2, 3}
        s2 = {4, 5, 6}
        s3 = {1, 2, 4}
        assert common() == set()
        assert common(s1, s2) == set()
        assert common(s2, s1) == set()
        assert common(s1, s3) == {2, 1}
        assert common(s3, s1) == {2, 1}
        assert common(s2, s3) == {4}
        assert common(s3, s2) == {4}
        assert common(s1, s2, s3) == set()
        assert common(s2, s2, s1) == set()
        assert common(*[s1 for i in range(10_000)]) == s1
