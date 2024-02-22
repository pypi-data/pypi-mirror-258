# -*- coding: utf-8 -*-
import pytest


@pytest.fixture()
def sample_testfile(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.fixture
        def fixture1():
            return "Value1"

        @pytest.fixture
        def fixture2():
            return "Value2"

        @pytest.fixture
        def fixture3():
            return "Value3"


        def test_fixcollect1(fixture1):
            pass

        def test_fixcollect2(fixture2):
            pass

        def test_fixcollect3(fixture1, fixture2):
            pass

        def test_withoutfix():
            pass
    """)
    return testdir


def test_collection_with_single_fixture(sample_testfile):
    """Make sure tests are collected as per fixture use"""

    result = sample_testfile.runpytest(
        '-v', '--collect-only', '--uses-fixtures=fixture1'
    )

    assert result.ret == 0
    resout = result.stdout.str()
    assert '2/4 tests collected' in resout
    assert 'test_fixcollect1' in resout
    assert 'test_fixcollect3' in resout
    assert 'test_withoutfix' not in resout


def test_collection_with_multi_fixture(sample_testfile):
    """Make sure tests are collected as per fixture use"""

    result = sample_testfile.runpytest(
        '-v', '--collect-only', '--uses-fixtures=fixture1,fixture2'
    )

    assert result.ret == 0
    resout = result.stdout.str()
    assert '3/4 tests collected' in resout
    assert 'test_fixcollect1' in resout
    assert 'test_fixcollect2' in resout
    assert 'test_fixcollect3' in resout
    assert 'test_withoutfix' not in resout
