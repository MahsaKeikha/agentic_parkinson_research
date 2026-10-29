import unittest

import numpy as np

from events import Episode, episodes, event_summary, match_events


class TestEventMetrics(unittest.TestCase):
    def test_episode_conversion_with_gap(self):
        t = np.array([0, 1, 2, 10, 11], dtype=float)
        y = np.array([0, 1, 1, 1, 0], dtype=float)
        observed = episodes(t, y, sample_period=1)
        self.assertEqual(observed, [Episode(1, 3), Episode(10, 11)])

    def test_nan_breaks_positive_episode(self):
        t = np.array([0, 1, 2, 3], dtype=float)
        y = np.array([1, np.nan, 1, 0])
        self.assertEqual(episodes(t, y, 1), [Episode(0, 1), Episode(2, 3)])

    def test_single_alert_cannot_match_twice(self):
        ref = [Episode(1, 2), Episode(3, 4)]
        alerts = [Episode(1.5, 3.5)]
        out = match_events(ref, alerts)
        self.assertEqual((out["event_tp"], out["event_fn"], out["event_fp"]), (1, 1, 0))

    def test_false_alert_rate_and_latency(self):
        ref = [Episode(10, 15)]
        alerts = [Episode(12, 13), Episode(30, 31)]
        out = event_summary(ref, alerts, recorded_seconds=3600)
        self.assertEqual(out["false_alerts_per_hour"], 1.0)
        self.assertEqual(out["mean_detected_latency_seconds"], 2.0)

    def test_empty_reference_does_not_invent_sensitivity(self):
        out = match_events([], [Episode(2, 3)])
        self.assertIsNone(out["event_sensitivity"])
        self.assertEqual(out["event_fp"], 1)


if __name__ == "__main__":
    unittest.main()
