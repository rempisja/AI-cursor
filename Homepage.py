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
        self.logo_label = tk.Label(self.logo_frame, text="", font=("Arial", 16, "bold"), bg="white")
        self.logo_label.grid(row=0, column=0, sticky="w")
        # Menu Button
        self.menu_button = tk.Button(self.logo_frame, text="☰", font=("Arial", 16),
                                   bg="white", bd=0, command=self.toggle_menu)
        self.menu_button.grid(row=0, column=2, sticky="e")
        # Menu Frame (initially hidden)
        self.menu_frame = tk.Frame(self, bg="#A8E6EF", width=200)  # Light blue background
        self.menu_frame.place(x=self.winfo_width(), y=50, width=0, height=300)  # Start with 0 width
        # Make the menu frame keep its width when shown
        self.menu_frame.pack_propagate(False)
        # Menu Options with white background buttons
        self.menu_options = [
            ("Main Menu", lambda: self.controller.show_frame("HomePage")),
            ("Switch\nGame", self.switch_game),
            ("Calibration", self.show_calibration)
        ]
        # Style for menu buttons
        button_style = {
            "font": ("Arial", 14),
            "bg": "white",
            "bd": 1,
            "relief": "solid",
            "width": 15,
            "height": 2
        }
        for i, (text, command) in enumerate(self.menu_options):
            btn = tk.Button(self.menu_frame, text=text, command=command, **button_style)
            btn.pack(pady=10, padx=20)
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
        # Variables for animation
        self.menu_visible = False
        self.animation_running = False
        self.target_width = 200  # Final width of menu
    def init_video_placeholder(self):
        # Create a play button icon in the video frame
        play_icon = tk.Label(self.video_frame,
                           text="▶",
                           font=("Arial", 48),
                           bg="#F0F0F0",
                           fg="#333333")
        play_icon.place(relx=0.5, rely=0.5, anchor="center")
    def toggle_menu(self):
        """Toggle the menu with animation"""
        if self.animation_running:
            return
        self.animation_running = True
        if not self.menu_visible:
            # Show animation
            self.animate_menu(0, self.target_width, True)
        else:
            # Hide animation
            self.animate_menu(self.target_width, 0, False)
    def animate_menu(self, start_width, end_width, showing):
        """Animate the menu sliding"""
        current_width = start_width
        step = (end_width - start_width) / 15  # Divide animation into 15 steps
        def update():
            nonlocal current_width
            current_width += step
            # Check if animation is complete
            if (step > 0 and current_width >= end_width) or \
               (step < 0 and current_width <= end_width):
                current_width = end_width
                self.menu_visible = showing
                self.animation_running = False
                if not showing:
                    self.menu_frame.place_forget()
                return
            # Update menu position and width
            x = self.winfo_width() - current_width
            self.menu_frame.place(x=x, y=50, width=current_width, height=300)
            self.after(10, update)  # Schedule next frame
        # Start animation
        if showing:
            self.menu_frame.place(x=self.winfo_width(), y=50, width=0, height=300)
        update()
    def switch_game(self):
        """Handle game switching"""
        # TODO: Implement game switching logic
        pass
    def show_calibration(self):
        """Show calibration screen"""
        # TODO: Implement calibration screen
        pass
    def start_playing(self):
        self.controller.show_frame("GamePage")

def main():
    app = GestureGameUI()
    app.mainloop()

if __name__ == "__main__":
    main()
