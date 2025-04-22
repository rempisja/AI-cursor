# Import required libraries
# cv2 for video capture and image processing
# mediapipe for hand tracking and landmark detection
import cv2 as cv
import mediapipe as mp
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Initialize mediapipe drawing utilities and hand detection model
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

class RockPaperScissorsGame:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors Game")
        self.root.geometry("1200x800")
        # Configure the grid
        self.root.grid_columnconfigure(0, weight=3)  # Camera section
        self.root.grid_columnconfigure(1, weight=1)  # Scoreboard section
        # Top bar frame
        self.top_frame = tk.Frame(self.root, bg='white')
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky='ew', padx=10, pady=5)
        # Logo
        self.logo_label = tk.Label(self.top_frame, text="LOGO", font=("Arial", 24, "bold"), bg='white')
        self.logo_label.pack(side=tk.LEFT, padx=10)
        # Menu button
        self.menu_button = ttk.Button(self.top_frame, text="☰")
        self.menu_button.pack(side=tk.RIGHT, padx=10)
        # Camera frame
        self.camera_frame = tk.Frame(self.root, bg='lightgray')
        self.camera_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        # Camera label for video feed
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack(expand=True, fill='both')
        # Scoreboard frame
        self.scoreboard_frame = tk.Frame(self.root, bg='#A8E6EF')  # Light blue background
        self.scoreboard_frame.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        # Scoreboard title
        self.score_title = tk.Label(self.scoreboard_frame,
                                  text="Scoreboard",
                                  font=("Arial", 20, "bold"),
                                  bg='white')
        self.score_title.pack(pady=10)
        # Score display
        self.score_display = tk.Frame(self.scoreboard_frame, bg='white')
        self.score_display.pack(pady=10, padx=10, fill='x')
        self.p1_score = 0
        self.p2_score = 0
        # Player scores
        self.p1_label = tk.Label(self.score_display,
                                text=f"Player 1: {self.p1_score}",
                                font=("Arial", 16),
                                bg='white')
        self.p1_label.pack(pady=5)
        self.p2_label = tk.Label(self.score_display,
                                text=f"Player 2: {self.p2_score}",
                                font=("Arial", 16),
                                bg='white')
        self.p2_label.pack(pady=5)
        # Game status
        self.status_label = tk.Label(self.scoreboard_frame,
                                   text="Ready?",
                                   font=("Arial", 18),
                                   bg='white')
        self.status_label.pack(pady=20)
        # Initialize MediaPipe
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_drawing_styles = mp.solutions.drawing_styles
        # Initialize video capture
        self.cap = cv.VideoCapture(0)
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        # Game state
        self.clock = 0
        self.p1_move = None
        self.p2_move = None
        # Start the game loop
        self.update_frame()
        self.root.mainloop()
    def getHandMove(self, hand_landmarks):
        landmarks = hand_landmarks.landmark
        # Check if fingers are bent (closed fist for rock)
        fingers_bent = all([landmarks[i].y > landmarks[i-2].y for i in [8,12,16,20]])
        # Check if fingers are spread (paper)
        fingers_spread = all([landmarks[i].y < landmarks[0].y for i in [8,12,16,20]])
        # Check for scissors (index and middle up, others down)
        scissors_position = (landmarks[8].y < landmarks[5].y and
                           landmarks[12].y < landmarks[9].y and
                           landmarks[16].y > landmarks[13].y and
                           landmarks[20].y > landmarks[17].y)
        if fingers_bent:
            return "rock"
        elif scissors_position:
            return "scissors"
        elif fingers_spread:
            return "paper"
        else:
            return None
    def update_frame(self):
        success, frame = self.cap.read()
        if success:
            # Process frame
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = self.hands.process(frame)
            frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
            frame = cv.flip(frame, 1)
            # Game logic
            if 0 <= self.clock <= 20:
                self.status_label.config(text="Ready?")
            elif self.clock < 30:
                self.status_label.config(text="3...")
            elif self.clock < 40:
                self.status_label.config(text="2...")
            elif self.clock < 50:
                self.status_label.config(text="1...")
            elif self.clock < 60:
                self.status_label.config(text="Go!")
            elif self.clock == 60:
                if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
                    self.p1_move = self.getHandMove(results.multi_hand_landmarks[0])
                    self.p2_move = self.getHandMove(results.multi_hand_landmarks[1])
                    self.determine_winner()
            # Convert frame to PhotoImage for tkinter
            image = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            photo = ImageTk.PhotoImage(image=image)
            self.camera_label.config(image=photo)
            self.camera_label.image = photo
            self.clock = (self.clock + 1) % 120
        self.root.after(10, self.update_frame)
    def determine_winner(self):
        if self.p1_move and self.p2_move:
            result_text = f"Player 1: {self.p1_move}\nPlayer 2: {self.p2_move}\n"
            if self.p1_move == self.p2_move:
                result_text += "Tie!"
            elif ((self.p1_move == "rock" and self.p2_move == "scissors") or
                  (self.p1_move == "scissors" and self.p2_move == "paper") or
                  (self.p1_move == "paper" and self.p2_move == "rock")):
                result_text += "Player 1 wins!"
                self.p1_score += 1
                self.p1_label.config(text=f"Player 1: {self.p1_score}")
            else:
                result_text += "Player 2 wins!"
                self.p2_score += 1
                self.p2_label.config(text=f"Player 2: {self.p2_score}")
            self.status_label.config(text=result_text)
    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()

if __name__ == "__main__":
    game = RockPaperScissorsGame()
