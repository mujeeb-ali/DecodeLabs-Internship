import string
import customtkinter as ctk

# Set the theme and color profile
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")  

class PasswordCheckerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Password Shield")
        self.geometry("460x420")
        self.resizable(False, False)

        # Track whether password visibility is ON or OFF
        self.password_visible = False

        # Title Label
        self.title_label = ctk.CTkLabel(
            self, text="Password Strength Analyzer", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(25, 20))

        # Password Input Header
        self.entry_label = ctk.CTkLabel(self, text="Enter your password:", font=ctk.CTkFont(size=13))
        self.entry_label.pack(anchor="w", padx=40)
        
        # --- CLEAN SIDE-BY-SIDE LAYOUT ---
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(padx=40, pady=(5, 15))

        # Password Entry Field (Explicitly wide and comfortable)
        self.password_entry = ctk.CTkEntry(
            self.input_frame, width=320, height=40, placeholder_text="Type password here...", show="*",
        )
        self.password_entry.pack(side="left", padx=(0, 10))
        self.password_entry.bind("<KeyRelease>", self.evaluate_password)

        # Eye Toggle Button (Explicitly fixed structural width)
        self.eye_button = ctk.CTkButton(
            self.input_frame, text="👁️", width=50, height=40, 
            font=ctk.CTkFont(size=16), command=self.toggle_password_visibility
        )
        self.eye_button.pack(side="right")
        # ---------------------------------------------------------------------

        # Visual Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self, width=380, height=8)
        self.progress_bar.set(0) 
        self.progress_bar.pack(pady=(0, 10))

        # Text Output for Strength Status
        self.status_label = ctk.CTkLabel(
            self, text="Status: Waiting for input...", font=ctk.CTkFont(size=15, weight="bold"), text_color="gray"
        )
        self.status_label.pack(pady=(5, 15))

        # Scrollable Feedback Box
        self.feedback_box = ctk.CTkTextbox(
            self, width=380, height=140, font=ctk.CTkFont(size=12), corner_radius=8, border_width=1
        )
        self.feedback_box.pack(pady=(0, 20))
        self.initialize_feedback()

    def toggle_password_visibility(self):
        """Toggles masking characters cleanly using predefined static widths."""
        if self.password_visible:
            self.password_entry.configure(show="*")
            self.eye_button.configure(text=" 👁️")
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.eye_button.configure(text=" 🔒")  
            self.password_visible = True

    def initialize_feedback(self):
        """Initializes the checklist state."""
        self.feedback_box.configure(state="normal")
        self.feedback_box.delete("1.0", ctk.END)
        initial_tips = (
            "⚠️ Requirements Checklist:\n\n"
            "❌ Minimum 8 characters (12+ preferred)\n"
            "❌ At least one uppercase letter (A-Z)\n"
            "❌ At least one number (0-9)\n"
            "❌ At least one special symbol (!, @, #, etc.)"
        )
        self.feedback_box.insert("1.0", initial_tips)
        self.feedback_box.configure(state="disabled")

    def evaluate_password(self, event=None):
        password = self.password_entry.get()

        if not password:
            self.progress_bar.set(0)
            self.progress_bar.configure(progress_color="#3a7ebf") 
            self.status_label.configure(text="Status: Waiting for input...", text_color="gray")
            self.initialize_feedback()
            return

        length = len(password)
        has_upper = any(char.isupper() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_symbol = any(char in string.punctuation for char in password)

        checklist = ["⚠️ Requirements Checklist:\n"]
        score = 0

        if length >= 8:
            checklist.append("✅ Minimum 8 characters" + (" (Excellent length! 🎉)" if length >= 12 else ""))
            score += 1
            if length >= 12: 
                score += 1
        else:
            checklist.append("❌ Minimum 8 characters")

        checklist.append("✅ At least one uppercase letter (A-Z)" if has_upper else "❌ At least one uppercase letter (A-Z)")
        if has_upper: score += 1

        checklist.append("✅ At least one number (0-9)" if has_digit else "❌ At least one number (0-9)")
        if has_digit: score += 1

        checklist.append("✅ At least one special symbol (!, @, #, etc.)" if has_symbol else "❌ At least one special symbol (!, @, #, etc.)")
        if has_symbol: score += 1

        progress_value = score / 5.0
        self.progress_bar.set(progress_value)

        if score <= 2:
            self.status_label.configure(text="Strength: WEAK ❌", text_color="#ff4757")
            self.progress_bar.configure(progress_color="#ff4757")  
        elif score <= 4:
            self.status_label.configure(text="Strength: MEDIUM 😐", text_color="#ffa502")
            self.progress_bar.configure(progress_color="#ffa502")  
        else:
            self.status_label.configure(text="Strength: STRONG 💪", text_color="#2ed573")
            self.progress_bar.configure(progress_color="#2ed573")  

        self.feedback_box.configure(state="normal")
        self.feedback_box.delete("1.0", ctk.END)
        self.feedback_box.insert("1.0", "\n".join(checklist))
        self.feedback_box.configure(state="disabled")

if __name__ == "__main__":
    app = PasswordCheckerApp()
    app.mainloop()