#!/usr/bin/env python3
"""
Script tạo file cấu hình ODAS cho 8-channel microphone array
"""

import numpy as np

def create_odas_config():
    """Tạo file cấu hình ODAS cho 8 microphones"""
    
    # Thông số cơ bản
    sample_rate = 16000
    hop_size = 128
    frame_size = 256
    bit_depth = 16
    n_channels = 8
    speed_of_sound = 343.0
    
    # Vị trí microphone array (8 microphones dạng tròn)
    radius = 0.05  # 5cm radius
    mic_positions = []
    
    for i in range(8):
        angle = 2 * np.pi * i / 8
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        z = 0.0
        mic_positions.append([x, y, z])
    
    mic_positions = np.array(mic_positions)
    
    config_content = f'''version = "2.1";

# Raw audio configuration
raw: {{
    fS = {sample_rate};
    hopSize = {hop_size};
    nBits = {bit_depth};
    nChannels = {n_channels};
    
    interface: {{
        type = "file";
        path = "original_8channels.pcm";
    }}
}}

# Channel mapping (skip channels 6-7, use 1-5 and 8)
mapping: {{
    map = (1, 2, 3, 4, 5, 8);
}}

# General configuration
general: {{
    epsilon = 1E-20;
    
    size: {{
        hopSize = {hop_size};
        frameSize = {frame_size};
    }};
    
    samplerate: {{
        mu = {sample_rate};
        sigma2 = 0.01;
    }};
    
    speedofsound: {{
        mu = {speed_of_sound};
        sigma2 = 25.0;
    }};
    
    # 8-microphone circular array (5cm radius)
    mics = (
        # Microphone 1 (0°)
        {{ mu = ({mic_positions[0,0]:.4f}, {mic_positions[0,1]:.4f}, {mic_positions[0,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 2 (45°)
        {{ mu = ({mic_positions[1,0]:.4f}, {mic_positions[1,1]:.4f}, {mic_positions[1,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 3 (90°)
        {{ mu = ({mic_positions[2,0]:.4f}, {mic_positions[2,1]:.4f}, {mic_positions[2,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 4 (135°)
        {{ mu = ({mic_positions[3,0]:.4f}, {mic_positions[3,1]:.4f}, {mic_positions[3,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 5 (180°)
        {{ mu = ({mic_positions[4,0]:.4f}, {mic_positions[4,1]:.4f}, {mic_positions[4,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }},
        # Microphone 8 (315°) - skip 6,7
        {{ mu = ({mic_positions[7,0]:.4f}, {mic_positions[7,1]:.4f}, {mic_positions[7,2]:.4f}); 
          direction = (0.000, 0.000, 1.000); 
          angle = (80.0, 90.0); }}
    );
    
    # Spatial filters
    spatialfilters = (
        {{
            direction = (0.000, 0.000, 1.000);
            angle = (80.0, 90.0);
        }}
    );
    
    nThetas = 181;
    gainMin = 0.25;
}};

# Stationary noise estimation
sne: {{
    b = 3;
    alphaS = 0.1;
    L = 150;
    delta = 3.0;
    alphaD = 0.1;
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
    
    # Output potential sources
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
    
    theta_new = 0.9;
    N_prob = 5;
    theta_prob = 0.8;
    N_inactive = (150, 200, 250, 250);
    theta_inactive = 0.9;
    
    kalman: {{
        sigmaQ = 0.001;
    }};
    
    target: ();
    
    # Output tracked sources
    tracked: {{
        format = "json";
        interface: {{
            type = "socket";
            ip = "127.0.0.1";
            port = 9000;
        }};
    }};
}};

# Sound Source Separation
sss: {{
    mode_sep = "dds";
    mode_pf = "ms";
    
    gain_sep = 1.0;
    gain_pf = 10.0;
    
    dds: {{}};
    
    ms: {{
        alphaPmin = 0.07;
        eta = 0.5;
        alphaZ = 0.8;
        thetaWin = 0.3;
        alphaWin = 0.3;
        maxAbsenceProb = 0.9;
        Gmin = 0.01;
        winSizeLocal = 3;
        winSizeGlobal = 23;
        winSizeFrame = 256;
    }};
    
    separated: {{
        fS = 44100;
        hopSize = 512;
        nBits = 16;
        
        interface: {{
            type = "file";
            path = "separated.raw";
        }};
    }};
    
    postfiltered: {{
        fS = 44100;
        hopSize = 512;
        nBits = 16;
        
        interface: {{
            type = "file";
            path = "postfiltered.raw";
        }};
    }};
}};

# Classification
classify: {{
    frameSize = 1024;
    winSize = 3;
    tauMin = 32;
    tauMax = 200;
    deltaTauMax = 7;
    alpha = 0.3;
    gamma = 0.05;
    phiMin = 0.15;
    r0 = 0.2;
    
    category: {{
        format = "undefined";
        interface: {{
            type = "blackhole";
        }};
    }};
}};
'''
    
    return config_content

if __name__ == "__main__":
    config = create_odas_config()
    
    with open("odas_8ch_config.cfg", "w") as f:
        f.write(config)
    
    print("Đã tạo file cấu hình: odas_8ch_config.cfg")
    print("Cấu hình cho 8-channel microphone array với:")
    print("- Channels 1-5 và 8 có audio")
    print("- Channels 6-7 bị bỏ qua")
    print("- Microphone array dạng tròn, bán kính 5cm")
    print("- Sample rate: 16000 Hz")
    print("- Output qua socket: port 9000 (tracked), 9001 (potential)")
