import numpy as np
import librosa
import soundfile as sf
from src.utils import app_logger

class NoiseReducer:
    def __init__(self, sr=22050, n_fft=2048, hop_length=512):
        self.sr = sr
        self.n_fft = n_fft
        self.hop_length = hop_length
    
    def spectral_subtraction(self, audio, noise_profile, strength=0.5):
        """
        Apply spectral subtraction to reduce noise.
        strength: 0.0 (no reduction) to 1.0 (aggressive reduction)
        """
        try:
            S = librosa.stft(audio, n_fft=self.n_fft, hop_length=self.hop_length)
            magnitude = np.abs(S)
            phase = np.angle(S)
            
            noise_profile = noise_profile.reshape(-1, 1)
            
            reduced_magnitude = magnitude - (strength * noise_profile)
            reduced_magnitude = np.maximum(reduced_magnitude, 0.1 * magnitude)
            
            S_reduced = reduced_magnitude * np.exp(1j * phase)
            
            audio_reduced = librosa.istft(S_reduced, hop_length=self.hop_length)
            
            audio_reduced = np.clip(audio_reduced, -1.0, 1.0)
            
            app_logger.info(f"Spectral subtraction applied with strength {strength}")
            return audio_reduced
        except Exception as e:
            app_logger.error(f"Error in spectral subtraction: {e}")
            return audio
    
    def apply_noise_reduction(self, audio_path, output_path, strength=0.5, 
                             noise_duration=1.0):
        """
        Load audio, detect noise profile, and apply reduction.
        """
        try:
            y, sr = librosa.load(audio_path, sr=self.sr)
            
            samples = int(noise_duration * sr)
            noise_audio = y[:samples]
            
            S_noise = librosa.stft(noise_audio, n_fft=self.n_fft, 
                                   hop_length=self.hop_length)
            noise_profile = np.mean(np.abs(S_noise), axis=1)
            
            y_reduced = self.spectral_subtraction(y, noise_profile, strength)
            
            sf.write(output_path, y_reduced, sr)
            
            app_logger.info(f"Noise-reduced audio saved to {output_path}")
            return output_path
        except Exception as e:
            app_logger.error(f"Error applying noise reduction: {e}")
            return None
    
    def reduce_with_fade(self, audio, noise_profile, strength=0.5, 
                        fade_duration=0.5):
        """
        Apply noise reduction with fade-in/out to avoid artifacts.
        """
        try:
            fade_samples = int(fade_duration * self.sr)
            
            y_reduced = self.spectral_subtraction(audio, noise_profile, strength)
            
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            
            result = y_reduced.copy()
            
            if len(result) > fade_samples:
                result[:fade_samples] = (
                    audio[:fade_samples] * (1 - fade_in) + 
                    y_reduced[:fade_samples] * fade_in
                )
                result[-fade_samples:] = (
                    y_reduced[-fade_samples:] * fade_out + 
                    audio[-fade_samples:] * (1 - fade_out)
                )
            
            app_logger.info(f"Noise reduction with fade applied")
            return result
        except Exception as e:
            app_logger.error(f"Error in reduce_with_fade: {e}")
            return audio
