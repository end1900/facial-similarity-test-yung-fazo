import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import face_recognition
import os
import numpy as np
import sys  # fixed dis 

# shi to get heic support ;,3
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass 

class FaceComparisonApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Yung Fazo Similarity Test")
        self.window.geometry("920x720")
        ctk.set_appearance_mode("dark")
        
        # This part ensures the EXE finds the bundled image 
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        self.uploaded_path = None
        self.reference_path = os.path.join(base_path, "fazo.png")
        self.setup_ui()
        self.load_ref()

    def round_img(self, path, size=(280, 280)):
        img = Image.open(path).convert("RGB")
        img.thumbnail(size, Image.Resampling.LANCZOS)
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=18, fill=255)
        out = Image.new('RGB', img.size, (20, 20, 20))
        out.paste(img, (0, 0))
        out.putalpha(mask)
        return ImageTk.PhotoImage(out)

    def setup_ui(self):
        main = ctk.CTkFrame(self.window, fg_color="#0a0a0a")
        main.pack(fill="both", expand=True)
        top = ctk.CTkFrame(main, fg_color="#009E49", height=140, corner_radius=0)
        top.pack(fill="x")
        top.pack_propagate(False)
        accent = ctk.CTkFrame(top, fg_color="#FCD116", height=6, corner_radius=0)
        accent.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(
            top, text="DE OPEN SOURCE OBEAH MACHINE", font=("Arial Black", 38, "bold"), text_color="#FCD116"
        ).pack(pady=(20, 5))
        ctk.CTkLabel(
            top, text="FAZO SKUNT DETECTOR", font=("Arial", 20, "bold"), text_color="white"
        ).pack(pady=(0, 5))
        ctk.CTkLabel(
            top, text="See if yuh look like de man or wah", font=("Arial", 14), text_color="#e0e0e0"
        ).pack(pady=(0, 15))
        body = ctk.CTkFrame(main, fg_color="transparent")
        body.pack(pady=25, padx=35, fill="both", expand=True)
        pics = ctk.CTkFrame(body, fg_color="transparent")
        pics.pack(fill="both", expand=True, pady=8)
        left_box = ctk.CTkFrame(pics, fg_color="#1a1a1a", corner_radius=12, border_width=2, border_color="#009E49")
        left_box.pack(side="left", padx=12, pady=8, fill="both", expand=True)
        left_top = ctk.CTkFrame(left_box, fg_color="#252525", corner_radius=8)
        left_top.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(
            left_top, text="YUH FACE", font=("Arial", 17, "bold"), text_color="#FCD116"
        ).pack(pady=8)
        self.user_pic = ctk.CTkLabel(
            left_box, text="Nuttin upload yet bai\nPut yuh face deh nah", font=("Arial", 15), text_color="#666666"
        )
        self.user_pic.pack(pady=25, expand=True)
        right_box = ctk.CTkFrame(pics, fg_color="#1a1a1a", corner_radius=12, border_width=2, border_color="#CE1126")
        right_box.pack(side="right", padx=12, pady=8, fill="both", expand=True)
        right_top = ctk.CTkFrame(right_box, fg_color="#252525", corner_radius=8)
        right_top.pack(fill="x", padx=12, pady=12)
        ctk.CTkLabel(
            right_top, text="DE REAL FAZO", font=("Arial", 17, "bold"), text_color="#FCD116"
        ).pack(pady=8)
        self.ref_pic = ctk.CTkLabel(
            right_box, text="Loading de man...", font=("Arial", 14), text_color="#666666"
        )
        self.ref_pic.pack(pady=25, expand=True)
        btn_area = ctk.CTkFrame(body, fg_color="transparent")
        btn_area.pack(pady=18)
        ctk.CTkButton(
            btn_area, text="UPLOAD YUH RASS", command=self.get_pic, font=("Arial", 16, "bold"), height=52, width=240, corner_radius=26, fg_color="#009E49", hover_color="#007a38", text_color="white"
        ).pack(side="left", padx=8)
        ctk.CTkButton(
            btn_area, text="RUN DE OBEAH", command=self.check_face, font=("Arial", 16, "bold"), height=52, width=240, corner_radius=26, fg_color="#CE1126", hover_color="#a00d1c", text_color="white"
        ).pack(side="right", padx=8)
        results = ctk.CTkFrame(body, fg_color="#1a1a1a", corner_radius=12, height=130, border_width=2, border_color="#FCD116")
        results.pack(fill="x", pady=18, padx=18)
        results.pack_propagate(False)
        self.output = ctk.CTkLabel(
            results, text="Upload yuh damn face fuh start nah man", font=("Arial", 18, "bold"), text_color="#888888", wraplength=800
        )
        self.output.pack(expand=True, pady=10)
        ctk.CTkLabel(
            main, text="Powered by pure obeah & AI black magic", font=("Arial", 10), text_color="#444444"
        ).pack(pady=8)

    def load_ref(self):
        if os.path.exists(self.reference_path):
            try:
                pic = self.round_img(self.reference_path)
                self.ref_pic.configure(image=pic, text="")
                self.ref_pic.image = pic
            except Exception as e:
                print(f"Error loading reference: {e}")
        else:
            self.ref_pic.configure(
                text="Wah de rass!\nfazo.png missing!\nPut de bloodclaat picture\nin de folder nah", text_color="#CE1126"
            )

    def get_pic(self):
        p = filedialog.askopenfilename(
            title="Pick yuh face nah", 
            filetypes=[("Pictures", "*.jpg *.jpeg *.png *.PNG *.JPG *.JPEG *.heic *.HEIC *.heif")]
        )
        if not p:
            return
        self.uploaded_path = p
        try:
            pic = self.round_img(p)
            self.user_pic.configure(image=pic, text="")
            self.user_pic.image = pic
            self.output.configure(
                text="Done! Now press de red button fuh run de obeah!", text_color="#009E49"
            )
        except Exception as e:
            messagebox.showerror("Wah de rass!", f"Dis picture mash up: {e}")

    def check_face(self):
        if not self.uploaded_path:
            messagebox.showwarning("Aye bai", "Upload yuh rass face first nah!")
            return
        if not os.path.exists(self.reference_path):
            messagebox.showerror("Wah de rass!", "fazo.png missing! Yuh mad or wah?")
            return
        self.output.configure(text="De obeah deh pon it...", text_color="#FCD116")
        self.window.update()
        try:
            u_pil = Image.open(self.uploaded_path).convert("RGB")
            u_img = np.array(u_pil)
            
            r_pil = Image.open(self.reference_path).convert("RGB")
            r_img = np.array(r_pil)
            
            u_locs = face_recognition.face_locations(u_img)
            u_faces = face_recognition.face_encodings(u_img, u_locs)
            r_faces = face_recognition.face_encodings(r_img)

            if len(u_faces) == 0:
                messagebox.showerror("Wah de ass?", "Me cyaan see no face! Yuh send bush picture or wah?")
                self.output.configure(text="Nah man, no face deh! Try again", text_color="#CE1126")
                return
            if len(r_faces) == 0:
                messagebox.showerror("Lawd have mercy!", "De reference picture cork up bad bad")
                self.output.configure(text="Reference ting mash up", text_color="#CE1126")
                return

            top, right, bottom, left = u_locs[0]
            face_pixels = u_img[top:bottom, left:right]
            avg_brightness = np.array(Image.fromarray(face_pixels).convert('L')).mean()
            
            pigment_multiplier = 1.0
            if avg_brightness < 90:    
                pigment_multiplier = 1.30
            elif avg_brightness < 135: 
                pigment_multiplier = 1.05

            u_face = u_faces[0]
            r_face = r_faces[0]
            dist = face_recognition.face_distance([r_face], u_face)[0]
            
            score = (((1 - dist) * 100) * 1.94) * pigment_multiplier
            
            if score > 100:
                score = 100

            if score >= 75:
                msg = "WHA DE RASS! YUH IS FAZO TWIN BAI! True bloodclaat skunt!"
                clr = "#00ff88"
            elif score >= 60:
                msg = "Aye bai, yuh kinda look like he, but yuh nah twins!"
                clr = "#FCD116"
            elif score >= 45:
                msg = "Ehhh… yuh lil bit like he, but doh lie, yuh nah Fazo."
                clr = "#ffaa00"
            elif score >= 30:
                msg = "Bai nah! Yuh doh look nuttin like he. Yuh look like old crappo pickney!"
                clr = "#ff6600"
            elif score >= 15:
                msg = "Bai stop de fuckry. Yuh nah Fazo, yuh look like rotten cassava, pure crappo!"
                clr = "#ff4444"
            else:
                msg = "Madness! YUH CRAPPO BAI! Yuh look like doh even wash yuh face today, nuttin like Fazo!"
                clr = "#CE1126"

            txt = f"{score:.1f}% Match\n{msg}"
            self.output.configure(text=txt, text_color=clr)
        except Exception as e:
            messagebox.showerror("Wah de rass!", f"De whole ting crash: {e}")
            self.output.configure(text="Ting cork up bad!", text_color="#CE1126")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FaceComparisonApp()
    app.run()
