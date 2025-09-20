#!/usr/bin/env python3
"""
Test script to demonstrate all AI models are working correctly
"""

import sys
import os
import numpy as np
import time

# Add the ai-models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-models'))

def test_heat_sensor_detection():
    """Test the heat sensor detection system"""
    print("🔥 Testing Heat Sensor Detection System...")
    try:
        from heat_sensor_detection import HeatSensorDetection
        
        detector = HeatSensorDetection()
        
        # Test heat signature detection
        heat_signatures = detector.get_heat_signatures()
        print(f"✅ Detected {len(heat_signatures)} heat signatures")
        
        for signature in heat_signatures[:2]:  # Show first 2
            print(f"   📍 Threat at ({signature['lat']:.4f}, {signature['lng']:.4f}) - Level: {signature['threat_level']}")
        
        # Test tactical analysis
        analysis = detector.analyze_threat(heat_signatures[0])
        print(f"✅ Tactical Analysis: {analysis['threat_assessment'][:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ Heat sensor test failed: {e}")
        return False

def test_ai_models_manager():
    """Test the AI models manager"""
    print("\n🤖 Testing AI Models Manager...")
    try:
        from ai_models_manager import AIModelsManager
        
        manager = AIModelsManager()
        
        # Test tactical analysis
        threat_data = {
            "enemy_count": 15,
            "vehicle_types": ["Tank", "APC"],
            "terrain": "Urban"
        }
        
        analysis = manager.get_tactical_analysis(threat_data)
        print(f"✅ Tactical Analysis Generated: {len(analysis)} characters")
        print(f"   Sample: {analysis[:100]}...")
        
        # Test route optimization
        start = (28.6139, 77.2090)  # Delhi
        end = (28.7041, 77.1025)    # Target
        obstacles = [(28.65, 77.15), (28.66, 77.16)]
        
        route = manager.optimize_route(start, end, obstacles)
        print(f"✅ Route Optimization: {route['status']} - Distance: {route['distance_km']:.2f}km")
        
        return True
    except Exception as e:
        print(f"❌ AI models test failed: {e}")
        return False

def test_computer_vision():
    """Test computer vision threat detection"""
    print("\n👁️ Testing Computer Vision System...")
    try:
        # Create a dummy image array
        dummy_image = np.random.randint(0, 255, (416, 416, 3), dtype=np.uint8)
        
        from threat_detection import ThreatDetector
        detector = ThreatDetector()
        
        # Test threat detection
        threats = detector.detect_threats(dummy_image)
        print(f"✅ Computer Vision Model Loaded Successfully")
        print(f"   Detection ready for: {len(detector.class_names)} object types")
        
        return True
    except Exception as e:
        print(f"❌ Computer vision test failed: {e}")
        return False

def test_swarm_coordination():
    """Test swarm intelligence coordination"""
    print("\n🐝 Testing Swarm Intelligence System...")
    try:
        from swarm_coordinator import SwarmCoordinator
        
        coordinator = SwarmCoordinator(num_agents=5)
        
        # Test swarm coordination
        mission = {
            "type": "reconnaissance",
            "target_area": [(28.6, 77.2), (28.7, 77.3)],
            "priority": "high"
        }
        
        assignments = coordinator.coordinate_mission(mission)
        print(f"✅ Swarm Coordination: {len(assignments)} agents assigned")
        
        for i, assignment in enumerate(assignments[:3]):  # Show first 3
            print(f"   Agent {i+1}: {assignment['task'][:30]}...")
        
        return True
    except Exception as e:
        print(f"❌ Swarm coordination test failed: {e}")
        return False

def main():
    """Run all AI model tests"""
    print("🚀 Military AI Simulation - Model Testing Suite")
    print("=" * 50)
    
    tests = [
        test_heat_sensor_detection,
        test_ai_models_manager,
        test_computer_vision,
        test_swarm_coordination
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            time.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All AI models are operational and ready for deployment!")
        print("🎖️ Military AI Simulation Platform is fully functional!")
    else:
        print(f"⚠️ {total - passed} tests failed. Check the logs above.")
    
    return passed == total

if __name__ == "__main__":
    main()