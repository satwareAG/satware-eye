# Xbox 360 Kinect Setup for Zorin OS 17.3

**Quick setup guide for Xbox 360 Kinect v1 on Zorin OS 17.3 (Ubuntu 22.04 base)**

## 🚀 One-Command Setup

```bash
curl -fsSL https://raw.githubusercontent.com/satwareAG/satware-eye/feature/kinect-integration/scripts/setup_kinect.sh | bash
```

## 📋 Manual Setup (5 Steps)

### Step 1: Install Dependencies
```bash
sudo apt update && sudo apt install git build-essential cmake libusb-1.0-0-dev freeglut3-dev libxmu-dev libxi-dev python3-pip
```

### Step 2: Build libfreenect
```bash
cd ~/Projects
git clone https://github.com/OpenKinect/libfreenect.git
cd libfreenect
mkdir build && cd build
cmake ..
make -j4
sudo make install
sudo ldconfig
```

### Step 3: Setup USB Permissions
```bash
sudo cp ../platform/linux/udev/51-kinect.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Step 4: Install Python Dependencies
```bash
pip3 install opencv-python numpy freenect
```

### Step 5: Setup Virtual Webcam (Optional)
```bash
sudo apt install v4l2loopback-dkms v4l2loopback-utils
sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="Kinect_RGB"
```

## ✅ Verification

### Test Hardware Detection
```bash
lsusb | grep Microsoft
# Should show: Xbox NUI Camera, Xbox NUI Motor, Xbox NUI Audio
```

### Test libfreenect
```bash
freenect-glview
# Should open window with RGB + depth visualization
```

### Test Python Integration
```bash
python3 scripts/test_kinect.py
# Should capture and save test images
```

## 🎯 Integration with satware-eye

### Option 1: Virtual Webcam Mode
```bash
# Start Kinect webcam stream
python3 scripts/kinect_to_webcam.py

# Open satware-eye in browser
# Camera should show "Kinect RGB" option
```

### Option 2: Direct Integration Mode
```bash
# Use enhanced satware-eye with native Kinect support
python3 -m http.server 8000
# Open: http://localhost:8000/kinect.html
```

## 🔧 Troubleshooting

### Permission Issues
```bash
# Reconnect Kinect USB cable after udev rules setup
# Check permissions: ls -l /dev/bus/usb/001/0*
```

### Library Not Found
```bash
sudo ldconfig
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

### Camera Access Denied
```bash
# Grant browser camera permissions
# For Chrome/Brave: Settings → Privacy → Camera → Allow localhost
```

## 📊 Hardware Requirements

- **Kinect**: Xbox 360 Kinect v1 with USB + power adapter
- **USB**: USB 2.0 port (USB 3.0 compatible)
- **Power**: 12V external power adapter required
- **OS**: Zorin OS 17.3 / Ubuntu 22.04 LTS
- **Memory**: 2GB+ RAM recommended
- **GPU**: Any modern GPU (CUDA optional for acceleration)

## 🎆 Features Enabled

- ✅ **RGB Camera**: 640x480 @ 30fps
- ✅ **Depth Sensor**: 640x480 @ 30fps, 11-bit precision
- ✅ **Motor Control**: -27° to +27° tilt range
- ✅ **LED Control**: Status indication (off, green, red, yellow, blink)
- ✅ **Accelerometer**: 3-axis motion data
- ✅ **Audio Array**: 4-microphone array (with firmware)

## 🔗 Related Files

- `scripts/setup_kinect.sh` - Automated setup script
- `scripts/kinect_to_webcam.py` - Virtual webcam streaming
- `scripts/test_kinect.py` - Hardware verification
- `kinect.html` - Enhanced interface with native Kinect support
- `js/kinect.js` - Kinect-specific JavaScript functions

---

**Need help?** Open an issue at https://github.com/satwareAG/satware-eye/issues