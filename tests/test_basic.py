"""
Test creating Miniconda installation and provisioning.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

from mcinstall import MinicondaInstaller, config


def test_show_config():
    print(json.dumps(config, indent=4))


def test_uname_m():
    out = subprocess.check_output(["uname", "-m"])
    print(out.decode("utf-8"))


def test_install_dependencies():
    with tempfile.TemporaryDirectory() as tempdir:
        mci = MinicondaInstaller(tempdir, verbose=True)
        mci.download()
        mci.install_miniconda()
        mci.update_miniconda_base()
        mci.install_pip(dependencies=["geopy"])
        mci.install_conda(channel="conda-forge", dependencies=["pyyaml"])

        # Run Miniconda's Python and import the installed dependencies.
        for pkg_name in ["geopy", "pyyaml"]:
            if pkg_name == "pyyaml":
                pkg_name = "yaml"
            cmd = [
                "%s/bin/python" % tempdir,
                "-c",
                '''import %s; print("%s %%s ok" %% %s.__version__)''' % \
                    (pkg_name, pkg_name, pkg_name)
            ]
            out = subprocess.check_output(cmd).decode("utf-8").strip()
            print(out)
            assert re.match("%s .+ ok" % pkg_name, out)

    print()
    assert not os.path.exists(tempdir)


def test_install_dependencies_index_url():
    with tempfile.TemporaryDirectory() as tempdir:
        mci = MinicondaInstaller(tempdir, verbose=True)
        mci.download()
        mci.install_miniconda()
        mci.update_miniconda_base()
        mci.install_pip(dependencies=["pypi_pkg_test"], index_url="https://test.pypi.org/simple/")

        # Run Miniconda's Python and import the installed dependencies.
        for pkg_name in ["pypi_pkg_test"]:
            cmd = [
                "%s/bin/python" % tempdir,
                "-c",
                '''import %s; print("%s %%s ok" %% %s)''' % \
                (pkg_name, pkg_name, pkg_name)
            ]
            out = subprocess.check_output(cmd).decode("utf-8").strip()
            print(out)
            assert re.match("%s .+ ok" % pkg_name, out)

    print()
    assert not os.path.exists(tempdir)


def test_install_dependencies_extra_index_url():
    with tempfile.TemporaryDirectory() as tempdir:
        mci = MinicondaInstaller(tempdir, verbose=True)
        mci.download()
        mci.install_miniconda()
        mci.update_miniconda_base()
        mci.install_pip(dependencies=["pypi_pkg_test"], index_url="https://test.pypi.org/simpletest/", extra_index_url="https://test.pypi.org/simple/")

        # Run Miniconda's Python and import the installed dependencies.
        for pkg_name in ["pypi_pkg_test"]:
            cmd = [
                "%s/bin/python" % tempdir,
                "-c",
                '''import %s; print("%s %%s ok" %% %s)''' % \
                (pkg_name, pkg_name, pkg_name)
            ]
            out = subprocess.check_output(cmd).decode("utf-8").strip()
            print(out)
            assert re.match("%s .+ ok" % pkg_name, out)

    print()
    assert not os.path.exists(tempdir)


def test_install_dependencies_extra_index_urls():
    with tempfile.TemporaryDirectory() as tempdir:
        mci = MinicondaInstaller(tempdir, verbose=True)
        mci.download()
        mci.install_miniconda()
        mci.update_miniconda_base()
        mci.install_pip(dependencies=["pypi_pkg_test"], index_url="https://test.pypi.org/simpletest/", extra_index_url="https://test.pypi.org/simpletest1/, https://test.pypi.org/simple/")

        # Run Miniconda's Python and import the installed dependencies.
        for pkg_name in ["pypi_pkg_test"]:
            cmd = [
                "%s/bin/python" % tempdir,
                "-c",
                '''import %s; print("%s %%s ok" %% %s)''' % \
                (pkg_name, pkg_name, pkg_name)
            ]
            out = subprocess.check_output(cmd).decode("utf-8").strip()
            print(out)
            assert re.match("%s .+ ok" % pkg_name, out)

    print()
    assert not os.path.exists(tempdir)
