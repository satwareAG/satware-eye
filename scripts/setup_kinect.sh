#!/bin/bash

# Xbox 360 Kinect Setup Script for Zorin OS 17.3
# Automated installation of libfreenect and dependencies

set -e

echo "🚀 satware Eye - Kinect Setup for Zorin OS 17.3"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root (except for sudo commands)"
   exit 1
fi

# Check OS compatibility
if ! grep -q "Ubuntu 22.04\|Zorin OS 17" /etc/os-release; then
    print_warning "This script is designed for Zorin OS 17.3 / Ubuntu 22.04"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Step 1: Update system and install dependencies
print_status "Step 1: Installing system dependencies..."
sudo apt update
sudo apt install -y git build-essential cmake libusb-1.0-0-dev \
    freeglut3-dev libxmu-dev libxi-dev python3-pip \
    v4l2loopback-dkms v4l2loopback-utils

print_success "Dependencies installed"

# Step 2: Create Projects directory and clone libfreenect
print_status "Step 2: Setting up libfreenect..."
cd ~
mkdir -p Projects
cd Projects

if [ -d "libfreenect" ]; then
    print_warning "libfreenect directory exists, updating..."
    cd libfreenect
    git pull
else
    print_status "Cloning libfreenect..."
    git clone https://github.com/OpenKinect/libfreenect.git
    cd libfreenect
fi

# Step 3: Build libfreenect
print_status "Step 3: Building libfreenect..."
mkdir -p build
cd build
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig

print_success "libfreenect built and installed"

# Step 4: Setup USB permissions
print_status "Step 4: Setting up USB permissions..."
sudo cp ../platform/linux/udev/51-kinect.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger

print_success "USB permissions configured"

# Step 5: Install Python dependencies
print_status "Step 5: Installing Python dependencies..."
pip3 install --user opencv-python numpy freenect

print_success "Python dependencies installed"

# Step 6: Setup virtual webcam
print_status "Step 6: Setting up virtual webcam..."
if sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="Kinect_RGB" 2>/dev/null; then
    print_success "Virtual webcam device created: /dev/video10"
else
    print_warning "Virtual webcam setup failed (may need manual configuration)"
fi

# Step 7: Download audio firmware
print_status "Step 7: Downloading Kinect audio firmware..."
if [ -f "/usr/local/share/fwfetcher.py" ]; then
    sudo python3 /usr/local/share/fwfetcher.py || print_warning "Audio firmware download failed"
else
    print_warning "fwfetcher.py not found, audio features may not work"
fi

# Verification
print_status "Verifying installation..."

# Check if Kinect is connected
if lsusb | grep -q "Microsoft.*Xbox NUI"; then
    print_success "Kinect hardware detected!"
    lsusb | grep "Microsoft.*Xbox NUI"
else
    print_warning "Kinect hardware not detected. Please connect your Kinect and restart."
fi

# Check if libfreenect tools are available
if command -v freenect-glview &> /dev/null; then
    print_success "libfreenect tools installed successfully"
else
    print_error "libfreenect tools not found in PATH"
fi

# Check virtual webcam
if [ -e "/dev/video10" ]; then
    print_success "Virtual webcam device ready: /dev/video10"
else
    print_warning "Virtual webcam device not found"
fi

echo
echo "🎉 Setup Complete!"
echo "=================="
echo
echo "Next steps:"
echo "1. Reconnect your Kinect USB cable"
echo "2. Test with: freenect-glview"
echo "3. Run: python3 scripts/test_kinect.py"
echo "4. Start webcam stream: python3 scripts/kinect_to_webcam.py"
echo
echo "For troubleshooting, see: KINECT_SETUP.md"
echo
print_success "satware Eye Kinect integration ready! 🎆👁️"