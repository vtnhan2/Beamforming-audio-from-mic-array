#!/usr/bin/env python3
"""
Audio Source Localization Script
Xử lý file original_8channels.pcm và xác định vị trí nguồn âm thanh trong không gian 3D
"""

import numpy as np
import struct
import json
import socket
import time
import threading
import os
import sys
from typing import List, Tuple, Optional
import argparse

class AudioProcessor:
    """Class xử lý audio và xác định vị trí nguồn âm thanh"""
    
    def __init__(self, config_file: str = "odas_8ch_config.cfg"):
        self.config_file = config_file
        self.sample_rate = 16000
        self.n_channels = 8
        self.bit_depth = 16
        self.active_channels = [0, 1, 2, 3, 4, 7]  # Channels 1-5 và 8 (0-indexed)
        self.silent_channels = [5, 6]  # Channels 6-7 (0-indexed)
        
        # Microphone array configuration (8 microphones in circular pattern)
        self.mic_positions = self._setup_microphone_array()
        
        # Sound source localization parameters
        self.speed_of_sound = 343.0  # m/s
        self.frame_size = 256
        self.hop_size = 128
        
    def _setup_microphone_array(self) -> np.ndarray:
        """Thiết lập vị trí microphone array (8 microphones dạng tròn)"""
        radius = 0.05  # 5cm radius
        positions = []
        
        for i in range(8):
            angle = 2 * np.pi * i / 8
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            z = 0.0
            positions.append([x, y, z])
            
        return np.array(positions)
    
    def read_pcm_file(self, filename: str) -> np.ndarray:
        """Đọc file PCM với cấu hình đã cho"""
        print(f"Doc file: {filename}")
        
        with open(filename, 'rb') as f:
            # Skip 2 bytes offset
            f.seek(2)
            
            # Đọc toàn bộ file
            raw_data = f.read()
            
        # Convert bytes to numpy array
        n_samples_total = len(raw_data) // 2  # 16-bit = 2 bytes per sample
        n_samples = n_samples_total // self.n_channels
        
        # Đảm bảo số samples chia hết cho số channels
        if n_samples_total % self.n_channels != 0:
            print(f"Warning: File size {len(raw_data)} bytes, expected multiple of {self.n_channels * 2}")
            n_samples = n_samples_total // self.n_channels
            # Cắt bỏ phần dư
            raw_data = raw_data[:n_samples * self.n_channels * 2]
        
        samples = struct.unpack(f'<{len(raw_data)//2}h', raw_data)
        audio_data = np.array(samples).reshape(n_samples, self.n_channels)
        
        print(f"Da doc {n_samples} samples, {self.n_channels} channels")
        print(f"Duration: {n_samples / self.sample_rate:.2f} seconds")
        
        return audio_data
    
    def analyze_audio_channels(self, audio_data: np.ndarray) -> dict:
        """Phân tích các channel để xác định channel nào có audio"""
        analysis = {}
        
        for ch in range(self.n_channels):
            channel_data = audio_data[:, ch]
            
            # Tính RMS energy
            rms = np.sqrt(np.mean(channel_data**2))
            
            # Tính zero crossing rate
            zcr = np.sum(np.diff(np.sign(channel_data)) != 0) / len(channel_data)
            
            # Phân loại channel
            has_audio = rms > 100 and zcr > 0.01  # Threshold values
            
            analysis[ch] = {
                'rms': rms,
                'zcr': zcr,
                'has_audio': has_audio,
                'max_amplitude': np.max(np.abs(channel_data))
            }
            
        return analysis
    
    def calculate_tdoa(self, audio_data: np.ndarray, ref_channel: int = 0) -> np.ndarray:
        """Tính Time Difference of Arrival (TDOA) giữa các microphone"""
        tdoas = []
        
        for ch in range(self.n_channels):
            if ch == ref_channel:
                tdoas.append(0.0)
                continue
                
            # Cross-correlation để tìm delay
            correlation = np.correlate(audio_data[:, ref_channel], audio_data[:, ch], mode='full')
            delay = np.argmax(correlation) - len(audio_data) + 1
            
            # Convert delay to time
            tdoa = delay / self.sample_rate
            tdoas.append(tdoa)
            
        return np.array(tdoas)
    
    def localize_sound_source(self, tdoas: np.ndarray) -> Tuple[float, float, float]:
        """Xác định vị trí nguồn âm thanh sử dụng TDOA"""
        # Simplified localization using least squares
        # Trong thực tế, cần thuật toán phức tạp hơn như MUSIC, SRP-PHAT
        
        n_mics = len(tdoas)
        A = np.zeros((n_mics-1, 3))
        b = np.zeros(n_mics-1)
        
        for i in range(1, n_mics):
            # Distance difference equation
            A[i-1, 0] = 2 * (self.mic_positions[i, 0] - self.mic_positions[0, 0])
            A[i-1, 1] = 2 * (self.mic_positions[i, 1] - self.mic_positions[0, 1])
            A[i-1, 2] = 2 * (self.mic_positions[i, 2] - self.mic_positions[0, 2])
            
            # Distance difference
            distance_diff = tdoas[i] * self.speed_of_sound
            b[i-1] = distance_diff
            
        # Solve least squares
        try:
            position = np.linalg.lstsq(A, b, rcond=None)[0]
            return position[0], position[1], position[2]
        except:
            return 0.0, 0.0, 0.0
    
    def process_audio_file(self, filename: str) -> dict:
        """Xử lý file audio và trả về kết quả localization"""
        print("Bat dau xu ly file audio...")
        
        # Đọc file PCM
        audio_data = self.read_pcm_file(filename)
        
        # Phan tich channels
        channel_analysis = self.analyze_audio_channels(audio_data)
        print("\nPhan tich channels:")
        for ch, analysis in channel_analysis.items():
            status = "CO AUDIO" if analysis['has_audio'] else "KHONG CO AUDIO"
            print(f"Channel {ch+1}: {status} - RMS: {analysis['rms']:.2f}, ZCR: {analysis['zcr']:.4f}")
        
        # Tinh TDOA
        print("\nTinh TDOA...")
        tdoas = self.calculate_tdoa(audio_data)
        print("TDOAs (seconds):", tdoas)
        
        # Localization
        print("\nXac dinh vi tri nguon am thanh...")
        x, y, z = self.localize_sound_source(tdoas)
        
        # Convert to spherical coordinates
        r = np.sqrt(x**2 + y**2 + z**2)
        azimuth = np.arctan2(y, x) * 180 / np.pi
        elevation = np.arcsin(z / r) * 180 / np.pi if r > 0 else 0
        
        result = {
            'position_cartesian': [float(x), float(y), float(z)],
            'position_spherical': {
                'distance': float(r),
                'azimuth': float(azimuth),
                'elevation': float(elevation)
            },
            'tdoas': tdoas.tolist(),
            'channel_analysis': channel_analysis,
            'processing_info': {
                'sample_rate': self.sample_rate,
                'n_channels': self.n_channels,
                'duration': len(audio_data) / self.sample_rate,
                'speed_of_sound': self.speed_of_sound
            }
        }
        
        return result
    
    def create_odas_config(self) -> str:
        """Tạo file cấu hình ODAS cho 8 channels"""
        config_content = f'''version = "2.1";

# Raw audio configuration
raw: {{
    fS = {self.sample_rate};
    hopSize = {self.hop_size};
    nBits = {self.bit_depth};
    nChannels = {self.n_channels};
    
    interface: {{
        type = "file";
        path = "original_8channels.pcm";
    }}
}}

# Channel mapping (skip channels 6-7)
mapping: {{
    map = (1, 2, 3, 4, 5, 8);
}}

# General configuration
general: {{
    epsilon = 1E-20;
    
    size: {{
        hopSize = {self.hop_size};
        frameSize = {self.frame_size};
    }};
    
    samplerate: {{
        mu = {self.sample_rate};
        sigma2 = 0.01;
    }};
    
    speedofsound: {{
        mu = {self.speed_of_sound};
        sigma2 = 25.0;
    }};
    
    # 8-microphone circular array
    mics = (
        # Microphone 1
        {{ mu = ({self.mic_positions[0,0]:.4f}, {self.mic_positions[0,1]:.4f}, {self.mic_positions[0,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 2  
        {{ mu = ({self.mic_positions[1,0]:.4f}, {self.mic_positions[1,1]:.4f}, {self.mic_positions[1,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 3
        {{ mu = ({self.mic_positions[2,0]:.4f}, {self.mic_positions[2,1]:.4f}, {self.mic_positions[2,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 4
        {{ mu = ({self.mic_positions[3,0]:.4f}, {self.mic_positions[3,1]:.4f}, {self.mic_positions[3,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 5
        {{ mu = ({self.mic_positions[4,0]:.4f}, {self.mic_positions[4,1]:.4f}, {self.mic_positions[4,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 8 (skip 6,7)
        {{ mu = ({self.mic_positions[7,0]:.4f}, {self.mic_positions[7,1]:.4f}, {self.mic_positions[7,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }}
    );
    
    nThetas = 181;
    gainMin = 0.25;
}};

# Sound Source Localization
ssl: {{
    nPots = 4;
    nMatches = 10;
    probMin = 0.5;
    nRefinedLevels = 1;
    interpRate = 4;
    
    scans = (
        {{ level = 2; delta = -1; }},
        {{ level = 4; delta = -1; }}
    );
    
    potential: {{
        format = "json";
        interface: {{
            type = "socket";
            ip = "127.0.0.1";
            port = 9001;
        }};
    }};
}};

# Sound Source Tracking
sst: {{
    mode = "kalman";
    add = "dynamic";
    
    active = (
        {{ weight = 1.0; mu = 0.3; sigma2 = 0.0025 }}
    );
    
    inactive = (
        {{ weight = 1.0; mu = 0.15; sigma2 = 0.0025 }}
    );
    
    sigmaR2_prob = 0.0025;
    sigmaR2_active = 0.0225;
    sigmaR2_target = 0.0025;
    Pfalse = 0.1;
    Pnew = 0.1;
    Ptrack = 0.8;
    
    tracked: {{
        format = "json";
        interface: {{
            type = "socket";
            ip = "127.0.0.1";
            port = 9000;
        }};
    }};
}};
'''
        return config_content

