import pytest
import sys

IS_WIN = sys.platform == "win32"


@pytest.fixture
def create_test_regtest_context_manager(testdir):
    testdir.makepyfile(
        """
        import tempfile

        def test_regtest(regtest, tmpdir):

            print("this is not recorded")
            with regtest:
                print("this is expected outcome")
                print(tmpdir.join("test").strpath)
                print(tempfile.gettempdir())
                print(tempfile.mkdtemp())
                print("obj id is", hex(id(tempfile)))
            regtest.flush()

         """
    )
    yield testdir


@pytest.fixture
def create_test_regtest_fh(testdir):
    testdir.makepyfile(
        """
        import tempfile

        def test_regtest(regtest, tmpdir):

            print("this is not recorded")
            print("this is expected outcome", file=regtest)
            print(tmpdir.join("test").strpath, file=regtest)
            print(tempfile.gettempdir(), file=regtest)
            print(tempfile.mkdtemp(), file=regtest)
            print("obj id is", hex(id(tempfile)), file=regtest)
            regtest.flush()

         """
    )
    yield testdir


@pytest.fixture
def create_test_regtest_all(testdir):
    testdir.makepyfile(
        """
        import tempfile

        def test_regtest(regtest_all, tmpdir):

            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    yield testdir


def test_regtest_context_manager(create_test_regtest_context_manager):
    _test_regtest_output(create_test_regtest_context_manager)


def test_regtest_fh(create_test_regtest_fh):
    _test_regtest_output(create_test_regtest_fh)


def test_regtest_all(create_test_regtest_all):
    _test_regtest_output(create_test_regtest_all)


def _test_regtest_output(test_setup):
    result = test_setup.runpytest()
    result.assert_outcomes(failed=1, passed=0, xfailed=0)

    expected_diff = """
    regression test output not recorded yet for test_regtest_*::test_regtest:

    this is expected outcome
    <tmpdir_from_fixture>/test
    <tmpdir_from_tempfile_module>
    <tmpdir_from_tempfile_module>
    obj id is 0x?????????""".strip().splitlines()

    result.stdout.fnmatch_lines(
        [line.lstrip() for line in expected_diff], consecutive=True
    )


def test_xfail(testdir):
    testdir.makepyfile(
        """
        import tempfile
        import pytest

        @pytest.mark.xfail
        def test_regtest_xfail(regtest_all, tmpdir):

            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    result = testdir.runpytest()
    result.assert_outcomes(xfailed=1)

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(xfailed=1)

    result = testdir.runpytest()
    result.assert_outcomes(xpassed=1)


def test_xfail_strict(testdir):
    testdir.makepyfile(
        """
        import tempfile
        import pytest

        @pytest.mark.xfail(strict=True)
        def test_regtest_xfail_strict(regtest_all, tmpdir):

            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=0, passed=0, xfailed=1)

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(xfailed=1)

    result = testdir.runpytest()
    result.assert_outcomes(failed=1)


def test_failed_test(testdir):
    testdir.makepyfile(
        """
        import tempfile
        import pytest

        def test_regtest(regtest_all, tmpdir):

            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))

            assert False
         """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(failed=1)


def test_converter_pre_v2(testdir):
    testdir.makepyfile(
        """
        import tempfile
        from pytest_regtest import register_converter_pre

        @register_converter_pre
        def to_upper_conv(line):
            return line.upper()

        def test_regtest(regtest_all, tmpdir):
            print("this is expected outcome")
            print("obj id is 0xabcdeffff")
         """
    )
    # suprorcess to avoid that converters from other test functions
    # here in test_plugin.py are still registered:
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(failed=1)

    result.stdout.fnmatch_lines(
        [
            "regression test output not recorded yet for test_converter_pre_v2.py::test_regtest:",
            "",
            "THIS IS EXPECTED OUTCOME",
            "OBJ ID IS 0XABCDEFFFF",
        ]
    )


    result = testdir.runpytest_subprocess("--regtest-reset")
    result.assert_outcomes(passed=1)


def test_converter_pre(testdir):
    testdir.makepyfile(
        """
        import tempfile
        from pytest_regtest import register_converter_pre

        @register_converter_pre
        def to_upper_conv(line, request):
            return line.upper()

        def test_regtest(regtest_all, tmpdir):
            print("this is expected outcome")
            print("obj id is 0xabcdeffff")
         """
    )
    # suprorcess to avoid that converters from other test functions
    # here in test_plugin.py are still registered:
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(failed=1)

    result.stdout.fnmatch_lines(
        [
            "regression test output not recorded yet for test_converter_pre.py::test_regtest:",
            "",
            "THIS IS EXPECTED OUTCOME",
            "OBJ ID IS 0XABCDEFFFF",
        ]
    )

    result = testdir.runpytest_subprocess("--regtest-reset")
    result.assert_outcomes(passed=1)


def test_converter_post_pre_v2(testdir):
    testdir.makepyfile(
        """
        import tempfile
        from pytest_regtest import register_converter_post

        @register_converter_post
        def to_upper_conv(line):
            return line.upper()

        def test_regtest(regtest_all, tmpdir):
            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(failed=1)
    expected_diff = """
    regression test output not recorded yet for test_*::test_regtest:

    THIS IS EXPECTED OUTCOME
    <TMPDIR_FROM_FIXTURE>/TEST
    <TMPDIR_FROM_TEMPFILE_MODULE>
    <TMPDIR_FROM_TEMPFILE_MODULE>
    OBJ ID IS 0X?????????""".strip().splitlines()

    result.stdout.fnmatch_lines(
        [line.lstrip() for line in expected_diff], consecutive=True
    )

    result = testdir.runpytest_subprocess("--regtest-reset")
    result.assert_outcomes(passed=1)


