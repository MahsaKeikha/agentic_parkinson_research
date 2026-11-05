"""Fail-closed dataset manifest audit; publication claims are not file facts."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

REQUIRED = {'subjectID','sessionID','taskID','timestamp','fog'}

def md5(path):
    d=hashlib.md5()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):d.update(chunk)
    return d.hexdigest()

def audit(sensor_path, clinical_path, manifest):
    """Manifest: file MD5, rows and columns from the actual release.

    Missing manifest fields cause UNVERIFIED status, never PASS.
    Paper-reported episodes are contextual, never forced to equal label runs.
    """
    s=pd.read_csv(sensor_path); c=pd.read_csv(clinical_path)
    if not REQUIRED.issubset(s):raise ValueError('Missing sensor columns: '+str(sorted(REQUIRED-set(s))))
    if 'subjectID' not in c:raise ValueError('Clinical subjectID missing')
    subject_ids=set(s.subjectID.dropna().astype(int))
    clinical_ids=set(c.subjectID.dropna().astype(int))
    checks={}
    for key,path,frame in [('sensor',sensor_path,s),('clinical',clinical_path,c)]:
        record=manifest.get(key,{})
        checks[f'{key}_md5']=(md5(path)==record['md5'].lower()) if record.get('md5') else None
        checks[f'{key}_rows']=(len(frame)==int(record['rows'])) if record.get('rows') is not None else None
        checks[f'{key}_columns']=(len(frame.columns)==int(record['columns'])) if record.get('columns') is not None else None
    checks['sensor_ids_in_clinical']=subject_ids.issubset(clinical_ids)
    checks['subject_count']=(len(subject_ids)==int(manifest['subject_count'])) if manifest.get('subject_count') is not None else None
    groups=[]
    for key,group in s.groupby(['subjectID','sessionID','taskID'],sort=False,dropna=False):
        t=group.timestamp.to_numpy(float)
        dif=np.diff(t)
        labels=group.fog.to_numpy()
        pos=labels==1
        groups.append({'key':[str(x) for x in key], 'rows':len(group),
                       'naive_positive_runs':int((pos & ~np.r_[False,pos[:-1]]).sum()),
                       'nonpositive_time_steps':int((dif<=0).sum()),
                       'median_positive_time_step':float(np.median(dif[dif>0])) if (dif>0).any() else None})
    verdict='FAIL' if any(v is False for v in checks.values()) else ('UNVERIFIED' if any(v is None for v in checks.values()) else 'PASS')
    return {'status':verdict,'checks':checks,'sensor':{'md5':md5(sensor_path),'rows':len(s),'columns':list(s), 'participants':len(subject_ids)},
            'clinical':{'md5':md5(clinical_path),'rows':len(c),'participants':len(clinical_ids)},'groups':groups,
            'note':'Positive binary-label runs are not the publication expert-adjudicated episode count.'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--sensor-data',type=Path,required=True)
    p.add_argument('--clinical-data',type=Path,required=True)
    p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    result=audit(a.sensor_data,a.clinical_data,json.loads(a.manifest.read_text()))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2))
    print(result['status'])
    raise SystemExit(0 if result['status']=='PASS' else 2)
if __name__=='__main__':main()
