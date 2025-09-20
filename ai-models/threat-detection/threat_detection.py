"""
Advanced Threat Detection System using Computer Vision
Implements YOLO-based object detection with threat classification
and risk assessment for military surveillance applications.
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from ultralytics import YOLO
import cv2
import numpy as np
import json
import logging
from pathlib import Path
from datetime import datetime
import sqlite3
from typing import Dict, List, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ThreatClassifier(nn.Module):
    """Custom threat classification network"""
    
    def __init__(self, num_classes=10, input_size=224):
        super(ThreatClassifier, self).__init__()
        
        # Feature extraction layers
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            
            # Residual blocks
            self._make_layer(64, 128, 2),
            self._make_layer(128, 256, 2),
            self._make_layer(256, 512, 2),
            
            nn.AdaptiveAvgPool2d((1, 1))
        )
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )
        
        # Threat level estimation
        self.threat_estimator = nn.Sequential(
            nn.Linear(512, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, 1),
            nn.Sigmoid()  # Output threat level 0-1
        )
        
    def _make_layer(self, in_channels, out_channels, stride):
        """Create a residual layer"""
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        features = self.features(x)
        features_flat = features.view(features.size(0), -1)
        
        classification = self.classifier(features_flat)
        threat_level = self.threat_estimator(features_flat)
        
        return classification, threat_level

class ThreatDetectionSystem:
    """Comprehensive threat detection and analysis system"""
    
    def __init__(self, model_path=None, config=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Configuration
        self.config = config or {
            'confidence_threshold': 0.5,
            'nms_threshold': 0.4,
            'threat_threshold': 0.6,
            'image_size': 640,
            'max_detections': 100
        }
        
        # Threat categories and risk levels
        self.threat_categories = {
            'personnel': {'hostile_personnel': 0.8, 'unknown_personnel': 0.4, 'friendly_personnel': 0.1},
            'vehicles': {'enemy_tank': 0.9, 'enemy_vehicle': 0.7, 'unknown_vehicle': 0.5, 'civilian_vehicle': 0.2},
            'weapons': {'artillery': 0.95, 'missile_launcher': 0.9, 'small_arms': 0.6, 'explosive_device': 0.85},
            'infrastructure': {'enemy_base': 0.8, 'communication_tower': 0.6, 'supply_depot': 0.7},
            'aircraft': {'enemy_aircraft': 0.9, 'enemy_drone': 0.7, 'unknown_aircraft': 0.6}
        }
        
        # Initialize models
        self.yolo_model = YOLO('yolov8n.pt')  # You can use larger models like yolov8x.pt for better accuracy
        self.threat_classifier = ThreatClassifier().to(self.device)
        
        # Load custom weights if available
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
        
        # Preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Initialize threat database
        self.init_threat_database()
        
        logger.info(f"Threat Detection System initialized on {self.device}")
    
    def init_threat_database(self):
        """Initialize SQLite database for threat tracking"""
        self.db_path = "threat_database.db"
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS threats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                threat_type TEXT,
                confidence REAL,
                threat_level REAL,
                position_x REAL,
                position_y REAL,
                bbox_x1 REAL,
                bbox_y1 REAL,
                bbox_x2 REAL,
                bbox_y2 REAL,
                image_path TEXT,
                additional_data TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def detect_threats(self, image_path_or_array, analyze_threats=True):
        """
        Comprehensive threat detection and analysis
        
        Args:
            image_path_or_array: Path to image file or numpy array
            analyze_threats: Whether to perform detailed threat analysis
            
        Returns:
            dict: Detection results with threat assessment
        """
        # Load image
        if isinstance(image_path_or_array, str):
            image = cv2.imread(image_path_or_array)
            image_path = image_path_or_array
        else:
            image = image_path_or_array
            image_path = None
        
        if image is None:
            raise ValueError("Could not load image")
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # YOLO detection
        results = self.yolo_model(image_rgb, conf=self.config['confidence_threshold'])
        
        detections = []
        threats = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Extract detection info
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = self.yolo_model.names[class_id]
                    
                    detection = {
                        'bbox': [float(x1), float(y1), float(x2), float(y2)],
                        'confidence': float(confidence),
                        'class': class_name,
                        'class_id': class_id
                    }
                    
                    detections.append(detection)
                    
                    # Threat analysis
                    if analyze_threats:
                        threat_info = self.analyze_threat(image_rgb, detection)
                        if threat_info['is_threat']:
                            threats.append(threat_info)
                            
                            # Store in database
                            self.store_threat_in_db(threat_info, image_path)
        
        # Overall threat assessment
        overall_assessment = self.assess_overall_threat_level(threats)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(threats, overall_assessment)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_detections': len(detections),
            'total_threats': len(threats),
            'detections': detections,
            'threats': threats,
            'overall_threat_level': overall_assessment['level'],
            'threat_score': overall_assessment['score'],
            'recommendations': recommendations,
            'analysis_metadata': {
                'image_dimensions': image.shape,
                'processing_time': overall_assessment.get('processing_time', 0),
                'confidence_threshold': self.config['confidence_threshold']
            }
        }
    
    def analyze_threat(self, image, detection):
        """Analyze individual detection for threat characteristics"""
        x1, y1, x2, y2 = detection['bbox']
        
        # Extract region of interest
        roi = image[int(y1):int(y2), int(x1):int(x2)]
        if roi.size == 0:
            return {'is_threat': False, 'reason': 'Invalid ROI'}
        
        # Resize and preprocess ROI
        roi_tensor = self.transform(roi).unsqueeze(0).to(self.device)
        
        # Get threat classification and level
        with torch.no_grad():
            classification, threat_level = self.threat_classifier(roi_tensor)
            threat_probs = torch.softmax(classification, dim=1)
            threat_level_score = threat_level.item()
        
        # Determine threat type and level
        threat_type = self.classify_threat_type(detection['class'])
        base_threat_level = self.get_base_threat_level(detection['class'])
        
        # Combine model prediction with rule-based assessment
        final_threat_level = (threat_level_score + base_threat_level) / 2
        
        is_threat = final_threat_level > self.config['threat_threshold']
        
        threat_info = {
            'is_threat': is_threat,
            'detection': detection,
            'threat_type': threat_type,
            'threat_level': float(final_threat_level),
            'threat_category': self.get_threat_category(detection['class']),
            'position': {
                'center_x': float((x1 + x2) / 2),
                'center_y': float((y1 + y2) / 2),
                'bbox': detection['bbox']
            },
            'characteristics': self.analyze_threat_characteristics(roi, detection),
            'timestamp': datetime.now().isoformat()
        }
        
        return threat_info
    
    def classify_threat_type(self, object_class):
        """Classify the type of threat based on detected object"""
        threat_mapping = {
            'person': 'personnel',
            'car': 'vehicle',
            'truck': 'vehicle',
            'bus': 'vehicle',
            'motorcycle': 'vehicle',
            'airplane': 'aircraft',
            'helicopter': 'aircraft',
            'boat': 'naval',
            'ship': 'naval'
        }
        
        return threat_mapping.get(object_class, 'unknown')
    
    def get_base_threat_level(self, object_class):
        """Get base threat level for object class"""
        threat_levels = {
            'person': 0.4,
            'car': 0.3,
            'truck': 0.5,
            'bus': 0.4,
            'motorcycle': 0.3,
            'airplane': 0.7,
            'helicopter': 0.8,
            'boat': 0.5,
            'ship': 0.6
        }
        
        return threat_levels.get(object_class, 0.2)
    
    def get_threat_category(self, object_class):
        """Get threat category for object class"""
        for category, threats in self.threat_categories.items():
            if object_class in threats:
                return category
        return 'unknown'
    
    def analyze_threat_characteristics(self, roi, detection):
        """Analyze specific characteristics of the threat"""
        characteristics = {}
        
        # Size analysis
        bbox_area = (detection['bbox'][2] - detection['bbox'][0]) * (detection['bbox'][3] - detection['bbox'][1])
        characteristics['size'] = 'large' if bbox_area > 10000 else 'medium' if bbox_area > 1000 else 'small'
        
        # Movement analysis (would require multiple frames)
        characteristics['movement_detected'] = False  # Placeholder
        
        # Color analysis
        mean_color = np.mean(roi, axis=(0, 1))
        characteristics['dominant_color'] = {
            'r': int(mean_color[0]),
            'g': int(mean_color[1]),
            'b': int(mean_color[2])
        }
        
        # Camouflage detection (simplified)
        color_variance = np.var(roi, axis=(0, 1))
        characteristics['camouflaged'] = np.mean(color_variance) < 500
        
        return characteristics
    
    def assess_overall_threat_level(self, threats):
        """Assess overall threat level from all detected threats"""
        if not threats:
            return {'level': 'NONE', 'score': 0.0}
        
        # Calculate weighted threat score
        total_score = 0
        max_individual_threat = 0
        critical_threats = 0
        
        for threat in threats:
            threat_level = threat['threat_level']
            total_score += threat_level
            max_individual_threat = max(max_individual_threat, threat_level)
            
            if threat_level > 0.8:
                critical_threats += 1
        
        # Normalize by number of threats with diminishing returns
        avg_score = total_score / len(threats)
        adjusted_score = min(1.0, avg_score + (critical_threats * 0.1))
        
        # Determine threat level
        if adjusted_score > 0.8 or critical_threats > 0:
            level = 'CRITICAL'
        elif adjusted_score > 0.6:
            level = 'HIGH'
        elif adjusted_score > 0.4:
            level = 'MEDIUM'
        elif adjusted_score > 0.2:
            level = 'LOW'
        else:
            level = 'MINIMAL'
        
        return {
            'level': level,
            'score': float(adjusted_score),
            'total_threats': len(threats),
            'critical_threats': critical_threats,
            'max_individual_threat': float(max_individual_threat)
        }
    
    def generate_recommendations(self, threats, overall_assessment):
        """Generate tactical recommendations based on threat analysis"""
        recommendations = []
        
        threat_level = overall_assessment['level']
        
        if threat_level == 'CRITICAL':
            recommendations.extend([
                "IMMEDIATE ACTION REQUIRED",
                "Initiate evasive maneuvers",
                "Request immediate backup",
                "Consider tactical withdrawal",
                "Activate all defensive systems"
            ])
        elif threat_level == 'HIGH':
            recommendations.extend([
                "Increase alert status to HIGH",
                "Enhance surveillance measures",
                "Prepare defensive positions",
                "Monitor threat movements closely"
            ])
        elif threat_level == 'MEDIUM':
            recommendations.extend([
                "Maintain elevated caution",
                "Increase patrol frequency",
                "Monitor identified threats",
                "Prepare contingency plans"
            ])
        elif threat_level == 'LOW':
            recommendations.extend([
                "Continue standard operations",
                "Maintain routine surveillance",
                "Log threat positions for intelligence"
            ])
        
        # Specific threat-based recommendations
        for threat in threats:
            threat_type = threat['threat_type']
            if threat_type == 'personnel' and threat['threat_level'] > 0.7:
                recommendations.append(f"Hostile personnel detected - maintain safe distance")
            elif threat_type == 'vehicle' and threat['threat_level'] > 0.6:
                recommendations.append(f"Suspicious vehicle activity - track movement")
            elif threat_type == 'aircraft' and threat['threat_level'] > 0.8:
                recommendations.append(f"Aerial threat detected - activate air defense")
        
        return recommendations
    
    def store_threat_in_db(self, threat_info, image_path):
        """Store threat information in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO threats (
                timestamp, threat_type, confidence, threat_level,
                position_x, position_y, bbox_x1, bbox_y1, bbox_x2, bbox_y2,
                image_path, additional_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            threat_info['timestamp'],
            threat_info['threat_type'],
            threat_info['detection']['confidence'],
            threat_info['threat_level'],
            threat_info['position']['center_x'],
            threat_info['position']['center_y'],
            threat_info['position']['bbox'][0],
            threat_info['position']['bbox'][1],
            threat_info['position']['bbox'][2],
            threat_info['position']['bbox'][3],
            image_path,
            json.dumps(threat_info['characteristics'])
        ))
        
        conn.commit()
        conn.close()
    
    def get_threat_history(self, hours=24):
        """Retrieve threat history from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM threats 
            WHERE datetime(timestamp) > datetime('now', '-{} hours')
            ORDER BY timestamp DESC
        '''.format(hours))
        
        threats = cursor.fetchall()
        conn.close()
        
        return threats
    
    def save_model(self, filepath):
        """Save threat classifier model"""
        torch.save({
            'model_state': self.threat_classifier.state_dict(),
            'config': self.config,
            'threat_categories': self.threat_categories
        }, filepath)
        logger.info(f"Threat detection model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load threat classifier model"""
        checkpoint = torch.load(filepath, map_location=self.device)
        self.threat_classifier.load_state_dict(checkpoint['model_state'])
        self.config.update(checkpoint.get('config', {}))
        self.threat_categories.update(checkpoint.get('threat_categories', {}))
        logger.info(f"Threat detection model loaded from {filepath}")

