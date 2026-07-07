import tkinter as tk
from tkinter import ttk, messagebox

from scipy.fftpack import shift

def encrypt_caesar(plaintext, shift):
    """Encrypts text by moving characters forward by the shift key."""
    ciphertext = ""
    for char in plaintext:
        if char.isupper():
            cipher_char = chr((ord(char) - 65 + shift) % 26 + 65)
            ciphertext += cipher_char
        elif char.islower():
            cipher_char = chr((ord(char) - 97 + shift) % 26 + 97)
            ciphertext += cipher_char
        else:
            ciphertext += char
    return ciphertext

def decrypt_caesar(ciphertext, shift):
    """Decrypts text by moving characters backward by the shift key."""
    plaintext = ""
    for char in ciphertext:
        if char.isupper():
            plain_char = chr((ord(char) - 65 - shift) % 26 + 65)
            plaintext += plain_char
        elif char.islower():
            plain_char = chr((ord(char) - 97 - shift) % 26 + 97)
            plaintext += plain_char
        else:
            plaintext += char
    return plaintext

class CryptoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DecodeLabs Cryptographic Engine")
        self.root.geometry("550x480")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Header Section
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)
        header_label = ttk.Label(header_frame, text="DECODELABS CRYPTOGRAPHIC ENGINE", font=("Helvetica", 14, "bold"))
        header_label.pack()
        subtitle_label = ttk.Label(header_frame, text="Project 2: Confidentiality Logic", font=("Helvetica", 10, "italic"))
        subtitle_label.pack()
        
        # Input Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text=" 1. Configuration & Input ", padding=15)
        config_frame.pack(fill=tk.X, padx=15, pady=5)
        
        ttk.Label(config_frame, text="Select Shift Key (0-25):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.shift_var = tk.IntVar(value=3)
        self.shift_box = ttk.Spinbox(config_frame, from_=0, to=25, textvariable=self.shift_var, width=5, command=self.process_crypto)
        self.shift_box.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(config_frame, text="Enter Raw Plaintext:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # --- Placeholder Implementation ---
        self.placeholder = "Enter text to encrypt here..."
        
        # Custom styling for placeholder text color
        self.style.configure("Custom.TEntry", foreground="gray")
        
        self.input_entry = ttk.Entry(config_frame, width=45, style="Custom.TEntry")
        self.input_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=10, pady=5)
        
        self.input_entry.insert(0, self.placeholder)
        
        # Bind focus events for the placeholder behavior
        self.input_entry.bind("<FocusIn>", self.clear_placeholder)
        self.input_entry.bind("<FocusOut>", self.restore_placeholder)
        # ----------------------------------
        
        # Direct Action Button
        btn_frame = ttk.Frame(self.root, padding=5)
        btn_frame.pack(fill=tk.X, padx=15)
        self.process_btn = ttk.Button(btn_frame, text="⚙️ Process Dual Cryptography (IPO Cycle)", command=self.process_crypto)
        self.process_btn.pack(fill=tk.X, pady=5)
        
        # Output Interface Frame
        output_frame = ttk.LabelFrame(self.root, text=" 2. Dual Processing Outputs ", padding=15)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        ttk.Label(output_frame, text="🔒 Encrypted Ciphertext Output:").pack(anchor=tk.W)
        self.cipher_text_box = ttk.Entry(output_frame, font=("Consolas", 11), state="readonly")
        self.cipher_text_box.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="🔓 Decrypted Reconstructed Output:").pack(anchor=tk.W, pady=(10, 0))
        self.plain_text_box = ttk.Entry(output_frame, font=("Consolas", 11), state="readonly")
        self.plain_text_box.pack(fill=tk.X, pady=5)
        
        # Footer
        footer_label = ttk.Label(self.root, text="Powered by DecodeLabs | Batch 2026", font=("Helvetica", 8))
        footer_label.pack(side=tk.BOTTOM, pady=5)

    def clear_placeholder(self, event):
        """Removes placeholder text and changes text color to black when user clicks inside."""
        if self.input_entry.get() == self.placeholder:
            self.input_entry.delete(0, tk.END)
            self.style.configure("Custom.TEntry", foreground="black")

    def restore_placeholder(self, event):
        """Restores placeholder text if the entry is left completely empty when clicking away."""
        if not self.input_entry.get().strip():
            self.style.configure("Custom.TEntry", foreground="gray")
            self.input_entry.insert(0, self.placeholder)

    def process_crypto(self):
        try:
            shift = self.shift_var.get()
        except tk.TclError:
            messagebox.showerror("Error", "Shift key must be an integer.")
            return

        raw_input = self.input_entry.get()
        
        # Skip processing if it's just the default placeholder instruction
        if raw_input == self.placeholder:
            return

        # 1. Step forward (Encrypt) [cite: 66, 178]
        encrypted = encrypt_caesar(raw_input, shift)    
        
        # 2. Step backward (Decrypt) [cite: 18]
        decrypted = decrypt_caesar(encrypted, shift)
        
        # Update text widgets cleanly [cite: 18]
        self.cipher_text_box.config(state="normal")
        self.cipher_text_box.delete(0, tk.END)
        self.cipher_text_box.insert(0, encrypted)
        self.cipher_text_box.config(state="readonly")
        
        self.plain_text_box.config(state="normal")
        self.plain_text_box.delete(0, tk.END)
        self.plain_text_box.insert(0, decrypted)
        self.plain_text_box.config(state="readonly")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoGUI(root)
    root.mainloop()