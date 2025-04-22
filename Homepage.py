import tkinter as tk
from tkinter import ttk
from gamepage import GamePage

class GestureGameUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PlayWithGestures")
        self.geometry("800x600")
        # Configure the main window
        self.configure(bg="white")
        # Create container for frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # Dictionary to hold all frames
        self.frames = {}
        # Create and store frames
        for F in (HomePage, GamePage):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # Show the home page initially
        self.show_frame("HomePage")
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="white")
        # Configure the main window
        self.grid_columnconfigure(0, weight=1)
        # Logo Frame
        self.logo_frame = tk.Frame(self, bg="white")
        self.logo_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.logo_frame.grid_columnconfigure(0, weight=1)
        self.logo_frame.grid_columnconfigure(2, weight=1)
        # Logo Label
        self.logo_label = tk.Label(self.logo_frame, text="LOGO", font=("Arial", 16, "bold"), bg="white")
        self.logo_label.grid(row=0, column=0, sticky="w")
        # Menu Button
        self.menu_button = tk.Button(self.logo_frame, text="☰", font=("Arial", 16),
                                   bg="white", bd=0, command=self.toggle_menu)
        self.menu_button.grid(row=0, column=2, sticky="e")
        # Title
        self.title_label = tk.Label(self,
                                  text='"PlayWithGestures - Control Games With Your Hands!"',
                                  font=("Arial", 20, "bold"),
                                  bg="white")
        self.title_label.grid(row=1, column=0, pady=20)
        # Video Frame
        self.video_frame = tk.Frame(self, bg="#F0F0F0", width=640, height=480)
        self.video_frame.grid(row=2, column=0, pady=20)
        self.video_frame.grid_propagate(False)
        # Play Button
        self.play_button_style = ttk.Style()
        self.play_button_style.configure("Custom.TButton",
                                       font=("Arial", 14),
                                       padding=10)
        self.play_button = ttk.Button(self,
                                    text="Start Playing",
                                    style="Custom.TButton",
                                    command=self.start_playing)
        self.play_button.grid(row=3, column=0, pady=20)
        # Initialize video placeholder
        self.init_video_placeholder()
    def init_video_placeholder(self):
        # Create a play button icon in the video frame
        play_icon = tk.Label(self.video_frame,
                           text="▶",
                           font=("Arial", 48),
                           bg="#F0F0F0",
                           fg="#333333")
        play_icon.place(relx=0.5, rely=0.5, anchor="center")
    def toggle_menu(self):
        # TODO: Implement menu toggle functionality
        pass
    def start_playing(self):
        self.controller.show_frame("GamePage")

def main():
    app = GestureGameUI()
    app.mainloop()

if __name__ == "__main__":
    main()
