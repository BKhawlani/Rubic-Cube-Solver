import cv2
import numpy as np
from tkinter import *
from tkinter import colorchooser, messagebox
from PIL import Image, ImageTk
import kociemba

class WelcomePage:
    def __init__(self, root):
        self.root = root
        self.setup_welcome_page()
        
    def setup_welcome_page(self):
        self.root.title("Rubik's Cube Solver - Welcome")
        self.root.geometry('800x500')
        self.root.configure(bg='#58F')
        self.root.minsize(800, 500)
        
        # Main title
        title = Label(self.root, text="Rubik's Cube Solver", 
                     font=('Arial', 24, 'bold'), bg='#58F', fg='white')
        title.pack(pady=50)
        
        # Subtitle
        subtitle = Label(self.root, text="Choose your input method:", 
                        font=('Arial', 16), bg='#58F', fg='white')
        subtitle.pack(pady=20)
        
        # Buttons frame
        btn_frame = Frame(self.root, bg='#58F')
        btn_frame.pack(pady=50)
        
        
        # Camera Input Button
        camera_btn = Button(btn_frame, text="Camera Input", 
                          font=('Arial', 14), width=15, height=3,
                          bg='#55ff55', command=self.open_camera_input)
        camera_btn.grid(row=0, column=0, padx=20)
        
        # Manual Input Button
        manual_btn = Button(btn_frame, text="Manual Input", 
                           font=('Arial', 14), width=15, height=3,
                           bg='#FFD700', command=self.open_manual_input)
        manual_btn.grid(row=0, column=1, padx=20)

        develeoper_inf = Label(self.root, text=" Developed by:\n Bashar Alkhawlani\n Under the supervision of:\n Dr. Öğr. Üyesi Ali Burak ÖNCÜL", 
                        font=('Arial', 12), bg='#58F', fg='white')
        develeoper_inf.pack(pady=15)
      

        
    def open_camera_input(self):
        self.root.destroy()  # Close welcome window
        root = Tk()
        app = CameraInputSolver(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
        
    def open_manual_input(self):
        self.root.destroy()  # Close welcome window
        root = Tk()
        app = ManualInputSolver(root)
        root.mainloop()

class ManualInputSolver:
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.setup_variables()
        self.setup_ui()
        
    def setup_main_window(self):
        self.root.title("Rubik's Cube Solver - Manual Input")
        self.root.geometry('1200x800')
        self.root.configure(bg='#58F')
        self.root.minsize(1000, 700)
        
    def setup_variables(self):
        self.current_face = 0
        self.face_names = ["Front", "Right", "Back", "Left", "Up", "Down"]
        self.color_map = {
            "Red": "#FF0000",
            "Green": "#00FF00",
            "Blue": "#0000FF",
            "Yellow": "#FFFF00",
            "White": "#FFFFFF",
            "Orange": "#FFA500",
            "Undefined": "#808080",
            "Black": "#000000"
        }
        
        # Initialize color counters
        self.color_counts = {
            "Red": 0,
            "Green": 0,
            "Blue": 0,
            "Yellow": 0,
            "White": 0,
            "Orange": 0,
            "Undefined": 0,
            "Black": 0
        }

        self.final_colors = [[["Undefined" for _ in range(3)] for _ in range(3)] for _ in range(6)]
        self.preview_colors = [["Undefined" for _ in range(3)] for _ in range(3)]
        
    def setup_ui(self):
        self.setup_preview_frame()
        self.setup_faces_display()
        self.setup_control_buttons()
        self.setup_color_counters()
        self.setup_status_bar()
        
    def setup_status_bar(self):
        self.status_var = StringVar()
        self.status_var.set("Ready - Face " + self.face_names[self.current_face])
        status_bar = Label(self.root, textvariable=self.status_var, bd=1, relief=SUNKEN, anchor=W)
        status_bar.pack(side=BOTTOM, fill=X)
        
    def setup_color_counters(self):
        self.counters_frame = LabelFrame(self.root, text="Color Counters", bg='white', font=('Arial', 12))
        self.counters_frame.place(x=560, y=450, width=300, height=200)
        
        self.counter_labels = {}
        colors = ["Red", "Green", "Blue", "Yellow", "White", "Orange"]
        
        for i, color in enumerate(colors):
            frame = Frame(self.counters_frame, bg='white')
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='w')
            
            Label(frame, text=color, bg='white', width=7).pack(side=LEFT)
            counter = Label(frame, text="0", bg='white', width=3, relief=SUNKEN)
            counter.pack(side=LEFT)
            self.counter_labels[color] = counter
    
    def update_color_counters(self):
        # Reset counters
        for color in self.color_counts:
            self.color_counts[color] = 0
        
        # Count colors in final_colors
        for face in self.final_colors:
            for row in face:
                for color in row:
                    self.color_counts[color] += 1
        
        # Update UI
        for color, label in self.counter_labels.items():
            label.config(text=str(self.color_counts[color]))
            
            # Highlight if count is not 9 (for main colors)
            if color in ["Red", "Green", "Blue", "Yellow", "White", "Orange"]:
                if self.color_counts[color] < 9:
                    label.config(bg='#FFCCCC')  # Light red for missing
                elif self.color_counts[color] > 9:
                    label.config(bg='#FFFF99')  # Light yellow for extra
                else:
                    label.config(bg='#CCFFCC')  # Light green for correct
            else:
                label.config(bg='white')
    
    def setup_preview_frame(self):
        self.preview_frame = LabelFrame(self.root, text="Color Input", bg='white', font=('Arial', 12))
        self.preview_frame.place(x=20, y=20, width=500, height=500)

        # Instructions
        Label(self.preview_frame, text="Click on each square to select its color", 
             font=('Arial', 10), bg='white').pack(pady=5)
        
        # Color selection buttons
        color_btn_frame = Frame(self.preview_frame, bg='white')
        color_btn_frame.pack(pady=5)
        
        colors = ["Red", "Green", "Blue", "Yellow", "White", "Orange"]
        for i, color in enumerate(colors):
            btn = Button(color_btn_frame, text=color, bg=self.color_map[color],
                       width=8, command=lambda c=color: self.set_selected_color(c))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
        
        # Renk göstergesi
        self.selected_color = "Undefined" 
        self.color_indicator = Label(self.preview_frame, text="Selected: None", 
                                   bg='white', font=('Arial', 12))
        self.color_indicator.pack(pady=5)
        
        # Cube face grid
        self.grid_frame = Frame(self.preview_frame, bg='white')
        self.grid_frame.pack(pady=10)
        
        self.preview_labels = []
        for i in range(3):
            row = []
            for j in range(3):
                lbl = Label(self.grid_frame, bg='gray', relief=RAISED, width=8, height=4)
                lbl.grid(row=i, column=j, padx=2, pady=2)
                lbl.bind("<Button-1>", lambda e, i=i, j=j: self.change_preview_color(i, j)) #fare tiklama ile renk degistime
                row.append(lbl)
            self.preview_labels.append(row)
    
    def set_selected_color(self, color):
        self.selected_color = color
        self.color_indicator.config(text=f"Selected: {color}", bg=self.color_map[color])
    

    
    def setup_faces_display(self):
        self.faces_frame = LabelFrame(self.root, text="Collected Faces", bg='white', font=('Arial', 12))
        self.faces_frame.place(x=560, y=20, width=500, height=400)

        self.face_displays = []
        for i in range(6):
            frame = Frame(self.faces_frame, bg='white')
            
            if i < 3:  
                frame.grid(row=0, column=i, padx=5, pady=5)
            else:      
                frame.grid(row=1, column=i-3, padx=5, pady=5)
            
            Label(frame, text=self.face_names[i], font=('Arial', 10)).pack()
            
            face_grid = []
            for row in range(3):
                row_frame = Frame(frame)
                row_frame.pack()
                row_labels = []
                for col in range(3):
                    lbl = Label(row_frame, bg='#808080', width=6, height=3, relief=RAISED)
                    lbl.pack(side=LEFT, padx=1, pady=1)
                    row_labels.append(lbl) 
                face_grid.append(row_labels) 
            self.face_displays.append(face_grid) #yuzleri kayidetme
    
    def setup_control_buttons(self):
        self.control_frame = Frame(self.root, bg='#58F')
        self.control_frame.place(x=20, y=520, width=500, height=300)

        self.face_label = Label(self.control_frame,
                              text=f"Current Face: {self.face_names[self.current_face]}",
                              font=('Arial', 14), bg='#58F')
        self.face_label.pack(pady=5)

        self.confirm_btn = Button(self.control_frame, text="Confirm Colors",
                                command=self.confirm_colors, font=('Arial', 12))
        self.confirm_btn.pack(pady=2)

        self.next_btn = Button(self.control_frame, text="Next Face",
                             command=self.next_face, font=('Arial', 12))
        self.next_btn.pack(pady=2)
        
        self.validate_btn = Button(self.control_frame, text="Validate Cube",
              command=self.validate_cube, font=('Arial', 12), bg='#FFD700')
        self.validate_btn.pack(pady=2)
        
        self.solve_btn = Button(self.control_frame, text="Solve Cube",
              command=self.solve_cube, font=('Arial', 12), bg='#55ff55')
        self.solve_btn.pack(pady=2)
        
        self.reset_btn = Button(self.control_frame, text="Reset All",
                              command=self.reset_all, font=('Arial', 12), bg='#ff5555')
        self.reset_btn.pack(pady=2)
        
        self.back_btn = Button(self.control_frame, text="Back to Home",
                             command=self.back_to_welcome, font=('Arial', 12))
        self.back_btn.pack(pady=2)
    
    def back_to_welcome(self):
        self.root.destroy()
        root = Tk()
        app = WelcomePage(root)
        root.mainloop()
    
    def change_preview_color(self, i, j):
        if self.selected_color != "Undefined":
            self.preview_colors[i][j] = self.selected_color
            self.preview_labels[i][j].config(bg=self.color_map[self.selected_color])
    
    def reset_all(self):
        self.final_colors = [[["Undefined" for _ in range(3)] for _ in range(3)] for _ in range(6)]
        self.preview_colors = [["Undefined" for _ in range(3)] for _ in range(3)]
        self.current_face = 0
        self.face_label.config(text=f"Current Face: {self.face_names[self.current_face]}")
        self.selected_color = "Undefined"
        self.color_indicator.config(text="Selected: None", bg='white')

        for i in range(3):
            for j in range(3):
                self.preview_labels[i][j].config(bg="#808080")

        self.update_faces_display()
        self.update_color_counters()
        print("Cube has been reset to initial state")
    
    def confirm_colors(self):
        for i in range(3):
            for j in range(3):
                self.final_colors[self.current_face][i][j] = self.preview_colors[i][j]
        print(f"Colors confirmed for {self.face_names[self.current_face]} face")
        self.update_faces_display()
        self.update_color_counters()
    
    def update_faces_display(self): #renk gosterme
        for face_idx in range(6):
            for row in range(3):
                for col in range(3):
                    color = self.final_colors[face_idx][row][col]
                    self.face_displays[face_idx][row][col].config(bg=self.color_map[color])
    
    def next_face(self):
        self.current_face = (self.current_face + 1) % 6
        self.face_label.config(text=f"Current Face: {self.face_names[self.current_face]}")

        self.preview_colors = [["Undefined" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.preview_labels[i][j].config(bg="#808080")
    
    def check_all_faces_completed(self):
        for face in self.final_colors:
            for row in face:
                for color in row:
                    if color == "Undefined":
                        return False
        return True
    
    def validate_cube(self):
        if not self.check_all_faces_completed():
            messagebox.showwarning("Warning", "Not all faces have been completed!")
            return False
        
        # Check color counts
        errors = []
        for color in ["Red", "Green", "Blue", "Yellow", "White", "Orange"]:
            if self.color_counts[color] != 9:
                errors.append(f"{color}: {self.color_counts[color]}/9")
        
        if errors:
            messagebox.showerror("Color Count Error", 
                               "Incorrect color counts detected:\n\n" + "\n".join(errors))
            return False
            
        messagebox.showinfo("Success", "Cube is valid and ready to solve!")
        return True
    
    def solve_cube(self):
        
        
        # Create Kociemba input string
        try:   #Kociemba icin Input hazırlama
            color_to_face = {
                self.final_colors[0][1][1]: 'F',  # Front center
                self.final_colors[1][1][1]: 'R',  # Right center
                self.final_colors[2][1][1]: 'B',  # Back center
                self.final_colors[3][1][1]: 'L',  # Left center
                self.final_colors[4][1][1]: 'U',  # Up center
                self.final_colors[5][1][1]: 'D'   # Down center
            }

            # Order: Up, Right, Front, Down, Left, Back
            face_order = [4, 1, 0, 5, 3, 2] #kociemba Algorithime gore ayarladim
            cube_str = ''
            
            for face_idx in face_order:
                for row in self.final_colors[face_idx]:
                    for color in row:
                        cube_str += color_to_face.get(color, '?')  # inputu düzenleme

            solution = kociemba.solve(cube_str)
            
            # Show solution in a new window
            self.show_solution_window(solution)
            
        except Exception as e:
            messagebox.showerror("Solving Error", f"Could not solve cube:\n{str(e)}")
    
    def show_solution_window(self, solution):
        solution_window = Toplevel(self.root)
        solution_window.title("Cube Solution")
        solution_window.geometry("600x800")  
        
        Label(solution_window, text="Rubik's Cube Solution", 
            font=('Arial', 16)).pack(pady=10)
        
        main_frame = Frame(solution_window)
        main_frame.pack(fill=BOTH, expand=True)
        
        canvas = Canvas(main_frame)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        move_images = { #move photolar yukleme
            "U": "Up.png",
            "U'": "up'.png",
            "U2": "Up2.png",
            "D": "Down.png",
            "D'": "down'.png",
            "D2": "down2.png",
            "F": "Front.png",
            "F'": "front'.png",
            "F2": "front2.png",
            "B": "back.png",
            "B'": "back'.png",
            "B2": "back2.png",
            "L": "left.png",
            "L'": "left'.png",
            "L2": "left2.png",
            "R": "Right.png",
            "R'": "Right'.png",
            "R2": "Right2.png"
        }
        
        steps = solution.split()
        self.solution_images = []  
        
        rows_frame = Frame(scrollable_frame)
        rows_frame.pack(fill=BOTH, expand=True)
        
        current_row = Frame(rows_frame)
        current_row.pack(fill=X, pady=5)
        
        for i, step in enumerate(steps):
           
            if i % 3 == 0 and i != 0:
                current_row = Frame(rows_frame)
                current_row.pack(fill=X, pady=5)
            
            step_frame = Frame(current_row, borderwidth=1, relief="solid", padx=10, pady=10)
            step_frame.pack(side=LEFT, expand=True, fill=BOTH)
            
            Label(step_frame, text=f"Step {i+1}", font=('Arial', 12, 'bold')).pack()
            
            image_path = rf"C:\Users\Bashar Alkhawlani\Desktop\مشاريع سنه ثالثه\Project\Rubik's Cube Solver_Son Hale\Rubik's cube moves\{move_images.get(step, 'default.jpg')}"
            try: #photoloari acma
                img = Image.open(image_path)
                img = img.resize((150, 150), Image.LANCZOS)  
                img_tk = ImageTk.PhotoImage(img)
                
                self.solution_images.append(img_tk)
                
                img_label = Label(step_frame, image=img_tk)
                img_label.image = img_tk 
                img_label.pack()
            except FileNotFoundError:
                Label(step_frame, text=f"Image not found\nfor move: {step}", 
                    font=('Arial', 10), fg="red").pack()
            
            Label(step_frame, text=step, font=('Arial', 14, 'bold')).pack()
        
        Button(solution_window, text="Close", command=solution_window.destroy, 
            font=('Arial', 12), padx=15, pady=5).pack(pady=20)

# Your original CameraInputSolver class remains unchanged
class CameraInputSolver:
    def __init__(self, root):
        self.root = root
        self.setup_main_window()
        self.setup_camera()
        self.setup_variables()
        self.setup_ui()
        self.update_camera()

    def setup_main_window(self):
        self.root.title("Rubik's Cube Solver - Real Time Preview")
        self.root.geometry('1200x800')
        self.root.configure(bg='#58F')
        self.root.minsize(1000, 700)

    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()

    def setup_variables(self):
        self.current_face = 0
        self.face_names = ["Front", "Right", "Back", "Left", "Up", "Down"]
        self.color_map = {
            "Red": "#FF0000",
            "Green": "#00FF00",
            "Blue": "#0000FF",
            "Yellow": "#FFFF00",
            "White": "#FFFFFF",
            "Orange": "#FFA500",
            "Undefined": "#808080",
            "Black": "#000000"
        }
        
        # Initialize color counters
        self.color_counts = {
            "Red": 0,
            "Green": 0,
            "Blue": 0,
            "Yellow": 0,
            "White": 0,
            "Orange": 0,
            "Undefined": 0,
            "Black": 0
        }

        self.final_colors = [[["Undefined" for _ in range(3)] for _ in range(3)] for _ in range(6)] #butun yuzler icin bir dizi
        self.preview_colors = [["Undefined" for _ in range(3)] for _ in range(3)] #gostrilecek yuzun renkler dizisi
        self.face_frames = []

    def setup_ui(self):
        self.setup_camera_frame()
        self.setup_preview_frame()
        self.setup_faces_display()
        self.setup_control_buttons()
        self.setup_color_counters()
        self.setup_status_bar()

    def setup_status_bar(self):
        self.status_var = StringVar() #degisebilir string 
        self.status_var.set("Ready - Face " + self.face_names[self.current_face])
        status_bar = Label(self.root, textvariable=self.status_var, bd=1, relief=SUNKEN, anchor=W)
        status_bar.pack(side=BOTTOM, fill=X)

    def setup_color_counters(self):
        self.counters_frame = LabelFrame(self.root, text="Color Counters", bg='white', font=('Arial', 12))
        self.counters_frame.place(x=560, y=340, width=300, height=200)
        
        self.counter_labels = {}
        colors = ["Red", "Green", "Blue", "Yellow", "White", "Orange"]
        
        for i, color in enumerate(colors):
            frame = Frame(self.counters_frame, bg='white')
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky='w')
            
            Label(frame, text=color, bg='white', width=7).pack(side=LEFT)
            counter = Label(frame, text="0", bg='white', width=3, relief=SUNKEN)
            counter.pack(side=LEFT)
            self.counter_labels[color] = counter

    def update_color_counters(self):
        # Reset counters
        for color in self.color_counts:
            self.color_counts[color] = 0
        
        # Count colors in final_colors
        for face in self.final_colors:
            for row in face:
                for color in row:
                    self.color_counts[color] += 1
        
        # Update UI
        for color, label in self.counter_labels.items():
            label.config(text=str(self.color_counts[color]))
            
            # Highlight if count is not 9 (for main colors)
            if color in ["Red", "Green", "Blue", "Yellow", "White", "Orange"]:
                if self.color_counts[color] < 9:
                    label.config(bg='#FFCCCC')  # Light red for missing
                elif self.color_counts[color] > 9:
                    label.config(bg='#FFFF99')  # Light yellow for extra
                else:
                    label.config(bg='#CCFFCC')  # Light green for correct
            else:
                label.config(bg='white')

    def setup_camera_frame(self):
        self.cam_frame = LabelFrame(self.root, text="Camera Feed", bg='green', font=('Arial', 12))
        self.cam_frame.place(x=20, y=20, width=520, height=520)

        self.cam_label = Label(self.cam_frame, bg='black')
        self.cam_label.place(x=10, y=10, width=500, height=500)

    def setup_preview_frame(self):
        self.preview_frame = LabelFrame(self.root, text="Color Preview", bg='white', font=('Arial', 12))
        self.preview_frame.place(x=560, y=20, width=300, height=300)

        self.preview_labels = []
        for i in range(3):
            row = []
            for j in range(3):
                lbl = Label(self.preview_frame, bg='gray', relief=RAISED, width=6, height=3)
                lbl.grid(row=i, column=j, padx=2, pady=2)
                row.append(lbl)
            self.preview_labels.append(row)

    def setup_faces_display(self):
        self.faces_frame = LabelFrame(self.root, text="Collected Faces", bg='white', font=('Arial', 12))
        self.faces_frame.place(x=880, y=20, width=280, height=520)

        self.face_displays = []
        for i in range(6):
            frame = Frame(self.faces_frame, bg='white')
            frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            
            Label(frame, text=self.face_names[i], font=('Arial', 10)).pack()
            
            face_grid = []
            for row in range(3):
                row_frame = Frame(frame)
                row_frame.pack()
                row_labels = []
                for col in range(3):
                    lbl = Label(row_frame, bg='#808080', width=4, height=2, relief=RAISED)
                    lbl.pack(side=LEFT, padx=1, pady=1)
                    row_labels.append(lbl)
                face_grid.append(row_labels)
            self.face_displays.append(face_grid)

    def setup_control_buttons(self):
        self.control_frame = Frame(self.root, bg='#58F')
        self.control_frame.place(x=20, y=510, width=520, height=300)

        self.face_label = Label(self.control_frame,
                              text=f"Current Face: {self.face_names[self.current_face]}",
                              font=('Arial', 14), bg='#58F')
        self.face_label.pack(pady=5)

        self.confirm_btn = Button(self.control_frame, text="Confirm Colors",
                                command=self.confirm_colors, font=('Arial', 12))
        self.confirm_btn.pack(pady=2)

        self.next_btn = Button(self.control_frame, text="Next Face",
                             command=self.next_face, font=('Arial', 12))
        self.next_btn.pack(pady=2)
        
        self.validate_btn = Button(self.control_frame, text="Validate Cube",
              command=self.validate_cube, font=('Arial', 12), bg='#FFD700')
        self.validate_btn.pack(pady=2)
        
        self.solve_btn = Button(self.control_frame, text="Solve Cube",
              command=self.solve_cube, font=('Arial', 12), bg='#55ff55')
        self.solve_btn.pack(pady=2)
        
        self.reset_btn = Button(self.control_frame, text="Reset All",
                              command=self.reset_all, font=('Arial', 12), bg='#ff5555')
        self.reset_btn.pack(pady=2)
        
        self.back_btn = Button(self.control_frame, text="Back to Home",
                             command=self.back_to_welcome, font=('Arial', 12))
        self.back_btn.pack(pady=2)
    
    def back_to_welcome(self):
        self.cap.release()
        self.root.destroy()
        root = Tk()
        app = WelcomePage(root)
        root.mainloop()

    def update_camera(self): 
        ret, frame = self.cap.read()
        if ret:
            frame = self.process_frame(frame)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.cam_label.imgtk = imgtk
            self.cam_label.configure(image=imgtk)
        
        self.root.after(10, self.update_camera) #her 10 milli saniye guncellenir

    def process_frame(self, frame): #işlem alanı
        height, width = frame.shape[:2] 
        cx, cy = width // 2, height // 2
        grid_size = 90
        size = 30

        for i in range(3):
            for j in range(3):
                x = cx + (j - 1) * grid_size
                y = cy + (i - 1) * grid_size

                color = self.detect_color(frame, x, y)
                self.preview_colors[i][j] = color

                hex_color = self.color_to_hex(color)
                self.preview_labels[i][j].config(bg=hex_color)

                cv2.rectangle(frame, (x-size, y-size), (x+size, y+size), (0, 255, 0), 2) #kareleri çizme

        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def detect_color(self, frame, x, y): #noktalardan color berlileme
        size = 10
        roi = frame[y-size:y+size, x-size:x+size]

        if roi.size == 0:
            return "Undefined"

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) #hsv renk uzayına
        avg_hue = np.mean(hsv[:,:,0])#renk tonu
        avg_sat = np.mean(hsv[:,:,1])#doygunluk
        avg_val = np.mean(hsv[:,:,2])#parlaklik

        if avg_val < 30:
            return "Black"
        elif avg_sat < 50:
            return "White"
        elif avg_hue < 5 or avg_hue > 175:
            return "Red"
        elif avg_hue < 22:
            return "Orange"
        elif avg_hue < 38:
            return "Yellow"
        elif avg_hue < 75:
            return "Green"
        elif avg_hue < 130:
            return "Blue"
        else:
            return "Undefined"

    def color_to_hex(self, color_name):
        return self.color_map.get(color_name, "#808080")



    def reset_all(self):
        self.final_colors = [[["Undefined" for _ in range(3)] for _ in range(3)] for _ in range(6)]
        self.preview_colors = [["Undefined" for _ in range(3)] for _ in range(3)]
        self.current_face = 0
        self.face_label.config(text=f"Current Face: {self.face_names[self.current_face]}")

        for i in range(3):
            for j in range(3):
                self.preview_labels[i][j].config(bg="#808080")

        self.update_faces_display()
        self.update_color_counters()
        print("Cube has been reset to initial state")

    def confirm_colors(self):
        for i in range(3):
            for j in range(3):
                self.final_colors[self.current_face][i][j] = self.preview_colors[i][j]
        print(f"Colors confirmed for {self.face_names[self.current_face]} face")
        self.update_faces_display()
        self.update_color_counters()

    def update_faces_display(self):
        for face_idx in range(6):
            for row in range(3):
                for col in range(3):
                    color = self.final_colors[face_idx][row][col]
                    self.face_displays[face_idx][row][col].config(bg=self.color_to_hex(color))

    def next_face(self):
        self.current_face = (self.current_face + 1) % 6
        self.face_label.config(text=f"Current Face: {self.face_names[self.current_face]}")

        self.preview_colors = [["Undefined" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.preview_labels[i][j].config(bg="#808080")

    def check_all_faces_completed(self):
        for face in self.final_colors:
            for row in face:
                for color in row:
                    if color == "Undefined":
                        return False
        return True
    

    def validate_color_distribution(self):
        centers = {
            self.final_colors[0][1][1],  # Front
            self.final_colors[1][1][1],  # Right
            self.final_colors[2][1][1],  # Back
            self.final_colors[3][1][1],  # Left
            self.final_colors[4][1][1],  # Up
            self.final_colors[5][1][1]   # Down
        }
        
        if len(centers) != 6:
            messagebox.showerror("Error", "Center colors must be unique for each face!")
            return False
        
        color_counts = {}
        for face in self.final_colors:
            for row in face:
                for color in row:
                    color_counts[color] = color_counts.get(color, 0) + 1
        
        for color, count in color_counts.items():
            if color in ["Red", "Green", "Blue", "Yellow", "White", "Orange"] and count != 9:
                messagebox.showerror("Error", f"Color {color} should have 9 stickers (has {count})")
                return False
        
        return True
    
    def validate_cube(self):
        if not self.check_all_faces_completed():
            messagebox.showwarning("Warning", "Not all faces have been completed!")
            return False
        if not self.validate_color_distribution():
            return False
        
        messagebox.showinfo("Success", "Cube is valid and ready to solve!")
        return True
    
   
    def solve_cube(self):
        # Check if all faces are collected
        if any(color == "Undefined" for face in self.final_colors for row in face for color in row):
            messagebox.showerror("Error", "Please complete all faces before solving!")
            return
        
        # Check color counts
        errors = []
        for color in ["Red", "Green", "Blue", "Yellow", "White", "Orange"]:
            if self.color_counts[color] != 9:
                errors.append(f"{color}: {self.color_counts[color]}/9")
        
        if errors:
            messagebox.showerror("Color Count Error", 
                               "Incorrect color counts detected:\n\n" + "\n".join(errors))
            return
        
        # Create Kociemba input string
        try:
            color_to_face = {
                self.final_colors[0][1][1]: 'F',  # Front center
                self.final_colors[1][1][1]: 'R',  # Right center
                self.final_colors[2][1][1]: 'B',  # Back center
                self.final_colors[3][1][1]: 'L',  # Left center
                self.final_colors[4][1][1]: 'U',  # Up center
                self.final_colors[5][1][1]: 'D'   # Down center
            }

            # Order: Up, Right, Front, Down, Left, Back
            face_order = [4, 1, 0, 5, 3, 2]
            cube_str = ''
            
            for face_idx in face_order:
                for row in self.final_colors[face_idx]:
                    for color in row:
                        cube_str += color_to_face.get(color, '?') #Kociemba algorithim input hazirlama

            solution = kociemba.solve(cube_str)
            
            # Show solution in a new window
            self.show_solution_window(solution)
            
        except Exception as e:
            messagebox.showerror("Solving Error", f"Could not solve cube:\n{str(e)}")
    
    def show_solution_window(self, solution):
        solution_window = Toplevel(self.root)
        solution_window.title("Cube Solution")
        solution_window.geometry("600x800")  
        
        Label(solution_window, text="Rubik's Cube Solution", 
            font=('Arial', 16)).pack(pady=10)
        
        main_frame = Frame(solution_window)
        main_frame.pack(fill=BOTH, expand=True)
        
        canvas = Canvas(main_frame)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
        move_images = {
            "U": "Up.png",
            "U'": "up'.png",
            "U2": "Up2.png",
            "D": "Down.png",
            "D'": "down'.png",
            "D2": "down2.png",
            "F": "Front.png",
            "F'": "front'.png",
            "F2": "front2.png",
            "B": "back.png",
            "B'": "back'.png",
            "B2": "back2.png",
            "L": "left.png",
            "L'": "left'.png",
            "L2": "left2.png",
            "R": "Right.png",
            "R'": "Right'.png",
            "R2": "Right2.png"
        }
        
        steps = solution.split()
        self.solution_images = []  
        
        rows_frame = Frame(scrollable_frame)
        rows_frame.pack(fill=BOTH, expand=True)
        
        current_row = Frame(rows_frame)
        current_row.pack(fill=X, pady=5)
        
        for i, step in enumerate(steps):
           
            if i % 3 == 0 and i != 0:
                current_row = Frame(rows_frame)
                current_row.pack(fill=X, pady=5)
            
            step_frame = Frame(current_row, borderwidth=1, relief="solid", padx=10, pady=10)
            step_frame.pack(side=LEFT, expand=True, fill=BOTH)
            
            Label(step_frame, text=f"Step {i+1}", font=('Arial', 12, 'bold')).pack()
            
            image_path = rf"C:\Users\Bashar Alkhawlani\Desktop\مشاريع سنه ثالثه\Project\Rubik's Cube Solver_Son Hale\Rubik's cube moves\{move_images.get(step, 'default.jpg')}"
            try:
                img = Image.open(image_path)
                img = img.resize((150, 150), Image.LANCZOS)  
                img_tk = ImageTk.PhotoImage(img)
                
                self.solution_images.append(img_tk)
                
                img_label = Label(step_frame, image=img_tk)
                img_label.image = img_tk 
                img_label.pack()
            except FileNotFoundError:
                Label(step_frame, text=f"Image not found\nfor move: {step}", 
                    font=('Arial', 10), fg="red").pack()
            
            Label(step_frame, text=step, font=('Arial', 14, 'bold')).pack()
        
        Button(solution_window, text="Close", command=solution_window.destroy, 
            font=('Arial', 12), padx=15, pady=5).pack(pady=20)


    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = WelcomePage(root) #NESNE YARATIOR
    root.mainloop()