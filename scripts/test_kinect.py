#!/usr/bin/env python3
"""
Kinect Hardware Test Script
Verifies Xbox 360 Kinect functionality and captures test images
"""

import freenect
import cv2
import numpy as np
import sys
import os
from datetime import datetime

def test_kinect_detection():
    """Test if Kinect hardware is detected"""
    print("🔍 Testing Kinect hardware detection...")
    
    try:
        # Try to initialize Kinect
        ctx = freenect.init()
        num_devices = freenect.num_devices(ctx)
        
        if num_devices == 0:
            print("❌ No Kinect devices found")
            return False
        
        print(f"✅ Found {num_devices} Kinect device(s)")
        
        # Get device info
        device = freenect.open_device(ctx, 0)
        if device:
            print("✅ Successfully opened Kinect device")
            freenect.close_device(device)
        
        freenect.shutdown(ctx)
        return True
        
    except Exception as e:
        print(f"❌ Kinect detection failed: {e}")
        return False

def test_rgb_camera():
    """Test RGB camera functionality"""
    print("\n📷 Testing RGB camera...")
    
    try:
        # Get RGB frame
        rgb_array, timestamp = freenect.sync_get_video()
        
        if rgb_array is None:
            print("❌ Failed to get RGB frame")
            return False, None
        
        print(f"✅ RGB frame captured: {rgb_array.shape}")
        print(f"   Resolution: {rgb_array.shape[1]}x{rgb_array.shape[0]}")
        print(f"   Channels: {rgb_array.shape[2]}")
        print(f"   Timestamp: {timestamp}")
        
        # Convert to BGR for OpenCV
        bgr_frame = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
        
        return True, bgr_frame
        
    except Exception as e:
        print(f"❌ RGB camera test failed: {e}")
        return False, None

def test_depth_sensor():
    """Test depth sensor functionality"""
    print("\n🌊 Testing depth sensor...")
    
    try:
        # Get depth frame
        depth_array, timestamp = freenect.sync_get_depth()
        
        if depth_array is None:
            print("❌ Failed to get depth frame")
            return False, None
        
        print(f"✅ Depth frame captured: {depth_array.shape}")
        print(f"   Resolution: {depth_array.shape[1]}x{depth_array.shape[0]}")
        print(f"   Data type: {depth_array.dtype}")
        print(f"   Timestamp: {timestamp}")
        print(f"   Depth range: {depth_array.min()} - {depth_array.max()}")
        
        # Convert to 8-bit for visualization
        depth_8bit = (depth_array / depth_array.max() * 255).astype(np.uint8)
        depth_colored = cv2.applyColorMap(depth_8bit, cv2.COLORMAP_JET)
        
        return True, depth_colored
        
    except Exception as e:
        print(f"❌ Depth sensor test failed: {e}")
        return False, None

def test_motor_control():
    """Test motor control functionality"""
    print("\n🎛️ Testing motor control...")
    
    try:
        # Test tilt motor
        print("   Testing tilt motor...")
        
        # Get current tilt
        current_tilt = freenect.sync_get_tilt_state()
        print(f"   Current tilt angle: {current_tilt}")
        
        # Test small movement
        test_angle = 5
        freenect.sync_set_tilt_degs(test_angle)
        print(f"   Set tilt to {test_angle} degrees")
        
        # Wait and check
        import time
        time.sleep(2)
        new_tilt = freenect.sync_get_tilt_state()
        print(f"   New tilt angle: {new_tilt}")
        
        # Return to center
        freenect.sync_set_tilt_degs(0)
        print("   Returned to center position")
        
        print("✅ Motor control working")
        return True
        
    except Exception as e:
        print(f"❌ Motor control test failed: {e}")
        return False

def test_led_control():
    """Test LED control functionality"""
    print("\n💡 Testing LED control...")
    
    try:
        import time
        
        # Test different LED states
        led_states = [
            (freenect.LED_OFF, "OFF"),
            (freenect.LED_GREEN, "GREEN"),
            (freenect.LED_RED, "RED"),
            (freenect.LED_YELLOW, "YELLOW"),
            (freenect.LED_BLINK_GREEN, "BLINK GREEN"),
            (freenect.LED_OFF, "OFF")
        ]
        
        for led_state, name in led_states:
            freenect.sync_set_led(led_state)
            print(f"   LED: {name}")
            time.sleep(1)
        
        print("✅ LED control working")
        return True
        
    except Exception as e:
        print(f"❌ LED control test failed: {e}")
        return False

def save_test_images(rgb_frame, depth_frame):
    """Save test images with timestamp"""
    print("\n💾 Saving test images...")
    
    try:
        # Create output directory
        output_dir = "kinect_test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save RGB image
        if rgb_frame is not None:
            rgb_filename = f"{output_dir}/kinect_rgb_{timestamp}.jpg"
            cv2.imwrite(rgb_filename, rgb_frame)
            print(f"✅ RGB image saved: {rgb_filename}")
        
        # Save depth image
        if depth_frame is not None:
            depth_filename = f"{output_dir}/kinect_depth_{timestamp}.jpg"
            cv2.imwrite(depth_filename, depth_frame)
            print(f"✅ Depth image saved: {depth_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save images: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 satware Eye - Kinect Hardware Test")
    print("=" * 40)
    
    # Test results
    results = {}
    
    # Test 1: Hardware detection
    results['detection'] = test_kinect_detection()
    if not results['detection']:
        print("\n❌ Hardware detection failed. Check connections and permissions.")
        return 1
    
    # Test 2: RGB camera
    results['rgb'], rgb_frame = test_rgb_camera()
    
    # Test 3: Depth sensor
    results['depth'], depth_frame = test_depth_sensor()
    
    # Test 4: Motor control
    results['motor'] = test_motor_control()
    
    # Test 5: LED control
    results['led'] = test_led_control()
    
    # Save test images
    if rgb_frame is not None or depth_frame is not None:
        results['save'] = save_test_images(rgb_frame, depth_frame)
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary")
    print("=" * 40)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.capitalize():15} {status}")
    
    # Overall result
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! Kinect is fully functional.")
        print("\nNext steps:")
        print("1. Run: python3 scripts/kinect_to_webcam.py")
        print("2. Open satware-eye in browser")
        print("3. Select 'Kinect RGB' camera")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check KINECT_SETUP.md for troubleshooting.")
        return 1

if __name__ == "__main__":
    sys.exit(main())