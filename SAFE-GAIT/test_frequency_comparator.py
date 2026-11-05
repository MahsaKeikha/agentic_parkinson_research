import unittest
import numpy as np
from frequency_comparator import spectral_features

class SpectralTests(unittest.TestCase):
    def test_shape_and_finiteness(self):
        samples=np.zeros((120,3))
        f=spectral_features(samples)
        self.assertEqual(f.shape,(7,))
        self.assertTrue(np.isfinite(f).all())
    def test_rotation_invariance(self):
        t=np.arange(120)/60
        x=np.column_stack([np.sin(2*np.pi*4*t),np.cos(2*np.pi*2*t),t])
        y=x[:,[1,2,0]]*np.array([-1.,1.,-1.])
        np.testing.assert_allclose(spectral_features(x),spectral_features(y),atol=1e-11)
    def test_spectral_band_discrimination(self):
        t=np.arange(120)/60
        low=np.column_stack([np.sin(2*np.pi*1*t),np.zeros(120),np.zeros(120)])
        high=np.column_stack([np.sin(2*np.pi*5*t),np.zeros(120),np.zeros(120)])
        self.assertFalse(np.allclose(spectral_features(low),spectral_features(high)))
    def test_nonfinite_rejected(self):
        x=np.zeros((120,3))
        x[2,0]=np.nan
        with self.assertRaises(ValueError):
            spectral_features(x)

if __name__=="__main__":
    unittest.main()
