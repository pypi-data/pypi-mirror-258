project('pypkgconf',
    ['c'],
    license: 'Apache-2.0',
    meson_version: '>=1.1.0',
    version: '2.1.1',
)



fs = import('fs')
pymod = import('python')
py = pymod.find_installation(modules: ['cffi'], pure: false)

pkgconf = subproject('pkgconf')
libpkgconf = pkgconf.get_variable('dep_libpkgconf')
libpkgconf_c = '_libpkgconf.c'
libpkgconf_include = meson.global_source_root() / 'subprojects' / 'pkgconf-2.1.1'
cdata = pkgconf.get_variable('cdata')
build_static = pkgconf.get_variable('build_static')

c_bindings = custom_target(
    'libpkgconf_c',
    command: [py, meson.current_source_dir() / 'cffibuild.py', libpkgconf_include, '@OUTPUT@'],
    output: [libpkgconf_c],
    depend_files: ['cffibuild.py'],
)


subdir('pypkgconf')

pytest = pymod.find_installation(modules: ['pytest'], required: false)
if pytest.found()
    pytest_env = environment(
        {
            'PYTHONPATH': meson.current_build_dir(),
            'PKG_DEFAULT_PATH': cdata.get_unquoted('PKG_DEFAULT_PATH')
        }
    )

    test(
        'pypkgconf',
        pytest,
        args: [
            '-m', 'pytest',
            '-vv',
            # '-o log_cli=true', '--log-cli-level=DEBUG',
            meson.current_source_dir() / 'tests'],
        env: pytest_env,
        depends: test_python_files,
    )
else
    message('Skipping Python tests as pytest was not found.')
endif
