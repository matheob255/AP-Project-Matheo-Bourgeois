import cv2
import tkinter as tk
import os
import random
from tkinter import filedialog, colorchooser, simpledialog, messagebox, Label, Button, Canvas
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageEnhance, ImageGrab

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set the window title
        self.title('Avatar Creator')
        # Set the size
        self.geometry('758x717')
        
        # Initialize the 5 pages
        self.frames = {}
        for F in (HomePage, AvatarCreationPage, AvatarFromImage, AvatarCustomizationPage, RandomAvatar):
            frame = F(self) # Create the frame
            self.frames[F] = frame # Store the frame in the frames dictionary
            frame.grid(row=0, column=0, sticky="nsew") # Grid the frame to the window
            frame.configure(bg='lightslateblue')  # Set the background color to light slate blue

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont] # Get the frame from the frames dictionary
        frame.tkraise() # Raise the frame to the front

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='lightskyblue')  # Set the background color

        # Create a border frame with a different background color
        border_frame = tk.Frame(self, bg='lightskyblue', width=1000, height=1000)
        border_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Load and display the logo image at the top of the page
        self.logo_image = tk.PhotoImage(file="LogoEgoMatic.png")
        logo_label = tk.Label(border_frame, image=self.logo_image, bg='lightskyblue')
        logo_label.pack(pady=(10, 0))

        # Add content inside the border frame
        tk.Label(border_frame, text="EGOMATIC", font=('Impact', 45), bg='lightskyblue', fg='lightslateblue').pack(pady=(0,20))

        # Button to start creating an avatar
        tk.Button(border_frame, text="CREATE YOUR AVATAR", command=lambda: parent.show_frame(AvatarCreationPage), font=('Garamond', 30, "bold"), fg='slateblue', bd=0, highlightthickness=0, width=35, height=3).pack(pady=30)
        
        # Separator Line
        separator = tk.Frame(border_frame, height=2, bg='lightslateblue', bd=0)
        separator.pack(fill='x', padx=20, pady=(15, 15))
        
        # Explanation text about the platform
        explanation_text = (
            "Welcome to EGOMATIC, your ultimate avatar creation platform.\n\n"
            "Here, you can design personalized avatars to represent you in virtual spaces. "
            "Choose from a wide range of features like skin tone, hair style, eyes, and more to create your unique digital representation.\n\n"
            "Let's get started!"
        )
        tk.Label(border_frame, text=explanation_text, font=('Garamond', 17), bg='lightskyblue', fg='lightslateblue', wraplength=460, justify='left').pack(pady=30)

class AvatarCreationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='lightskyblue')

        # Border Frame
        border_frame = tk.Frame(self, bg='lightskyblue', bd=10)  # The bd parameter is used to create a padding that acts as a border.
        border_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Interior Frame that will hold the content, contrasting with the border color
        content_frame = tk.Frame(border_frame, bg='lightskyblue', bd=0)
        content_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Add a label to the content frame
        tk.Label(content_frame, text="HOW DO YOU WANT TO CREATE YOUR AVATAR ?", font=('Impact', 36), bg='lightskyblue', fg='lightslateblue').pack(pady=20)

        # 1st button to create the avatar from an image
        tk.Button(content_frame, text="FROM YOUR OWN IMAGE", command=lambda: parent.show_frame(AvatarFromImage), font = ('Garamond', 24), fg='slateblue', bd = 0, highlightthickness = 0, width = 32, height = 2).pack(pady=(45, 0))
        
        # Add an explanation text label below the 1st button
        explanation_text = ("\u2191\nClick to create your own Avatar from a portrait picture")
        tk.Label(content_frame, text=explanation_text, font=('Garamond', 16), bg='lightskyblue', fg='lightslateblue', justify='center').pack(pady=0)
        
        # 2nd button to create the avatar from scratch
        tk.Button(content_frame, text="FROM SCRATCH", command=lambda: parent.show_frame(AvatarCustomizationPage), font = ('Garamond', 24), fg='slateblue', bd = 0, highlightthickness = 0, width = 32, height = 2).pack(pady=(45, 0))
        
        # Add an explanation text label below the 2nd button
        explanation_text = ("\u2191\nClick to create your Avatar from zero")
        tk.Label(content_frame, text=explanation_text, font=('Garamond', 16), bg='lightskyblue', fg='lightslateblue', justify='center').pack(pady=0)

        # 3rd button to create a random avatar
        tk.Button(content_frame, text="RANDOM AVATAR", command=lambda: parent.show_frame(RandomAvatar), font = ('Garamond', 24), fg='slateblue', bd = 0, highlightthickness = 0, width = 32, height = 2).pack(pady=(45, 0))
        
        # Add an explanation text label below the 3rd button
        explanation_text = ("\u2191\nClick to generate randomly your Avatar")
        tk.Label(content_frame, text=explanation_text, font=('Garamond', 16), bg='lightskyblue', fg='lightslateblue', justify='center').pack(pady=0)

        # Back button to return to the home page
        tk.Button(content_frame, text="\u2190", command=lambda: parent.show_frame(HomePage), font = ('Garamond', 24), fg='slateblue', bd = 0, highlightthickness = 0, width = 15, height = 1).pack(pady=40)

