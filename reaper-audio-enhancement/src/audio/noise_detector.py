import numpy as np
import librosa
from src.utils import app_logger

class NoiseDetector:
    def __init__(self, sr=22050, n_fft=2048, hop_length=512):
        self.sr = sr
        self.n_fft = n_fft
        self.hop_length = hop_length
    
    def detect_noise_profile(self, audio, duration=2.0):
        """
        Detect noise profile from audio (assumes first N seconds are noise).
        Returns noise magnitude spectrum.
        """
        try:
            samples = int(duration * self.sr)
            noise_audio = audio[:samples]
            
            S = librosa.stft(noise_audio, n_fft=self.n_fft, hop_length=self.hop_length)
            magnitude = np.abs(S)
            noise_profile = np.mean(magnitude, axis=1)
            
            app_logger.info(f"Noise profile detected from {duration}s of audio")
            return noise_profile
        except Exception as e:
            app_logger.error(f"Error detecting noise profile: {e}")
            return None
    
    def analyze_audio(self, audio_path):
        """
        Analyze audio file for noise characteristics.
        Returns dict with noise analysis results.
        """
        try:
            y, sr = librosa.load(audio_path, sr=self.sr)
            
            S = librosa.stft(y, n_fft=self.n_fft, hop_length=self.hop_length)
            magnitude = np.abs(S)
            
            rms = librosa.feature.rms(y=y, hop_length=self.hop_length)[0]
            
            spectral_centroid = librosa.feature.spectral_centroid(
                y=y, sr=sr, hop_length=self.hop_length
            )[0]
            
            noise_profile = self.detect_noise_profile(y, duration=1.0)
            
            problematic_frames = np.where(rms < np.mean(rms) * 0.3)[0]
            
            results = {
                "duration": librosa.get_duration(y=y, sr=sr),
                "rms_energy": rms,
                "spectral_centroid": spectral_centroid,
                "noise_profile": noise_profile,
                "problematic_frames": problematic_frames,
                "mean_rms": np.mean(rms),
                "std_rms": np.std(rms),
                "sample_rate": sr,
            }
            
            app_logger.info(f"Audio analysis complete: {results['duration']:.2f}s duration")
            return results
        except Exception as e:
            app_logger.error(f"Error analyzing audio: {e}")
            return None
    
    def detect_noise_regions(self, audio, threshold_percentile=25):
        """
        Detect regions with significant noise.
        Returns list of (start_frame, end_frame) tuples.
        """
        try:
            S = librosa.stft(audio, n_fft=self.n_fft, hop_length=self.hop_length)
            magnitude = np.abs(S)
            
            frame_energy = np.mean(magnitude, axis=0)
            threshold = np.percentile(frame_energy, threshold_percentile)
            
            noise_frames = np.where(frame_energy < threshold)[0]
            
            regions = []
            if len(noise_frames) > 0:
                start = noise_frames[0]
                for i in range(1, len(noise_frames)):
                    if noise_frames[i] - noise_frames[i-1] > 1:
                        regions.append((start, noise_frames[i-1]))
                        start = noise_frames[i]
                regions.append((start, noise_frames[-1]))
            
            app_logger.info(f"Detected {len(regions)} noise regions")
            return regions
        except Exception as e:
            app_logger.error(f"Error detecting noise regions: {e}")
            return []
