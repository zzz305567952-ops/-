"""Dependency-free checks that keep offline test runs actionable."""

from __future__ import annotations

from pathlib import Path


def test_app_package_and_requirements_are_present() -> None:
    repo_root = Path(__file__).resolve().parents[1]

    assert (repo_root / "app" / "__init__.py").is_file()
    assert (repo_root / "app" / "main.py").is_file()
    assert (repo_root / "requirements.txt").is_file()

    requirements = (repo_root / "requirements.txt").read_text(encoding="utf-8")
    for package_name in ("fastapi", "pydantic", "python-docx", "openpyxl", "python-multipart", "uvicorn"):
        assert package_name in requirements
