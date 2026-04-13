import unittest
import numpy as np
from pathlib import Path
import tempfile
import soundfile as sf

from src.audio import NoiseDetector, NoiseReducer

class TestNoiseDetector(unittest.TestCase):
    def setUp(self):
        self.detector = NoiseDetector()
        self.sr = 22050
        self.duration = 2
        self.samples = int(self.sr * self.duration)
        
        self.test_audio = 0.3 * np.sin(2 * np.pi * 440 * np.linspace(0, self.duration, self.samples))
        self.test_audio += 0.1 * np.random.randn(self.samples)
    
    def test_detect_noise_profile(self):
        profile = self.detector.detect_noise_profile(self.test_audio, duration=1.0)
        self.assertIsNotNone(profile)
        self.assertEqual(len(profile), self.detector.n_fft // 2 + 1)
    
    def test_detect_noise_regions(self):
        regions = self.detector.detect_noise_regions(self.test_audio)
        self.assertIsInstance(regions, list)

class TestNoiseReducer(unittest.TestCase):
    def setUp(self):
        self.reducer = NoiseReducer()
        self.sr = 22050
        self.duration = 2
        self.samples = int(self.sr * self.duration)
        
        self.test_audio = 0.3 * np.sin(2 * np.pi * 440 * np.linspace(0, self.duration, self.samples))
        self.test_audio += 0.1 * np.random.randn(self.samples)
        
        self.noise_profile = np.ones(self.reducer.n_fft // 2 + 1) * 0.1
    
    def test_spectral_subtraction(self):
        reduced = self.reducer.spectral_subtraction(self.test_audio, self.noise_profile, strength=0.5)
        self.assertAlmostEqual(len(reduced), len(self.test_audio), delta=100)
        self.assertTrue(np.all(np.isfinite(reduced)))
    
    def test_reduce_with_fade(self):
        reduced = self.reducer.reduce_with_fade(self.test_audio, self.noise_profile, strength=0.5)
        self.assertAlmostEqual(len(reduced), len(self.test_audio), delta=100)
        self.assertTrue(np.all(np.isfinite(reduced)))

if __name__ == "__main__":
    unittest.main()
