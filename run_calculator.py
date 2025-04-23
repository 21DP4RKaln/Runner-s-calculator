import tkinter as tk
from tkinter import ttk, messagebox
import re
import math
import random
import time

class ModernRunnerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Skrējēja Kalkulators")
        self.root.geometry("1200x900")
        self.root.resizable(True, True)
        
        # Krāsu shēma - dark mode
        self.bg_color = "#121212"  # tumši pelēks/melns fons
        self.card_bg = "#1E1E1E"   # nedaudz gaišāks pelēks priekš kartēm
        self.primary_color = "#4169E1"  # royal blue
        self.secondary_color = "#9370DB"  # medium purple
        self.accent_color = "#7B68EE"  # medium slate blue
        self.text_color = "#E0E0E0"  # gandrīz balts teksts
        self.text_secondary = "#A0A0A0"  # sekundārais teksts
        
        # Fonts
        self.font_title = ("Helvetica", 20, "bold")
        self.font_subtitle = ("Helvetica", 14, "bold")
        self.font_normal = ("Helvetica", 12)
        self.font_small = ("Helvetica", 10)
        
        # Stils
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Izmantojam "clam" tēmu, ko var vieglāk pielāgot
        
        # Konfigurējam stilus
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg)
        
        self.style.configure("TLabel", 
                          background=self.bg_color, 
                          foreground=self.text_color, 
                          font=self.font_normal)
        
        self.style.configure("Card.TLabel", 
                          background=self.card_bg, 
                          foreground=self.text_color)
                          
        self.style.configure("Secondary.TLabel", 
                          background=self.bg_color, 
                          foreground=self.text_secondary, 
                          font=self.font_small)
        
        self.style.configure("TButton", 
                          font=self.font_normal, 
                          background=self.primary_color, 
                          foreground=self.text_color)
        
        self.style.map("TButton",
                    background=[('active', self.secondary_color)],
                    foreground=[('active', self.text_color)])
                    
        self.style.configure("Accent.TButton", 
                          background=self.accent_color, 
                          foreground=self.text_color)
        
        self.style.map("Accent.TButton",
                    background=[('active', self.secondary_color)],
                    foreground=[('active', self.text_color)])
                    
        self.style.configure("TEntry", 
                          fieldbackground=self.card_bg, 
                          foreground=self.text_color, 
                          insertcolor=self.text_color)
                          
        # Iestatīt fonu
        self.root.configure(bg=self.bg_color)
        
        # Parādīt sākuma ekrānu
        self.show_splash_screen()
        
    def show_splash_screen(self):
        """Parāda sākuma ekrānu ar animāciju"""
        # Notīrīt ekrānu, ja nepieciešams
        for widget in self.root.winfo_children():
            widget.destroy()
            
        splash_frame = ttk.Frame(self.root, style="TFrame")
        splash_frame.pack(fill=tk.BOTH, expand=True)
        
        # Izveidot Canvas gradientam
        gradient_canvas = tk.Canvas(splash_frame, width=600, height=100, bg=self.bg_color, highlightthickness=0)
        gradient_canvas.pack(pady=(80, 0))
        
        # Izveidot gradienta tekstu nosaukumam
        text_id = gradient_canvas.create_text(300, 50, text="Skrējēja Kalkulators", font=("Helvetica", 36, "bold"))
        
        # Krāsu gradients (no primary līdz secondary)
        def create_gradient():
            colors = []
            r1, g1, b1 = int(self.primary_color[1:3], 16), int(self.primary_color[3:5], 16), int(self.primary_color[5:], 16)
            r2, g2, b2 = int(self.secondary_color[1:3], 16), int(self.secondary_color[3:5], 16), int(self.secondary_color[5:], 16)
            r3, g3, b3 = int(self.accent_color[1:3], 16), int(self.accent_color[3:5], 16), int(self.accent_color[5:], 16)
            
            steps = 20
            for i in range(steps):
                # Linear interpolation no primary uz accent
                if i < steps/2:
                    t = (i / (steps/2))
                    r = int(r1 + t*(r3-r1))
                    g = int(g1 + t*(g3-g1))
                    b = int(b1 + t*(b3-b1))
                # Linear interpolation no accent uz secondary
                else:
                    t = ((i - steps/2) / (steps/2))
                    r = int(r3 + t*(r2-r3))
                    g = int(g3 + t*(g2-g3))
                    b = int(b3 + t*(b2-b3))
                    
                color = f"#{r:02x}{g:02x}{b:02x}"
                colors.append(color)
            return colors
                
        gradient_colors = create_gradient()
        
        # Animēt gradienta krāsu
        def animate_gradient():
            # Paņemt pirmo krāsu un pielikt beigās
            gradient_colors.append(gradient_colors.pop(0))
            
            gradient_canvas.itemconfig(text_id, fill=gradient_colors[0])
            gradient_canvas.after(100, animate_gradient)
            
        self.root.after(100, animate_gradient)
        
        # Apakšvirsraksts
        subtitle_label = ttk.Label(splash_frame, 
                                text="Plāno savus treniņus efektīvi", 
                                font=self.font_subtitle, 
                                foreground=self.text_secondary)
        subtitle_label.pack(pady=10)
        
        # Skrējēja animācija
        canvas = tk.Canvas(splash_frame, width=600, height=150, bg=self.bg_color, highlightthickness=0)
        canvas.pack(pady=20)
        
        runner_text = canvas.create_text(10, 75, text="🏃", font=("Arial", 40), fill=self.primary_color, anchor="w")
        finish_line = canvas.create_line(550, 50, 550, 100, width=3, fill=self.accent_color)
        
        # Progress bar
        progress_frame = ttk.Frame(splash_frame, style="TFrame")
        progress_frame.pack(pady=20)
        
        # Pielāgots progress bar ar minimālistisku stilu
        progress_bg = tk.Frame(progress_frame, width=400, height=6, bg=self.card_bg)
        progress_bg.pack(pady=10)
        
        progress_fg = tk.Frame(progress_bg, width=0, height=6, bg=self.accent_color)
        progress_fg.place(x=0, y=0)
        
        status_label = ttk.Label(progress_frame, 
                              text="Ielādējas...", 
                              font=self.font_small, 
                              foreground=self.text_secondary,
                              style="Secondary.TLabel")
        status_label.pack()

        # Start poga (sākotnēji neredzama)
        start_button = ttk.Button(splash_frame, 
                               text="Sākt Programmu", 
                               command=self.show_info,
                               style="Accent.TButton")
        start_button.pack(pady=20)
        start_button.pack_forget()  # Sākotnēji paslēpta
        
        # Autors
        author_label = ttk.Label(splash_frame, 
                              text="Izstrādātājs: Skrējēju atbalsta komanda", 
                              font=self.font_small, 
                              foreground=self.text_secondary,
                              style="Secondary.TLabel")
        author_label.pack(side=tk.BOTTOM, pady=10)
        
        # Animācija
        def animate_splash():
            nonlocal runner_text
            x_pos = canvas.coords(runner_text)[0]
            
            if x_pos < 530:  # Ja nav sasniegts finišs
                canvas.move(runner_text, 5, 0)  # Pakustēt pa labi
                canvas.after(30, animate_splash)  # Izsaukt funkciju atkal pēc 30ms
                
                # Atjaunot progress bar
                progress_val = min(100, int((x_pos / 530) * 100))
                progress_width = int((progress_val / 100) * 400)
                progress_fg.config(width=progress_width)
                
                # Atjaunot statusa tekstu
                loading_texts = [
                    "Ielādējas...", 
                    "Aprēķinu formulas tiek sagatavotas...",
                    "Skaitām distances...",
                    "Mērām tempus...",
                    "Gandrīz gatavs..."
                ]
                status_index = min(int(progress_val / 20), len(loading_texts)-1)
                status_label.config(text=loading_texts[status_index])
            else:
                # Animācija pabeigta, parādīt pogu
                status_label.config(text="Programma gatava!")
                start_button.pack(pady=20)
        
        # Sākt animāciju
        self.root.after(500, animate_splash)
    
    def show_info(self):
        """Parāda informāciju par programmu"""
        # Notīrīt ekrānu
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Galvenais konteiners
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Virsraksts ar gradient efektu
        title_canvas = tk.Canvas(main_frame, width=400, height=60, bg=self.bg_color, highlightthickness=0)
        title_canvas.pack(pady=(10, 30))
        
        title_text = title_canvas.create_text(200, 30, text="Par Programmu", 
                                           font=self.font_title, 
                                           fill=self.primary_color)
        
        # Informācijas rāmis
        info_frame = ttk.Frame(main_frame, style="Card.TFrame")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Programmas apraksts
        desc_text = """
        Šī programma ir radīta, lai palīdzētu skrējējiem plānot savus treniņus,
        aprēķinot nepieciešamos parametrus atkarībā no jūsu mērķiem.
        
        Ar šo kalkulatoru varat:
        """
        desc_label = ttk.Label(info_frame, 
                            text=desc_text, 
                            justify="left", 
                            wraplength=600,
                            style="Card.TLabel")
        desc_label.pack(anchor="w", pady=20, padx=20)
        
        # Funkcionalitātes saraksts ar ikonām
        features = [
            ("⏱️ Aprēķināt nepieciešamo tempu (min/km), ievadot distanci un laiku"),
            ("🕒 Aprēķināt paredzamo laiku (min), ievadot distanci un tempu"),
            ("📏 Aprēķināt iespējamo distanci (km), ievadot laiku un tempu")
        ]
        
        for feature in features:
            feature_frame = ttk.Frame(info_frame, style="Card.TFrame")
            feature_frame.pack(fill=tk.X, pady=5, anchor="w", padx=20)
            
            feature_label = ttk.Label(feature_frame, 
                                   text=feature, 
                                   justify="left", 
                                   wraplength=600,
                                   style="Card.TLabel")
            feature_label.pack(anchor="w", padx=20, pady=5)
        
        # Formulu piemēri
        formula_frame = ttk.Frame(info_frame, style="Card.TFrame")
        formula_frame.pack(fill=tk.X, pady=20, padx=20)
        
        formula_title = ttk.Label(formula_frame, 
                               text="Formulas:", 
                               font=self.font_subtitle,
                               foreground=self.secondary_color,
                               style="Card.TLabel")
        formula_title.pack(anchor="w", pady=(10, 5), padx=20)
        
        formulas = [
            "• Temps = Laiks (min) / Distance (km)",
            "• Laiks = Temps (min/km) × Distance (km)",
            "• Distance = Laiks (min) / Temps (min/km)"
        ]
        
        for formula in formulas:
            formula_label = ttk.Label(formula_frame, 
                                   text=formula, 
                                   justify="left",
                                   style="Card.TLabel")
            formula_label.pack(anchor="w", padx=20, pady=2)
        
        # Motivācijas citāts
        quote_frame = tk.Frame(info_frame, bg=self.card_bg, bd=0, highlightthickness=1, highlightbackground=self.secondary_color)
        quote_frame.pack(fill=tk.X, pady=20, padx=30)
        
        quote = self.get_random_quote()
        quote_label = tk.Label(quote_frame, 
                            text=f'"{quote}"', 
                            font=("Helvetica", 12, "italic"), 
                            fg=self.text_color, 
                            bg=self.card_bg)
        quote_label.pack(pady=15, padx=10)
        
        # Pogas rāmis
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=30)
        
        # Sākt pogas
        start_button = ttk.Button(button_frame, 
                               text="Sākt Lietot Programmu", 
                               command=self.create_main_page,
                               style="Accent.TButton")
        start_button.pack(pady=10)
    
    def create_main_page(self):
        """Izveido galveno programmas lapu"""
        # Notīrīt ekrānu
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Izveidot dalītu skatu - kreisā puse navigācija, labā puse saturs
        main_container = ttk.Frame(self.root, style="TFrame")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Kreisā puse - izvēlne
        self.menu_frame = ttk.Frame(main_container, style="Card.TFrame", width=200)
        self.menu_frame.pack(fill=tk.Y, expand=False, side=tk.LEFT, padx=2, pady=2)
        
        # Nodrošināt, ka menu_frame saglabā savu platumu
        self.menu_frame.pack_propagate(False)
        
        # Labā puse - saturs
        self.content_frame = ttk.Frame(main_container, style="TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=2, pady=2)
        
        # Izvēlnes virsraksts
        menu_title = ttk.Label(self.menu_frame, 
                            text="Kalkulatori", 
                            font=self.font_subtitle, 
                            foreground=self.primary_color,
                            style="Card.TLabel")
        menu_title.pack(pady=(20, 20), padx=10)
        
        # Izvēlnes pogas
        menu_options = [
            ("Tempa Kalkulators", lambda: self.show_calculator("pace"), "⏱️"),
            ("Laika Kalkulators", lambda: self.show_calculator("time"), "🕒"),
            ("Distances Kalkulators", lambda: self.show_calculator("distance"), "📏"),
            ("Informācija", self.show_info, "ℹ️")
        ]
        
        for text, command, icon in menu_options:
            button_text = f"{icon} {text}"
            button = tk.Button(self.menu_frame, 
                            text=button_text, 
                            command=command,
                            font=self.font_normal, 
                            bg=self.card_bg, 
                            fg=self.text_color,
                            bd=0,
                            highlightthickness=0, 
                            activebackground=self.primary_color,
                            activeforeground=self.text_color,
                            width=20, 
                            anchor="w", 
                            padx=10, 
                            height=2)
            button.pack(fill=tk.X, pady=1)
        
        # Motivācijas citāts
        quote_frame = tk.Frame(self.menu_frame, bg=self.card_bg, bd=0, highlightthickness=1, highlightbackground=self.secondary_color)
        quote_frame.pack(fill=tk.X, pady=20, padx=10, side=tk.BOTTOM)
        
        quote = self.get_random_quote()
        quote_label = tk.Label(quote_frame, 
                            text=f'"{quote}"', 
                            font=("Helvetica", 10, "italic"), 
                            fg=self.text_secondary, 
                            bg=self.card_bg, 
                            wraplength=180)
        quote_label.pack(pady=10, padx=10)
        
        # Sākotnēji parādīt tempa kalkulatoru
        self.show_calculator("pace")
    
    def show_calculator(self, calc_type):
        """Parāda izvēlēto kalkulatoru"""
        # Notīrīt saturu
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Attēlot virsrakstu un saturu atkarībā no tipa
        if calc_type == "pace":
            self.create_pace_calculator()
        elif calc_type == "time":
            self.create_time_calculator()
        elif calc_type == "distance":
            self.create_distance_calculator()
    
    def create_pace_calculator(self):
        """Izveido tempa kalkulatora formu"""
        # Virsraksts
        title_frame = ttk.Frame(self.content_frame, style="TFrame")
        title_frame.pack(fill=tk.X, pady=(20, 30), padx=30)
        
        title_label = ttk.Label(title_frame, 
                             text="⏱️ Tempa Kalkulators", 
                             font=self.font_title, 
                             foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Apraksts
        desc_frame = ttk.Frame(self.content_frame, style="TFrame")
        desc_frame.pack(fill=tk.X, pady=5, padx=30)
        
        desc_text = "Aprēķini nepieciešamo tempu, lai sasniegtu mērķa distanci noteiktā laikā."
        desc_label = ttk.Label(desc_frame, text=desc_text, wraplength=500)
        desc_label.pack(anchor="w")
        
        # Formula
        formula_frame = ttk.Frame(self.content_frame, style="TFrame")
        formula_frame.pack(fill=tk.X, pady=5, padx=30)
        
        formula_text = "Formula: Temps = Laiks / Distance"
        formula_label = ttk.Label(formula_frame, 
                               text=formula_text, 
                               font=self.font_small, 
                               foreground=self.text_secondary,
                               style="Secondary.TLabel")
        formula_label.pack(anchor="w")
        
        # Ievades lauki
        input_frame = ttk.Frame(self.content_frame, style="TFrame")
        input_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Stila rāmis
        entry_style_frame = ttk.Frame(input_frame, style="Card.TFrame")
        entry_style_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Distance
        distance_frame = ttk.Frame(entry_style_frame, style="Card.TFrame")
        distance_frame.pack(fill=tk.X, pady=15, padx=20)
        
        distance_label = ttk.Label(distance_frame, 
                                text="Distance (km):", 
                                width=20, 
                                anchor="w",
                                style="Card.TLabel")
        distance_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Pielāgots input lauks
        distance_var = tk.StringVar()
        distance_entry = tk.Entry(distance_frame, 
                               textvariable=distance_var, 
                               width=15,
                               bg=self.bg_color,
                               fg=self.text_color,
                               insertbackground=self.text_color,
                               relief="flat",
                               highlightthickness=1,
                               highlightcolor=self.primary_color,
                               highlightbackground=self.secondary_color)
        distance_entry.pack(side=tk.LEFT)
        
        distance_example = ttk.Label(distance_frame, 
                                  text="Piemērs: 5", 
                                  font=self.font_small, 
                                  foreground=self.text_secondary,
                                  style="Secondary.TLabel")
        distance_example.pack(side=tk.LEFT, padx=10)
        
        # Laiks
        time_frame = ttk.Frame(entry_style_frame, style="Card.TFrame")
        time_frame.pack(fill=tk.X, pady=15, padx=20)
        
        time_label = ttk.Label(time_frame, 
                            text="Laiks (hh:mm:ss):", 
                            width=20, 
                            anchor="w",
                            style="Card.TLabel")
        time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        time_var = tk.StringVar()
        time_entry = tk.Entry(time_frame, 
                           textvariable=time_var, 
                           width=15,
                           bg=self.bg_color,
                           fg=self.text_color,
                           insertbackground=self.text_color,
                           relief="flat",
                           highlightthickness=1,
                           highlightcolor=self.primary_color,
                           highlightbackground=self.secondary_color)
        time_entry.pack(side=tk.LEFT)
        
        time_example = ttk.Label(time_frame, 
                              text="Piemērs: 00:35:00 vai 35:00", 
                              font=self.font_small, 
                              foreground=self.text_secondary,
                              style="Secondary.TLabel")
        time_example.pack(side=tk.LEFT, padx=10)
        
        # Rezultāts
        result_frame = ttk.Frame(self.content_frame, style="TFrame")
        result_frame.pack(fill=tk.X, pady=20, padx=30)
        
        result_bg = tk.Frame(result_frame, bg=self.card_bg, bd=0)
        result_bg.pack(fill=tk.X)
        
        self.result_label = tk.Label(result_bg, 
                                  text="Rezultāts parādīsies šeit", 
                                  font=self.font_subtitle, 
                                  fg=self.text_secondary,
                                  bg=self.card_bg, 
                                  padx=20, 
                                  pady=20)
        self.result_label.pack(fill=tk.X)
        
        # Vizualizācija
        visual_frame = ttk.Frame(self.content_frame, style="Card.TFrame")
        visual_frame.pack(fill=tk.X, pady=10, padx=30)
        
        canvas = tk.Canvas(visual_frame, 
                        width=500, 
                        height=100, 
                        bg=self.card_bg, 
                        highlightthickness=0)
        canvas.pack(padx=20, pady=20)
        
        # Zīmēsim skrējēja ikonu un rezultātu vizualizāciju
        runner_icon = canvas.create_text(40, 50, text="🏃", font=("Arial", 24))
        track = canvas.create_line(80, 50, 480, 50, width=2, fill=self.text_secondary)
        
        # Pogas
        button_frame = ttk.Frame(self.content_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=20, padx=30)
        
        calculate_button = ttk.Button(button_frame, 
                                   text="Aprēķināt Tempu", 
                                   style="Accent.TButton")
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, text="Notīrīt")
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Papildu informācija
        info_frame = ttk.Frame(self.content_frame, style="TFrame")
        info_frame.pack(fill=tk.X, pady=10, padx=30, side=tk.BOTTOM)
        
        info_text = "Padoms: Ievadiet distanci un vēlamo laiku, lai aprēķinātu nepieciešamo tempu."
        info_label = ttk.Label(info_frame, 
                            text=info_text, 
                            font=self.font_small, 
                            foreground=self.text_secondary,
                            style="Secondary.TLabel")
        info_label.pack(anchor="w")
        
        # Funkcijas
        def calculate():
            """Aprēķina tempu"""
            distance_str = distance_var.get().strip()
            time_str = time_var.get().strip()
            
            try:
                # Pārbaudīt distanci
                if not distance_str:
                    raise ValueError("Distance nav ievadīta.")
                distance = float(distance_str.replace(',', '.'))
                if distance <= 0:
                    raise ValueError("Distancei jābūt pozitīvam skaitlim.")
                
                # Pārbaudīt laiku
                if not time_str:
                    raise ValueError("Laiks nav ievadīts.")
                
                # Laika pārbaude un pārvēršana minūtēs
                time_in_minutes = self.parse_time_to_minutes(time_str)
                if time_in_minutes <= 0:
                    raise ValueError("Laikam jābūt pozitīvam.")
                
                # Aprēķināt tempu
                pace_in_minutes = time_in_minutes / distance
                
                # Formatēt tempu
                pace_formatted = self.format_minutes_to_time(pace_in_minutes)
                
                # Parādīt rezultātu
                self.result_label.config(text=f"Jūsu temps: {pace_formatted} min/km", 
                                       fg=self.text_color, 
                                       bg=self.card_bg)
                
                # Atjaunot vizualizāciju
                self.update_pace_visualization(canvas, runner_icon, pace_in_minutes)
                
            except ValueError as e:
                messagebox.showerror("Kļūda", str(e))
            except Exception as e:
                messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
        
        def reset():
            """Notīrīt ievades laukus"""
            distance_var.set("")
            time_var.set("")
            self.result_label.config(text="Rezultāts parādīsies šeit", 
                                  fg=self.text_secondary, 
                                  bg=self.card_bg)
            
            # Atiestatīt vizualizāciju
            canvas.coords(runner_icon, 40, 50)
            canvas.delete("pace_indicator")
        
        # Piesaistīt funkcijas pogām
        calculate_button.config(command=calculate)
        reset_button.config(command=reset)
    
    def create_time_calculator(self):
        """Izveido laika kalkulatora formu"""
        # Virsraksts
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill=tk.X, pady=(20, 30), padx=30)
        
        title_label = ttk.Label(title_frame, text="🕒 Laika Kalkulators", font=self.font_title, foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Apraksts
        desc_frame = ttk.Frame(self.content_frame)
        desc_frame.pack(fill=tk.X, pady=10, padx=30)
        
        desc_text = "Aprēķini, cik ilgs laiks būs nepieciešams, lai noskrietu norādīto distanci ar noteiktu tempu."
        desc_label = ttk.Label(desc_frame, text=desc_text, wraplength=500)
        desc_label.pack(anchor="w")
        
        # Formula
        formula_frame = ttk.Frame(self.content_frame)
        formula_frame.pack(fill=tk.X, pady=10, padx=30)
        
        formula_text = "Formula: Laiks = Temps × Distance"
        formula_label = ttk.Label(formula_frame, text=formula_text, font=self.font_small, foreground="#666666")
        formula_label.pack(anchor="w")
        
        # Ievades lauki
        input_frame = ttk.Frame(self.content_frame)
        input_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Stila rāmis
        entry_style_frame = ttk.Frame(input_frame, style="Card.TFrame")
        entry_style_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Distance
        distance_frame = ttk.Frame(entry_style_frame)
        distance_frame.pack(fill=tk.X, pady=10, padx=20)
        
        distance_label = ttk.Label(distance_frame, text="Distance (km):", width=20, anchor="w")
        distance_label.pack(side=tk.LEFT, padx=(0, 10))
        
        distance_var = tk.StringVar()
        distance_entry = ttk.Entry(distance_frame, textvariable=distance_var, width=15)
        distance_entry.pack(side=tk.LEFT)
        
        distance_example = ttk.Label(distance_frame, text="Piemērs: 10", font=self.font_small, foreground="#888888")
        distance_example.pack(side=tk.LEFT, padx=10)
        
        # Temps
        pace_frame = ttk.Frame(entry_style_frame)
        pace_frame.pack(fill=tk.X, pady=10, padx=20)
        
        pace_label = ttk.Label(pace_frame, text="Temps (min/km):", width=20, anchor="w")
        pace_label.pack(side=tk.LEFT, padx=(0, 10))
        
        pace_var = tk.StringVar()
        pace_entry = ttk.Entry(pace_frame, textvariable=pace_var, width=15)
        pace_entry.pack(side=tk.LEFT)
        
        pace_example = ttk.Label(pace_frame, text="Piemērs: 6:30", font=self.font_small, foreground="#888888")
        pace_example.pack(side=tk.LEFT, padx=10)
        
        # Rezultāts
        result_frame = ttk.Frame(self.content_frame)
        result_frame.pack(fill=tk.X, pady=20, padx=30)
        
        result_label = ttk.Label(result_frame, text="Rezultāts parādīsies šeit", 
                               font=self.font_subtitle, foreground="#888888",
                               background="#f0f0f0", padding=20)
        result_label.pack(fill=tk.X)
        
        # Vizualizācija
        visual_frame = ttk.Frame(self.content_frame)
        visual_frame.pack(fill=tk.X, pady=10, padx=30)
        
        canvas = tk.Canvas(visual_frame, width=500, height=100, bg=self.bg_color, highlightthickness=0)
        canvas.pack()
        
        # Pulksteņa ikona un laika vizualizācija
        clock_icon = canvas.create_text(50, 50, text="⏱️", font=("Arial", 24))
        timeline = canvas.create_line(80, 50, 480, 50, width=2, fill="#cccccc")
        
        # Pogas
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=20, padx=30)
        
        calculate_button = ttk.Button(button_frame, text="Aprēķināt Laiku", 
                                    style="Accent.TButton")
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, text="Notīrīt")
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Papildu informācija
        info_frame = ttk.Frame(self.content_frame)
        info_frame.pack(fill=tk.X, pady=10, padx=30, side=tk.BOTTOM)
        
        info_text = "Padoms: Ievadiet distanci un tempu, lai aprēķinātu, cik ilgs laiks būs nepieciešams."
        info_label = ttk.Label(info_frame, text=info_text, font=self.font_small, foreground="#888888")
        info_label.pack(anchor="w")
        
        # Funkcijas
        def calculate():
            """Aprēķina laiku"""
            distance_str = distance_var.get().strip()
            pace_str = pace_var.get().strip()
            
            try:
                # Pārbaudīt distanci
                if not distance_str:
                    raise ValueError("Distance nav ievadīta.")
                distance = float(distance_str.replace(',', '.'))
                if distance <= 0:
                    raise ValueError("Distancei jābūt pozitīvam skaitlim.")
                
                # Pārbaudīt tempu
                if not pace_str:
                    raise ValueError("Temps nav ievadīts.")
                
                # Tempa pārbaude un pārvēršana minūtēs
                pace_in_minutes = self.parse_pace_to_minutes(pace_str)
                if pace_in_minutes <= 0:
                    raise ValueError("Tempam jābūt pozitīvam.")
                
                # Aprēķināt laiku
                time_in_minutes = pace_in_minutes * distance
                
                # Formatēt laiku
                time_formatted = self.format_minutes_to_time(time_in_minutes)
                
                # Parādīt rezultātu
                result_label.config(text=f"Jūsu laiks: {time_formatted}", 
                                   foreground="#000000", background="#d4edda")
                
                # Atjaunot vizualizāciju
                self.update_time_visualization(canvas, clock_icon, time_in_minutes)
                
            except ValueError as e:
                messagebox.showerror("Kļūda", str(e))
            except Exception as e:
                messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
        
        def reset():
            """Notīrīt ievades laukus"""
            distance_var.set("")
            pace_var.set("")
            result_label.config(text="Rezultāts parādīsies šeit", 
                              foreground="#888888", background="#f0f0f0")
            
            # Atiestatīt vizualizāciju
            canvas.coords(clock_icon, 50, 50)
            canvas.delete("time_indicator")

        # Piesaistīt funkcijas pogām
        calculate_button.config(command=calculate)
        reset_button.config(command=reset)
    
    def create_distance_calculator(self):
        """Izveido distances kalkulatora formu"""
        # Virsraksts
        title_frame = ttk.Frame(self.content_frame)
        title_frame.pack(fill=tk.X, pady=(20, 30), padx=30)
        
        title_label = ttk.Label(title_frame, text="📏 Distances Kalkulators", font=self.font_title, foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Apraksts
        desc_frame = ttk.Frame(self.content_frame)
        desc_frame.pack(fill=tk.X, pady=10, padx=30)
        
        desc_text = "Aprēķini, cik lielu distanci var noskriet noteiktā laikā ar konkrētu tempu."
        desc_label = ttk.Label(desc_frame, text=desc_text, wraplength=500)
        desc_label.pack(anchor="w")
        
        # Formula
        formula_frame = ttk.Frame(self.content_frame)
        formula_frame.pack(fill=tk.X, pady=10, padx=30)
        
        formula_text = "Formula: Distance = Laiks / Temps"
        formula_label = ttk.Label(formula_frame, text=formula_text, font=self.font_small, foreground="#666666")
        formula_label.pack(anchor="w")
        
        # Ievades lauki
        input_frame = ttk.Frame(self.content_frame)
        input_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Stila rāmis
        entry_style_frame = ttk.Frame(input_frame, style="Card.TFrame")
        entry_style_frame.pack(fill=tk.X, pady=10, padx=10)
        
        # Laiks
        time_frame = ttk.Frame(entry_style_frame)
        time_frame.pack(fill=tk.X, pady=10, padx=20)
        
        time_label = ttk.Label(time_frame, text="Laiks (hh:mm:ss):", width=20, anchor="w")
        time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        time_var = tk.StringVar()
        time_entry = ttk.Entry(time_frame, textvariable=time_var, width=15)
        time_entry.pack(side=tk.LEFT)
        
        time_example = ttk.Label(time_frame, text="Piemērs: 01:30:00 vai 45:00", font=self.font_small, foreground="#888888")
        time_example.pack(side=tk.LEFT, padx=10)
        
        # Temps
        pace_frame = ttk.Frame(entry_style_frame)
        pace_frame.pack(fill=tk.X, pady=10, padx=20)
        
        pace_label = ttk.Label(pace_frame, text="Temps (min/km):", width=20, anchor="w")
        pace_label.pack(side=tk.LEFT, padx=(0, 10))
        
        pace_var = tk.StringVar()
        pace_entry = ttk.Entry(pace_frame, textvariable=pace_var, width=15)
        pace_entry.pack(side=tk.LEFT)
        
        pace_example = ttk.Label(pace_frame, text="Piemērs: 5:45", font=self.font_small, foreground="#888888")
        pace_example.pack(side=tk.LEFT, padx=10)
        
        # Rezultāts
        result_frame = ttk.Frame(self.content_frame)
        result_frame.pack(fill=tk.X, pady=20, padx=30)
        
        result_label = ttk.Label(result_frame, text="Rezultāts parādīsies šeit", 
                         font=self.font_subtitle, foreground="#888888",
                         background="#f0f0f0", padding=20)
        result_label.pack(fill=tk.X)
        
        # Vizualizācija
        visual_frame = ttk.Frame(self.content_frame)
        visual_frame.pack(fill=tk.X, pady=10, padx=30)
        
        canvas = tk.Canvas(visual_frame, width=500, height=100, bg=self.bg_color, highlightthickness=0)
        canvas.pack()
        
        # Distances ikona un vizualizācija
        distance_icon = canvas.create_text(50, 50, text="📏", font=("Arial", 24))
        track = canvas.create_line(80, 50, 480, 50, width=2, fill="#cccccc")
        
        # Pogas
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(fill=tk.X, pady=20, padx=30)
        
        calculate_button = ttk.Button(button_frame, text="Aprēķināt Distanci", 
                                style="Accent.TButton")
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, text="Notīrīt")
        reset_button.pack(side=tk.LEFT, padx=5)
        
        # Papildu informācija
        info_frame = ttk.Frame(self.content_frame)
        info_frame.pack(fill=tk.X, pady=10, padx=30, side=tk.BOTTOM)
        
        info_text = "Padoms: Ievadiet laiku un tempu, lai aprēķinātu, cik lielu distanci var noskriet."
        info_label = ttk.Label(info_frame, text=info_text, font=self.font_small, foreground="#888888")
        info_label.pack(anchor="w")
        
        # Funkcijas
        def calculate():
            """Aprēķina distanci"""
            time_str = time_var.get().strip()
            pace_str = pace_var.get().strip()
            
            try:
                # Pārbaudīt laiku
                if not time_str:
                    raise ValueError("Laiks nav ievadīts.")
                
                # Laika pārbaude un pārvēršana minūtēs
                time_in_minutes = self.parse_time_to_minutes(time_str)
                if time_in_minutes <= 0:
                    raise ValueError("Laikam jābūt pozitīvam.")
                
                # Pārbaudīt tempu
                if not pace_str:
                    raise ValueError("Temps nav ievadīts.")
                
                # Tempa pārbaude un pārvēršana minūtēs
                pace_in_minutes = self.parse_pace_to_minutes(pace_str)
                if pace_in_minutes <= 0:
                    raise ValueError("Tempam jābūt pozitīvam.")
                
                # Aprēķināt distanci
                distance = time_in_minutes / pace_in_minutes
                
                # Parādīt rezultātu
                result_label.config(text=f"Jūsu distance: {distance:.2f} km", 
                               foreground="#000000", background="#d4edda")
                
                # Atjaunot vizualizāciju
                self.update_distance_visualization(canvas, distance_icon, distance)
                
            except ValueError as e:
                messagebox.showerror("Kļūda", str(e))
            except Exception as e:
                messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
        
        def reset():
            """Notīrīt ievades laukus"""
            time_var.set("")
            pace_var.set("")
            result_label.config(text="Rezultāts parādīsies šeit", 
                          foreground="#888888", background="#f0f0f0")
            
            # Atiestatīt vizualizāciju
            canvas.coords(distance_icon, 50, 50)
            canvas.delete("distance_indicator")
        
        # Piesaistīt funkcijas pogām
        calculate_button.config(command=calculate)
        reset_button.config(command=reset)

    def parse_time_to_minutes(self, time_str):
        """Pārveido laika virkni (hh:mm:ss vai mm:ss) minūtēs"""
        try:
            # Atdalīt laika komponentes
            parts = time_str.split(':')
            
            if len(parts) == 3:  # hh:mm:ss
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = int(parts[2])
                return hours * 60 + minutes + seconds / 60
            elif len(parts) == 2:  # mm:ss
                minutes = int(parts[0])
                seconds = int(parts[1])
                return minutes + seconds / 60
            elif len(parts) == 1:  # tikai minūtes
                return float(parts[0])
            else:
                raise ValueError("Nepareizs laika formāts. Izmantojiet hh:mm:ss vai mm:ss.")
        except Exception:
            raise ValueError("Nepareizs laika formāts. Izmantojiet hh:mm:ss vai mm:ss.")

    def parse_pace_to_minutes(self, pace_str):
        """Pārveido tempa virkni (mm:ss) minūtēs"""
        try:
            # Atdalīt tempa komponentes
            parts = pace_str.split(':')
            
            if len(parts) == 2:  # mm:ss
                minutes = int(parts[0])
                seconds = int(parts[1])
                return minutes + seconds / 60
            elif len(parts) == 1:  # tikai minūtes
                return float(parts[0])
            else:
                raise ValueError("Nepareizs tempa formāts. Izmantojiet mm:ss.")
        except Exception:
            raise ValueError("Nepareizs tempa formāts. Izmantojiet mm:ss.")

    def format_minutes_to_time(self, minutes):
        """Formatē minūtes kā mm:ss"""
        total_seconds = int(minutes * 60)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"

    def update_pace_visualization(self, canvas, runner_icon, pace_minutes):
        """Atjauno tempa vizualizāciju"""
        # Notīrīt iepriekšējo vizualizāciju
        canvas.delete("pace_indicator")
        
        # Aprēķināt ātruma vizualizāciju (apgriezti - mazāks temps = ātrāk)
        min_pace = 4  # ātrākais temps, ko vizualizēt (4 min/km)
        max_pace = 10  # lēnākais temps, ko vizualizēt (10 min/km)
        
        # Normalizēt tempu
        normalized_pace = min(max(pace_minutes, min_pace), max_pace)
        
        # Aprēķināt pozīciju (apgriezts - mazāks temps = tālāk pa labi)
        position = 480 - ((normalized_pace - min_pace) / (max_pace - min_pace)) * 400
        
        # Pārvietot skrējēja ikonu
        canvas.coords(runner_icon, position, 50)
        
        # Pievienot tempa indikatoru
        canvas.create_line(position, 45, position, 55, width=2, fill=self.secondary_color, tags="pace_indicator")
        canvas.create_text(position, 30, text=f"{self.format_minutes_to_time(pace_minutes)} min/km", 
                          font=self.font_small, fill=self.primary_color, tags="pace_indicator")

    def update_time_visualization(self, canvas, clock_icon, time_minutes):
        """Atjauno laika vizualizāciju"""
        # Notīrīt iepriekšējo vizualizāciju
        canvas.delete("time_indicator")
        
        # Aprēķināt laika vizualizāciju
        min_time = 15  # minimālais laiks, ko vizualizēt (15 min)
        max_time = 120  # maksimālais laiks, ko vizualizēt (2h)
        
        # Normalizēt laiku
        normalized_time = min(max(time_minutes, min_time), max_time)
        
        # Aprēķināt pozīciju
        position = 80 + ((normalized_time - min_time) / (max_time - min_time)) * 400
        
        # Pievienot laika indikatoru
        canvas.create_line(position, 45, position, 55, width=2, fill=self.secondary_color, tags="time_indicator")
        
        # Formatēt laiku hh:mm formātā
        hours = int(time_minutes) // 60
        minutes = int(time_minutes) % 60
        time_str = f"{hours}:{minutes:02d}" if hours > 0 else f"{minutes} min"
        
        canvas.create_text(position, 30, text=time_str, 
                          font=self.font_small, fill=self.primary_color, tags="time_indicator")

    def update_distance_visualization(self, canvas, distance_icon, distance):
        """Atjauno distances vizualizāciju"""
        # Notīrīt iepriekšējo vizualizāciju
        canvas.delete("distance_indicator")
        
        # Aprēķināt distances vizualizāciju
        min_distance = 1  # minimālā distance, ko vizualizēt (1 km)
        max_distance = 42  # maksimālā distance, ko vizualizēt (maratons 42 km)
        
        # Normalizēt distanci
        normalized_distance = min(max(distance, min_distance), max_distance)
        
        # Aprēķināt pozīciju
        position = 80 + ((normalized_distance - min_distance) / (max_distance - min_distance)) * 400
        
        # Pievienot distances indikatoru
        canvas.create_line(position, 45, position, 55, width=2, fill=self.secondary_color, tags="distance_indicator")
        canvas.create_text(position, 30, text=f"{distance:.2f} km", 
                          font=self.font_small, fill=self.primary_color, tags="distance_indicator")

    def get_random_quote(self):
        """Atgriež nejauši izvēlētu motivējošu citātu"""
        quotes = [
            "Dzīve ir kā maratons, ne sprints.",
            "Katrs solis tevi tuvina mērķim.",
            "Skrējiens ir kā dzīve, tam nepieciešama disciplīna.",
            "Svarīgākais ir neapstāties.",
            "Labāk lēni skriet, nekā vispār neskriet.",
            "Vislielākā uzvara ir uzvara pār sevi.",
            "Mērķis nav vienmēr tikai finišs, bet gan ceļš.",
            "Patiess skrējējs sacenšas tikai ar sevi.",
            "Labs temps nozīmē saprātīgu piepūli.",
            "Katrs kilometrs ir sasniegums."
        ]
        return random.choice(quotes)

# Palaist programmu
if __name__ == "__main__":
    root = tk.Tk()
    app = ModernRunnerCalculator(root)
    root.mainloop()