def main():
    parser = argparse.ArgumentParser(description='Audio Source Localization')
    parser.add_argument('--input', '-i', default='original_8channels.pcm', 
                       help='Input PCM file')
    parser.add_argument('--output', '-o', default='../../output/results/localization_result.json',
                       help='Output JSON file')
    parser.add_argument('--config', '-c', default='odas_8ch_config.cfg',
                       help='ODAS config file')
    parser.add_argument('--create-config', action='store_true',
                       help='Create ODAS config file')
    
    args = parser.parse_args()
    
    # Tạo processor
    processor = AudioProcessor()
    
    # Tạo config file nếu được yêu cầu
    if args.create_config:
        config_content = processor.create_odas_config()
        with open(args.config, 'w') as f:
            f.write(config_content)
        print(f"Đã tạo file cấu hình: {args.config}")
        return
    
    # Kiểm tra file input
    if not os.path.exists(args.input):
        print(f"Lỗi: Không tìm thấy file {args.input}")
        return
    
    try:
        # Xử lý audio
        result = processor.process_audio_file(args.input)
        
        # Lưu kết quả
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"\n=== KET QUA LOCALIZATION ===")
        print(f"Vi tri Cartesian (x, y, z): {result['position_cartesian']}")
        print(f"Vi tri Spherical:")
        print(f"  - Khoang cach: {result['position_spherical']['distance']:.3f} m")
        print(f"  - Goc phuong vi: {result['position_spherical']['azimuth']:.1f}°")
        print(f"  - Goc nang: {result['position_spherical']['elevation']:.1f}°")
        print(f"\nKet qua da luu vao: {args.output}")
        
    except Exception as e:
        print(f"Loi: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
