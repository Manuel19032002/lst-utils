import pathlib
import tempfile

from rutas_organize_def import (
    clean_path,
    find_version_folder,
    compress_logs,
    compress_history,
    compress_gainsel,
)


# =========================
# TEST clean_path
# =========================
def test_clean_path():
    raw = "xxx%(BASE)s/data/test"
    base = "/home/user"

    result = clean_path(raw, base)

    assert str(result) == "/home/user/data/test"


# =========================
# TEST find_version_folder
# =========================
def test_find_version_folder(tmp_path):
    day = tmp_path / "20250101"
    day.mkdir()

    v = day / "v0.11_test"
    v.mkdir()

    result = find_version_folder(day)

    assert result == v


# =========================
# TEST compress_logs (SIMULATION)
# =========================
def test_compress_logs_simulation(tmp_path):
    base = tmp_path / "v0.11"
    log = base / "log"

    log.mkdir(parents=True)

    # crear archivos fake
    (log / "a.err").write_text("error")
    (log / "b.out").write_text("output")

    compress_logs(base, simulate=True)

    # en simulación NO debe borrar ni crear tar
    assert (log / "a.err").exists()
    assert (log / "b.out").exists()
    assert not (log / "logs_err.tar.gz").exists()
    assert not (log / "logs_out.tar.gz").exists()


# =========================
# TEST compress_history (SIMULATION)
# =========================
def test_compress_history_simulation(tmp_path):
    base = tmp_path

    f = base / "file.history"
    f.write_text("data")

    compress_history(base, simulate=True)

    # no debe borrar ni crear tar
    assert f.exists()
    assert not (base / "all_history.tar.gz").exists()


# =========================
# TEST compress_gainsel (SIMULATION)
# =========================
def test_compress_gainsel_simulation(tmp_path):
    path = tmp_path

    (path / "a.log").write_text("log")
    (path / "b_check.log").write_text("log")

    compress_gainsel(path, simulate=True)

    assert (path / "a.log").exists()
    assert (path / "b_check.log").exists()
    assert not (path / "normal_logs.tar.gz").exists()
    assert not (path / "check_logs.tar.gz").exists()
# =====================================
# Ahora los reales
#=====================================

def test_compress_logs_real(tmp_path):
    base = tmp_path / "v0.11"
    log = base / "log"
    log.mkdir(parents=True)

    err = log / "a.err"
    out = log / "b.out"

    err.write_text("error")
    out.write_text("output")

    # ejecución REAL
    compress_logs(base, simulate=False)

    # ✔ se crean tar
    assert (log / "logs_err.tar.gz").exists()
    assert (log / "logs_out.tar.gz").exists()

    # ✔ se borran originales
    assert not err.exists()
    assert not out.exists()

#==============================================

def test_compress_history_real(tmp_path):
    base = tmp_path

    f = base / "file.history"
    f.write_text("data")

    compress_history(base, simulate=False)

    # ✔ tar creado
    assert (base / "all_history.tar.gz").exists()

    # ✔ original borrado
    assert not f.exists()
#================================================

def test_compress_gainsel_real(tmp_path):
    path = tmp_path

    a = path / "a.log"
    b = path / "b_check.log"

    a.write_text("log")
    b.write_text("log")

    compress_gainsel(path, simulate=False)

    # ✔ tars creados
    assert (path / "normal_logs.tar.gz").exists()
    assert (path / "check_logs.tar.gz").exists()

    # ✔ originales borrados
    assert not a.exists()
    assert not b.exists()
#==========================================
# Nightfinish
#==========================================
import subprocess
import os

def test_launcher_no_nightfinished(tmp_path, monkeypatch):
    # simulamos LSTN1
    fake_root = tmp_path

    monkeypatch.setenv("LSTN1", str(fake_root))
    monkeypatch.setenv("OBS_DATE", "20260101")

    # NO creamos NightFinished.txt

    result = subprocess.run(
        ["bash", "launch_organize.sh", "-s", "--no-gainsel", "--no-running"],
        capture_output=True,
        text=True
    )

    # comprobamos que NO se ejecuta el flujo real del launcher
    assert result.returncode == 0
#=========================================================

def test_launcher_with_nightfinished(tmp_path, monkeypatch):
    fake_root = tmp_path

    monkeypatch.setenv("LSTN1", str(fake_root))
    monkeypatch.setenv("OBS_DATE", "20260101")

    obsdate = "20260101"

    # creamos estructura simulada
    night_file = fake_root / "OSA/Closer" / obsdate / "v0.11" / "NightFinished.txt"
    night_file.parent.mkdir(parents=True, exist_ok=True)
    night_file.write_text("done")

    result = subprocess.run(
        ["bash", "launch_organize.sh", "-s", "--no-gainsel", "--no-running"],
        capture_output=True,
        text=True
    )

    # comprobación SOLO de la condición real del sistema
    assert night_file.exists()
    assert result.returncode == 0
