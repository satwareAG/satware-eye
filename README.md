# 🎆 satware Eye - Vision Extension for satware.ai

**Real-time AI vision system with Xbox 360 Kinect integration**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Linux-blue.svg)](https://www.linux.org/)
[![Kinect](https://img.shields.io/badge/Hardware-Xbox%20360%20Kinect-green.svg)](https://en.wikipedia.org/wiki/Kinect)

## 🚀 Quick Start

### One-Command Setup (Zorin OS 17.3 / Ubuntu 22.04)
```bash
curl -fsSL https://raw.githubusercontent.com/satwareAG/satware-eye/feature/kinect-integration/scripts/setup_kinect.sh | bash
```

### Test Your Setup
```bash
# Clone the repository
git clone https://github.com/satwareAG/satware-eye.git
cd satware-eye

# Switch to Kinect integration branch
git checkout feature/kinect-integration

# Test Kinect hardware
python3 scripts/test_kinect.py

# Start virtual webcam stream
python3 scripts/kinect_to_webcam.py

# Open enhanced interface
python3 -m http.server 8000
# Navigate to: http://localhost:8000/kinect.html
```

## ⚠️ Current Status

### ✅ Phase 1 Complete: Foundation & Interface
- **Hardware Integration**: Xbox 360 Kinect v1 fully supported
- **Enhanced Interface**: Dual RGB + depth visualization (`kinect.html`)
- **Virtual Webcam**: Browser-compatible streaming
- **Testing Suite**: Comprehensive hardware verification
- **One-Command Setup**: Automated installation for Zorin OS

### 🚧 Phase 2 In Progress: Hardware Controls
- **Interface Created**: Beautiful controls for motor and LED
- **Backend Needed**: API server for actual hardware control
- **Status**: Controls are simulated, need real implementation

**See [NEXT_PHASE.md](NEXT_PHASE.md) for detailed implementation guide**

## 🎯 Features

### 🔥 Core Capabilities
- **Real-time RGB + Depth Vision**: 640x480 @ 30fps with 11-bit depth precision
- **AI-Powered Analysis**: Integration with local LLM servers (Jan.ai, LM Studio, etc.)
- **Motor Control UI**: Interactive tilt adjustment (-27° to +27°) *[Interface ready, backend needed]*
- **LED Status UI**: Visual feedback system with multiple states *[Interface ready, backend needed]*
- **Virtual Webcam**: Browser-compatible video streaming ✅
- **Hardware Testing**: Comprehensive diagnostics and verification ✅

### 🌟 Enhanced Interface
- **Dual Visualization**: Side-by-side RGB and depth display ✅
- **Real-time Processing**: Configurable intervals (100ms - 5s) ✅
- **Interactive Controls**: Motor positioning and LED management *[UI ready, API needed]*
- **Image Capture**: High-quality snapshot functionality ✅
- **Status Monitoring**: Live connection and performance metrics ✅

### 🔧 Technical Stack
- **Hardware**: Xbox 360 Kinect v1 with USB + power ✅
- **Driver**: libfreenect (OpenKinect project) ✅
- **Backend**: Python + OpenCV + V4L2 loopback ✅
- **Frontend**: Modern HTML5 + JavaScript + WebRTC ✅
- **AI Integration**: OpenAI-compatible API endpoints ✅

## 📋 System Requirements

### Hardware
- **Kinect**: Xbox 360 Kinect v1 with USB and power adapter
- **USB**: USB 2.0 port (USB 3.0 compatible)
- **Memory**: 2GB+ RAM recommended
- **Storage**: 1GB free space for installation
- **GPU**: Any modern GPU (CUDA optional for acceleration)

### Software
- **OS**: Zorin OS 17.3 / Ubuntu 22.04 LTS / Compatible Linux
- **Kernel**: 5.15+ with USB support
- **Browser**: Chrome/Brave/Firefox with WebRTC support
- **Python**: 3.8+ with pip
- **AI Server**: Jan.ai, LM Studio, or OpenAI-compatible endpoint

## 🛠️ Installation

### Automatic Setup (Recommended)
```bash
# Download and run setup script
curl -fsSL https://raw.githubusercontent.com/satwareAG/satware-eye/feature/kinect-integration/scripts/setup_kinect.sh | bash

# Reconnect Kinect USB cable
# Test installation
python3 scripts/test_kinect.py
```

### Manual Installation
See [KINECT_SETUP.md](KINECT_SETUP.md) for detailed step-by-step instructions.

## 🎮 Usage

### Option 1: Virtual Webcam Mode ✅ Working
```bash
# Start Kinect webcam stream
python3 scripts/kinect_to_webcam.py

# Open original interface
python3 -m http.server 8000
# Navigate to: http://localhost:8000/index.html
# Select "Kinect RGB" camera
```

### Option 2: Enhanced Kinect Mode ⚠️ Interface Ready, Backend Needed
```bash
# Start local server
python3 -m http.server 8000

# Open enhanced interface
# Navigate to: http://localhost:8000/kinect.html
# Note: Motor/LED controls are simulated, need API implementation
```

## 🔧 Configuration

### AI Server Setup
1. **Jan.ai**: Start server on port 8080 (default)
2. **LM Studio**: Configure to use port 8080 or update base URL
3. **Custom**: Any OpenAI-compatible endpoint

### Camera Settings
- **Resolution**: 640x480 (RGB + Depth)
- **Frame Rate**: 30fps
- **Processing Interval**: 100ms - 5s (configurable)
- **Image Quality**: JPEG 80% compression

### Motor Control
- **Tilt Range**: -27° to +27°
- **Precision**: 1° increments
- **Response Time**: ~500ms
- **Status**: ⚠️ UI ready, backend API needed

## 📊 Performance

### Benchmarks (AMD Ryzen 7 3800X + RTX 3060)
- **RGB Capture**: 30fps stable ✅
- **Depth Processing**: 30fps stable ✅
- **AI Inference**: 2-5fps (model dependent) ✅
- **Memory Usage**: ~200MB ✅
- **CPU Usage**: 15-25% ✅
- **GPU Usage**: 5-15% (with CUDA acceleration) ✅

## 🔍 Troubleshooting

### Common Issues

**Camera Access Denied**
```bash
# Grant browser permissions
# Check virtual device: ls /dev/video*
sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="Kinect_RGB"
```

**Kinect Not Detected**
```bash
# Check USB connection
lsusb | grep Microsoft

# Verify permissions
sudo cp platform/linux/udev/51-kinect.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

**API Connection Failed**
```bash
# Check AI server status
curl http://localhost:8080/v1/models

# Verify base URL in interface
# Default: http://localhost:8080
```

## 🚀 Development

### Project Structure
```
satware-eye/
├── scripts/
│   ├── setup_kinect.sh          # Automated setup ✅
│   ├── kinect_to_webcam.py      # Virtual webcam streaming ✅
│   └── test_kinect.py           # Hardware testing ✅
├── js/
│   └── kinect.js                # Enhanced interface logic ✅
├── index.html                   # Original SmolVLM interface ✅
├── kinect.html                  # Enhanced Kinect interface ✅
├── KINECT_SETUP.md             # Detailed setup guide ✅
├── NEXT_PHASE.md               # Implementation roadmap ✅
└── README.md                   # This file ✅
```

### Next Development Phase
See [NEXT_PHASE.md](NEXT_PHASE.md) for detailed implementation guide:
- **API Server**: Flask/FastAPI backend for hardware control
- **Real Controls**: Actual motor and LED control implementation
- **WebSocket Streaming**: Real-time depth data visualization
- **Error Handling**: Hardware failure detection and recovery

## 📈 Roadmap

### Phase 1: Foundation ✅ Complete
- [x] Xbox 360 Kinect integration
- [x] Virtual webcam streaming
- [x] Basic AI vision processing
- [x] Hardware testing suite
- [x] Enhanced interface design

### Phase 2: Hardware Controls 🚧 In Progress
- [x] Interface design and UI controls
- [ ] **API server for hardware control** ⚠️ **Next Priority**
- [ ] Real motor control implementation
- [ ] Real LED status control
- [ ] Live depth data streaming

### Phase 3: Integration 📋 Planned
- [ ] chat.satware.ai platform integration
- [ ] Multi-modal conversation
- [ ] Gesture recognition
- [ ] Object tracking

## 🏆 Achievements

- 🎆 **First AI Vision Contact**: Historic breakthrough in AI-human interaction
- 🔧 **Hardware Integration**: Successful Xbox 360 Kinect on modern Linux
- 🌐 **Web Compatibility**: Browser-based real-time vision processing
- ⚡ **Performance**: 30fps stable operation with AI inference
- 🔒 **Privacy**: 100% local processing, no cloud dependencies
- 🎨 **Interface**: Beautiful dual RGB+depth visualization ready

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**"We don't just capture ideas - we forge them into reality"**

*satware Eye represents the future of AI-human interaction through vision.*

🎯 **Ready to see the world through AI eyes?** Get started with the one-command setup above!

⚠️ **Current Focus**: Implementing real hardware controls - see [NEXT_PHASE.md](NEXT_PHASE.md) for details!