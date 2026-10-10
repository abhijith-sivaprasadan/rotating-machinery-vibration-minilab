# Continuous integration

Add an end-to-end synthetic-tone FFT/report smoke check and preserve band integration compatibility with NumPy 2.x.

CI uses synthetic 25 Hz and 60 Hz tones to check frequency recovery, finite outputs and report generation. It does not validate phone sensor calibration or real rotating-machinery measurements. The local uncommitted API application is not part of this published branch.

Workflows: `.github/workflows/ci.yml`.
