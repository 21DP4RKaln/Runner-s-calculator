import tkinter as tk
from tkinter import ttk, messagebox
import re
import math

class RunnerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Skrējēja Kalkulators")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Krāsu shēma
        self.bg_color = "#1E1E1E"  # tumši pelēks fons
        self.card_bg = "#2D2D30"   # nedaudz gaišāks pelēks priekš kartēm
        self.primary_color = "#FFD700"  # dzeltens (gold)
        self.accent_color = "#FFC000"  # nedaudz tumšāks dzeltens
        self.text_color = "#F0F0F0"  # gandrīz balts teksts
        self.text_secondary = "#A0A0A0"  # sekundārais teksts
        
        # Fonts
        self.font_title = ("Arial", 18, "bold")
        self.font_subtitle = ("Arial", 12, "bold")
        self.font_normal = ("Arial", 11)
        self.font_small = ("Arial", 9)
        
        # Stils
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Konfigurējam stilus
        self.configure_styles()
        
        # Iestatīt fonu
        self.root.configure(bg=self.bg_color)
        
        # Parādīt sākuma lapu
        self.show_start_page()
        
    def configure_styles(self):
        """Konfigurē visus TTK stilus"""
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_bg)
        
        self.style.configure("TLabel", 
                          background=self.bg_color, 
                          foreground=self.text_color, 
                          font=self.font_normal)
        
        self.style.configure("Card.TLabel", 
                          background=self.card_bg, 
                          foreground=self.text_color)
        
        self.style.configure("TButton", 
                          font=self.font_normal, 
                          background=self.primary_color, 
                          foreground="#000000")
        
        self.style.map("TButton",
                    background=[('active', self.accent_color)],
                    foreground=[('active', "#000000")])
        
        self.style.configure("TEntry", 
                          fieldbackground=self.card_bg, 
                          foreground=self.text_color)
                          
        # Spinbox stils
        self.style.configure("TSpinbox", 
                          fieldbackground=self.card_bg,
                          foreground=self.text_color,
                          arrowcolor=self.primary_color)
    
    def create_main_page(self):
        """Izveido galveno programmas lapu"""
        # Notīrīt ekrānu ja nepieciešams
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Izveidot dalītu skatu - kreisā puse navigācija, labā puse saturs
        main_container = ttk.Frame(self.root, style="TFrame")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Kreisā puse - izvēlne
        self.menu_frame = ttk.Frame(main_container, style="Card.TFrame", width=180)
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
            ("Distances Kalkulators", lambda: self.show_calculator("distance"), "📏")
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
                            activeforeground="#000000",
                            width=18, 
                            anchor="w", 
                            padx=10)
            button.pack(fill=tk.X, pady=1)
          # Atstarpe pirms atgriešanās pogas (Spacer)
        spacer = ttk.Frame(self.menu_frame, style="Card.TFrame", height=30)
        spacer.pack(fill=tk.X, pady=10)
        
        # Poga atgriezties uz sākumlapu
        home_button = tk.Button(self.menu_frame, 
                            text="🏠 Atgriezties sākumā", 
                            command=self.show_start_page,
                            font=self.font_normal, 
                            bg=self.card_bg, 
                            fg=self.primary_color, 
                            bd=0,
                            highlightthickness=0, 
                            activebackground=self.primary_color,
                            activeforeground="#000000",
                            width=18, 
                            anchor="w", 
                            padx=10)
        home_button.pack(fill=tk.X, side=tk.BOTTOM, padx=0, pady=(0, 10))
        
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
        title_frame.pack(fill=tk.X, pady=(20, 20), padx=30)
        
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
                               foreground=self.text_secondary)
        formula_label.pack(anchor="w")
        
        # Ievades lauki
        input_frame = ttk.Frame(self.content_frame, style="Card.TFrame")
        input_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Distance
        distance_frame = ttk.Frame(input_frame, style="Card.TFrame")
        distance_frame.pack(fill=tk.X, pady=15, padx=20)
        
        distance_label = ttk.Label(distance_frame, 
                                text="Distance (km):", 
                                width=16, 
                                anchor="w",
                                style="Card.TLabel")
        distance_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Pielāgots input lauks
        distance_var = tk.StringVar()
        distance_entry = tk.Entry(distance_frame, 
                               textvariable=distance_var, 
                               width=10,
                               bg=self.bg_color,
                               fg=self.text_color,
                               insertbackground=self.text_color,
                               relief="flat",
                               highlightthickness=1,
                               highlightcolor=self.primary_color,
                               highlightbackground=self.accent_color)
        distance_entry.pack(side=tk.LEFT)
        
        distance_example = ttk.Label(distance_frame, 
                                  text="Piemērs: 5", 
                                  font=self.font_small, 
                                  foreground=self.text_secondary,
                                  style="Card.TLabel")
        distance_example.pack(side=tk.LEFT, padx=10)
        
        # Laiks - atsevišķi lauki stundām, minūtēm un sekundēm
        time_frame = ttk.Frame(input_frame, style="Card.TFrame")
        time_frame.pack(fill=tk.X, pady=15, padx=20)
        
        time_label = ttk.Label(time_frame, 
                            text="Laiks:", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Konteiners laika ievadei
        time_input_frame = ttk.Frame(time_frame, style="Card.TFrame")
        time_input_frame.pack(side=tk.LEFT)
        
        # Stundu ievade
        hours_var = tk.StringVar(value="0")
        hours_spinbox = ttk.Spinbox(time_input_frame, 
                                 from_=0, 
                                 to=23, 
                                 width=3,
                                 textvariable=hours_var,
                                 wrap=True)
        hours_spinbox.pack(side=tk.LEFT, padx=(0, 2))
        
        ttk.Label(time_input_frame, text=":", style="Card.TLabel").pack(side=tk.LEFT)
        
        # Minūšu ievade
        minutes_var = tk.StringVar(value="0")
        minutes_spinbox = ttk.Spinbox(time_input_frame, 
                                   from_=0, 
                                   to=59, 
                                   width=3,
                                   textvariable=minutes_var,
                                   wrap=True)
        minutes_spinbox.pack(side=tk.LEFT, padx=(2, 2))
        
        ttk.Label(time_input_frame, text=":", style="Card.TLabel").pack(side=tk.LEFT)
        
        # Sekunžu ievade
        seconds_var = tk.StringVar(value="0")
        seconds_spinbox = ttk.Spinbox(time_input_frame, 
                                   from_=0, 
                                   to=59, 
                                   width=3,
                                   textvariable=seconds_var,
                                   wrap=True)
        seconds_spinbox.pack(side=tk.LEFT, padx=(2, 0))
        
        time_format_label = ttk.Label(time_frame, 
                                   text="hh:mm:ss", 
                                   font=self.font_small, 
                                   foreground=self.text_secondary,
                                   style="Card.TLabel")
        time_format_label.pack(side=tk.LEFT, padx=10)
        
        # Rezultāts
        result_frame = ttk.Frame(self.content_frame, style="TFrame")
        result_frame.pack(fill=tk.X, pady=20, padx=30)
        
        result_bg = tk.Frame(result_frame, bg=self.card_bg, bd=0)
        result_bg.pack(fill=tk.X)
        
        self.pace_result_label = tk.Label(result_bg, 
                                    text="Rezultāts parādīsies šeit", 
                                    font=self.font_subtitle, 
                                    fg=self.text_secondary,
                                    bg=self.card_bg, 
                                    padx=20, 
                                    pady=20)
        self.pace_result_label.pack(fill=tk.X)
        
        # Pogas
        button_frame = ttk.Frame(self.content_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=20, padx=30)
        
        calculate_button = ttk.Button(button_frame, 
                                   text="Aprēķināt Tempu", 
                                   command=lambda: self.calculate_pace(distance_var, hours_var, minutes_var, seconds_var))
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, 
                               text="Notīrīt", 
                               command=lambda: self.reset_pace_fields(distance_var, hours_var, minutes_var, seconds_var))
        reset_button.pack(side=tk.LEFT, padx=5)
    
    def create_time_calculator(self):
        """Izveido laika kalkulatora formu"""
        # Virsraksts
        title_frame = ttk.Frame(self.content_frame, style="TFrame")
        title_frame.pack(fill=tk.X, pady=(20, 20), padx=30)
        
        title_label = ttk.Label(title_frame, 
                             text="🕒 Laika Kalkulators", 
                             font=self.font_title, 
                             foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Apraksts
        desc_frame = ttk.Frame(self.content_frame, style="TFrame")
        desc_frame.pack(fill=tk.X, pady=5, padx=30)
        
        desc_text = "Aprēķini laiku, kas nepieciešams, lai noskrietu noteiktu distanci ar konkrētu tempu."
        desc_label = ttk.Label(desc_frame, text=desc_text, wraplength=500)
        desc_label.pack(anchor="w")
        
        # Formula
        formula_frame = ttk.Frame(self.content_frame, style="TFrame")
        formula_frame.pack(fill=tk.X, pady=5, padx=30)
        
        formula_text = "Formula: Laiks = Temps × Distance"
        formula_label = ttk.Label(formula_frame, 
                               text=formula_text, 
                               font=self.font_small, 
                               foreground=self.text_secondary)
        formula_label.pack(anchor="w")
        
        # Ievades lauki
        input_frame = ttk.Frame(self.content_frame, style="Card.TFrame")
        input_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Distance
        distance_frame = ttk.Frame(input_frame, style="Card.TFrame")
        distance_frame.pack(fill=tk.X, pady=15, padx=20)
        
        distance_label = ttk.Label(distance_frame, 
                                text="Distance (km):", 
                                width=16, 
                                anchor="w",
                                style="Card.TLabel")
        distance_label.pack(side=tk.LEFT, padx=(0, 10))
        
        distance_var = tk.StringVar()
        distance_entry = tk.Entry(distance_frame, 
                               textvariable=distance_var, 
                               width=10,
                               bg=self.bg_color,
                               fg=self.text_color,
                               insertbackground=self.text_color,
                               relief="flat",
                               highlightthickness=1,
                               highlightcolor=self.primary_color,
                               highlightbackground=self.accent_color)
        distance_entry.pack(side=tk.LEFT)
        
        distance_example = ttk.Label(distance_frame, 
                                  text="Piemērs: 10", 
                                  font=self.font_small, 
                                  foreground=self.text_secondary,
                                  style="Card.TLabel")
        distance_example.pack(side=tk.LEFT, padx=10)
        
        # Temps - atsevišķi lauki minūtēm un sekundēm
        pace_frame = ttk.Frame(input_frame, style="Card.TFrame")
        pace_frame.pack(fill=tk.X, pady=15, padx=20)
        
        pace_label = ttk.Label(pace_frame, 
                            text="Temps (min/km):", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        pace_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Konteiners tempa ievadei
        pace_input_frame = ttk.Frame(pace_frame, style="Card.TFrame")
        pace_input_frame.pack(side=tk.LEFT)
        
        # Minūšu ievade
        pace_minutes_var = tk.StringVar(value="5")
        pace_minutes_spinbox = ttk.Spinbox(pace_input_frame, 
                                        from_=0, 
                                        to=59, 
                                        width=3,
                                        textvariable=pace_minutes_var,
                                        wrap=True)
        pace_minutes_spinbox.pack(side=tk.LEFT, padx=(0, 2))
        
        ttk.Label(pace_input_frame, text=":", style="Card.TLabel").pack(side=tk.LEFT)
        
        # Sekunžu ievade
        pace_seconds_var = tk.StringVar(value="30")
        pace_seconds_spinbox = ttk.Spinbox(pace_input_frame, 
                                        from_=0, 
                                        to=59, 
                                        width=3,
                                        textvariable=pace_seconds_var,
                                        wrap=True)
        pace_seconds_spinbox.pack(side=tk.LEFT, padx=(2, 0))
        
        pace_format_label = ttk.Label(pace_frame, 
                                   text="min:sec", 
                                   font=self.font_small, 
                                   foreground=self.text_secondary,
                                   style="Card.TLabel")
        pace_format_label.pack(side=tk.LEFT, padx=10)
        
        # Rezultāts
        result_frame = ttk.Frame(self.content_frame, style="TFrame")
        result_frame.pack(fill=tk.X, pady=20, padx=30)
        
        result_bg = tk.Frame(result_frame, bg=self.card_bg, bd=0)
        result_bg.pack(fill=tk.X)
        
        self.time_result_label = tk.Label(result_bg, 
                                       text="Rezultāts parādīsies šeit", 
                                       font=self.font_subtitle, 
                                       fg=self.text_secondary,
                                       bg=self.card_bg, 
                                       padx=20, 
                                       pady=20)
        self.time_result_label.pack(fill=tk.X)
        
        # Pogas
        button_frame = ttk.Frame(self.content_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=20, padx=30)
        
        calculate_button = ttk.Button(button_frame, 
                                   text="Aprēķināt Laiku", 
                                   command=lambda: self.calculate_time(distance_var, pace_minutes_var, pace_seconds_var))
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, 
                               text="Notīrīt", 
                               command=lambda: self.reset_time_fields(distance_var, pace_minutes_var, pace_seconds_var))
        reset_button.pack(side=tk.LEFT, padx=5)

    def create_distance_calculator(self):
        """Izveido distances kalkulatora formu"""
        # Virsraksts
        title_frame = ttk.Frame(self.content_frame, style="TFrame")
        title_frame.pack(fill=tk.X, pady=(20, 20), padx=30)
        
        title_label = ttk.Label(title_frame, 
                             text="📏 Distances Kalkulators", 
                             font=self.font_title, 
                             foreground=self.primary_color)
        title_label.pack(side=tk.LEFT)
        
        # Apraksts
        desc_frame = ttk.Frame(self.content_frame, style="TFrame")
        desc_frame.pack(fill=tk.X, pady=5, padx=30)
        
        desc_text = "Aprēķini, cik lielu distanci var noskriet noteiktā laikā ar konkrētu tempu."
        desc_label = ttk.Label(desc_frame, text=desc_text, wraplength=500)
        desc_label.pack(anchor="w")
        
        # Formula
        formula_frame = ttk.Frame(self.content_frame, style="TFrame")
        formula_frame.pack(fill=tk.X, pady=5, padx=30)
        
        formula_text = "Formula: Distance = Laiks / Temps"
        formula_label = ttk.Label(formula_frame, 
                               text=formula_text, 
                               font=self.font_small, 
                               foreground=self.text_secondary)
        formula_label.pack(anchor="w")
        
        # Ievades lauki
        input_frame = ttk.Frame(self.content_frame, style="Card.TFrame")
        input_frame.pack(fill=tk.X, pady=20, padx=30)
        
        # Laiks - atsevišķi lauki stundām, minūtēm un sekundēm
        time_frame = ttk.Frame(input_frame, style="Card.TFrame")
        time_frame.pack(fill=tk.X, pady=15, padx=20)
        
        time_label = ttk.Label(time_frame, 
                            text="Laiks:", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Konteiners laika ievadei
        time_input_frame = ttk.Frame(time_frame, style="Card.TFrame")
        time_input_frame.pack(side=tk.LEFT)
        
        # Stundu ievade
        hours_var = tk.StringVar(value="0")
        hours_spinbox = ttk.Spinbox(time_input_frame, 
                                 from_=0, 
                                 to=23, 
                                 width=3,
                                 textvariable=hours_var,
                                 wrap=True)
        hours_spinbox.pack(side=tk.LEFT, padx=(0, 2))
        
        ttk.Label(time_input_frame, text=":", style="Card.TLabel").pack(side=tk.LEFT)
        
        # Minūšu ievade
        minutes_var = tk.StringVar(value="45")
        minutes_spinbox = ttk.Spinbox(time_input_frame, 
                                   from_=0, 
                                   to=59, 
                                   width=3,
                                   textvariable=minutes_var,
                                   wrap=True)
        minutes_spinbox.pack(side=tk.LEFT, padx=(2, 2))
        
        ttk.Label(time_input_frame, text=":", style="Card.TLabel").pack(side=tk.LEFT)
        
        # Sekunžu ievade
        seconds_var = tk.StringVar(value="0")
        seconds_spinbox = ttk.Spinbox(time_input_frame, 
                                   from_=0, 
                                   to=59, 
                                   width=3,
                                   textvariable=seconds_var,
                                   wrap=True)
        seconds_spinbox.pack(side=tk.LEFT, padx=(2, 0))
        
        time_format_label = ttk.Label(time_frame, 
                                   text="hh:mm:ss", 
                                   font=self.font_small, 
                                   foreground=self.text_secondary,
                                   style="Card.TLabel")
        time_format_label.pack(side=tk.LEFT, padx=10)
        
        # Temps - atsevišķi lauki minūtēm un sekundēm
        pace_frame = ttk.Frame(input_frame, style="Card.TFrame")
        pace_frame.pack(fill=tk.X, pady=15, padx=20)
        
        pace_label = ttk.Label(pace_frame, 
                            text="Temps (min/km):", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        pace_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Konteiners tempa ievadei
        pace_input_frame = ttk.Frame(pace_frame, style="Card.TFrame")
        pace_input_frame.pack(side=tk.LEFT)
        
        # Minūšu ievade
        pace_minutes_var = tk.StringVar(value="5")
        pace_minutes_spinbox = ttk.Spinbox(pace_input_frame, 
                                        from_=0, 
                                        to=59, 
                                        width=3,
                                        textvariable=pace_minutes_var,
                                        wrap=True)
        pace_minutes_spinbox.pack(side=tk.LEFT, padx=(0, 2))
        
        ttk.Label(pace_input_frame, text=":", style="Card.TLabel").pack(side=tk.LEFT)
        
        # Sekunžu ievade
        pace_seconds_var = tk.StringVar(value="45")
        pace_seconds_spinbox = ttk.Spinbox(pace_input_frame, 
                                        from_=0, 
                                        to=59, 
                                        width=3,
                                        textvariable=pace_seconds_var,
                                        wrap=True)
        pace_seconds_spinbox.pack(side=tk.LEFT, padx=(2, 0))
        
        pace_format_label = ttk.Label(pace_frame, 
                                   text="min:sec", 
                                   font=self.font_small, 
                                   foreground=self.text_secondary,
                                   style="Card.TLabel")
        pace_format_label.pack(side=tk.LEFT, padx=10)
        
        # Rezultāts
        result_frame = ttk.Frame(self.content_frame, style="TFrame")
        result_frame.pack(fill=tk.X, pady=20, padx=30)
        
        result_bg = tk.Frame(result_frame, bg=self.card_bg, bd=0)
        result_bg.pack(fill=tk.X)
        
        self.distance_result_label = tk.Label(result_bg, 
                                          text="Rezultāts parādīsies šeit", 
                                          font=self.font_subtitle, 
                                          fg=self.text_secondary,
                                          bg=self.card_bg, 
                                          padx=20, 
                                          pady=20)
        self.distance_result_label.pack(fill=tk.X)
        
        # Pogas
        button_frame = ttk.Frame(self.content_frame, style="TFrame")
        button_frame.pack(fill=tk.X, pady=20, padx=30)
        
        calculate_button = ttk.Button(button_frame, 
                                   text="Aprēķināt Distanci", 
                                   command=lambda: self.calculate_distance(hours_var, minutes_var, seconds_var, 
                                                                        pace_minutes_var, pace_seconds_var))
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, 
                               text="Notīrīt", 
                               command=lambda: self.reset_distance_fields(hours_var, minutes_var, seconds_var, 
                                                                       pace_minutes_var, pace_seconds_var))
        reset_button.pack(side=tk.LEFT, padx=5)
    
    def calculate_pace(self, distance_var, hours_var, minutes_var, seconds_var):
        """Aprēķina tempu"""
        try:
            # Pārbaudīt distanci
            distance_str = distance_var.get().strip().replace(',', '.')
            if not distance_str:
                raise ValueError("Distance nav ievadīta.")
            
            try:
                distance = float(distance_str)
                if distance <= 0:
                    raise ValueError("Distancei jābūt pozitīvam skaitlim.")
            except ValueError:
                raise ValueError("Ievadītā distance nav derīgs skaitlis.")
            
            # Pārbaudīt laiku
            try:
                hours = int(hours_var.get())
                minutes = int(minutes_var.get())
                seconds = int(seconds_var.get())
                
                if hours < 0 or minutes < 0 or seconds < 0:
                    raise ValueError("Laika vērtībām jābūt pozitīvām.")
                
                if minutes >= 60 or seconds >= 60:
                    raise ValueError("Minūtēm un sekundēm jābūt mazākām par 60.")
                
                # Aprēķināt kopējo laiku minūtēs
                time_in_minutes = hours * 60 + minutes + seconds / 60
                
                if time_in_minutes <= 0:
                    raise ValueError("Kopējam laikam jābūt lielākam par nulli.")
            except ValueError as e:
                if "invalid literal for int()" in str(e):
                    raise ValueError("Laikam jābūt skaitlim.")
                else:
                    raise e
            
            # Aprēķināt tempu
            pace_in_minutes = time_in_minutes / distance
            
            # Formatēt tempu
            pace_minutes = int(pace_in_minutes)
            pace_seconds = int((pace_in_minutes - pace_minutes) * 60)
            pace_formatted = f"{pace_minutes}:{pace_seconds:02d}"
            
            # Parādīt rezultātu
            self.pace_result_label.config(
                text=f"Jūsu temps: {pace_formatted} min/km", 
                fg=self.primary_color
            )
            
        except ValueError as e:
            messagebox.showerror("Kļūda", str(e))
        except Exception as e:
            messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
    
    def calculate_time(self, distance_var, pace_minutes_var, pace_seconds_var):
        """Aprēķina laiku"""
        try:
            # Pārbaudīt distanci
            distance_str = distance_var.get().strip().replace(',', '.')
            if not distance_str:
                raise ValueError("Distance nav ievadīta.")
            
            try:
                distance = float(distance_str)
                if distance <= 0:
                    raise ValueError("Distancei jābūt pozitīvam skaitlim.")
            except ValueError:
                raise ValueError("Ievadītā distance nav derīgs skaitlis.")
            
            # Pārbaudīt tempu
            try:
                pace_minutes = int(pace_minutes_var.get())
                pace_seconds = int(pace_seconds_var.get())
                
                if pace_minutes < 0 or pace_seconds < 0:
                    raise ValueError("Tempa vērtībām jābūt pozitīvām.")
                
                if pace_seconds >= 60:
                    raise ValueError("Sekundēm jābūt mazākām par 60.")
                
                # Aprēķināt kopējo tempu minūtēs
                pace_in_minutes = pace_minutes + pace_seconds / 60
                
                if pace_in_minutes <= 0:
                    raise ValueError("Tempam jābūt lielākam par nulli.")
            except ValueError as e:
                if "invalid literal for int()" in str(e):
                    raise ValueError("Tempam jābūt skaitlim.")
                else:
                    raise e
            
            # Aprēķināt laiku
            time_in_minutes = pace_in_minutes * distance
            
            # Formatēt laiku
            hours = int(time_in_minutes // 60)
            minutes = int(time_in_minutes % 60)
            seconds = int((time_in_minutes - int(time_in_minutes)) * 60)
            
            # Rezultāta formatēšana
            if hours > 0:
                time_formatted = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                time_formatted = f"{minutes}:{seconds:02d}"
            
            # Parādīt rezultātu
            self.time_result_label.config(
                text=f"Jūsu laiks: {time_formatted}", 
                fg=self.primary_color
            )
            
        except ValueError as e:
            messagebox.showerror("Kļūda", str(e))
        except Exception as e:
            messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
    
    def calculate_distance(self, hours_var, minutes_var, seconds_var, pace_minutes_var, pace_seconds_var):
        """Aprēķina distanci"""
        try:
            # Pārbaudīt laiku
            try:
                hours = int(hours_var.get())
                minutes = int(minutes_var.get())
                seconds = int(seconds_var.get())
                
                if hours < 0 or minutes < 0 or seconds < 0:
                    raise ValueError("Laika vērtībām jābūt pozitīvām.")
                
                if minutes >= 60 or seconds >= 60:
                    raise ValueError("Minūtēm un sekundēm jābūt mazākām par 60.")
                
                # Aprēķināt kopējo laiku minūtēs
                time_in_minutes = hours * 60 + minutes + seconds / 60
                
                if time_in_minutes <= 0:
                    raise ValueError("Kopējam laikam jābūt lielākam par nulli.")
            except ValueError as e:
                if "invalid literal for int()" in str(e):
                    raise ValueError("Laikam jābūt skaitlim.")
                else:
                    raise e
            
            # Pārbaudīt tempu
            try:
                pace_minutes = int(pace_minutes_var.get())
                pace_seconds = int(pace_seconds_var.get())
                
                if pace_minutes < 0 or pace_seconds < 0:
                    raise ValueError("Tempa vērtībām jābūt pozitīvām.")
                
                if pace_seconds >= 60:
                    raise ValueError("Sekundēm jābūt mazākām par 60.")
                
                # Aprēķināt kopējo tempu minūtēs
                pace_in_minutes = pace_minutes + pace_seconds / 60
                
                if pace_in_minutes <= 0:
                    raise ValueError("Tempam jābūt lielākam par nulli.")
            except ValueError as e:
                if "invalid literal for int()" in str(e):
                    raise ValueError("Tempam jābūt skaitlim.")
                else:
                    raise e
            
            # Aprēķināt distanci
            distance = time_in_minutes / pace_in_minutes
            
            # Parādīt rezultātu
            self.distance_result_label.config(
                text=f"Jūsu distance: {distance:.2f} km", 
                fg=self.primary_color
            )
            
        except ValueError as e:
            messagebox.showerror("Kļūda", str(e))
        except Exception as e:
            messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
    
    def reset_pace_fields(self, distance_var, hours_var, minutes_var, seconds_var):
        """Notīrīt tempa kalkulatora laukus"""
        distance_var.set("")
        hours_var.set("0")
        minutes_var.set("0")
        seconds_var.set("0")
        self.pace_result_label.config(
            text="Rezultāts parādīsies šeit", 
            fg=self.text_secondary
        )
    
    def reset_time_fields(self, distance_var, pace_minutes_var, pace_seconds_var):
        """Notīrīt laika kalkulatora laukus"""
        distance_var.set("")
        pace_minutes_var.set("5")
        pace_seconds_var.set("30")
        self.time_result_label.config(
            text="Rezultāts parādīsies šeit", 
            fg=self.text_secondary
        )
    
    def reset_distance_fields(self, hours_var, minutes_var, seconds_var, pace_minutes_var, pace_seconds_var):
        """Notīrīt distances kalkulatora laukus"""
        hours_var.set("0")
        minutes_var.set("45")
        seconds_var.set("0")
        pace_minutes_var.set("5")
        pace_seconds_var.set("45")
        self.distance_result_label.config(
            text="Rezultāts parādīsies šeit", 
            fg=self.text_secondary
        )
    
    def show_start_page(self):
        """Parāda vienkāršu sākuma lapu ar programmas nosaukumu un īsu aprakstu"""
        # Notīrīt ekrānu, ja nepieciešams
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Galvenais konteiners
        main_frame = ttk.Frame(self.root, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Virsraksts
        title_frame = ttk.Frame(main_frame, style="TFrame")
        title_frame.pack(pady=(40, 10))
        
        # Programmas informācijas karte
        info_frame = ttk.Frame(main_frame, style="Card.TFrame")
        info_frame.pack(fill=tk.X, padx=50, pady=10)
        
        # Programmas virsraksts
        title_label = ttk.Label(info_frame, 
                             text="SKRĒJĒJA KALKULATORS", 
                             font=("Arial", 24, "bold"), 
                             foreground=self.primary_color,
                             style="Card.TLabel")
        title_label.pack(pady=(20, 10), padx=20)
        
        # Programmas apraksts
        intro_text = """
        Vienkāršs un ērts rīks, kas palīdzēs tev plānot skrējienus un sasniegt savus mērķus!
        
        Ar šo kalkulatoru tu vari:
          • Aprēķināt tempu (min/km), ievadot distanci un laiku
          • Aprēķināt laiku, ievadot distanci un tempu
          • Aprēķināt distanci, ievadot laiku un tempu
        
        Programmu izstrādāja: Kristiāna Kočubeja
        """
        
        intro_label = ttk.Label(info_frame, 
                             text=intro_text, 
                             wraplength=500, 
                             justify=tk.LEFT, 
                             padding=20,
                             style="Card.TLabel")
        intro_label.pack(fill=tk.X)
        
        # Sākt pogas rāmis
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=40)
        
        # Sākt poga
        start_button = ttk.Button(button_frame, 
                               text="SĀKT LIETOT KALKULATORU",
                               padding=(20, 10),
                               command=self.create_main_page)
        start_button.pack()

# Palaist programmu
if __name__ == "__main__":
    root = tk.Tk()
    app = RunnerCalculator(root)
    root.mainloop()