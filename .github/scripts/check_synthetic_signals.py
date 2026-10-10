"""End-to-end FFT/report regression using explicitly synthetic analytic tones."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix="phyphox-ci-") as directory:
    work = Path(directory)
    time = np.arange(8000) / 400.0
    for i, frequency in enumerate((25.0, 60.0), start=1):
        pd.DataFrame({"Time (s)": time,
                      "Linear Acceleration z (m/s^2)": np.sin(2*np.pi*frequency*time)}).to_csv(
            work / f"Raw Data Speed {i}.csv", index=False)
    subprocess.run([sys.executable, str(ROOT / "src/phyphox_all_in_one.py")],
                   cwd=work, env=dict(os.environ, MPLBACKEND="Agg"), check=True, timeout=180)
    output = work / "phyphox_full_report"
    metrics = pd.read_csv(output / "summary_metrics.csv")
    print(metrics.to_string(index=False))
    assert len(metrics) == 2
    assert np.isfinite(metrics.select_dtypes(include="number").to_numpy()).all()
    np.testing.assert_allclose(metrics["DominantPeak_Hz"], [25.0, 60.0], atol=0.2, rtol=0)
    assert (output / "report.html").stat().st_size > 0
    assert len(list(output.glob("*.png"))) >= 10
    print("PASS: synthetic frequency recovery, finite metrics, report and plots")
