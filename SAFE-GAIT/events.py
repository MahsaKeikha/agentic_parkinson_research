"""Event-level FoG detection metrics with explicit one-to-one matching.

This module expects one participant/session and a uniformly time-indexed
sequence of *nonoverlapping* binary labels. It does not train models or claim
clinical validity. Callers must freeze sampling rate and episode conventions.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Episode:
    start: float
    end: float

    @property
    def duration(self):
        return self.end - self.start


def episodes(times, labels, sample_period, max_gap_factor=1.5, min_duration=0.0):
    """Return positive episodes, respecting discontinuities in observed time.

    Times mark sample starts; episode end is exclusive. NaN labels break runs.
    """
    times = np.asarray(times, dtype=float)
    labels = np.asarray(labels, dtype=float)
    if len(times) != len(labels) or sample_period <= 0:
        raise ValueError("times/labels length mismatch or invalid sample period")
    if len(times) and (not np.isfinite(times).all() or np.any(np.diff(times) <= 0)):
        raise ValueError("timestamps must be finite and strictly increasing")
    found = []
    active = None
    last = None
    for t, label in zip(times, labels):
        positive = label == 1
        gap = last is not None and t - last > max_gap_factor * sample_period
        if active is not None and (not positive or gap):
            end = last + sample_period
            if end - active >= min_duration:
                found.append(Episode(float(active), float(end)))
            active = None
        if positive and active is None:
            active = t
        last = t
    if active is not None:
        end = last + sample_period
        if end - active >= min_duration:
            found.append(Episode(float(active), float(end)))
    return found


def match_events(reference, alerts, tolerance_seconds=0.0):
    """Maximum-cardinality one-to-one event matching.

    An alert is eligible if it overlaps an expanded reference interval. Ties
    are considered in onset order. One alert cannot satisfy multiple events.
    This is a specified operational rule, not a universally accepted FoG metric.
    """
    if tolerance_seconds < 0:
        raise ValueError("tolerance_seconds must be nonnegative")
    ordered = sorted(reference, key=lambda e: (e.start, e.end))
    # Augmenting-path bipartite matching maximizes detected events rather than
    # allowing an early greedy choice to block a later reference episode.
    # Sorting makes tie resolution deterministic; not a latency optimum.
    eligible = [sorted(
        (i for i, alert in enumerate(alerts)
         if alert.end > ref.start - tolerance_seconds
         and alert.start < ref.end + tolerance_seconds),
        key=lambda i: (alerts[i].start, alerts[i].end, i))
        for ref in ordered]
    owner = {}
    def augment(ref_idx, visited):
        for alert_idx in eligible[ref_idx]:
            if alert_idx in visited:
                continue
            visited.add(alert_idx)
            if alert_idx not in owner or augment(owner[alert_idx], visited):
                owner[alert_idx] = ref_idx
                return True
        return False
    for idx in range(len(ordered)):
        augment(idx, set())
    matched = sorted(((ordered[ref_idx], alerts[alert_idx])
                      for alert_idx, ref_idx in owner.items()),
                     key=lambda pair: (pair[0].start, pair[1].start))
    latencies = [max(0.0, alert.start - ref.start) for ref, alert in matched]
    tp = len(matched)
    return {"event_tp": tp, "event_fn": len(reference) - tp,
            "event_fp": len(alerts) - tp,
            "event_sensitivity": tp / len(reference) if reference else None,
            "event_precision": tp / len(alerts) if alerts else None,
            "latency_seconds": latencies}


def merge_close_alerts(alerts, gap_seconds):
    """Coalesce alerts separated by at most a specified refractory gap.

    Must operate within one uninterrupted recording block, never across
    subjects or task/session breaks. A merged alert starts at the first onset.
    """
    if gap_seconds < 0:
        raise ValueError("gap_seconds must be nonnegative")
    ordered = sorted(alerts, key=lambda event: (event.start, event.end))
    merged = []
    for alert in ordered:
        if not merged or alert.start - merged[-1].end > gap_seconds:
            merged.append(alert)
        else:
            last = merged[-1]
            merged[-1] = Episode(last.start, max(last.end, alert.end))
    return merged


def event_summary(reference, alerts, recorded_seconds, tolerance_seconds=0.0):
    if recorded_seconds <= 0:
        raise ValueError("recorded_seconds must be positive")
    metrics = match_events(reference, alerts, tolerance_seconds)
    metrics["false_alerts_per_hour"] = 3600 * metrics["event_fp"] / recorded_seconds
    metrics["mean_detected_latency_seconds"] = (
        float(np.mean(metrics["latency_seconds"])) if metrics["latency_seconds"] else None)
    return metrics
