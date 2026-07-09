#!/usr/bin/env python3
"""Recovery-gap table for all annotators (baselines EXPLORATORY per pre-registration §6).

Δ = F1(undecomposed) − F1(stated_formula), on the 448 out-of-sample texts and the 748
total. GPT-OSS: 142 missing calls were imputed as "no" at ingest (see
data/annotations/gptoss_en_missing_calls.csv for a per-call manifest).

Run from the repository root:  python3 analysis/gap_table.py
"""
from __future__ import annotations

import csv
import numpy as np


def f1(y, g):
    tp = ((y == 1) & (g == 1)).sum(); fp = ((y == 1) & (g == 0)).sum()
    fn = ((y == 0) & (g == 1)).sum()
    return 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0


def main():
    corpus = {r['text_id']: r for r in csv.DictReader(open('data/corpus.csv'))}
    print(f"{'annotator':12} {'scope':6} {'undecomposed':>12} {'formula':>8} {'Δ':>7}")
    for name in ['amalia_pt', 'amalia_en', 'llama_en', 'gptoss_en']:
        ann = {r['text_id']: r for r in csv.DictReader(open(f'data/annotations/{name}.csv'))}
        ids = sorted(ann)
        hol = np.array([int(ann[t]['undecomposed']) for t in ids])
        form = np.array([int(ann[t]['stated_formula']) for t in ids])
        gt = np.array([int(corpus[t]['gt_code']) for t in ids])
        fresh = np.array([corpus[t]['pilot300'] == 'no' for t in ids])
        for scope, m in [('448', fresh), ('748', np.ones(len(ids), bool))]:
            h, f = f1(hol[m], gt[m]), f1(form[m], gt[m])
            print(f"{name:12} {scope:6} {h:12.3f} {f:8.3f} {h - f:+7.3f}")


if __name__ == '__main__':
    main()
