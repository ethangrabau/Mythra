import tkinter as tk
from PIL import Image, ImageTk

def display_image(image_path):
    root = tk.Tk()
    root.title("Image Display Test")
    root.geometry("800x600")  # Set window size

    # Load and resize the image
    img = Image.open(image_path)
    img = img.resize((800, 600), Image.Resampling.LANCZOS)  # Resize the image to fit the window
    img_tk = ImageTk.PhotoImage(img)

    # Create a canvas and display the image
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

    # Add an Exit button on top of the image
    exit_button = tk.Button(root, text="Exit", command=root.quit)
    exit_button.place(relx=0.9, rely=0.05)  # Position at the top-right

    root.mainloop()

# Test the function with your image path
display_image("/Users/ethangrabau/Documents/SampleScreenshot.png")