class AvatarFromImage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='light blue')
        self.parent = parent

        # Border Frame
        border_frame = tk.Frame(self, bg='lightskyblue', bd=10)
        border_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Interior Frame that will hold the content, contrasting with the border color
        content_frame = tk.Frame(border_frame, bg='lightskyblue', bd=0)
        content_frame.pack(padx=10, pady=10, fill='both', expand=True)

        # Button to upload an image
        self.upload_button = Button(content_frame, text="Upload Image", command=self.upload_image, font = ('Garamond', 18), fg='slateblue', bd = 0, highlightthickness = 0, width = 30, height = 2)
        self.upload_button.grid(row=0, column=0, pady=10)

        # Canvas to display the image
        self.canvas = Canvas(content_frame, width=200, height=200, bg='white')
        self.canvas.grid(row=1, column=0, padx=70, pady=20)
        
        # Button to apply a cartoon effect
        self.filter_button = Button(content_frame, text="Create your Avatar", command=self.apply_filter, font = ('Garamond', 18), fg='slateblue', bd = 0, highlightthickness = 0, width = 30, height = 2)
        self.filter_button.grid(row=2, column=0, padx=70, pady=20)

        # Separator Line
        separator = tk.Frame(content_frame, height=3, bg='lightslateblue', bd=0)
        separator.grid(row=3, column=0, padx=70, pady=20, sticky='ew')

        # Button to save the avatar
        self.save_button = Button(content_frame, text="Download Avatar", command=self.save_image, font=('Garamond', 18), fg='slateblue', bd=0, highlightthickness=0, width=20, height=2)
        self.save_button.grid(row=4, column=0, padx=70, pady=20)

        # Back button to return to the avatar creation page
        self.back_button = Button(content_frame, text="\u2190", command=lambda: parent.show_frame(AvatarCreationPage), font = ('Garamond', 18), fg='slateblue', bd = 0, highlightthickness = 0, width = 5, height = 1)
        self.back_button.grid(row=5, column=0, padx=70, pady=20)

        # Explanation text about the uploaded image
        explanation_text = ("\u2190 Make sure that a face is visible")
        tk.Label(content_frame, text=explanation_text, font=('Garamond', 17), bg='lightskyblue', fg='lightslateblue', justify='left').grid(row=0, column=1, padx=0)

        # Explanation text about the cartoon effect
        explanation_text = ("\u2190 Click to apply a cartoon effect")
        tk.Label(content_frame, text=explanation_text, font=('Garamond', 17), bg='lightskyblue', fg='lightslateblue', justify='left').grid(row=2, column=1, padx=0)

        self.image_path = None
        self.original_image = None
        self.tk_image = None

    def upload_image(self):
        # Open a file dialog to select an image, and display it on the canvas
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.process_image()

    def process_image(self):
        # Load image with OpenCV
        image = cv2.imread(self.image_path)

         # Convert to grayscale for detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load the face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Check if a face is detected
        if len(faces) == 0:
            print("No face detected.")
            return

        # Focus on the first detected face
        for (x, y, w, h) in faces:
            # Extend the rectangle upwards by 40% of the height to include hair
            extension_up = int(h * 0.40)
            y = max(0, y - extension_up)  # Make sure the new y is not out of the image
            # Extend the rectangle downwards by 20% of the height
            extension_down = int(h * 0.20)
    
            # Ensure the new height doesn't go past the image's bottom
            if y + h + extension_down > image.shape[0]:
                extension_down = image.shape[0] - (y + h)

            # Extend the rectangle leftwards and rightwards by 20% of the width
            extension_left = int(w * 0.20)
            x = max(0, x - extension_left)  # Ensure the new x is not out of the image
            extension_right = int(w * 0.20)
            if x + w + extension_right > image.shape[1]:
                extension_right = image.shape[1] - (x + w)
            
            # Increase the height and width to include the extended regions
            h += extension_up + extension_down
            w += extension_left + extension_right

            face_image = image[y:y+h, x:x+w]
            break

        # Convert back to PIL image and resize to fit the canvas
        self.original_image = Image.fromarray(cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB))
        self.original_image.thumbnail((200, 200))
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.canvas.create_image(100, 100, image=self.tk_image)

        # Store the processed image for saving
        self.processed_image = self.original_image

    def display_image(self):
        # Display the image on the canvas
        self.original_image = Image.open(self.image_path)
        self.original_image.thumbnail((200, 200))  # Resize to fit the canvas
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.canvas.create_image(100, 100, image=self.tk_image)  # Center the image

    def apply_filter(self):
        # Apply a stylized filter to the image and display it on the canvas
        if self.original_image:
            img = self.original_image.convert('RGB')

            # Apply a bilateral filter to reduce noise and preserve edges
            img = img.filter(ImageFilter.ModeFilter(5))  # Adjust size to fine-tune smoothing

            # Convert to grayscale and find edges for a sketch-like effect
            edges = img.convert('L').filter(ImageFilter.FIND_EDGES)
            edges = edges.filter(ImageFilter.EDGE_ENHANCE)

            # Invert edges for a sketch-like effect
            edges = ImageOps.invert(edges)

            # Merge edges back into the image with reduced opacity for soft edge emphasis
            img = Image.blend(img, edges.convert('RGB'), alpha=0.15)  # Soften the edge blending

            # Reduce colors to enhance the cartoon effect
            img = img.quantize(colors=64, method=Image.MEDIANCUT)

            # Increase contrast to make the cartoon more vibrant
            img = img.convert('RGB')  # Convert image to RGB mode
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)

            # Sharpen to enhance details lightly
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.2)

            # Resize to fit the canvas and convert to a format Tkinter can use
            img.thumbnail((200, 200))
            self.processed_image = img  # Store the processed image
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(100, 100, image=self.tk_image)

    def save_image(self):
        # Saves the filtered image to a PNG file
        if hasattr(self, 'processed_image'):  # Check if the processed image exists
            file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                    filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.processed_image.save(file_path)  # Save the processed image
                print(f"Processed image saved as {file_path}")
            else:
                print("Save operation cancelled.")
        else:
            print("No processed image to save.")

class AvatarCustomizationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='light blue')
        self.parent = parent

        # Define the steps and options for each step
        self.steps = ["Background", "Skin Tone", "Eyes", "Nose", "Mouth", "Eyebrows", "Hair"]
        self.current_step_index = 0  # Start with the first step
        self.selections = {}  # Dictionary to store selections by step
        self.history = []  # To track previous selections for back navigation

        # Define the border frame
        self.border_frame = tk.Frame(self, bg='lightskyblue', bd=10)
        self.border_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew', columnspan=2)

        # Define the content frame
        self.content_frame = tk.Frame(self.border_frame, bg='lightskyblue', bd=0)
        self.content_frame.pack(fill='both', expand=True)

        # Create the canvas to display the avatar
        self.avatar_canvas = tk.Canvas(self.content_frame, width=300, height=300, bg='white', borderwidth=2, relief=tk.SOLID)
        self.avatar_canvas.grid(row=1, column=2, rowspan=5, padx=20, pady=20, sticky='nsew')

        self.image_ids = {}  # This dictionary will store the current image ID by category

        # Dictionary to store the images for each feature
        self.images = {
            "Background White": tk.PhotoImage(file="backgroundwhite.png"),
            "Background Black": tk.PhotoImage(file="backgroundblack.png"),
            "Background Blue": tk.PhotoImage(file="backgroundblue.png"),
            "Background Red": tk.PhotoImage(file="backgroundred.png"),
            "Background Yellow": tk.PhotoImage(file="backgroundyellow.png"),
            "Background Green": tk.PhotoImage(file="backgroundgreen.png"),
            "Background Purple": tk.PhotoImage(file="backgroundpurple.png"),
            "Background Orange": tk.PhotoImage(file="backgroundorange.png"),
            "Tone 1": tk.PhotoImage(file="skintone1.png"),
            "Tone 2": tk.PhotoImage(file="skintone2.png"),
            "Tone 3": tk.PhotoImage(file="skintone3.png"),
            "Tone 4": tk.PhotoImage(file="skintone4.png"),
            "Tone 5": tk.PhotoImage(file="skintone5.png"),
            "Tone 6": tk.PhotoImage(file="skintone6.png"),
            "Tone 7": tk.PhotoImage(file="skintone7.png"),
            "Tone 8": tk.PhotoImage(file="skintone8.png"),
            "Eyes 1": tk.PhotoImage(file="eyes1.png"),
            "Eyes 2": tk.PhotoImage(file="eyes2.png"),
            "Eyes 3": tk.PhotoImage(file="eyes3.png"),
            "Eyes 4": tk.PhotoImage(file="eyes4.png"),
            "Eyes 5": tk.PhotoImage(file="eyes5.png"),
            "Eyes 6": tk.PhotoImage(file="eyes6.png"),
            "Eyes 7": tk.PhotoImage(file="eyes7.png"),
            "Eyes 8": tk.PhotoImage(file="eyes8.png"),
            "Nose 1": tk.PhotoImage(file="nose1.png"),
            "Nose 2": tk.PhotoImage(file="nose2.png"),
            "Nose 3": tk.PhotoImage(file="nose3.png"),
            "Nose 4": tk.PhotoImage(file="nose4.png"),
            "Nose 5": tk.PhotoImage(file="nose5.png"),
            "Nose 6": tk.PhotoImage(file="nose6.png"),
            "Nose 7": tk.PhotoImage(file="nose7.png"),
            "Nose 8": tk.PhotoImage(file="nose8.png"),
            "Mouth 1": tk.PhotoImage(file="mouth1.png"),
            "Mouth 2": tk.PhotoImage(file="mouth2.png"),
            "Mouth 3": tk.PhotoImage(file="mouth3.png"),
            "Mouth 4": tk.PhotoImage(file="mouth4.png"),
            "Mouth 5": tk.PhotoImage(file="mouth5.png"),
            "Mouth 6": tk.PhotoImage(file="mouth6.png"),
            "Mouth 7": tk.PhotoImage(file="mouth7.png"),
            "Mouth 8": tk.PhotoImage(file="mouth8.png"),
            "Eyebrows 1": tk.PhotoImage(file="eyebrows1.png"),
            "Eyebrows 2": tk.PhotoImage(file="eyebrows2.png"),
            "Eyebrows 3": tk.PhotoImage(file="eyebrows3.png"),
            "Eyebrows 4": tk.PhotoImage(file="eyebrows4.png"),
            "Eyebrows 5": tk.PhotoImage(file="eyebrows5.png"),
            "Eyebrows 6": tk.PhotoImage(file="eyebrows6.png"),
            "Eyebrows 7": tk.PhotoImage(file="eyebrows7.png"),
            "Eyebrows 8": tk.PhotoImage(file="eyebrows8.png"),
            "Hair 1": tk.PhotoImage(file="hair1.png"),
            "Hair 2": tk.PhotoImage(file="hair2.png"),
            "Hair 3": tk.PhotoImage(file="hair3.png"),
            "Hair 4": tk.PhotoImage(file="hair4.png"),
            "Hair 5": tk.PhotoImage(file="hair5.png"),
            "Hair 6": tk.PhotoImage(file="hair6.png"),
            "Hair 7": tk.PhotoImage(file="hair7.png"),
            "Hair 8": tk.PhotoImage(file="hair8.png")
        }

        # Dictionary to store image placement on the canvas for each step
        self.feature_positions = {
            "Background": (150, 150),
            "Eyes": (150, 160),
            "Mouth": (150, 235),
            "Nose": (150, 185),
            "Hair": {
                "Hair 1": (150, 110),
                "Hair 2": (150, 110),
                "Hair 3": (150, 110),
                "Hair 4": (150, 96),
                "Hair 5": (150, 125),
                "Hair 6": (150, 150),
                "Hair 7": (150, 202),
                "Hair 8": (150, 140)
            },
            "Eyebrows": (150, 140),
            "Skin Tone": (150, 175)
        }

        self.create_step_widgets()

    def create_step_widgets(self):
        # Clear previous widgets
        for widget in self.content_frame.winfo_children():
            if widget != self.avatar_canvas:
                widget.destroy()
        
        step = self.steps[self.current_step_index]
        options = {}

        # Define the options for each step
        if step == "Background":
            options = {
                "Background White": "White",
                "Background Black": "Black", 
                "Background Blue": "Blue",
                "Background Red": "Red",
                "Background Yellow": "Yellow",
                "Background Green": "Green",
                "Background Purple": "Purple",
                "Background Orange": "Orange"
            }
        elif step == "Skin Tone":
            options = {
                "Tone 1": "skintone1.png",
                "Tone 2": "skintone2.png", 
                "Tone 3": "skintone3.png",
                "Tone 4": "skintone4.png",
                "Tone 5": "skintone5.png",
                "Tone 6": "skintone6.png",
                "Tone 7": "skintone7.png",
                "Tone 8": "skintone8.png"
            }
        elif step == "Eyes":
            options = {
                "Eyes 1": "eyes1.png",
                "Eyes 2": "eyes2.png", 
                "Eyes 3": "eyes3.png",
                "Eyes 4": "eyes4.png",
                "Eyes 5": "eyes5.png",
                "Eyes 6": "eyes6.png",
                "Eyes 7": "eyes7.png",
                "Eyes 8": "eyes8.png"
            }
        elif step == "Nose":
            options = {
                "Nose 1": "nose1.png",
                "Nose 2": "nose2.png", 
                "Nose 3": "nose3.png",
                "Nose 4": "nose4.png",
                "Nose 5": "nose5.png",
                "Nose 6": "nose6.png",
                "Nose 7": "nose7.png",
                "Nose 8": "nose8.png"
            }
        elif step == "Mouth":
            options = {
                "Mouth 1": "mouth1.png",
                "Mouth 2": "mouth2.png", 
                "Mouth 3": "mouth3.png",
                "Mouth 4": "mouth4.png",
                "Mouth 5": "mouth5.png",
                "Mouth 6": "mouth6.png",
                "Mouth 7": "mouth7.png",
                "Mouth 8": "mouth8.png"
            }
        elif step == "Eyebrows":
            options = {
                "Eyebrows 1": "eyebrows1.png",
                "Eyebrows 2": "eyebrows2.png", 
                "Eyebrows 3": "eyebrows3.png",
                "Eyebrows 4": "eyebrows4.png",
                "Eyebrows 5": "eyebrows5.png",
                "Eyebrows 6": "eyebrows6.png",
                "Eyebrows 7": "eyebrows7.png",
                "Eyebrows 8": "eyebrows8.png"
            }    
        elif step == "Hair":
            options = {
                "Hair 1": "hair1.png",
                "Hair 2": "hair2.png", 
                "Hair 3": "hair3.png",
                "Hair 4": "hair4.png",
                "Hair 5": "hair5.png",
                "Hair 6": "hair6.png",
                "Hair 7": "hair7.png",
                "Hair 8": "hair8.png"
            }    

        background_colors = {
            "Background White": "white",
            "Background Black": "black",
            "Background Blue": "blue",     
            "Background Red": "red",
            "Background Yellow": "yellow",
            "Background Green": "green",
            "Background Purple": "purple",
            "Background Orange": "orange"
        }
        
        # Create the title for the current step, to define the feature to customize
        title_label = tk.Label(self.content_frame, text=f"Choose your avatar's {step}", font=('Impact', 24), bg='lightskyblue', fg='lightslateblue')
        title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky='ew')

        # Grid position variables
        row_count = 1
        column_count = 0

        # Number of options per row
        options_per_row = 2

        # Create a separator line
        separator = tk.Frame(self.content_frame, height=5, bg='lightslateblue')
        separator.grid(row=row_count, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Update the row count
        row_count += 1

        # Loop through options and create buttons
        for index, (option, value) in enumerate(options.items()):
            # Create a button for each background option
            if "Background" in option:
                fg_color = background_colors.get(option, "black")  # Default to black if the option is not in the dictionary  
                button = tk.Button(self.content_frame, text=value, command=lambda opt=option: self.select_option(opt, step),
                                fg=fg_color, bd=0, highlightthickness=0, font=('Garamond', 16), width=15, height=2)
            # Create buttons with images for other options
            else:
                img = tk.PhotoImage(file=value)
                small_img = img.subsample(4, 4)
                button = tk.Button(self.content_frame, image=small_img, command=lambda opt=option: self.select_option(opt, step),
                                bd=0, highlightthickness=0, width=150, height=60)
                button.image = small_img    # Keep a reference to the image to prevent garbage collection

            # Grid position calculations
            button.grid(row=row_count, column=column_count, padx=10, pady=10, sticky='ew')

            # Update indices for rows and columns
            if column_count < options_per_row - 1:
                column_count += 1
            else:
                column_count = 0
                row_count += 1

        # Create a separator line
        separator = tk.Frame(self.content_frame, height=5, bg='lightslateblue')
        separator.grid(row=row_count, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # Update the row count
        row_count += 1

        # Create a 'Next' button to advance to the next step
        next_button = tk.Button(self.content_frame, text="Next", command=self.advance_step,
                                    font=('Garamond', 16), fg='slateblue', bd=0, highlightthickness=0, width=20, height=2)
        next_button.grid(row=row_count, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
        # Create a 'Back Home' button to stop the customization and go back to the home page
        back_home_button = tk.Button(self.content_frame, text="Back Home", command=self.back_home,
                                    font=('Garamond', 12), fg='slateblue', bd=0, highlightthickness=0, width=20, height=1)
        back_home_button.grid(row=row_count + 2, column=0, padx=10, pady=10, sticky='ew')

        # Create a 'Restart' button to restart the customization process
        restart_button = tk.Button(self.content_frame, text="Restart", command=self.restart_customization,
                                    font=('Garamond', 12), fg='slateblue', bd=0, highlightthickness=0, width=20, height=1)
        restart_button.grid(row=row_count + 2, column=1, padx=10, pady=10, sticky='ew')

    def back_home(self):
        # Go back to the home page
        self.parent.show_frame(HomePage)
    
    def get_options_for_step(self, step):
        # Returns options based on the current step
        return self.sub_options.get(step, [])

    def select_option(self, selection, category):
        # Save the current state to history before changing
        self.history.append((self.current_step_index, self.selections.copy()))

        #  Delete old image if it exists
        if category in self.image_ids:
            self.avatar_canvas.delete(self.image_ids[category])

        # Update selections and canvas
        self.selections[category] = selection
        if selection in self.images:
            position = self.feature_positions[category]  # Get the general position for the category
            if category == "Hair":  # Check if the category is Hair to use specific positions
                position = self.feature_positions["Hair"][selection]  # Update position based on specific hair choice

            # Create the new image on the canvas
            image_id = self.avatar_canvas.create_image(*position, image=self.images[selection], anchor='center')
            self.image_ids[category] = image_id # Store the image ID for future reference

    def advance_step(self):
        # Move to the next step or show the final options
        if self.current_step_index < len(self.steps) - 1:
            self.current_step_index += 1
            self.create_step_widgets()
        else:
            self.show_final_options()

    def show_final_options(self):
        # Clear non-canvas widgets from the content frame
        for widget in self.content_frame.winfo_children():
            if widget != self.avatar_canvas:
                widget.destroy()

        # Display the final avatar creation message
        title_label = tk.Label(self.content_frame, text="Congratulations ! You've just created your Avatar", font=('Impact', 24), bg='lightskyblue', fg='lightslateblue')
        title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky='ew')

        # Ensure the canvas is properly positioned; perhaps it needs repositioning after widget removal
        self.avatar_canvas.grid(row=1, column=0, rowspan=3, padx=20, pady=20, sticky='nsew')

        # Create a new frame for buttons and position it to the right of the canvas
        button_frame = tk.Frame(self.content_frame, bg='lightskyblue')
        button_frame.grid(row=1, column=1, sticky='ns', padx=20)

        # Configure the grid layout manager to distribute space
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=3)  # Canvas column gets more weight
        self.content_frame.grid_columnconfigure(1, weight=1)  # Button column gets less weight, adjust as needed

        # Create a button to download the avatar
        download_button = tk.Button(button_frame, text="Download Avatar", command=self.download_avatar,
                                    font=('Garamond', 23), fg='slateblue', bd=0, highlightthickness=0, height=3)
        download_button.grid(row=0, column=0, pady=30, sticky='ew')

        # Create a button to restart the customization process
        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_customization,
                                    font=('Garamond', 16), fg='slateblue', bd=0, highlightthickness=0, height=2)
        restart_button.grid(row=1, column=0, pady=30, sticky='ew')
        
        # Create a button to go back to the home page
        back_home_button = tk.Button(button_frame, text="Back Home", command=self.back_home,
                                    font=('Garamond', 16), fg='slateblue', bd=0, highlightthickness=0, height=2)
        back_home_button.grid(row=2, column=0, pady=30, sticky='ew')

    def restart_customization(self):
        # Reset to the first step
        self.current_step_index = 0  

        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Recreate the canvas
        self.avatar_canvas = tk.Canvas(self.content_frame, width=300, height=300, bg='white', borderwidth=2, relief=tk.SOLID)
        self.avatar_canvas.grid(row=1, column=2, rowspan=5, padx=20, pady=20, sticky='nsew')

        # Recreate the layout and the widgets for the first step
        self.create_step_widgets()

    def download_avatar(self):
        # Ask the user for a file path to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not file_path:
            # User clicked "Cancel", so exit the function
            return

        # Save the current canvas content as a postscript file
        ps_path = file_path + '.ps'  # Temporarily save as a postscript file
        self.avatar_canvas.postscript(file=ps_path, colormode='color')

        # Convert the postscript file to an image file (PNG or JPEG)
        with Image.open(ps_path) as img:
            img.save(file_path)  # Save the image in the desired format

        print(f"Avatar saved as {file_path}")  # Inform the user

        os.remove(ps_path)

    def back_home(self):
        # Go back to the home page
        self.parent.show_frame(HomePage)

