import unittest
from event_protocol_sensitivity import score_at_decisions,sensitivity_grid
class TestEventProtocolSensitivity(unittest.TestCase):
    def test_alert_after_event_end_not_retroactive(self):
        m=score_at_decisions([(1.,2.)],[2.1],[1],hold_seconds=1.)
        self.assertEqual(m["event_tp"],0)
        self.assertEqual(m["event_fn"],1)
    def test_tolerance_may_change_event_match(self):
        a=score_at_decisions([(1.,2.)],[2.1],[1],hold_seconds=0.,tolerance_seconds=0.)
        b=score_at_decisions([(1.,2.)],[2.1],[1],hold_seconds=0.,tolerance_seconds=.2)
        self.assertEqual(a["event_tp"],0)
        self.assertEqual(b["event_tp"],1)
    def test_grid_auditable(self):
        rows=sensitivity_grid([(1.,3.)],[2.],[1])
        self.assertEqual(len(rows),9)
        self.assertTrue(all(x["event_tp"]+x["event_fn"]==1 for x in rows))
    def test_no_backwards_decision_times(self):
        with self.assertRaises(ValueError):
            score_at_decisions([], [2.,1.],[1,1])
if __name__=="__main__":
    unittest.main()