def test_converter_post(testdir):
    testdir.makepyfile(
        """
        import tempfile
        from pytest_regtest import register_converter_post

        @register_converter_post
        def to_upper_conv(line, request):
            return line.upper()

        def test_regtest(regtest_all, tmpdir):
            print("this is expected outcome")
            print(tmpdir.join("test").strpath)
            print(tempfile.gettempdir())
            print(tempfile.mkdtemp())
            print("obj id is", hex(id(tempfile)))
         """
    )
    result = testdir.runpytest_subprocess()
    result.assert_outcomes(failed=1)

    expected_diff = """
    regression test output not recorded yet for test_*::test_regtest:

    THIS IS EXPECTED OUTCOME
    <TMPDIR_FROM_FIXTURE>/TEST
    <TMPDIR_FROM_TEMPFILE_MODULE>
    <TMPDIR_FROM_TEMPFILE_MODULE>
    OBJ ID IS 0X?????????""".strip().splitlines()

    result.stdout.fnmatch_lines(
        [line.lstrip() for line in expected_diff], consecutive=True
    )

    result = testdir.runpytest_subprocess("--regtest-reset")
    result.assert_outcomes(passed=1)


def test_consider_line_endings(create_test_regtest_fh):
    create_test_regtest_fh.runpytest("--regtest-reset")

    # just check if cmd line flags work without throwing exceptions:
    create_test_regtest_fh.runpytest("--regtest-consider-line-endings")


def test_tee(create_test_regtest_fh):
    create_test_regtest_fh.runpytest("--regtest-reset")

    # just check if cmd line flags work without throwing exceptions:
    result = create_test_regtest_fh.runpytest("--regtest-tee")
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(
        """
recorded raw output to regtest fixture: *
this is expected outcome
*
*
*
obj id is 0x*
""".strip().splitlines(),
        consecutive=True,
    )


def test_parameterized_tests(testdir):
    testdir.makepyfile(
        """
        import pytest

        @pytest.mark.parametrize("a", [1, "2", (1, 2, 3), "[]", "'a", '"b'])
        def test_regtest_parameterized(regtest, a):
            print(a, file=regtest)
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=6)

    result = testdir.runpytest("--regtest-reset", "-v")
    result.assert_outcomes(passed=6)

    result = testdir.runpytest()
    result.assert_outcomes(passed=6)


def test_with_long_filename_result_file(testdir):
    long_str = "abc123" * 20
    testdir.makepyfile(
        f"""
        import pytest

        @pytest.mark.parametrize("a", ["{long_str}"])
        def test_regtest_long(regtest, a):
            print(a, file=regtest)
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)

    test_func_id = "test_with_long_filename_result_file.py::test_regtest_long"
    test_func_id_fname = test_func_id.replace(".py::", ".")

    result.stdout.fnmatch_lines(
        f"""
regression test output not recorded yet for {test_func_id}[{long_str}]:

{long_str}
            """.strip().splitlines()
    )

    result = testdir.runpytest("--regtest-reset", "-v")
    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines(
        f"""
total number of failed regression tests: 0
the following output files have been reset:
  _regtest_outputs/{test_func_id_fname}[{long_str[:70]}__fa3b11731b.out
""".strip().splitlines(),
        consecutive=True,
    )

    result = testdir.runpytest()

    result.assert_outcomes(passed=1)


def test_disabled_std_conversion(testdir):
    testdir.makepyfile(
        """
        import time
        def test_regtest_long(regtest):
            print("object at 0x1027cbd90", file=regtest)
        """
    )
    result = testdir.runpytest()
    result.assert_outcomes(failed=1)

    result = testdir.runpytest("--regtest-reset")
    result.assert_outcomes(passed=1)

    result = testdir.runpytest("--regtest-disable-stdconv")
    result.assert_outcomes(failed=1)

    result.stdout.fnmatch_lines(
        [
            ">   -object at 0x1027cbd90",
            ">   +object at 0x?????????",
        ],
        consecutive=True,
    )
