from ._libpkgconf import ffi, lib


def pypkgconf_version() -> str:
    return '2.1.1'


def pkgconf_version() -> str:
    return ffi.string(lib.package_version()).decode()
