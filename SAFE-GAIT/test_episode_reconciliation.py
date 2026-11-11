import unittest
import pandas as pd
from episode_reconciliation import reconcile

def frame(t,y,ids=None):
    n=len(t)
    return pd.DataFrame({"subjectID":ids if ids is not None else [1]*n,
                         "sessionID":[1]*n,"taskID":[1]*n,"timestamp":t,"fog":y})
class TestEpisodeReconciliation(unittest.TestCase):
    def test_separated_positive_runs(self):
        self.assertEqual(reconcile(frame([0,1/60,2/60,3/60],[1,1,0,1]),timestamp_unit="s")["binary_positive_runs"],2)
    def test_gap_splits_run(self):
        r=reconcile(frame([0,1/60,2,2+1/60],[1]*4),timestamp_unit="s")
        self.assertEqual((r["binary_positive_runs"],r["n_gaps"]),(2,1))
    def test_participant_change(self):
        r=reconcile(frame([0,1/60,0,1/60],[1]*4,[1,1,2,2]),timestamp_unit="s")
        self.assertEqual((r["binary_positive_runs"],r["participants"]),(2,2))
    def test_explicit_millisecond_unit(self):
        self.assertEqual(reconcile(frame([0,1000/60,2000/60],[1]*3),timestamp_unit="ms")["binary_positive_runs"],1)
    def test_reject_invalid_units(self):
        with self.assertRaises(ValueError):
            reconcile(frame([0],[1]),timestamp_unit="seconds")
    def test_nonincreasing_timestamp(self):
        r=reconcile(frame([0,1/60,0,1/60],[1]*4),timestamp_unit="s")
        self.assertEqual((r["binary_positive_runs"],r["n_nonincreasing_timestamp_steps"]),(2,1))
    def test_empty_dataframe(self):
        self.assertEqual(reconcile(frame([],[]),timestamp_unit="s")["number_of_contiguous_blocks"],0)
    def test_nan_timestamp_rejected(self):
        with self.assertRaises(ValueError):
            reconcile(frame([0,float("nan")],[0,1]),timestamp_unit="s")
    def test_unknown_label_breaks_positive_run(self):
        r=reconcile(frame([0,1/60,2/60],[1,2,1]),timestamp_unit="s")
        self.assertEqual(r["binary_positive_runs"],2)
        self.assertEqual(r["blocks"][0]["valid_labeled_rows"],2)
    def test_participant_change_with_timestamp_reset(self):
        r=reconcile(frame([0,1/60,0,1/60],[1]*4,[1,1,2,2]),timestamp_unit="s")
        self.assertEqual(r["blocks"][1]["block_boundary_reason"],"recording_key_change")
    def test_task_change_splits_positive_run(self):
        f=frame([0,1/60,2/60],[1,1,1])
        f.loc[2,"taskID"]=2
        r=reconcile(f,timestamp_unit="s")
        self.assertEqual(r["binary_positive_runs"],2)
    def test_invalid_sampling_hz_rejected(self):
        with self.assertRaises(ValueError):
            reconcile(frame([0],[1]),timestamp_unit="s",sampling_hz=0)
if __name__=="__main__":
    unittest.main()
