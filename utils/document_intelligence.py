"""
Document Intelligence Module - Enhanced with OCR and CNN for Smart Audit AI
Supports Tesseract OCR, MobileNet CNN, and document fraud detection
"""

import cv2
import numpy as np
import pandas as pd
import os
import joblib
from PIL import Image
import pytesseract
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class DocumentIntelligence:
    def __init__(self):
        self.ocr_config = r'--oem 3 --psm 6'  # OCR Engine Mode and Page Segmentation Mode
        self.models = {}
        self.encoders = {}
        self.model_path = os.path.join(os.path.dirname(__file__), 'document_models')
        os.makedirs(self.model_path, exist_ok=True)
        
        # Initialize MobileNetV2 base model
        self.base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        
    def extract_text_from_image(self, image_path):
        """Extract text from document image using Tesseract OCR"""
        try:
            # Read image
            if isinstance(image_path, str):
                img = cv2.imread(image_path)
            else:
                img = image_path
            
            # Preprocess image for better OCR
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply image preprocessing techniques
            # 1. Noise reduction
            denoised = cv2.medianBlur(gray, 5)
            
            # 2. Contrast enhancement
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # 3. Binarization
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text
            text = pytesseract.image_to_string(binary, config=self.ocr_config)
            
            # Extract additional data (confidence scores, bounding boxes)
            data = pytesseract.image_to_data(binary, output_type=pytesseract.Output.DICT)
            
            # Calculate confidence metrics
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = np.mean(confidences) if confidences else 0
            
            return {
                'text': text.strip(),
                'confidence': avg_confidence,
                'word_count': len(text.split()),
                'char_count': len(text),
                'line_count': len(text.split('\n')),
                'processing_success': True
            }
            
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'word_count': 0,
                'char_count': 0,
                'line_count': 0,
                'processing_success': False,
                'error': str(e)
            }
    
    def preprocess_image_for_cnn(self, img_path, target_size=(224, 224)):
        """Preprocess image for CNN analysis"""
        try:
            if isinstance(img_path, str):
                img = image.load_img(img_path, target_size=target_size)
            else:
                img = Image.fromarray(img_path).resize(target_size)
            
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            
            return img_array
            
        except Exception as e:
            print(f"Image preprocessing error: {str(e)}")
            return None
    
    def extract_image_features(self, img_path):
        """Extract features from document image using MobileNetV2"""
        try:
            img_array = self.preprocess_image_for_cnn(img_path)
            if img_array is None:
                return None
            
            # Extract features using base model
            features = self.base_model.predict(img_array)
            features_flattened = GlobalAveragePooling2D()(features)
            
            return features_flattened.numpy()
            
        except Exception as e:
            print(f"Feature extraction error: {str(e)}")
            return None
    
    def create_document_fraud_model(self):
        """Create CNN model for document fraud detection"""
        try:
            # Create model based on MobileNetV2
            base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
            base_model.trainable = False  # Freeze base model
            
            model = Sequential([
                base_model,
                GlobalAveragePooling2D(),
                Dropout(0.2),
                Dense(128, activation='relu'),
                Dropout(0.5),
                Dense(64, activation='relu'),
                Dense(1, activation='sigmoid')  # Binary classification (fraud/legitimate)
            ])
            
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            return model
            
        except Exception as e:
            print(f"Model creation error: {str(e)}")
            return None
    
    def generate_synthetic_document_data(self, n_samples=1000):
        """Generate synthetic document analysis data for training"""
        np.random.seed(42)
        
        # Simulate document features
        data = {
            'text_confidence': np.random.normal(85, 15, n_samples),  # OCR confidence
            'word_count': np.random.poisson(150, n_samples),  # Words in document
            'char_count': np.random.poisson(1200, n_samples),  # Characters
            'line_count': np.random.poisson(25, n_samples),  # Lines
            'image_quality_score': np.random.normal(0.8, 0.15, n_samples),  # Image quality
            'document_type': np.random.choice(['ID', 'Insurance', 'Medical', 'Financial', 'Legal'], n_samples),
            'has_watermark': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            'has_signatures': np.random.choice([0, 1], n_samples, p=[0.4, 0.6]),
            'has_stamps': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
            'color_consistency': np.random.normal(0.9, 0.1, n_samples),
            'font_consistency': np.random.normal(0.85, 0.15, n_samples),
            'alignment_score': np.random.normal(0.8, 0.2, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Generate fraud labels based on realistic patterns
        fraud_score = np.zeros(n_samples)
        
        # Lower text confidence indicates potential fraud
        fraud_score += np.where(df['text_confidence'] < 70, 2, 0)
        
        # Inconsistent formatting
        fraud_score += np.where(df['font_consistency'] < 0.6, 2, 0)
        fraud_score += np.where(df['alignment_score'] < 0.5, 1, 0)
        fraud_score += np.where(df['color_consistency'] < 0.7, 1, 0)
        
        # Missing security features
        fraud_score += np.where((df['has_watermark'] == 0) & (df['document_type'].isin(['ID', 'Financial'])), 1, 0)
        
        # Poor image quality
        fraud_score += np.where(df['image_quality_score'] < 0.5, 1, 0)
        
        # Convert to binary fraud label (threshold at 3)
        df['is_fraudulent'] = (fraud_score >= 3).astype(int)
        
        return df
    
    def train_document_fraud_classifier(self):
        """Train document fraud detection classifier"""
        print("Training document fraud detection model...")
        
        # Generate training data
        df = self.generate_synthetic_document_data(n_samples=5000)
        
        # Prepare features
        feature_cols = [col for col in df.columns if col not in ['is_fraudulent', 'document_type']]
        
        # Encode document type
        le = LabelEncoder()
        df['document_type_encoded'] = le.fit_transform(df['document_type'])
        self.encoders['document_type_encoder'] = le
        
        # Add encoded document type to features
        feature_cols.append('document_type_encoded')
        
        X = df[feature_cols]
        y = df['is_fraudulent']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Train traditional ML model for document analysis
        from sklearn.ensemble import RandomForestClassifier
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # Evaluate
        train_accuracy = rf_model.score(X_train, y_train)
        test_accuracy = rf_model.score(X_test, y_test)
        
        print(f"Document fraud classifier - Train accuracy: {train_accuracy:.4f}, Test accuracy: {test_accuracy:.4f}")
        
        # Save model
        self.models['document_fraud_classifier'] = rf_model
        joblib.dump(rf_model, os.path.join(self.model_path, 'document_fraud_classifier.pkl'))
        joblib.dump(self.encoders, os.path.join(self.model_path, 'document_encoders.pkl'))
        
        return rf_model
    
    def load_document_models(self):
        """Load trained document analysis models"""
        try:
            classifier_path = os.path.join(self.model_path, 'document_fraud_classifier.pkl')
            encoders_path = os.path.join(self.model_path, 'document_encoders.pkl')
            
            if os.path.exists(classifier_path) and os.path.exists(encoders_path):
                self.models['document_fraud_classifier'] = joblib.load(classifier_path)
                self.encoders.update(joblib.load(encoders_path))
                return True
            else:
                print("Document models not found. Training new models...")
                self.train_document_fraud_classifier()
                return True
        except Exception as e:
            print(f"Error loading document models: {str(e)}")
            return False
    
    def analyze_document_authenticity(self, image_path, document_type='Insurance'):
        """Comprehensive document authenticity analysis"""
        try:
            # Extract text using OCR
            ocr_result = self.extract_text_from_image(image_path)
            
            if not ocr_result['processing_success']:
                return {
                    'authenticity_score': 1,
                    'fraud_probability': 0.9,
                    'analysis_results': ['OCR processing failed - unable to analyze document'],
                    'recommendations': ['Manual review required due to processing errors']
                }
            
            # Analyze image quality and features
            img = cv2.imread(image_path) if isinstance(image_path, str) else image_path
            quality_metrics = self.analyze_image_quality(img)
            
            # Load models
            if not self.load_document_models():
                return {
                    'authenticity_score': 5,
                    'fraud_probability': 0.5,
                    'analysis_results': ['Model loading failed - using basic analysis'],
                    'recommendations': ['Manual expert review recommended']
                }
            
            # Prepare features for fraud detection
            features = {
                'text_confidence': ocr_result['confidence'],
                'word_count': ocr_result['word_count'],
                'char_count': ocr_result['char_count'],
                'line_count': ocr_result['line_count'],
                'image_quality_score': quality_metrics['overall_quality'],
                'has_watermark': quality_metrics['has_watermark'],
                'has_signatures': quality_metrics['has_signatures'],
                'has_stamps': quality_metrics['has_stamps'],
                'color_consistency': quality_metrics['color_consistency'],
                'font_consistency': quality_metrics['font_consistency'],
                'alignment_score': quality_metrics['alignment_score'],
                'document_type': document_type
            }
            
            # Encode document type
            if 'document_type_encoder' in self.encoders:
                try:
                    doc_type_encoded = self.encoders['document_type_encoder'].transform([document_type])[0]
                except:
                    doc_type_encoded = 0  # Default encoding for unknown types
            else:
                doc_type_encoded = 0
            
            features['document_type_encoded'] = doc_type_encoded
            
            # Create feature vector
            feature_vector = [[
                features['text_confidence'],
                features['word_count'],
                features['char_count'],
                features['line_count'],
                features['image_quality_score'],
                features['has_watermark'],
                features['has_signatures'],
                features['has_stamps'],
                features['color_consistency'],
                features['font_consistency'],
                features['alignment_score'],
                features['document_type_encoded']
            ]]
            
            # Predict fraud probability
            model = self.models['document_fraud_classifier']
            fraud_probability = float(model.predict_proba(feature_vector)[0, 1])
            
            # Calculate authenticity score (1-10, where 10 is most authentic)
            authenticity_score = int(10 - (fraud_probability * 9))
            
            # Generate analysis results
            analysis_results = []
            recommendations = []
            
            # OCR Analysis
            if ocr_result['confidence'] < 70:
                analysis_results.append(f"⚠️ Low OCR confidence ({ocr_result['confidence']:.1f}%) - possible image quality issues")
                recommendations.append("Consider requesting higher quality document scan")
            else:
                analysis_results.append(f"✅ Good OCR confidence ({ocr_result['confidence']:.1f}%)")
            
            # Text analysis
            if ocr_result['word_count'] < 20:
                analysis_results.append("⚠️ Unusually low word count for document type")
            
            # Image quality analysis
            if quality_metrics['overall_quality'] < 0.6:
                analysis_results.append("⚠️ Poor image quality detected")
                recommendations.append("Request better quality image or original document")
            
            # Security features
            if not quality_metrics['has_watermark'] and document_type in ['ID', 'Financial', 'Insurance']:
                analysis_results.append("⚠️ Missing expected watermark or security features")
                recommendations.append("Verify document source and authenticity")
            
            # Formatting consistency
            if quality_metrics['font_consistency'] < 0.7:
                analysis_results.append("⚠️ Inconsistent font formatting detected")
                recommendations.append("Manual review for potential tampering")
            
            if quality_metrics['alignment_score'] < 0.6:
                analysis_results.append("⚠️ Poor text alignment - possible editing")
            
            # Overall assessment
            if fraud_probability > 0.7:
                analysis_results.append("🚨 HIGH FRAUD RISK - Multiple authenticity issues detected")
                recommendations.append("REJECT document and request alternatives")
            elif fraud_probability > 0.4:
                analysis_results.append("⚠️ MODERATE FRAUD RISK - Additional verification needed")
                recommendations.append("Manual expert review recommended")
            else:
                analysis_results.append("✅ LOW FRAUD RISK - Document appears authentic")
                recommendations.append("Proceed with standard verification")
            
            return {
                'authenticity_score': authenticity_score,
                'fraud_probability': fraud_probability,
                'ocr_results': ocr_result,
                'quality_metrics': quality_metrics,
                'analysis_results': analysis_results,
                'recommendations': recommendations,
                'extracted_text': ocr_result['text']
            }
            
        except Exception as e:
            return {
                'authenticity_score': 1,
                'fraud_probability': 0.9,
                'analysis_results': [f'Analysis error: {str(e)}'],
                'recommendations': ['Manual review required due to processing errors']
            }
    
    def analyze_image_quality(self, img):
        """Analyze image quality and detect security features"""
        try:
            # Convert to different color spaces for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Image quality metrics
            # 1. Blur detection (Laplacian variance)
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 2. Brightness and contrast
            brightness = np.mean(gray)
            contrast = np.std(gray)
            
            # 3. Noise level (using standard deviation of smoothed image)
            smoothed = cv2.GaussianBlur(gray, (5, 5), 0)
            noise_level = np.std(gray - smoothed)
            
            # Security features detection (simplified)
            # 1. Watermark detection (look for repeated patterns)
            has_watermark = self.detect_watermark(gray)
            
            # 2. Signature detection (look for irregular shapes)
            has_signatures = self.detect_signatures(gray)
            
            # 3. Stamp detection (look for circular/rectangular patterns)
            has_stamps = self.detect_stamps(gray)
            
            # Formatting analysis
            # 1. Color consistency
            color_consistency = self.analyze_color_consistency(hsv)
            
            # 2. Font consistency (simplified - based on edge patterns)
            font_consistency = self.analyze_font_consistency(gray)
            
            # 3. Alignment score
            alignment_score = self.analyze_text_alignment(gray)
            
            # Calculate overall quality score
            quality_factors = [
                min(blur_score / 100, 1.0),  # Normalize blur score
                min(contrast / 50, 1.0),     # Normalize contrast
                max(0, 1 - noise_level / 20) # Normalize noise (lower is better)
            ]
            overall_quality = np.mean(quality_factors)
            
            return {
                'overall_quality': float(overall_quality),
                'blur_score': float(blur_score),
                'brightness': float(brightness),
                'contrast': float(contrast),
                'noise_level': float(noise_level),
                'has_watermark': has_watermark,
                'has_signatures': has_signatures,
                'has_stamps': has_stamps,
                'color_consistency': float(color_consistency),
                'font_consistency': float(font_consistency),
                'alignment_score': float(alignment_score)
            }
            
        except Exception as e:
            # Return default values on error
            return {
                'overall_quality': 0.5,
                'blur_score': 0,
                'brightness': 128,
                'contrast': 30,
                'noise_level': 10,
                'has_watermark': 0,
                'has_signatures': 0,
                'has_stamps': 0,
                'color_consistency': 0.7,
                'font_consistency': 0.7,
                'alignment_score': 0.7
            }
    
    def detect_watermark(self, gray_img):
        """Simple watermark detection"""
        # Apply frequency domain analysis to detect repeated patterns
        f_transform = np.fft.fft2(gray_img)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.log(np.abs(f_shift) + 1)
        
        # Check for regular patterns that might indicate watermarks
        pattern_strength = np.std(magnitude_spectrum)
        return 1 if pattern_strength > 5 else 0
    
    def detect_signatures(self, gray_img):
        """Simple signature detection based on contours"""
        edges = cv2.Canny(gray_img, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Look for irregular, curved contours that might be signatures
        signature_like_contours = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            if area > 500 and perimeter > 100:
                # Check if contour is irregular (not rectangular/circular)
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                if area / hull_area < 0.7:  # Irregular shape
                    signature_like_contours += 1
        
        return 1 if signature_like_contours > 0 else 0
    
    def detect_stamps(self, gray_img):
        """Simple stamp detection using circle and rectangle detection"""
        # Detect circles (round stamps)
        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=50, param2=30, minRadius=10, maxRadius=100)
        
        # Detect rectangles (rectangular stamps)
        edges = cv2.Canny(gray_img, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        rectangular_stamps = 0
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4 and cv2.contourArea(contour) > 1000:
                rectangular_stamps += 1
        
        has_circles = circles is not None and len(circles[0]) > 0
        has_rectangles = rectangular_stamps > 0
        
        return 1 if (has_circles or has_rectangles) else 0
    
    def analyze_color_consistency(self, hsv_img):
        """Analyze color consistency across the document"""
        # Calculate color distribution in different regions
        h, w = hsv_img.shape[:2]
        regions = [
            hsv_img[0:h//2, 0:w//2],      # Top-left
            hsv_img[0:h//2, w//2:w],      # Top-right
            hsv_img[h//2:h, 0:w//2],      # Bottom-left
            hsv_img[h//2:h, w//2:w]       # Bottom-right
        ]
        
        # Calculate mean hue and saturation for each region
        region_stats = []
        for region in regions:
            mean_hue = np.mean(region[:, :, 0])
            mean_sat = np.mean(region[:, :, 1])
            region_stats.append([mean_hue, mean_sat])
        
        # Calculate consistency as inverse of variance
        region_stats = np.array(region_stats)
        consistency = 1.0 / (1.0 + np.var(region_stats))
        
        return min(consistency, 1.0)
    
    def analyze_font_consistency(self, gray_img):
        """Analyze font consistency using edge patterns"""
        # Apply edge detection
        edges = cv2.Canny(gray_img, 50, 150)
        
        # Analyze edge density in text regions
        # This is a simplified approach - in practice, you'd use more sophisticated text detection
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Calculate edge pattern consistency
        edge_density = np.sum(dilated) / dilated.size
        
        # Simple metric: consistent fonts should have consistent edge patterns
        # This is very simplified and would need more sophisticated analysis in practice
        consistency = min(edge_density * 10, 1.0)  # Normalize
        
        return consistency
    
    def analyze_text_alignment(self, gray_img):
        """Analyze text alignment using line detection"""
        # Detect horizontal lines (text baselines)
        edges = cv2.Canny(gray_img, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
        
        if lines is None:
            return 0.5  # Default score if no lines detected
        
        # Analyze horizontal line angles
        horizontal_lines = []
        for line in lines:
            rho, theta = line[0]
            if abs(theta) < np.pi/6 or abs(theta - np.pi) < np.pi/6:  # Near horizontal
                horizontal_lines.append(theta)
        
        if not horizontal_lines:
            return 0.5
        
        # Calculate alignment consistency
        angle_variance = np.var(horizontal_lines)
        alignment_score = 1.0 / (1.0 + angle_variance * 100)
        
        return min(alignment_score, 1.0)

# Global instance
document_ai = DocumentIntelligence()

def analyze_document_smart(image_path, document_type='Insurance'):
    """Smart document analysis using ML and OCR"""
    return document_ai.analyze_document_authenticity(image_path, document_type)

def extract_text_smart(image_path):
    """Extract text from document using enhanced OCR"""
    return document_ai.extract_text_from_image(image_path)

def batch_document_analysis(image_paths, document_types=None):
    """Analyze multiple documents in batch"""
    results = []
    
    if document_types is None:
        document_types = ['Insurance'] * len(image_paths)
    
    for i, (img_path, doc_type) in enumerate(zip(image_paths, document_types)):
        try:
            result = analyze_document_smart(img_path, doc_type)
            result['document_id'] = i
            result['document_path'] = img_path
            results.append(result)
        except Exception as e:
            results.append({
                'document_id': i,
                'document_path': img_path,
                'authenticity_score': 1,
                'fraud_probability': 0.9,
                'analysis_results': [f'Processing error: {str(e)}'],
                'recommendations': ['Manual review required']
            })
    
    return results
