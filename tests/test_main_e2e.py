"""Tests extremo a extremo de main.py (subproceso, sin red ni delays de red)."""
import subprocess
import sys


def test_main_salir_exit_code_cero():
    resultado = subprocess.run(
        [sys.executable, "main.py"],
        input="12\n",
        capture_output=True,
        text=True,
        timeout=15,
        cwd=".",
    )
    assert resultado.returncode == 0
    assert "¡Hasta luego!" in resultado.stdout


def test_main_flujo_sin_red():
    resultado = subprocess.run(
        [sys.executable, "main.py"],
        input="4\n\n12\n",
        capture_output=True,
        text=True,
        timeout=15,
        cwd=".",
    )
    assert resultado.returncode == 0
    assert "PELÍCULAS POPULARES" in resultado.stdout
    assert "¡Hasta luego!" in resultado.stdout