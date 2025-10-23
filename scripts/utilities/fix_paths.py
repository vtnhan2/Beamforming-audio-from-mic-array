#!/usr/bin/env python3
"""
Script để sửa đường dẫn trong tất cả Python files sau khi tổ chức lại cấu trúc folder
"""

import os
import re
import glob

def fix_paths_in_file(filepath):
    """Sửa đường dẫn trong một file"""
    print(f"Fixing paths in: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Các thay đổi đường dẫn cần thiết
    replacements = [
        # Input files
        (r'"audio/original_8channels\.pcm"', '"../../output/audio/original_8channels.pcm"'),
        (r"'audio/original_8channels\.pcm'", "'../../output/audio/original_8channels.pcm'"),
        
        # Output directories
        (r'"audio/amplitude_analysis"', '"../../output/audio/amplitude_analysis"'),
        (r"'audio/amplitude_analysis'", "'../../output/audio/amplitude_analysis'"),
        
        (r'"audio/beamforming"', '"../../output/audio/beamforming"'),
        (r"'audio/beamforming'", "'../../output/audio/beamforming'"),
        
        (r'"audio/channels"', '"../../output/audio/channels"'),
        (r"'audio/channels'", "'../../output/audio/channels'"),
        
        (r'"audio/combined_processing"', '"../../output/audio/combined_processing"'),
        (r"'audio/combined_processing'", "'../../output/audio/combined_processing'"),
        
        (r'"audio/filtered"', '"../../output/audio/filtered"'),
        (r"'audio/filtered'", "'../../output/audio/filtered'"),
        
        (r'"audio/reference_beamforming"', '"../../output/audio/reference_beamforming"'),
        (r"'audio/reference_beamforming'", "'../../output/audio/reference_beamforming'"),
        
        (r'"audio/bandpass_600_3000"', '"../../output/audio/bandpass_600_3000"'),
        (r"'audio/bandpass_600_3000'", "'../../output/audio/bandpass_600_3000'"),
        
        (r'"audio/filtered_all"', '"../../output/audio/filtered_all"'),
        (r"'audio/filtered_all'", "'../../output/audio/filtered_all'"),
        
        # JSON output files
        (r'"audio_analysis_result\.json"', '"../../output/results/audio_analysis_result.json"'),
        (r"'audio_analysis_result\.json'", "'../../output/results/audio_analysis_result.json'"),
        
        (r'"localization_result\.json"', '"../../output/results/localization_result.json"'),
        (r"'localization_result\.json'", "'../../output/results/localization_result.json'"),
        
        # Visualization files
        (r'"audio_channels_analysis\.png"', '"../../output/visualizations/audio_channels_analysis.png"'),
        (r"'audio_channels_analysis\.png'", "'../../output/visualizations/audio_channels_analysis.png'"),
    ]
    
    # Apply replacements
    original_content = content
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Only write if content changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  [OK] Updated paths in {filepath}")
        return True
    else:
        print(f"  - No changes needed in {filepath}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("FIXING PATHS IN PYTHON SCRIPTS")
    print("="*60)
    
    # Find all Python files in scripts directory
    script_dirs = [
        "../analysis",
        "../beamforming", 
        "../filtering",
        "../localization"
    ]
    
    updated_files = []
    
    for script_dir in script_dirs:
        if os.path.exists(script_dir):
            python_files = glob.glob(os.path.join(script_dir, "*.py"))
            for py_file in python_files:
                if fix_paths_in_file(py_file):
                    updated_files.append(py_file)
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Updated {len(updated_files)} files:")
    for file in updated_files:
        print(f"  - {file}")
    
    print("\nAll Python scripts should now work with the new folder structure!")
    print("="*60)

if __name__ == "__main__":
    main()
