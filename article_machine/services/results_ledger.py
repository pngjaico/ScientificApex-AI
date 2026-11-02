"""Cross-Artifact Numerical Ledger Auditor and Clinical ML Methodology Evaluator.

1. Audits numerical consistency between canonical analysis outputs (analysis/results_ledger.json)
   and paired PT-BR / English manuscripts (handling decimal point vs comma equivalence).
2. Evaluates TRIPOD+AI / PROBAST+AI clinical prediction requirements:
   - Patient-level partition leakage audit (zero patient overlap between train and test)
   - Discrimination (exact Mann-Whitney AUROC)
   - Calibration (Brier score, calibration-in-the-large, logit calibration slope, calibration error)
   - Decision Curve Analysis (DCA Net Benefit vs Treat-All and Treat-None)
   - Split-Conformal Prediction set coverage (1 - alpha finite-sample guarantee)
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


def _pt_en_numeric_variants(val_str: str) -> set[str]:
    """Return acceptable string representations in PT-BR (comma/dot) and EN (dot)."""
    clean = str(val_str).strip()
    variants = {clean}
    if "." in clean:
        variants.add(clean.replace(".", ","))
    if "," in clean:
        variants.add(clean.replace(",", "."))
    return variants


def audit_numerical_consistency(
    project_dir: Path,
    ledger_rel_path: str = "analysis/results_ledger.json",
) -> dict[str, Any]:
    """Verify that canonical numbers in analysis/results_ledger.json match PT-BR and EN manuscripts."""
    root = Path(project_dir).resolve()
    ledger_path = root / ledger_rel_path
    if not ledger_path.is_file():
        return {
            "contract": "NumericalConsistencyAuditV1",
            "status": "blocked",
            "issues": [f"Canonical results ledger not found at '{ledger_rel_path}'."],
        }

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    metrics: dict[str, Any] = ledger.get("metrics", ledger) if isinstance(ledger, dict) else {}
    if not isinstance(metrics, dict) or not metrics:
        return {
            "contract": "NumericalConsistencyAuditV1",
            "status": "blocked",
            "issues": ["results_ledger.json must contain a non-empty 'metrics' object."],
        }

    default_stubs = {
        "",
        "# manuscript",
        "# manuscrito",
        "# manuscript\n\nuse {{claim:claim-id}} markers for every factual assertion.",
    }
    draft_files: dict[str, Path] = {}
    for label, rel in [
        ("portugues", "drafts/portugues/manuscrito.md"),
        ("ingles", "drafts/ingles/manuscrito.md"),
        ("canonical", "drafts/manuscript.md"),
    ]:
        candidate = root / rel
        if candidate.is_file():
            raw = candidate.read_text(encoding="utf-8", errors="replace").strip()
            if label == "canonical" and raw.lower() in default_stubs:
                continue
            draft_files[label] = candidate

    if not draft_files:
        return {
            "contract": "NumericalConsistencyAuditV1",
            "status": "blocked",
            "issues": ["No manuscript draft files found to verify against results_ledger.json."],
        }

    issues: list[str] = []
    verified_metrics: dict[str, list[str]] = {}

    for draft_label, draft_path in draft_files.items():
        text = draft_path.read_text(encoding="utf-8", errors="replace")
        verified_metrics[draft_label] = []
        for key, raw_value in metrics.items():
            if isinstance(raw_value, (int, float, str)):
                variants = _pt_en_numeric_variants(str(raw_value))
                if any(v in text for v in variants):
                    verified_metrics[draft_label].append(key)
                else:
                    issues.append(
                        f"Draft '{draft_label}' ({draft_path.relative_to(root).as_posix()}) is missing "
                        f"canonical value for '{key}' (expected {sorted(variants)})."
                    )

    return {
        "contract": "NumericalConsistencyAuditV1",
        "status": "pass" if not issues else "blocked",
        "ledger_path": ledger_rel_path,
        "checked_drafts": {k: v.relative_to(root).as_posix() for k, v in draft_files.items()},
        "verified_metrics": verified_metrics,
        "issues": issues,
    }


def _clip_prob(p: float, eps: float = 1e-6) -> float:
    return max(eps, min(1.0 - eps, float(p)))


def _logit(p: float) -> float:
    cp = _clip_prob(p)
    return math.log(cp / (1.0 - cp))


def _sigmoid(x: float) -> float:
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def _compute_auroc(y_true: list[int], y_prob: list[float]) -> float:
    pos = [p for y, p in zip(y_true, y_prob, strict=True) if y == 1]
    neg = [p for y, p in zip(y_true, y_prob, strict=True) if y == 0]
    if not pos or not neg:
        return 0.5
    concordant = 0.0
    for p_pos in pos:
        for p_neg in neg:
            if p_pos > p_neg:
                concordant += 1.0
            elif p_pos == p_neg:
                concordant += 0.5
    return concordant / (len(pos) * len(neg))


def _fit_logistic_calibration(y_true: list[int], y_prob: list[float]) -> tuple[float, float]:
    """Fit logistic calibration model logit(P(Y=1)) = alpha + beta * logit(p) via Newton-Raphson."""
    n = len(y_true)
    if n < 4 or len(set(y_true)) < 2:
        return 0.0, 1.0

    logits = [_logit(p) for p in y_prob]
    # 1. Calibration-in-the-large (alpha with slope fixed to 1): solve sum(sigmoid(a + l_i) - y_i) = 0
    alpha_citl = 0.0
    for _ in range(25):
        preds = [_sigmoid(alpha_citl + lx) for lx in logits]
        grad = sum(y - pr for y, pr in zip(y_true, preds, strict=True))
        hess = sum(pr * (1.0 - pr) for pr in preds)
        if hess < 1e-9:
            break
        step = grad / hess
        alpha_citl += step
        if abs(step) < 1e-7:
            break

    # 2. Calibration slope (beta) in 2-parameter fit logit(Y=1) = a + b * logit(p)
    a, b = 0.0, 1.0
    for _ in range(35):
        preds = [_sigmoid(a + b * lx) for lx in logits]
        weights = [pr * (1.0 - pr) for pr in preds]
        g0 = sum(y - pr for y, pr in zip(y_true, preds, strict=True))
        g1 = sum((y - pr) * lx for y, pr, lx in zip(y_true, preds, logits, strict=True))
        h00 = sum(weights) + 1e-6
        h01 = sum(w * lx for w, lx in zip(weights, logits, strict=True))
        h11 = sum(w * lx * lx for w, lx in zip(weights, logits, strict=True)) + 1e-6
        det = h00 * h11 - h01 * h01
        if abs(det) < 1e-12:
            break
        da = (h11 * g0 - h01 * g1) / det
        db = (-h01 * g0 + h00 * g1) / det
        a += da
        b += db
        if max(abs(da), abs(db)) < 1e-6:
            break

    return alpha_citl, b


def evaluate_clinical_prediction_metrics(
    y_true: list[int],
    y_prob: list[float],
    *,
    patient_ids_train: list[str] | None = None,
    patient_ids_test: list[str] | None = None,
    thresholds: list[float] | None = None,
    conformal_alpha: float = 0.10,
) -> dict[str, Any]:
    """Audit leakage and compute TRIPOD+AI discrimination, calibration, DCA Net Benefit, and conformal sets."""
    issues: list[str] = []

    if len(y_true) != len(y_prob) or len(y_true) == 0:
        return {
            "contract": "ClinicalPredictionEvaluationV1",
            "status": "blocked",
            "issues": ["y_true and y_prob must be non-empty lists of equal length."],
        }

    if any(y not in (0, 1) for y in y_true):
        issues.append("Binary outcome y_true must contain only 0 and 1.")
    if any(p < 0.0 or p > 1.0 for p in y_prob):
        issues.append("Predicted probabilities y_prob must lie in [0.0, 1.0].")

    # 1. Patient-level leakage check (PROBAST+AI Domain 4)
    overlap_patients: list[str] = []
    if patient_ids_train is not None and patient_ids_test is not None:
        overlap_patients = sorted(set(map(str, patient_ids_train)) & set(map(str, patient_ids_test)))
        if overlap_patients:
            issues.append(
                f"CRITICAL PATIENT LEAKAGE: {len(overlap_patients)} patient(s) appear in both train "
                f"and test partitions: {overlap_patients[:5]}"
            )

    if issues:
        return {
            "contract": "ClinicalPredictionEvaluationV1",
            "status": "blocked",
            "patient_overlap_count": len(overlap_patients),
            "issues": issues,
        }

    n = len(y_true)
    events = sum(y_true)
    prevalence = events / n
    auroc = _compute_auroc(y_true, y_prob)
    brier = sum((p - y) ** 2 for y, p in zip(y_true, y_prob, strict=True)) / n
    cal_intercept, cal_slope = _fit_logistic_calibration(y_true, y_prob)

    # Expected Calibration Error (ECE across 5 quantile bins)
    paired = sorted(zip(y_prob, y_true, strict=True), key=lambda item: item[0])
    bin_size = max(1, n // 5)
    ece = 0.0
    for start in range(0, n, bin_size):
        chunk = paired[start : start + bin_size]
        mean_p = sum(item[0] for item in chunk) / len(chunk)
        mean_y = sum(item[1] for item in chunk) / len(chunk)
        ece += (len(chunk) / n) * abs(mean_p - mean_y)

    # Decision Curve Analysis (DCA) Net Benefit
    eval_thresholds = thresholds or [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    dca_curve: list[dict[str, float | bool]] = []
    useful_thresholds: list[float] = []
    for pt in eval_thresholds:
        if pt <= 0.0 or pt >= 1.0:
            continue
        odds = pt / (1.0 - pt)
        tp = sum(1 for y, p in zip(y_true, y_prob, strict=True) if p >= pt and y == 1)
        fp = sum(1 for y, p in zip(y_true, y_prob, strict=True) if p >= pt and y == 0)
        nb_model = (tp / n) - (fp / n) * odds
        nb_all = prevalence - (1.0 - prevalence) * odds
        nb_none = 0.0
        beats_both = nb_model > max(nb_all, nb_none)
        if beats_both:
            useful_thresholds.append(round(pt, 4))
        dca_curve.append(
            {
                "threshold": round(pt, 4),
                "net_benefit_model": round(nb_model, 6),
                "net_benefit_treat_all": round(nb_all, 6),
                "net_benefit_treat_none": 0.0,
                "outperforms_default_strategies": beats_both,
            }
        )

    # Split-Conformal Prediction non-conformity scores s_i = 1 - P(Y = y_i)
    scores = sorted(1.0 - (p if y == 1 else (1.0 - p)) for y, p in zip(y_true, y_prob, strict=True))
    q_idx = min(n - 1, max(0, math.ceil((n + 1) * (1.0 - conformal_alpha)) - 1))
    q_hat = scores[q_idx]
    covered = 0
    ambiguous_sets = 0
    for y, p in zip(y_true, y_prob, strict=True):
        pred_set = []
        if (1.0 - p) <= q_hat:
            pred_set.append(1)
        if p <= q_hat:
            pred_set.append(0)
        if y in pred_set:
            covered += 1
        if len(pred_set) > 1:
            ambiguous_sets += 1

    return {
        "contract": "ClinicalPredictionEvaluationV1",
        "status": "pass",
        "n": n,
        "events": events,
        "prevalence": round(prevalence, 6),
        "patient_leakage_detected": False,
        "discrimination": {
            "auroc": round(auroc, 6),
        },
        "calibration": {
            "brier_score": round(brier, 6),
            "calibration_intercept": round(cal_intercept, 6),
            "calibration_slope": round(cal_slope, 6),
            "ece": round(ece, 6),
        },
        "decision_curve_analysis": {
            "thresholds_evaluated": dca_curve,
            "clinically_useful_thresholds": useful_thresholds,
        },
        "conformal_prediction": {
            "alpha": conformal_alpha,
            "target_coverage": round(1.0 - conformal_alpha, 4),
            "empirical_coverage": round(covered / n, 6),
            "quantile_threshold": round(q_hat, 6),
            "ambiguous_set_fraction": round(ambiguous_sets / n, 6),
        },
        "issues": [],
    }
