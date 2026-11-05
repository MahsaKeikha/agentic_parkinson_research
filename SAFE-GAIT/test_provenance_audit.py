import hashlib
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from provenance_audit import audit

class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        p=Path(self.tmp.name)
        self.sensor=p/'sensor.csv';self.clinical=p/'clinical.csv'
        pd.DataFrame({'subjectID':[1,1,1,2], 'sessionID':[1]*4,
                      'taskID':[1]*4,'timestamp':[0,1,2,3],'fog':[0,1,1,0]}).to_csv(self.sensor,index=False)
        pd.DataFrame({'subjectID':[1,2]}).to_csv(self.clinical,index=False)
        self.manifest={'sensor':{'md5':hashlib.md5(self.sensor.read_bytes()).hexdigest(),'rows':4,'columns':5},
                       'clinical':{'md5':hashlib.md5(self.clinical.read_bytes()).hexdigest(),'rows':2,'columns':1},
                       'subject_count':2}
    def test_verified_manifest_passes(self):
        self.assertEqual(audit(self.sensor,self.clinical,self.manifest)['status'],'PASS')
    def test_bad_checksum_fails(self):
        self.manifest['sensor']['md5']='0'*32
        self.assertEqual(audit(self.sensor,self.clinical,self.manifest)['status'],'FAIL')
    def test_missing_manifest_fails_closed(self):
        del self.manifest['clinical']['rows']
        self.assertEqual(audit(self.sensor,self.clinical,self.manifest)['status'],'UNVERIFIED')
    def test_publication_events_not_forced_equal(self):
        r=audit(self.sensor,self.clinical,self.manifest)
        self.assertIn('naive_positive_runs',r['groups'][0])
        self.assertNotIn('expert_episodes',r)
if __name__=='__main__':unittest.main()
