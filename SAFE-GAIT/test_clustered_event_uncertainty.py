import unittest
from clustered_event_uncertainty import metrics, summarize_subjects

def row(ref=1,tp=0,fp=1,seconds=3600):
    return {"reference_episodes":ref,"event_tp":tp,"event_fn":ref-tp,
            "event_fp":fp,"alerts":tp+fp,"exposure_seconds":seconds,
            "windows":10,"abstained_windows":2}

class ClusterTests(unittest.TestCase):
    def test_accounting_and_point_estimates(self):
        out=metrics([row(2,1,2,3600),row(1,1,0,3600)])
        self.assertAlmostEqual(out["event_recall"],2/3)
        self.assertAlmostEqual(out["false_alerts_per_hour"],1)
    def test_consistency_rejects_invalid_events(self):
        bad=row()
        bad["event_fn"]=99
        with self.assertRaises(ValueError):
            metrics([bad])
    def test_no_reference_events_is_undefined(self):
        out=metrics([row(0,0,0)])
        self.assertIsNone(out["event_recall"])
    def test_subject_resampling_is_reproducible(self):
        data={"a":row(2,1,1),"b":row(1,0,2),"c":row(3,2,0)}
        a=summarize_subjects(data,replicates=100,seed=17)
        b=summarize_subjects(data,replicates=100,seed=17)
        self.assertEqual(a,b)
        self.assertEqual(a["participants"],3)
        self.assertEqual(a["bootstrap_95_percentile"]["event_recall"]["evaluable_replicates"],100)
    def test_zero_event_replicates_marked_unevaluable(self):
        out=summarize_subjects({"a":row(0,0,0)},replicates=10)
        self.assertIsNone(out["bootstrap_95_percentile"]["event_recall"]["lower"])
        self.assertEqual(out["bootstrap_95_percentile"]["event_recall"]["evaluable_replicates"],0)

if __name__=="__main__":
    unittest.main()
