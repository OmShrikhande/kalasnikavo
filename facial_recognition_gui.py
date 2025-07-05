from tkinter import Tk, Label, Button, filedialog, Text, Scrollbar, END, Frame
from faceOM import find_most_similar  # Import the function from faceOM.py
import os
import threading  # Import threading for background processing

class FacialRecognitionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Recognition GUI")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2f")  # Dark background

        # Title Label
        self.title_label = Label(
            root, text="Facial Recognition System", font=("Arial", 20, "bold"), bg="#1e1e2f", fg="#ffffff"
        )
        self.title_label.pack(pady=20)

        # Select Image Button
        self.select_image_button = Button(
            root, text="Select Image", command=self.select_image, font=("Arial", 14), bg="#3c3f41", fg="#ffffff", relief="flat"
        )
        self.select_image_button.pack(pady=10)

        # Logs Frame
        self.logs_frame = Frame(root, bg="#1e1e2f")
        self.logs_frame.pack(pady=10, fill="both", expand=True)

        self.logs_text = Text(
            self.logs_frame, wrap="word", font=("Consolas", 12), bg="#2b2b3d", fg="#ffffff", insertbackground="#ffffff", relief="flat"
        )
        self.logs_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = Scrollbar(self.logs_frame, command=self.logs_text.yview, bg="#1e1e2f")
        self.scrollbar.pack(side="right", fill="y")
        self.logs_text.config(yscrollcommand=self.scrollbar.set)

        # Dataset Folder
        self.dataset_folder = os.path.join(os.getcwd(), "facialDataset/Faces/Faces")  # Path to dataset folder
        if not os.path.exists(self.dataset_folder):
            os.makedirs(self.dataset_folder)
            self.log(f"Dataset folder created at: {self.dataset_folder}")
        else:
            self.log(f"Dataset folder found at: {self.dataset_folder}")

    def log(self, message):
        """Log messages to the text area."""
        self.logs_text.insert(END, message + "\n")
        self.logs_text.see(END)

    def select_image(self):
        """Open a file dialog to select an image."""
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if image_path:
            self.log(f"Selected Image: {os.path.basename(image_path)}")  # Show only the image name
            # Run face matching in a separate thread
            threading.Thread(target=self.run_face_matching, args=(image_path,), daemon=True).start()

    def run_face_matching(self, image_path):
        """Run the face matching algorithm and display results."""
        self.log("Starting face matching...")
        best_match, elapsed_time = find_most_similar(image_path, self.dataset_folder, self.log)

        if best_match:
            self.log(f"Best match: {best_match['Image']} with {best_match['Confidence (%)']}% confidence")
        else:
            self.log("No matching faces found.")

        self.log(f"Time taken for scanning: {elapsed_time:.2f} seconds")

# Run the GUI
if __name__ == "__main__":
    root = Tk()
    app = FacialRecognitionGUI(root)
    root.mainloop()