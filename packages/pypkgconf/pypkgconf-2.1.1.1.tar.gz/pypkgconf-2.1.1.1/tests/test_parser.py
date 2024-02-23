import pypkgconf

import pytest

import logging


def test_comments(lib1_env):
    result = pypkgconf.query_args("--libs comments", env=lib1_env)

    assert result == ["-lfoo"]


def test_comments_in_fields(lib1_env):
    result = pypkgconf.query_args("--libs comments-in-fields", env=lib1_env)

    assert result == ["-lfoo"]


def test_dos(lib1_env):
    result = pypkgconf.query_args("--libs dos-lineendings", env=lib1_env)

    assert result == ["-L/test/lib/dos-lineendings", "-ldos-lineendings"]


def test_no_trailing_newline(lib1_env):
    result = pypkgconf.query_args("--cflags no-trailing-newline", env=lib1_env)

    assert result == ["-I/test/include/no-trailing-newline"]


def test_parse(lib1_env):
    result = pypkgconf.query_args("--libs argv-parse", env=lib1_env)

    assert result == ["-llib-3", "-llib-1", "-llib-2", "-lpthread"]


def test_bad_option(lib1_env):
    with pytest.raises(pypkgconf.PkgConfError):
        pypkgconf.query_args("--exists -foo", env=lib1_env)


def test_argv_parse_3(lib1_env):
    result = pypkgconf.query_args("--libs argv-parse-3", env=lib1_env)

    assert result == ["-llib-1", "-pthread", "/test/lib/lib2.so"]


def test_quoting(lib1_env):
    result = pypkgconf.query_args("--libs tilde-quoting", env=lib1_env)
    assert result == ["-L~", "-ltilde"]

    result = pypkgconf.query_args("--cflags tilde-quoting", env=lib1_env)
    assert result == ["-I~"]


def test_paren_quoting(lib1_env):
    result = pypkgconf.query_args("--libs paren-quoting", env=lib1_env)

    # FIXME: escape $?
    assert result == ["-L$(libdir)", "-ltilde"]


def test_multiline_field(lib1_env):
    result = pypkgconf.query_args("--list-all", env=lib1_env)

    assert "multiline description" in "\n".join(result)


def test_multiline_bogus_header(lib1_env):
    assert pypkgconf.query_args("--exists multiline-bogus", env=lib1_env) == []


