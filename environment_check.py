"""Verify that the course development environment is ready."""

import importlib
import platform
import shutil
import sys

REQUIRED_PACKAGES = ["numpy", "matplotlib", "pandas", "pytest"]


def main() -> int:
    """Run environment checks and return 0 on success, 1 on failure."""
    print("Advanced Algorithms - Environment Check")
    print("=" * 42)
    print(f"Python version: {platform.python_version()}")
    print(f"Python executable: {sys.executable}")

    ok = True

    if sys.version_info < (3, 9):
        print("[FAIL] Python 3.9 or later is required.")
        ok = False
    else:
        print("[PASS] Python version is supported.")

    for package in REQUIRED_PACKAGES:
        try:
            module = importlib.import_module(package)
            version = getattr(module, "__version__", "installed")
            print(f"[PASS] {package}: {version}")
        except ImportError:
            print(f"[FAIL] {package} is not installed.")
            ok = False

    if shutil.which("git"):
        print("[PASS] Git is installed.")
    else:
        print("[FAIL] Git was not found in PATH.")
        ok = False

    print("=" * 42)
    if ok:
        print("Environment is ready.")
        return 0

    print("Environment needs attention. Fix the failed items above.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
