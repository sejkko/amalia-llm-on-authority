# Agreement is not measurement: auditing AMÁLIA-9B as a social-science annotator

Replication package for the paper *[title TBD]* (Pita, 2026). The study audits AMÁLIA-9B,
Portugal's national large language model, as an annotator of the moral foundation
Authority/Subversion on a purpose-built European-Portuguese corpus, against
pre-registered criteria.

**Pre-registration:** [10.5281/zenodo.21178967](https://doi.org/10.5281/zenodo.21178967)
(deposited before any model annotated the 448-text confirmatory set).

## Reproduce the paper's results

```bash
pip install -r requirements.txt
python3 analysis/confirmatory.py   # pre-registered primary endpoint + H1/H2/S3 verdicts
python3 analysis/gap_table.py      # recovery-gap table, all annotators
```

Both scripts read only the files under `data/` and complete in about a minute.

## Contents

| Path | Contents |
|---|---|
| `data/corpus.csv` | The 748 paired texts: `text_id`, `text_en` (English source, from the Moral Foundations Reddit Corpus, Trager et al. 2022), `text_pt` (European-Portuguese transcreation), `gt_code` (1 = Authority/Subversion present per MFRC annotators), `contested_status` (`unanimous` / `contested`), `pilot300` (`yes` = pilot text; confirmatory tests use `pilot300 == no` only) |
| `data/annotations/` | One file per annotator × instruction condition (`amalia_pt`, `amalia_en`, `llama_en`, `gptoss_en`): `undecomposed` (holistic judgement), seven clause columns, `stated_formula` (verdict recomposed under the construct's stated rule `(D_entity AND (A_order_stance OR A_assess_authority)) OR A_order_values`). The paper's **recovery gap** is F1(`undecomposed`) − F1(`stated_formula`) against `gt_code` |
| `data/evidence/` | Per text × clause: the annotator's `answer`, quoted `evidence` span, and one-sentence `justification` |
| `constructs/` | The frozen instrument: `construct_en.yaml` (calibrated English construct) and `construct_pt.yaml` (its faithful European-Portuguese rendering) |
| `MODELS.md` | Every model used, with exact identities, roles, and serving details |
| `analysis/` | The two analysis scripts above |

**Missing-data note (GPT-OSS only).** 142 of GPT-OSS's 8,228 calls returned unrecoverable
output and were imputed as *no*; `data/annotations/gptoss_en_missing_calls.csv` lists
every imputed call. Llama has no missing calls; AMÁLIA had a single unparsable clause
call (1/8,228, PT condition), defaulted the same way.

**Re-annotation.** Any OpenAI-compatible model can be evaluated the same way: render the
construct's holistic prompt and its clauses (`constructs/*.yaml`) over `text_pt` or
`text_en`, collect yes/no answers with evidence spans, recompose `stated_formula` by the
rule above, and score with `analysis/gap_table.py`.

**Error-reading endpoints (S1/S2).** The panel's target set is fully derivable here:
unanimous-negative texts in the test set (`gt_code == 0`, `contested_status == unanimous`,
`pilot300 == no`) that AMÁLIA's `undecomposed` coded 1 — 46 texts, each with the model's
complete clause answers, quoted spans, and justifications in `data/evidence/amalia_pt.csv`.
Replicators can re-read them with readers and a protocol of their own choosing and apply
the registered criteria (≥50% shortcut basis; ≥50% evidence at most partially grounded).

## Licenses

- **Code** (`analysis/`): MIT (see `LICENSE`).
- **Data** (`data/`, `constructs/`): CC-BY 4.0 (see `DATA_LICENSE.md`). English source
  texts and labels derive from the Moral Foundations Reddit Corpus (Trager et al. 2022),
  itself CC-BY 4.0 — cite MFRC when using `text_en` or `gt_code`.

## Citation

See `CITATION.cff`. Paper citation TBD. Pre-registration: Pita, M. (2026). Zenodo.
https://doi.org/10.5281/zenodo.21178967
