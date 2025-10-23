#!/bin/bash

# Script chạy ODAS localization cho file original_8channels.pcm

echo "=== ODAS Audio Source Localization ==="
echo "File: original_8channels.pcm"
echo "Channels: 8 (1-5 và 8 có audio, 6-7 không có audio)"
echo "Format: 16-bit PCM, 16000 Hz"
echo ""

# Kiểm tra file input
if [ ! -f "original_8channels.pcm" ]; then
    echo "Lỗi: Không tìm thấy file original_8channels.pcm"
    echo "Vui lòng đặt file vào thư mục hiện tại"
    exit 1
fi

# Kiểm tra file cấu hình
if [ ! -f "odas_8ch_config.cfg" ]; then
    echo "Tạo file cấu hình ODAS..."
    python3 create_odas_config.py
    if [ $? -ne 0 ]; then
        echo "Lỗi: Không thể tạo file cấu hình"
        exit 1
    fi
fi

# Kiểm tra ODAS executable
if [ ! -f "./odaslive" ]; then
    echo "Lỗi: Không tìm thấy odaslive executable"
    echo "Vui lòng build ODAS trước:"
    echo "  mkdir build && cd build"
    echo "  cmake .. && make"
    echo "  cp odaslive .."
    exit 1
fi

echo "Bắt đầu xử lý audio với ODAS..."
echo "Config: odas_8ch_config.cfg"
echo ""

# Chạy ODAS
./odaslive -c odas_8ch_config.cfg -v

echo ""
echo "Xử lý hoàn tất!"
echo "Kết quả có thể được lắng nghe qua:"
echo "- Socket port 9000: tracked sources"
echo "- Socket port 9001: potential sources"
echo ""
echo "Để lắng nghe kết quả:"
echo "  netcat -l 9000  # tracked sources"
echo "  netcat -l 9001  # potential sources"
