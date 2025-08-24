import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import random
import os

class ImageEncryptionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Image Encryption Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")
        
        # Variables
        self.original_image = None
        self.encrypted_image = None
        self.image_path = None
        self.encryption_key = random.randint(1000, 9999)
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = tk.Label(main_frame, text="🔐 Advanced Image Encryption Tool", 
                              font=("Arial", 24, "bold"), fg="white", bg="#2c3e50")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E))
        
        ttk.Label(file_frame, text="Select Image:").grid(row=0, column=0, padx=(0, 10))
        self.file_entry = ttk.Entry(file_frame, width=50)
        self.file_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(file_frame, text="Browse", command=self.browse_image).grid(row=0, column=2)
        ttk.Button(file_frame, text="Load", command=self.load_image).grid(row=0, column=3, padx=(10, 0))
        
        # Encryption options
        options_frame = ttk.LabelFrame(main_frame, text="Encryption Options", padding="10")
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.N, tk.S), padx=(0, 10))
        
        # Encryption method
        ttk.Label(options_frame, text="Encryption Method:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.method_var = tk.StringVar(value="xor")
        methods = [("XOR Operation", "xor"), ("Pixel Swapping", "swap"), 
                  ("Add/Subtract", "addsub"), ("Bit Shifting", "bitshift")]
        
        for i, (text, value) in enumerate(methods):
            ttk.Radiobutton(options_frame, text=text, variable=self.method_var, 
                           value=value).grid(row=i+1, column=0, sticky=tk.W, pady=2)
        
        # Key input
        ttk.Label(options_frame, text="Encryption Key:").grid(row=5, column=0, sticky=tk.W, pady=(20, 5))
        self.key_var = tk.StringVar(value=str(self.encryption_key))
        ttk.Entry(options_frame, textvariable=self.key_var, width=15).grid(row=6, column=0, sticky=tk.W)
        
        # Operation buttons
        button_frame = ttk.Frame(options_frame)
        button_frame.grid(row=7, column=0, pady=(20, 0), sticky=tk.W)
        
        ttk.Button(button_frame, text="Encrypt", command=self.encrypt_image, 
                  style="Accent.TButton").grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Decrypt", command=self.decrypt_image).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Reset", command=self.reset_image).grid(row=0, column=2)
        
        # Save buttons
        save_frame = ttk.Frame(options_frame)
        save_frame.grid(row=8, column=0, pady=(20, 0), sticky=tk.W)
        
        ttk.Button(save_frame, text="Save Encrypted", command=self.save_encrypted).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(save_frame, text="Save Decrypted", command=self.save_decrypted).grid(row=0, column=1)
        
        # Image display area
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Original image
        orig_frame = ttk.LabelFrame(display_frame, text="Original Image")
        orig_frame.grid(row=0, column=0, padx=(0, 10), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.orig_canvas = tk.Canvas(orig_frame, width=400, height=300, bg="#34495e")
        self.orig_canvas.pack(padx=10, pady=10)
        ttk.Label(orig_frame, text="No image loaded").pack(pady=50)
        
        # Encrypted image
        enc_frame = ttk.LabelFrame(display_frame, text="Encrypted Image")
        enc_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.enc_canvas = tk.Canvas(enc_frame, width=400, height=300, bg="#34495e")
        self.enc_canvas.pack(padx=10, pady=10)
        ttk.Label(enc_frame, text="No encrypted image").pack(pady=50)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        style = ttk.Style()
        style.configure("Accent.TButton", background="#3498db", foreground="white")
        
    def browse_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            
    def load_image(self):
        file_path = self.file_entry.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid image file")
            return
            
        try:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.orig_canvas)
            self.status_var.set(f"Image loaded: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def display_image(self, image, canvas):
        # Clear canvas
        canvas.delete("all")
        
        # Resize image for display
        display_image = image.copy()
        display_image.thumbnail((380, 280))
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(display_image)
        
        # Display on canvas
        canvas.create_image(200, 150, image=photo)
        canvas.image = photo  # Keep reference
        
    def encrypt_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Please load an image first")
            return
            
        try:
            key = int(self.key_var.get())
            method = self.method_var.get()
            
            # Convert image to numpy array
            img_array = np.array(self.original_image)
            
            if method == "xor":
                encrypted_array = self.xor_encryption(img_array, key)
            elif method == "swap":
                encrypted_array = self.pixel_swapping(img_array, key)
            elif method == "addsub":
                encrypted_array = self.add_subtract_encryption(img_array, key)
            elif method == "bitshift":
                encrypted_array = self.bit_shift_encryption(img_array, key)
            else:
                encrypted_array = img_array
                
            # Convert back to PIL Image
            self.encrypted_image = Image.fromarray(encrypted_array)
            self.display_image(self.encrypted_image, self.enc_canvas)
            self.status_var.set(f"Image encrypted using {method} method")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric key")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            
    def decrypt_image(self):
        if self.encrypted_image is None:
            messagebox.showerror("Error", "No encrypted image to decrypt")
            return
            
        try:
            key = int(self.key_var.get())
            method = self.method_var.get()
            
            # Convert encrypted image to numpy array
            enc_array = np.array(self.encrypted_image)
            
            if method == "xor":
                decrypted_array = self.xor_encryption(enc_array, key)  # XOR is symmetric
            elif method == "swap":
                decrypted_array = self.pixel_swapping(enc_array, key)  # Swapping is symmetric
            elif method == "addsub":
                decrypted_array = self.add_subtract_decryption(enc_array, key)
            elif method == "bitshift":
                decrypted_array = self.bit_shift_decryption(enc_array, key)
            else:
                decrypted_array = enc_array
                
            # Display decrypted image
            decrypted_image = Image.fromarray(decrypted_array)
            self.display_image(decrypted_image, self.enc_canvas)
            self.status_var.set(f"Image decrypted using {method} method")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric key")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {str(e)}")
            
    def xor_encryption(self, img_array, key):
        """XOR each pixel with the key"""
        encrypted = img_array.copy()
        encrypted = encrypted ^ (key % 256)
        return np.clip(encrypted, 0, 255).astype(np.uint8)
    
    def pixel_swapping(self, img_array, key):
        """Swap pixels based on the key"""
        encrypted = img_array.copy()
        random.seed(key)
        
        if len(encrypted.shape) == 3:  # Color image
            h, w, c = encrypted.shape
            for i in range(h):
                for j in range(w):
                    swap_i = random.randint(0, h-1)
                    swap_j = random.randint(0, w-1)
                    encrypted[i, j], encrypted[swap_i, swap_j] = encrypted[swap_i, swap_j], encrypted[i, j].copy()
        else:  # Grayscale
            h, w = encrypted.shape
            for i in range(h):
                for j in range(w):
                    swap_i = random.randint(0, h-1)
                    swap_j = random.randint(0, w-1)
                    encrypted[i, j], encrypted[swap_i, swap_j] = encrypted[swap_i, swap_j], encrypted[i, j]
                    
        return encrypted
    
    def add_subtract_encryption(self, img_array, key):
        """Add key to each pixel (mod 256)"""
        encrypted = img_array.copy()
        encrypted = (encrypted + key) % 256
        return encrypted.astype(np.uint8)
    
    def add_subtract_decryption(self, img_array, key):
        """Subtract key from each pixel (mod 256)"""
        decrypted = img_array.copy()
        decrypted = (decrypted - key) % 256
        return decrypted.astype(np.uint8)
    
    def bit_shift_encryption(self, img_array, key):
        """Bit shift encryption"""
        encrypted = img_array.copy()
        shift_amount = key % 7 + 1
        encrypted = (encrypted << shift_amount) | (encrypted >> (8 - shift_amount))
        return encrypted.astype(np.uint8)
    
    def bit_shift_decryption(self, img_array, key):
        """Bit shift decryption"""
        decrypted = img_array.copy()
        shift_amount = key % 7 + 1
        decrypted = (decrypted >> shift_amount) | (decrypted << (8 - shift_amount))
        return decrypted.astype(np.uint8)
    
    def reset_image(self):
        """Reset to original image"""
        if self.original_image:
            self.display_image(self.original_image, self.orig_canvas)
        self.enc_canvas.delete("all")
        ttk.Label(self.enc_canvas.master, text="No encrypted image").pack(pady=50)
        self.encrypted_image = None
        self.status_var.set("Image reset")
        
    def save_encrypted(self):
        if self.encrypted_image is None:
            messagebox.showerror("Error", "No encrypted image to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.encrypted_image.save(file_path)
                self.status_var.set(f"Encrypted image saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Encrypted image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                
    def save_decrypted(self):
        if self.original_image is None:
            messagebox.showerror("Error", "No original image to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.original_image.save(file_path)
                self.status_var.set(f"Original image saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Original image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

def main():
    root = tk.Tk()
    app = ImageEncryptionTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()


