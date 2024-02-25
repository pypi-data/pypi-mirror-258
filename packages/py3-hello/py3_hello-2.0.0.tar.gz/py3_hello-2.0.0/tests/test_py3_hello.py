# -*- coding: utf-8 -*-

from click.testing import CliRunner
from py3_hello import py3_hello


class TestPy3Hello:
    def test_hello_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(py3_hello.hello, ["--help"])
        assert result.exit_code == 0
        assert "[OPTIONS]" in result.stdout

    def test_hello_version(self) -> None:
        runner = CliRunner()
        result = runner.invoke(py3_hello.hello, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.stdout

    def test_hello_no_option(self) -> None:
        runner = CliRunner()
        result = runner.invoke(py3_hello.hello)
        assert result.exit_code == 0
        assert "Hello, World!" in result.stdout

    def test_hello_short_option(self) -> None:
        runner = CliRunner()
        result = runner.invoke(py3_hello.hello, ["-n", "Alice"])
        assert result.exit_code == 0
        assert "Hello, Alice!" in result.stdout

    def test_hello_long_option(self) -> None:
        runner = CliRunner()
        result = runner.invoke(py3_hello.hello, ["--name", "Alice"])
        assert result.exit_code == 0
        assert "Hello, Alice!" in result.stdout
