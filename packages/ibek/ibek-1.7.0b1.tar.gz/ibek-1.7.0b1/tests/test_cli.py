"""
System tests that run the CLI commands and compare the output to expected
results.
"""

import json
import subprocess
import sys
from pathlib import Path

from pytest_mock import MockerFixture

from ibek import __version__
from ibek.globals import IBEK_DEFS, PVI_DEFS, PVI_YAML_PATTERN, SUPPORT_YAML_PATTERN
from ibek.ioc import clear_entity_model_ids
from ibek.runtime_cmds.commands import generate
from ibek.support_cmds.commands import generate_links
from tests.conftest import run_cli


def test_cli_version():
    cmd = [sys.executable, "-m", "ibek", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__


def test_ibek_schema(tmp_path: Path, samples: Path):
    """generate the global ibek schema"""
    schema_path = tmp_path / "schema.json"
    run_cli("support", "generate-schema", "--output", schema_path)
    expected = json.loads(
        (samples / "schemas" / "ibek.support.schema.json").read_text()
    )

    actual = json.loads((schema_path).read_text())
    assert expected == actual


def test_single_schema(tmp_path: Path, samples: Path):
    """generate schema from a support module definition yaml"""
    clear_entity_model_ids()

    schema_path = tmp_path / "single.ibek.support.schema.json"
    yaml_path = samples / "support" / "motorSim.ibek.support.yaml"
    run_cli("ioc", "generate-schema", yaml_path, "--output", schema_path)

    expected = json.loads(
        (samples / "schemas" / "single.ibek.ioc.schema.json").read_text()
    )

    actual = json.loads((schema_path).read_text())
    assert expected == actual


def test_motor_sim_schema(tmp_path: Path, samples: Path):
    clear_entity_model_ids()
    """generate schema for a container with two support modules"""

    schema_combined = tmp_path / "motorSim.ibek.ioc.schema.json"
    yaml_path1 = samples / "support" / "asyn.ibek.support.yaml"
    yaml_path2 = samples / "support" / "motorSim.ibek.support.yaml"
    run_cli(
        "ioc",
        "generate-schema",
        "--no-ibek-defs",
        yaml_path1,
        yaml_path2,
        "--output",
        schema_combined,
    )

    expected = json.loads(
        (samples / "schemas" / "motorSim.ibek.ioc.schema.json").read_text()
    )

    actual = json.loads((schema_combined).read_text())
    assert expected == actual


def test_build_runtime_motorSim(tmp_path: Path, samples: Path):
    """
    build an ioc runtime script from an IOC instance entity file
    and multiple support module definition files

    Also verifies database subst file generation for multiple
    entity instantiations.
    """
    clear_entity_model_ids()
    ioc_yaml = samples / "iocs" / "ibek-mo-ioc-01.yaml"
    support_yaml1 = samples / "support" / "asyn.ibek.support.yaml"
    support_yaml2 = samples / "support" / "motorSim.ibek.support.yaml"
    out_file = tmp_path / "motorSim.st.cmd"
    out_db = tmp_path / "motorSim.ioc.subst"

    generate(
        ioc_yaml,
        [support_yaml1, support_yaml2],
        out_file,
        out_db,
    )

    example_boot = (samples / "outputs" / "motorSim.st.cmd").read_text()
    actual_boot = out_file.read_text()
    assert example_boot == actual_boot

    example_db = (samples / "outputs" / "motorSim.ioc.subst").read_text()
    actual_db = out_db.read_text()
    assert example_db == actual_db

    example_index = (samples / "outputs" / "index.bob").read_text()
    actual_index = (samples / "epics" / "opi" / "index.bob").read_text()
    assert example_index == actual_index

    example_pvi = (samples / "outputs" / "simple.pvi.bob").read_text()
    actual_pvi = (samples / "epics" / "opi" / "simple.pvi.bob").read_text()
    assert example_pvi == actual_pvi


def test_build_utils_features(tmp_path: Path, samples: Path):
    """
    build an ioc runtime script to verify utils features
    """
    clear_entity_model_ids()
    ioc_yaml = samples / "iocs" / "utils.ibek.ioc.yaml"
    support_yaml = samples / "support" / "utils.ibek.support.yaml"
    out_file = tmp_path / "st.cmd"
    out_db = tmp_path / "ioc.subst"

    run_cli(
        "runtime",
        "generate",
        ioc_yaml,
        support_yaml,
        "--out",
        out_file,
        "--db-out",
        out_db,
    )

    example_boot = (samples / "outputs" / "utils.st.cmd").read_text()
    actual_boot = out_file.read_text()
    assert example_boot == actual_boot

    example_db = (samples / "outputs" / "utils.ioc.subst").read_text()
    actual_db = out_db.read_text()
    assert example_db == actual_db


def test_generate_links_ibek(samples: Path, mocker: MockerFixture):
    symlink_mock = mocker.patch("ibek.support_cmds.commands.symlink_files")

    generate_links(samples / "support")

    symlink_mock.assert_any_call(samples / "support", PVI_YAML_PATTERN, PVI_DEFS)
    symlink_mock.assert_any_call(samples / "support", SUPPORT_YAML_PATTERN, IBEK_DEFS)