def test_escaped_backslash(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(f"--with-path={selfdir} --cflags escaped-backslash")

    assert result == ["-IC:\\\\A"]


def test_quoted(lib1_env):
    result = pypkgconf.query_args("--cflags quotes", env=lib1_env)

    # FIXME: is it ok?
    assert result == [
        '-DQUOTED=\\"bla\\"',
        '-DA=\\"escaped\\ string\\\'\\ literal\\"',
        "-DB=\\\\1$",
        "-DC=bla",
    ]


def test_flag_order_1(lib1_env):
    result = pypkgconf.query_args("--libs flag-order-1", env=lib1_env)

    assert result == ["-L/test/lib", "-Bdynamic", "-lfoo", "-Bstatic", "-lbar"]


def test_flag_order_2(lib1_env):
    result = pypkgconf.query_args("--libs flag-order-1 foo", env=lib1_env)

    assert result == ["-L/test/lib", "-Bdynamic", "-lfoo", "-Bstatic", "-lbar", "-lfoo"]


def test_flag_order_3(lib1_env):
    result = pypkgconf.query_args("--libs flag-order-3", env=lib1_env)

    assert result == [
        "-L/test/lib",
        "-Wl,--start-group",
        "-lfoo",
        "-lbar",
        "-Wl,--end-group",
    ]


def test_flag_order_4(lib1_env):
    result = pypkgconf.query_args("--libs flag-order-3 foo", env=lib1_env)

    assert result == [
        "-L/test/lib",
        "-Wl,--start-group",
        "-lfoo",
        "-lbar",
        "-Wl,--end-group",
        "-lfoo",
    ]


def test_variable_whitespace(lib1_env):
    result = pypkgconf.query_args("--cflags variable-whitespace", env=lib1_env)

    assert result == ["-I/test/include"]


def test_fragment_quoting(lib1_env):
    result = pypkgconf.query_args("--cflags fragment-quoting", env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", '-DQUOTED=\\"/test/share/doc\\"']


def test_fragment_quoting_2(lib1_env):
    result = pypkgconf.query_args("--cflags fragment-quoting-2", env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", "-DQUOTED=/test/share/doc"]


def test_fragment_quoting_3(lib1_env):
    result = pypkgconf.query_args("--cflags fragment-quoting-3", env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", '-DQUOTED=\\"/test/share/doc\\"']


def test_fragment_quoting_5(lib1_env):
    result = pypkgconf.query_args("--cflags fragment-quoting-5", env=lib1_env)

    assert result == ["-fPIC", "-I/test/include/foo", "-DQUOTED=/test/share/doc"]


def test_fragment_quoting_7(lib1_env):
    result = pypkgconf.query_args("--cflags fragment-quoting-7", env=lib1_env)

    assert result == [
        "-Dhello=10",
        "-Dworld=+32",
        "-DDEFINED_FROM_PKG_CONFIG=hello\\ world",
    ]


def test_fragment_escaping_1(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(f"--with-path={selfdir} --cflags fragment-escaping-1")

    assert result == ["-IC:\\\\D\\ E"]


def test_fragment_escaping_2(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(f"--with-path={selfdir} --cflags fragment-escaping-2")

    assert result == ["-IC:\\\\D\\ E"]


def test_fragment_escaping_3(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(f"--with-path={selfdir} --cflags fragment-escaping-3")

    assert result == ["-IC:\\\\D\\ E"]


# FIXME: how to test macro arithmetics in Python...
# def test_fragment_quoting_7a(testsdir):
#     selfdir = (testsdir / 'lib1').as_posix()
#     result = pypkgconf.query_args(f'--with-path={selfdir} --cflags fragment-quoting-7')

#     assert result == ['-Dhello=10', '-Dworld=+32', '-DDEFINED_FROM_PKG_CONFIG=hello\\ world']

# 	cat > test.c <<- __TESTCASE_END__
# 		int main(int argc, char *argv[]) { return DEFINED_FROM_PKG_CONFIG; }
# 	__TESTCASE_END__
# 	cc -o test-fragment-quoting-7 ${test_cflags} ./test.c
# 	atf_check -e 42 ./test-fragment-quoting-7
# 	rm -f test.c test-fragment-quoting-7


def test_fragment_comment(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(f"--with-path={selfdir} --cflags fragment-comment")

    assert result == ["kuku=\\#ttt"]


@pytest.mark.skip(reason="--msvc-syntax not implemented")
def test_msvc_fragment_quoting(lib1_env):
    result = pypkgconf.query_args(
        "--libs --msvc-syntax fragment-escaping-1", env=lib1_env
    )

    assert result == ['/libpath:"C:\\D E"', "E.lib"]


@pytest.mark.skip(reason="--msvc-syntax not implemented")
def test_msvc_fragment_render_cflags(lib1_env):
    result = pypkgconf.query_args("--cflags --static --msvc-syntax foo", env=lib1_env)

    assert result == ["/I/test/include/foo", "/DFOO_STATIC"]


def test_tuple_dequote(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(f"--with-path={selfdir} --libs tuple-quoting")

    assert result == ["-L/test/lib", "-lfoo"]


def test_version_with_whitespace(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(
        f"--with-path={selfdir} --modversion malformed-version"
    )

    assert result == ["3.922"]


def test_version_with_whitespace_2(testsdir):
    selfdir = (testsdir / "lib1").as_posix()
    result = pypkgconf.query_args(
        f"--with-path={selfdir} --print-provides malformed-version"
    )

    assert result == ["malformed-version = 3.922"]


def test_version_with_whitespace_diagnostic(testsdir, caplog):
    selfdir = (testsdir / "lib1").as_posix()

    with caplog.at_level(logging.WARNING):
        result = pypkgconf.query_args(
            f"--with-path={selfdir} --validate malformed-version"
        )

    assert result == []
    assert any(record.levelname == "WARNING" for record in caplog.records)
