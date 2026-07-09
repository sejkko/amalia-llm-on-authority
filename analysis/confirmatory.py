#!/usr/bin/env python3
"""Pre-registered confirmatory analysis (Zenodo DOI 10.5281/zenodo.21178967, §4–§5).

Primary endpoint: recovery gap Δ = F1(undecomposed) − F1(stated_formula) per instruction
condition, on the 448 texts unseen at registration (corpus.csv: pilot300 == "no").
H1: Δ ≥ 0.10 in both conditions with 95% bootstrap CI lower bound > 0.05.
H2: Δ(PT) < Δ(EN), CI of the paired difference excludes 0.
S3: D_entity firing < 40% in both conditions.
Bootstrap: 10,000 text resamples, seed 20260703.

Run from the repository root:  python3 analysis/confirmatory.py
"""
from __future__ import annotations

import csv
import numpy as np

SEED, B = 20260703, 10_000


def f1(y, g):
    tp = ((y == 1) & (g == 1)).sum(); fp = ((y == 1) & (g == 0)).sum()
    fn = ((y == 0) & (g == 1)).sum()
    return 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0


def load(name):
    corpus = {r['text_id']: r for r in csv.DictReader(open('data/corpus.csv'))}
    ann = {r['text_id']: r for r in csv.DictReader(open(f'data/annotations/{name}.csv'))}
    ids = sorted(ann)
    hol = np.array([int(ann[t]['undecomposed']) for t in ids])
    form = np.array([int(ann[t]['stated_formula']) for t in ids])
    dent = np.array([int(ann[t]['D_entity']) for t in ids])
    gt = np.array([int(corpus[t]['gt_code']) for t in ids])
    fresh = np.array([corpus[t]['pilot300'] == 'no' for t in ids])
    return hol, form, dent, gt, fresh


def main():
    boot = {}
    for cond, name in [('pt', 'amalia_pt'), ('en', 'amalia_en')]:
        hol, form, dent, gt, fresh = load(name)
        rng = np.random.default_rng(SEED)
        h, f = f1(hol[fresh], gt[fresh]), f1(form[fresh], gt[fresh])
        n = int(fresh.sum()); sel = np.where(fresh)[0]
        idx = rng.integers(0, n, size=(B, n))
        gaps = np.array([f1(hol[sel[i]], gt[sel[i]]) - f1(form[sel[i]], gt[sel[i]]) for i in idx])
        lo, hi = np.percentile(gaps, [2.5, 97.5])
        boot[cond] = gaps
        verdict = 'OPEN' if (h - f >= 0.10 and lo > 0.05) else ('CLOSED' if h - f < 0.05 else 'INDETERMINATE')
        print(f"{cond.upper()} 448: undecomposed {h:.3f}  formula {f:.3f}  "
              f"Δ={h - f:+.3f}  CI95[{lo:+.3f},{hi:+.3f}]  → gap {verdict}")
        print(f"   S3 D_entity firing: {dent[fresh].mean():.1%} "
              f"({'PASS' if dent[fresh].mean() < 0.40 else 'FAIL'} <40%)")

    # H2 paired on the same texts
    hp, fp_, _, gp, fresh = load('amalia_pt')
    he, fe, _, ge, _ = load('amalia_en')
    rng = np.random.default_rng(SEED)
    n = int(fresh.sum()); sel = np.where(fresh)[0]
    idx = rng.integers(0, n, size=(B, n))
    diffs = np.array([(f1(he[sel[i]], ge[sel[i]]) - f1(fe[sel[i]], ge[sel[i]]))
                      - (f1(hp[sel[i]], gp[sel[i]]) - f1(fp_[sel[i]], gp[sel[i]])) for i in idx])
    point = (f1(he[fresh], ge[fresh]) - f1(fe[fresh], ge[fresh])) - \
            (f1(hp[fresh], gp[fresh]) - f1(fp_[fresh], gp[fresh]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    print(f"H2 Δ(EN)−Δ(PT): {point:+.3f}  CI95[{lo:+.3f},{hi:+.3f}]  "
          f"→ {'SUPPORTED' if lo > 0 else ('REVERSED' if hi < 0 else 'NOT SUPPORTED (CI spans 0)')}")


if __name__ == '__main__':
    main()
