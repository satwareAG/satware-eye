#!/usr/bin/env python3
"""
Kinect to Virtual Webcam Stream
Streams Xbox 360 Kinect RGB feed to /dev/video10 for browser access
"""

import freenect
import cv2
import numpy as np
import sys
import time
import signal
import argparse

class KinectWebcamStreamer:
    def __init__(self, device_path='/dev/video10', fps=30, show_preview=False):
        self.device_path = device_path
        self.fps = fps
        self.show_preview = show_preview
        self.running = False
        self.out = None
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.stop()
    
    def get_video_frame(self):
        """Get RGB frame from Kinect and convert to BGR for OpenCV"""
        try:
            array, _ = freenect.sync_get_video()
            # Convert RGB to BGR for OpenCV
            return cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Error getting Kinect frame: {e}")
            return None
    
    def setup_output(self):
        """Setup video output to virtual webcam device"""
        try:
            # MJPG codec works well with most browsers
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.out = cv2.VideoWriter(
                self.device_path, 
                fourcc, 
                self.fps, 
                (640, 480)
            )
            
            if not self.out.isOpened():
                raise Exception(f"Could not open {self.device_path}")
                
            print(f"✅ Video output setup: {self.device_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up video output: {e}")
            return False
    
    def start(self):
        """Start the Kinect to webcam streaming"""
        print("🚀 Starting Kinect → Virtual Webcam Stream")
        print("=" * 50)
        print(f"📷 Source: Xbox 360 Kinect RGB Camera")
        print(f"🎥 Output: {self.device_path}")
        print(f"⚡ FPS: {self.fps}")
        print(f"👁️ Preview: {'Enabled' if self.show_preview else 'Disabled'}")
        print("=" * 50)
        print("Press Ctrl+C to stop")
        print()
        
        # Setup video output
        if not self.setup_output():
            return False
        
        self.running = True
        frame_count = 0
        start_time = time.time()
        
        try:
            while self.running:
                # Get frame from Kinect
                frame = self.get_video_frame()
                if frame is None:
                    print("⚠️ Failed to get Kinect frame, retrying...")
                    time.sleep(0.1)
                    continue
                
                # Write to virtual webcam
                self.out.write(frame)
                frame_count += 1
                
                # Show preview if enabled
                if self.show_preview:
                    cv2.imshow('Kinect → Webcam Stream', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                # Print status every 100 frames
                if frame_count % 100 == 0:
                    elapsed = time.time() - start_time
                    actual_fps = frame_count / elapsed
                    print(f"📊 Frames: {frame_count}, FPS: {actual_fps:.1f}")
                
                # Control frame rate
                time.sleep(1.0 / self.fps)
                
        except Exception as e:
            print(f"❌ Streaming error: {e}")
            return False
        
        return True
    
    def stop(self):
        """Stop the streaming"""
        self.running = False
        
        if self.out:
            self.out.release()
            print("✅ Video output released")
        
        if self.show_preview:
            cv2.destroyAllWindows()
            print("✅ Preview windows closed")
        
        print("🛑 Kinect webcam stream stopped")

def check_kinect():
    """Check if Kinect is connected and accessible"""
    try:
        # Try to get a frame to verify Kinect is working
        frame = freenect.sync_get_video()[0]
        print("✅ Kinect detected and accessible")
        return True
    except Exception as e:
        print(f"❌ Kinect not accessible: {e}")
        print("💡 Make sure:")
        print("   - Kinect is connected via USB")
        print("   - Kinect has external power")
        print("   - libfreenect is properly installed")
        print("   - USB permissions are configured")
        return False

def check_virtual_device(device_path):
    """Check if virtual video device exists"""
    import os
    if os.path.exists(device_path):
        print(f"✅ Virtual device found: {device_path}")
        return True
    else:
        print(f"❌ Virtual device not found: {device_path}")
        print("💡 Create it with:")
        print(f"   sudo modprobe v4l2loopback devices=1 video_nr=10 card_label=\"Kinect_RGB\"")
        return False

def main():
    parser = argparse.ArgumentParser(description='Stream Kinect RGB to virtual webcam')
    parser.add_argument('--device', '-d', default='/dev/video10', 
                       help='Virtual video device path (default: /dev/video10)')
    parser.add_argument('--fps', '-f', type=int, default=30,
                       help='Frame rate (default: 30)')
    parser.add_argument('--preview', '-p', action='store_true',
                       help='Show preview window')
    parser.add_argument('--check', '-c', action='store_true',
                       help='Check system requirements and exit')
    
    args = parser.parse_args()
    
    # Check mode
    if args.check:
        print("🔍 Checking system requirements...")
        kinect_ok = check_kinect()
        device_ok = check_virtual_device(args.device)
        
        if kinect_ok and device_ok:
            print("✅ All requirements met!")
            return 0
        else:
            print("❌ Requirements not met")
            return 1
    
    # Verify requirements before starting
    if not check_kinect():
        return 1
    
    if not check_virtual_device(args.device):
        return 1
    
    # Start streaming
    streamer = KinectWebcamStreamer(
        device_path=args.device,
        fps=args.fps,
        show_preview=args.preview
    )
    
    success = streamer.start()
    streamer.stop()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())