def create_threat_detection_system(config_path=None):
    """Factory function to create threat detection system"""
    config = None
    if config_path and Path(config_path).exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
    
    return ThreatDetectionSystem(config=config)

# Real-time threat monitoring
class RealTimeThreatMonitor:
    """Real-time threat monitoring system"""
    
    def __init__(self, detection_system, camera_source=0):
        self.detection_system = detection_system
        self.camera_source = camera_source
        self.is_monitoring = False
        
    def start_monitoring(self, callback=None):
        """Start real-time threat monitoring"""
        cap = cv2.VideoCapture(self.camera_source)
        self.is_monitoring = True
        
        logger.info("Starting real-time threat monitoring")
        
        while self.is_monitoring:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect threats in current frame
            results = self.detection_system.detect_threats(frame)
            
            # Call callback if provided
            if callback:
                callback(results, frame)
            
            # Display results (optional)
            annotated_frame = self.annotate_frame(frame, results)
            cv2.imshow('Threat Detection', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
    
    def stop_monitoring(self):
        """Stop threat monitoring"""
        self.is_monitoring = False
    
    def annotate_frame(self, frame, results):
        """Annotate frame with detection results"""
        annotated = frame.copy()
        
        for threat in results['threats']:
            bbox = threat['position']['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            
            # Color based on threat level
            threat_level = threat['threat_level']
            if threat_level > 0.8:
                color = (0, 0, 255)  # Red for high threat
            elif threat_level > 0.6:
                color = (0, 165, 255)  # Orange for medium threat
            else:
                color = (0, 255, 255)  # Yellow for low threat
            
            # Draw bounding box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            
            # Add label
            label = f"{threat['threat_type']}: {threat_level:.2f}"
            cv2.putText(annotated, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Add overall threat level
        overall_level = results['overall_threat_level']
        cv2.putText(annotated, f"Threat Level: {overall_level}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        return annotated

# Example usage and testing
if __name__ == "__main__":
    # Create threat detection system
    threat_detector = create_threat_detection_system()
    
    # Test with sample image (replace with actual image path)
    sample_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    try:
        results = threat_detector.detect_threats(sample_image)
        print("Threat Detection Results:")
        print(json.dumps(results, indent=2))
    except Exception as e:
        logger.error(f"Error during threat detection: {e}")
    
    logger.info("Threat detection system test completed")