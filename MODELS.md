# Models manifest

Every model used in the study, its role, and its exact configuration. Roles follow the
sealed-box rule (pre-registered): models under evaluation appear nowhere in corpus
construction.

## Annotators under evaluation

| Model | Exact ID | Role | Parameters |
|---|---|---|---|
| AMALIA-9B (DPO, June 2026) | `amalia-llm/AMALIA-9B-0626-DPO` | Subject annotator, both instruction conditions | temp 0, top_p 1.0, max_tokens 512, `response_format=json_object`; robustness pass with `response_format=none` |
| Llama 3.3 70B | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | Baseline (EN instructions), via Together AI | temp 0, top_p 1.0, max_tokens 512, `json_object` |
| GPT-OSS 120B | `openai/gpt-oss-120b` | Baseline (EN instructions), via Together AI | temp 0, top_p 1.0, max_tokens 4000, `json_object` |

**AMALIA variant, precisely:** the study used the June-2026 vintage with **both**
post-training phases — SFT followed by DPO preference alignment — i.e. the DPO chat
checkpoint, not the SFT-only checkpoint. Hub revision pinned:
`b23cd37c370289cf0cbfff35039da65a28b0e816` (head of `main` at pull time for both the
pilot and full runs; pods created 2026-07-03 17:52 and 22:02 UTC, after that commit).
The weight files of this revision are byte-identical (LFS oids) to the 2026-07-01
launch upload (`1194af49`) — the intervening commits changed documentation only — so
results are comparable to launch-day benchmark reports. The `-1225-*` vintage and the
`-0626-SFT` checkpoint were **not** evaluated.

**AMALIA serving:** self-hosted, vLLM **0.24.0** (`vllm/vllm-openai:latest` image, pulled
2026-07-03/04), dtype bfloat16, max_model_len 8192, 1× NVIDIA L40S (RunPod Secure Cloud).
Total GPU: 2.35 h across pilot + full runs.

**GPT-OSS envelope handling:** GPT-OSS wraps answers in a `{"final": "<stringified
JSON>"}` envelope. Responses were normalized before ingest
(unwrapping the envelope, parsing the inner JSON); 142/8,228 calls (1.7%) were unrecoverable
(reasoning loops) and imputed as *no* — per-call manifest in
`data/annotations/gptoss_en_missing_calls.csv`. AMALIA and Llama required no
normalization; AMALIA additionally held the JSON contract on 99.7% of calls (746/748, both
conditions) with **no** grammar constraint.

## Corpus-construction models (never evaluated)

| Model | Exact ID | Role | Parameters |
|---|---|---|---|
| DeepSeek V4 Pro | `deepseek-ai/DeepSeek-V4-Pro` | Transcreation generator; back-translator for audits | generation temp 0.7; back-translation temp 0 |
| Qwen3 235B | `Qwen/Qwen3-235B-A22B-Instruct-2507-tput` | Transcreation verification gate | temp 0; five-criterion verdict (meaning, stance, variety, naturalness, entities) |

All via Together AI, 2026-07-03/04. Human authority: all gate-exhausted items and audit
flags were adjudicated by the author (a European-Portuguese native speaker); every human
intervention was logged with named attribution (9 pilot + 6 full-run adjudications,
2 audit fixes).

## Analysis panel (S1/S2 shortcut reading)

The confirmatory shortcut-share and groundedness statistics rest on a reading panel of
LLM auditors: **Claude Fable 5** (Anthropic, `claude-fable-5`, July 2026), orchestrated
as two independent readers per text with opposed lenses (charitable vs skeptical) and a
third judge for disagreements; readers classify each error's basis
(authority_construct / equality_lookalike / other_moral_outrage / entity_presence_only /
no_signal) and the groundedness of the quoted evidence (yes / partial / no).
Inter-reader agreement before adjudication: 78% (pilot), 63% (confirmatory round,
computed over basis × construct_present pairs). The panel never saw ground-truth labels'
provenance beyond the FP/FN/control framing stated in the protocol.

## Rendering and localization

Prompts were rendered from the frozen constructs in `constructs/`; in the Portuguese
condition the full instruction scaffold is Portuguese (deterministic localisation,
verified so that no English scaffold survives; answer tokens stay `yes`/`no` in both
conditions to hold the parse contract constant). Re-annotation of any model requires only
an OpenAI-compatible endpoint (see README, Re-annotation).
