import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import torch
from transformers import ViTImageProcessor, ViTForImageClassification
import time
from datetime import datetime

class AdvancedDriverMonitor:
    def __init__(self):
        # Initialize device
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Initialize MediaPipe
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Load ViT model
        print("Loading ViT model...")
        self.vit_processor = ViTImageProcessor.from_pretrained("trpakov/vit-face-expression")
        self.vit_model = ViTForImageClassification.from_pretrained("trpakov/vit-face-expression").to(self.device)
        
        # Fine-tuned thresholds
        self.EYE_AR_THRESH = 0.25
        self.EYE_AR_CONSEC_FRAMES = 90
        self.YAWN_THRESH = 0.52
        self.YAWN_CONSEC_FRAMES = 100
        self.HAND_FACE_DIST_THRESH = 0.15
        self.MIN_FACE_SIZE = 100
        
        # Counters and states
        self.eye_counter = 0
        self.yawn_counter = 0
        self.blink_counter = 0
        self.hand_near_face_counter = 0
        self.total_blinks = 0
        self.total_yawns = 0
        self.drowsy_periods = 0
        
        # State flags
        self.is_yawning = False
        self.is_drowsy = False
        self.hand_near_face = False
        
        # Time tracking
        self.start_time = time.time()
        self.frame_count = 0
        self.last_blink_time = time.time()
        self.alerts = []
        
        # Create log file
        self.log_file = open(f"driver_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w")

    def log_event(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_file.write(f"{timestamp}: {event}\n")
        self.log_file.flush()

    def calculate_ear(self, eye_points):
        try:
            A = dist.euclidean(eye_points[1], eye_points[5])
            B = dist.euclidean(eye_points[2], eye_points[4])
            C = dist.euclidean(eye_points[0], eye_points[3])
            return (A + B) / (2.0 * C)
        except:
            return 1.0

    def calculate_mar(self, mouth_points):
        try:
            A = dist.euclidean(mouth_points[2], mouth_points[6])
            B = dist.euclidean(mouth_points[3], mouth_points[5])
            C = dist.euclidean(mouth_points[0], mouth_points[4])
            return (A + B) / (2.0 * C)
        except:
            return 0.0

    def detect_hand_over_face(self, hand_landmarks, face_landmarks, frame_shape):
        if not hand_landmarks or not face_landmarks:
            return False
            
        face_points = np.array([[p.x * frame_shape[1], p.y * frame_shape[0]] 
                               for p in face_landmarks.landmark])
        hand_points = np.array([[p.x * frame_shape[1], p.y * frame_shape[0]] 
                               for p in hand_landmarks.landmark])
        
        face_center = np.mean(face_points, axis=0)
        hand_center = np.mean(hand_points, axis=0)
        
        distance = np.linalg.norm(face_center - hand_center)
        normalized_distance = distance / frame_shape[1]
        
        return normalized_distance < self.HAND_FACE_DIST_THRESH

    def draw_status_panel(self, frame, metrics):
        # Create semi-transparent overlay
        overlay = frame.copy()
        panel_height = len(metrics) * 30 + 20
        cv2.rectangle(overlay, (10, 10), (300, panel_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Draw metrics
        for i, (label, value) in enumerate(metrics):
            text = f"{label}: {value}"
            cv2.putText(frame, text, (20, 35 + i*25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    def process_frame(self, frame):
        self.frame_count += 1
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results_face = self.face_mesh.process(rgb_frame)
        results_hands = self.hands.process(rgb_frame)
        
        self.alerts = []
        metrics = []
        face_detected = False
        
        if results_face.multi_face_landmarks:
            face_detected = True
            for face_landmarks in results_face.multi_face_landmarks:
                # Draw facial landmarks
                self.mp_drawing.draw_landmarks(
                    frame, face_landmarks, self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )
                
                # Get eye landmarks
                left_eye = np.array([[face_landmarks.landmark[p].x * frame.shape[1],
                                    face_landmarks.landmark[p].y * frame.shape[0]]
                                   for p in [33, 160, 158, 133, 153, 144]])
                right_eye = np.array([[face_landmarks.landmark[p].x * frame.shape[1],
                                     face_landmarks.landmark[p].y * frame.shape[0]]
                                    for p in [362, 385, 387, 263, 373, 380]])
                # Get mouth landmarks
                mouth = np.array([[face_landmarks.landmark[p].x * frame.shape[1],
                                 face_landmarks.landmark[p].y * frame.shape[0]]
                                for p in [61, 62, 63, 64, 65, 66, 67]])
                
                left_ear = self.calculate_ear(left_eye)
                right_ear = self.calculate_ear(right_eye)
                ear = (left_ear + right_ear) / 2.0
                mar = self.calculate_mar(mouth)
                metrics.extend([
                    ("EAR", f"{ear:.2f}"),
                    ("MAR", f"{mar:.2f}"),
                    ("Blinks", self.total_blinks),
                    ("Yawns", self.total_yawns),
                    ("Drowsy Events", self.drowsy_periods)
                ])
                
                # Detect drowsiness
                if ear < self.EYE_AR_THRESH:
                    self.eye_counter += 1
                    if self.eye_counter >= self.EYE_AR_CONSEC_FRAMES:
                        if not self.is_drowsy:
                            self.drowsy_periods += 1
                            self.is_drowsy = True
                        self.alerts.append("DROWSINESS ALERT!")
                        self.log_event("Drowsiness detected")
                else:
                    if self.eye_counter >= 3:  # Minimum frames for a blink
                        self.total_blinks += 1
                    self.eye_counter = 0
                    self.is_drowsy = False
                
                # Detect yawning
                if mar > self.YAWN_THRESH:
                    self.yawn_counter += 1
                    if self.yawn_counter >= self.YAWN_CONSEC_FRAMES:
                        if not self.is_yawning:
                            self.total_yawns += 1
                            self.is_yawning = True
                        self.alerts.append("YAWNING DETECTED!")
                        self.log_event("Yawning detected")
                else:
                    self.yawn_counter = 0
                    self.is_yawning = False
                
                # Check for hands near face
                if results_hands.multi_hand_landmarks:
                    for hand_landmarks in results_hands.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        if self.detect_hand_over_face(hand_landmarks, face_landmarks, frame.shape):
                            if not self.hand_near_face:
                                self.hand_near_face = True
                                self.log_event("Hand near face detected")
                            self.alerts.append("HAND OVER FACE!")
                        else:
                            self.hand_near_face = False
                
                # Combined drowsiness indicators
                if self.is_drowsy and self.is_yawning:
                    self.alerts.append("SEVERE DROWSINESS WARNING!")
                    self.log_event("Severe drowsiness detected")
        
        # Clear states if no face detected
        if not face_detected:
            self.alerts = []
            self.eye_counter = 0
            self.yawn_counter = 0
            self.is_drowsy = False
            self.is_yawning = False
            self.hand_near_face = False
        
        # Draw status panel
        self.draw_status_panel(frame, metrics)
        
        # Display alerts
        for i, alert in enumerate(self.alerts):
            cv2.putText(frame, alert, (10, frame.shape[0] - 30 - i*30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        # Display FPS
        fps = self.frame_count / (time.time() - self.start_time)
        cv2.putText(frame, f"FPS: {fps:.1f}", (frame.shape[1] - 120, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame

    def start_monitoring(self, source=0):
    # Initialize camera with specific settings
        cap = cv2.VideoCapture(source)

        # Set camera properties
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        cap.set(cv2.CAP_PROP_FPS,30)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

        # Verify camera settings
        actual_fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Camera FPS: {actual_fps}")

        # Enable CUDA for OpenCV if available
        if cv2.cuda.getCudaEnabledDeviceCount() > 0:
            print("CUDA enabled for video processing")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Convert frame to GPU if CUDA is available
            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                gpu_frame = cv2.cuda_GpuMat()
                gpu_frame.upload(frame)
                # Process frame on GPU
                processed_frame = self.process_frame(gpu_frame.download())
            else:
                processed_frame = self.process_frame(frame)

            cv2.imshow("Driver Monitoring System", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    monitor = AdvancedDriverMonitor()
    monitor.start_monitoring()