import unittest

from constrained import choose_feasible


class TestConstrainedSelection(unittest.TestCase):
    def test_infeasible_is_explicit(self):
        candidates = [{"threshold": 0.1, "sensitivity": 0.9, "false_alerts_per_hour": 80},
                      {"threshold": 0.8, "sensitivity": 0.2, "false_alerts_per_hour": 4}]
        self.assertIsNone(choose_feasible(candidates, 0.7, 30))

    def test_prefers_low_alert_burden(self):
        candidates = [{"threshold": 0.4, "sensitivity": 0.8, "false_alerts_per_hour": 20},
                      {"threshold": 0.5, "sensitivity": 0.7, "false_alerts_per_hour": 12}]
        self.assertEqual(choose_feasible(candidates, 0.7, 30)["threshold"], 0.5)

    def test_no_events_never_passes_constraint(self):
        candidates = [{"threshold": 0.5, "sensitivity": None, "false_alerts_per_hour": 0}]
        self.assertIsNone(choose_feasible(candidates, 0.7, 30))


if __name__ == "__main__":
    unittest.main()
