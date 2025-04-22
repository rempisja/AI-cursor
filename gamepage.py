import tkinter as tk
from tkinter import ttk
import subprocess

class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")
        # Title
        self.title_label = tk.Label(self,
                                  text="Game Page",
                                  font=("Arial", 20, "bold"),
                                  bg="white")
        self.title_label.pack(pady=20)
        # Rock-Paper-Scissors Button
        self.rps_button = ttk.Button(self,
                                   text="Play Rock-Paper-Scissors",
                                   command=self.start_rps_game)
        self.rps_button.pack(pady=20)
        # Back Button
        self.back_button = ttk.Button(self,
                                    text="Back to Home",
                                    command=self.go_to_home)
        self.back_button.pack(pady=20)
        # Game content will go here
        self.game_content = tk.Label(self,
                                   text="Game content will be displayed here",
                                   font=("Arial", 14),
                                   bg="white")
        self.game_content.pack(pady=20)
    def go_to_home(self):
        self.controller.show_frame("HomePage")
    def start_rps_game(self):
        # Launch the rock-paper-scissors game in a new process
        subprocess.Popen(['python', 'rock-paper-scissors.py'])