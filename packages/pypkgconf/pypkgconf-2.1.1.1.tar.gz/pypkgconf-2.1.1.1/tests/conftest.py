import pytest

import os
from pathlib import Path
import typing as T


@pytest.fixture
def testsdir() -> Path:
    """Get the most recent version of pkgconf-x.y.z"""
    subprojects = Path(__file__).parents[1] / 'subprojects'
    pkgconf_dirs = sorted(d for d in subprojects.iterdir() if d.name.startswith('pkgconf-'))
    return  pkgconf_dirs[-1] / 'tests'


@pytest.fixture
def lib1_env(testsdir) -> T.Dict[str, str]:
    return {'PKG_CONFIG_PATH': str(testsdir / 'lib1')}


@pytest.fixture
def lib2_env(testsdir) -> T.Dict[str, str]:
    return {'PKG_CONFIG_PATH': str(testsdir / 'lib2')}


@pytest.fixture
def lib1_lib2_env(lib1_env, lib2_env) -> T.Dict[str, str]:
    paths = [lib1_env['PKG_CONFIG_PATH'], lib2_env['PKG_CONFIG_PATH']]
    return {'PKG_CONFIG_PATH': os.pathsep.join(paths)}
