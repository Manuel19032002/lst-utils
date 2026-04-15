import pathlib
import shutil
import tarfile

SIMULATION = True  # 🔴 cambiar a False cuando estés seguro

# =========================
# PATHS
# =========================
RUNNING_PATH = pathlib.Path("running_an_comp/v0.11")
GAINSEL_PATH = pathlib.Path("GainSelec_comp")


# =========================
# 1. RUNNING ANALYSIS (LOGS)
# =========================
def compress_running_logs():
    log_path = RUNNING_PATH / "log"

    if not log_path.exists():
        print("[RUNNING] No log directory found")
        return

    err_files = list(log_path.glob("*.err"))
    out_files = list(log_path.glob("*.out"))

    err_tar = log_path / "logs_err.tar.gz"
    out_tar = log_path / "logs_out.tar.gz"

    print(f"[RUNNING] {len(err_files)} .err files")
    print(f"[RUNNING] {len(out_files)} .out files")

    # ---- ERR ----
    if err_files:
        print(f"[RUNNING] Compressing .err → {err_tar.name}")

        if not SIMULATION:
            with tarfile.open(err_tar, "w:gz") as tar:
                for f in err_files:
                    tar.add(f, arcname=f.name)

            for f in err_files:
                f.unlink()

            print("     ✅ .err compressed")

    # ---- OUT ----
    if out_files:
        print(f"[RUNNING] Compressing .out → {out_tar.name}")

        if not SIMULATION:
            with tarfile.open(out_tar, "w:gz") as tar:
                for f in out_files:
                    tar.add(f, arcname=f.name)

            for f in out_files:
                f.unlink()

            print("     ✅ .out compressed")


# =========================
# 2. RUNNING ANALYSIS (HISTORY)
# =========================
def compress_history_direct():
    files = list(RUNNING_PATH.glob("*.history"))

    grouped = {}

    for f in files:
        key = f.name.split(".")[0]
        grouped.setdefault(key, []).append(f)

    for key, group_files in grouped.items():
        tar_name = RUNNING_PATH / f"{key}.tar.gz"

        print(f"[RUNNING] Compressing history {key} ({len(group_files)} files)")

        if SIMULATION:
            continue

        try:
            with tarfile.open(tar_name, "w:gz") as tar:
                for f in group_files:
                    tar.add(f, arcname=f.name)

            for f in group_files:
                f.unlink()

            print("     ✅ history compressed")

        except Exception as e:
            print(f"     ❌ ERROR: {e}")


# =========================
# 3. GAIN SELECTION LOGS
# =========================
def compress_gain_logs():
    if not GAINSEL_PATH.exists():
        print("[GAINSEL] Directory not found")
        return

    check_logs = list(GAINSEL_PATH.glob("*check*.log"))
    normal_logs = [f for f in GAINSEL_PATH.glob("*.log") if "check" not in f.name]

    check_tar = GAINSEL_PATH / "check_logs.tar.gz"
    normal_tar = GAINSEL_PATH / "normal_logs.tar.gz"

    print(f"[GAINSEL] {len(check_logs)} check logs")
    print(f"[GAINSEL] {len(normal_logs)} normal logs")

    # ---- CHECK ----
    if check_logs:
        print(f"[GAINSEL] Compressing check logs → {check_tar.name}")

        if not SIMULATION:
            with tarfile.open(check_tar, "w:gz") as tar:
                for f in check_logs:
                    tar.add(f, arcname=f.name)

            for f in check_logs:
                f.unlink()

            print("     ✅ check logs compressed")

    # ---- NORMAL ----
    if normal_logs:
        print(f"[GAINSEL] Compressing normal logs → {normal_tar.name}")

        if not SIMULATION:
            with tarfile.open(normal_tar, "w:gz") as tar:
                for f in normal_logs:
                    tar.add(f, arcname=f.name)

            for f in normal_logs:
                f.unlink()

            print("     ✅ normal logs compressed")


# =========================
# MAIN
# =========================
def main():
    print(f"Mode: {'SIMULATION' if SIMULATION else 'REAL'}")
    print("=" * 60)

    print("\n🔹 RUNNING ANALYSIS")
    compress_running_logs()
    compress_history_direct()

    print("\n🔹 GAIN SELECTION")
    compress_gain_logs()

    print("\n" + "=" * 60)
    print("Done.")


if __name__ == "__main__":
    main()