class RandomAvatar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='lightskyblue')
        self.parent = parent
        self.grid()

        # Border Frame
        self.border_frame = tk.Frame(self, bg='lightskyblue', bd=10)
        self.border_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew', columnspan=2)

        # Interior Frame that will hold the content, contrasting with the border color
        self.content_frame = tk.Frame(self.border_frame, bg='lightskyblue', bd=0)
        self.content_frame.pack(fill='both', expand=True)

        # To hold references to PhotoImages
        self.image_refs = []

        # Load images from files
        self.images = self.load_images()

        # Dictionary to store image placement on the canvas for each step
        self.feature_positions = {
            "Background": (150, 150),
            "Eyes": (150, 160),
            "Mouth": (150, 235),
            "Nose": (150, 185),
            "Hair": {
                "Hair 1": (150, 110),
                "Hair 2": (150, 110),
                "Hair 3": (150, 110),
                "Hair 4": (150, 96),
                "Hair 5": (150, 125),
                "Hair 6": (150, 150),
                "Hair 7": (150, 202),
                "Hair 8": (150, 140)
            },
            "Eyebrows": (150, 140),
            "Skin Tone": (150, 175)
        }
        self.create_widgets()

    def load_images(self):
        image_paths = {
            "Background": ["backgroundwhite.png", "backgroundblack.png", "backgroundred.png", "backgroundblue.png", "backgroundyellow.png", "backgroundgreen.png", "backgroundpurple.png", "backgroundorange.png"],
            "Skin Tone": ["skintone1.png", "skintone2.png", "skintone3.png", "skintone4.png", "skintone5.png", "skintone6.png", "skintone7.png", "skintone8.png"],
            "Eyes": ["eyes1.png", "eyes2.png", "eyes3.png", "eyes4.png", "eyes5.png", "eyes6.png", "eyes7.png", "eyes8.png"],
            "Nose": ["nose1.png", "nose2.png", "nose3.png", "nose4.png", "nose5.png", "nose6.png", "nose7.png", "nose8.png"],
            "Mouth": ["mouth1.png", "mouth2.png", "mouth3.png", "mouth4.png", "mouth5.png", "mouth6.png", "mouth7.png", "mouth8.png"],
            "Eyebrows": ["eyebrows1.png", "eyebrows2.png", "eyebrows3.png", "eyebrows4.png", "eyebrows5.png", "eyebrows6.png", "eyebrows7.png", "eyebrows8.png"],
            "Hair": ["hair1.png", "hair2.png", "hair3.png", "hair4.png", "hair5.png", "hair6.png", "hair7.png", "hair8.png"]
        }
        
        # Store the images in a dictionary
        images = {}

        # Load images from files
        for category, paths in image_paths.items():
            photo_list = []
            for path in paths:
                img = Image.open(path)
                photo = ImageTk.PhotoImage(img)
                self.image_refs.append(photo)
                photo_list.append(photo)
            images[category] = photo_list
        return images
    
    def create_image(self, file):
        image = Image.open(file)  # Open the image file
        photo = ImageTk.PhotoImage(file=file)
        self.image_refs.append(photo)  # Keep a reference
        return photo

    def create_widgets(self):
        # Title label when the randomized avatar is created
        title_label = tk.Label(self.content_frame, text="Congratulations ! You've just created your Avatar", font=('Impact', 24), bg='lightskyblue', fg='lightslateblue')
        title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Canvas for displaying avatar
        self.avatar_canvas = tk.Canvas(self.content_frame, width=300, height=300, bg='white', borderwidth=2, relief=tk.SOLID)
        self.avatar_canvas.grid(row=1, column=0, padx=20, pady=20)

        # Button to generate a random avatar
        random_button = tk.Button(self.content_frame, text="Generate Random Avatar", command=self.generate_random_avatar,
                                  font=('Garamond', 16), fg='slateblue', bd=0, highlightthickness=0, width=20, height=2)
        random_button.grid(row=2, column=0, padx=20, pady=(20, 0))

        # Explanation text about the random avatar generation
        explanation_text = ("\u2191\nClick as many times as necessary")
        explanation_text = tk.Label(self.content_frame, text=explanation_text, font=('Garamond', 16), bg='lightskyblue', fg='lightslateblue', justify='center')
        explanation_text.grid(row=3, column=0, padx=20, pady=(0, 20))

        # Create a new frame for buttons and position it to the right of the canvas
        button_frame = tk.Frame(self.content_frame, bg='lightskyblue')
        button_frame.grid(row=1, column=1, sticky='ns', padx=20)

        # Add the 1st button to download the avatar
        download_button = tk.Button(button_frame, text="Download Avatar", command=self.download_avatar,
                                    font=('Garamond', 23), fg='slateblue', bd=0, highlightthickness=0, height=3)
        download_button.grid(row=0, column=0, pady=50, sticky='ew')
        
        # Add the 2nd button to come back home
        back_home_button = tk.Button(button_frame, text="Back Home", command=self.back_home,
                                    font=('Garamond', 16), fg='slateblue', bd=0, highlightthickness=0, height=2)
        back_home_button.grid(row=1, column=0, pady=50, sticky='ew')

    def generate_random_avatar(self):
        self.avatar_canvas.delete("all")  # Clear the canvas

        # Display a random image from each category
        for category, images in self.images.items():
            image = random.choice(images)  # Randomly select an image from each category
            if category == "Hair":
                # For hair, find which hair image was selected
                hair_index = images.index(image)
                hair_key = f"Hair {hair_index + 1}"
                x, y = self.feature_positions["Hair"][hair_key]  # Get specific position for the hair that has been randomly selected
            else:
                x, y = self.feature_positions[category]  # General position for other categories

            self.avatar_canvas.create_image(x, y, image=image, anchor='center')
    
    def download_avatar(self):
        # Ask the user for a file path to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if not file_path:
            # User clicked "Cancel", so exit the function
            return

        # Save the current canvas content as a postscript file
        ps_path = file_path + '.ps'  # Temporarily save as a postscript file
        self.avatar_canvas.postscript(file=ps_path, colormode='color')

        # Convert the postscript file to an image file (PNG or JPEG)
        with Image.open(ps_path) as img:
            img.save(file_path)  # Save the image in the desired format

        print(f"Avatar saved as {file_path}")  # Inform the user

        os.remove(ps_path)

    def back_home(self):
        # Go back to the home page
        self.parent.show_frame(HomePage)

if __name__ == "__main__":
    app = App()
    app.mainloop()