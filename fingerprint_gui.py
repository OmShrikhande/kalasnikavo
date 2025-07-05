import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time
from faceOM import find_most_similar  # Import the function from faceOM.py
from oldfingerprintom import compare_fingerprints  # Import the function from oldfingerprintom.py
import os
import subprocess

# === CONFIG ===
FINGERPRINT_DATASET_PATH = r"C:\xampp\htdocs\college project face fingerprint\fingerprtintDataset\altered\Altered easy"
FACIAL_DATASET_PATH = os.path.join(os.getcwd(), "facialDataset/Faces/Faces")

class CombinedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial and Fingerprint Recognition System")
        self.root.attributes("-fullscreen", True)  # Enable full-screen mode
        self.root.configure(bg="#111111")

        # Title Label
        self.title_label = tk.Label(
            root, text="Facial and Fingerprint Recognition System", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="#ffffff"
        )
        self.title_label.pack(pady=20)

        # === Facial Recognition Section ===
        facial_frame = ttk.Frame(root)
        facial_frame.pack(side="left", padx=20, pady=10, fill="both", expand=True)

        ttk.Label(facial_frame, text="Facial Recognition", font=("Arial", 16), background="#1e1e1e", foreground="white").pack(pady=10)

        self.facial_logs_text = tk.Text(
            facial_frame, wrap="word", font=("Consolas", 12), bg="#2b2b3d", fg="#ffffff", insertbackground="#ffffff", relief="flat", height=20
        )
        self.facial_logs_text.pack(fill="both", expand=True)

        self.facial_scrollbar = ttk.Scrollbar(facial_frame, command=self.facial_logs_text.yview)
        self.facial_scrollbar.pack(side="right", fill="y")
        self.facial_logs_text.config(yscrollcommand=self.facial_scrollbar.set)

        self.facial_select_button = ttk.Button(
            facial_frame, text="Select Facial Image", command=self.select_facial_image
        )
        self.facial_select_button.pack(pady=10)

        # === Fingerprint Recognition Section ===
        fingerprint_frame = ttk.Frame(root)
        fingerprint_frame.pack(side="right", padx=20, pady=10, fill="both", expand=True)

        ttk.Label(fingerprint_frame, text="Fingerprint Recognition", font=("Arial", 16), background="#1e1e1e", foreground="white").pack(pady=10)

        self.fingerprint_logs_text = tk.Text(
            fingerprint_frame, wrap="word", font=("Consolas", 12), bg="#2b2b3d", fg="#ffffff", insertbackground="#ffffff", relief="flat", height=20
        )
        self.fingerprint_logs_text.pack(fill="both", expand=True)

        self.fingerprint_scrollbar = ttk.Scrollbar(fingerprint_frame, command=self.fingerprint_logs_text.yview)
        self.fingerprint_scrollbar.pack(side="right", fill="y")
        self.fingerprint_logs_text.config(yscrollcommand=self.fingerprint_scrollbar.set)

        self.fingerprint_select_button = ttk.Button(
            fingerprint_frame, text="Select Fingerprint File", command=self.select_fingerprint_file
        )
        self.fingerprint_select_button.pack(pady=10)

        # === Model Training & Evaluation Section ===
        model_frame = ttk.Frame(root)
        model_frame.pack(side="bottom", padx=20, pady=10, fill="both", expand=True)

        ttk.Label(model_frame, text="Model Training & Evaluation", font=("Arial", 16), background="#1e1e1e", foreground="white").pack(pady=10)

        self.model_logs_text = tk.Text(
            model_frame, wrap="word", font=("Consolas", 12), bg="#2b2b3d", fg="#ffffff", insertbackground="#ffffff", relief="flat", height=12
        )
        self.model_logs_text.pack(fill="both", expand=True)

        self.model_scrollbar = ttk.Scrollbar(model_frame, command=self.model_logs_text.yview)
        self.model_scrollbar.pack(side="right", fill="y")
        self.model_logs_text.config(yscrollcommand=self.model_scrollbar.set)

        self.model_run_button = ttk.Button(
            model_frame, text="Run Model Training & Evaluation", command=self.run_facefingerdev
        )
        self.model_run_button.pack(pady=10)

        # Start Both Processes Button
        self.start_button = ttk.Button(
            root, text="Start Alternating Processes", command=self.start_alternating_processes
        )
        self.start_button.pack(pady=10)

        # Stop Processes Button
        self.stop_button = ttk.Button(
            root, text="Stop Processes", command=self.stop_all_processes
        )
        self.stop_button.pack(pady=10)

        # Exit Full-Screen Button
        self.exit_button = ttk.Button(
            root, text="Exit Full-Screen", command=self.exit_fullscreen
        )
        self.exit_button.pack(pady=10)

        # Variables to store selected files
        self.selected_facial_image = None
        self.selected_fingerprint_file = None
        self.facial_done = False
        self.fingerprint_done = False
        self.stop_processes = False  # Flag to stop processes

    def log_facial(self, message):
        """Log messages to the facial recognition log panel."""
        self.facial_logs_text.insert(tk.END, message + "\n")
        self.facial_logs_text.see(tk.END)

    def log_fingerprint(self, message):
        """Log messages to the fingerprint recognition log panel."""
        self.fingerprint_logs_text.insert(tk.END, message + "\n")
        self.fingerprint_logs_text.see(tk.END)

    def log_model(self, message):
        """Log messages to the model training & evaluation log panel."""
        self.model_logs_text.insert(tk.END, message + "\n")
        self.model_logs_text.see(tk.END)

    def select_facial_image(self):
        """Open a file dialog to select a facial image."""
        image_path = filedialog.askopenfilename(
            title="Select Facial Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if image_path:
            self.selected_facial_image = image_path
            self.log_facial(f"Selected Facial Image: {os.path.basename(image_path)}")

    def select_fingerprint_file(self):
        """Open a file dialog to select a fingerprint file."""
        file_path = filedialog.askopenfilename(
            title="Select Fingerprint File",
            filetypes=[("Bitmap Files", "*.bmp")]
        )
        if file_path:
            self.selected_fingerprint_file = file_path
            self.log_fingerprint(f"Selected Fingerprint File: {os.path.basename(file_path)}")

    def start_alternating_processes(self):
        """Start alternating facial and fingerprint recognition processes."""
        self.stop_processes = False  # Reset the stop flag
        if self.selected_facial_image and self.selected_fingerprint_file:
            threading.Thread(target=self.alternating_processes, daemon=True).start()
        else:
            if not self.selected_facial_image:
                self.log_facial("No facial image selected.")
            if not self.selected_fingerprint_file:
                self.log_fingerprint("No fingerprint file selected.")

    def stop_all_processes(self):
        """Stop all running processes."""
        self.stop_processes = True
        self.log_facial("Stopping all processes...")
        self.log_fingerprint("Stopping all processes...")

    def alternating_processes(self):
        """Alternate between facial and fingerprint recognition processes."""
        while not (self.facial_done and self.fingerprint_done):
            if self.stop_processes:
                self.log_facial("Facial recognition process stopped.")
                self.log_fingerprint("Fingerprint recognition process stopped.")
                break

            if not self.facial_done:
                self.log_facial("Starting facial recognition for 30 seconds...")
                facial_thread = threading.Thread(target=self.run_facial_recognition, daemon=True)
                facial_thread.start()
                facial_thread.join(timeout=30)  # Run for 30 seconds
                if facial_thread.is_alive():
                    self.log_facial("Facial recognition paused after 30 seconds.")
                else:
                    self.facial_done = True
                    self.log_facial("Facial recognition completed.")

            if self.stop_processes:
                self.log_facial("Facial recognition process stopped.")
                self.log_fingerprint("Fingerprint recognition process stopped.")
                break

            if not self.fingerprint_done:
                self.log_fingerprint("Starting fingerprint recognition for 30 seconds...")
                fingerprint_thread = threading.Thread(target=self.run_fingerprint_recognition, daemon=True)
                fingerprint_thread.start()
                fingerprint_thread.join(timeout=30)  # Run for 30 seconds
                if fingerprint_thread.is_alive():
                    self.log_fingerprint("Fingerprint recognition paused after 30 seconds.")
                else:
                    self.fingerprint_done = True
                    self.log_fingerprint("Fingerprint recognition completed.")

            # Add a small delay to prevent the loop from consuming too much CPU
            time.sleep(1)

        if not self.stop_processes:
            # Log final completion
            self.log_facial("Facial recognition process completed.")
            self.log_fingerprint("Fingerprint recognition process completed.")

    def run_facial_recognition(self):
        """Run the facial recognition process."""
        self.log_facial("Running facial recognition...")
        best_match, elapsed_time = find_most_similar(self.selected_facial_image, FACIAL_DATASET_PATH, self.log_facial)
        if best_match:
            self.log_facial(f"Best match: {best_match['Image']} with {best_match['Confidence (%)']}% confidence")
        else:
            self.log_facial("No matching faces found.")
        self.log_facial(f"Time taken for facial recognition: {elapsed_time:.2f} seconds")

    def run_fingerprint_recognition(self):
        """Run the fingerprint recognition process."""
        self.log_fingerprint("Running fingerprint recognition...")

        # Create a progress bar for fingerprint recognition
        progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start()

        try:
            # Pass the progress bar to the compare_fingerprints function
            compare_fingerprints(self.selected_fingerprint_file, None, self.fingerprint_logs_text, progress_bar)
        except Exception as e:
            self.log_fingerprint(f"Error during fingerprint recognition: {e}")
        finally:
            progress_bar.stop()
            progress_bar.destroy()

        self.log_fingerprint("Fingerprint recognition completed.")

    def run_facefingerdev(self):
        """Run facefingerdev.py and show its output in the model log panel."""
        self.model_logs_text.delete(1.0, tk.END)
        self.log_model("Running facefingerdev.py ...")
        def run_script():
            try:
                # Use the selected facial image if available, else no argument
                args = [r".venv\Scripts\python.exe", "facefingerdev.py"]
                if self.selected_facial_image:
                    args.append(self.selected_facial_image)
                process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=os.path.dirname(os.path.abspath(__file__)),
                    universal_newlines=True,
                    bufsize=1
                )
                for line in process.stdout:
                    self.log_model(line.rstrip())
                process.stdout.close()
                process.wait()
                self.log_model("facefingerdev.py finished.")
            except Exception as e:
                self.log_model(f"Error running facefingerdev.py: {e}")
        threading.Thread(target=run_script, daemon=True).start()

    def exit_fullscreen(self):
        """Exit full-screen mode."""
        self.root.attributes("-fullscreen", False)

# Run the GUI

if __name__ == "__main__":
    root = tk.Tk()
    app = CombinedGUI(root)
    root.mainloop()
