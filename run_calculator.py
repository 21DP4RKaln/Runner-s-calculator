import tkinter as tk
from tkinter import ttk, messagebox
import re
import math

class SimpleRunnerCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Skrējēja Kalkulators")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Krāsu shēma - dzeltens kā primārā krāsa
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
                          foreground="#000000")  # Melnais teksts uz dzeltena fona
        
        self.style.map("TButton",
                    background=[('active', self.accent_color)],
                    foreground=[('active', "#000000")])
        
        self.style.configure("TEntry", 
                          fieldbackground=self.card_bg, 
                          foreground=self.text_color)
    
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
        
        # Laiks
        time_frame = ttk.Frame(input_frame, style="Card.TFrame")
        time_frame.pack(fill=tk.X, pady=15, padx=20)
        
        time_label = ttk.Label(time_frame, 
                            text="Laiks (mm:ss):", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        time_var = tk.StringVar()
        time_entry = tk.Entry(time_frame, 
                           textvariable=time_var, 
                           width=10,
                           bg=self.bg_color,
                           fg=self.text_color,
                           insertbackground=self.text_color,
                           relief="flat",
                           highlightthickness=1,
                           highlightcolor=self.primary_color,
                           highlightbackground=self.accent_color)
        time_entry.pack(side=tk.LEFT)
        
        time_example = ttk.Label(time_frame, 
                              text="Piemērs: 35:00", 
                              font=self.font_small, 
                              foreground=self.text_secondary,
                              style="Card.TLabel")
        time_example.pack(side=tk.LEFT, padx=10)
        
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
                                   command=lambda: self.calculate_pace(distance_var, time_var))
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, 
                               text="Notīrīt", 
                               command=lambda: self.reset_fields(distance_var, time_var, self.pace_result_label))
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
        
        # Temps
        pace_frame = ttk.Frame(input_frame, style="Card.TFrame")
        pace_frame.pack(fill=tk.X, pady=15, padx=20)
        
        pace_label = ttk.Label(pace_frame, 
                            text="Temps (min/km):", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        pace_label.pack(side=tk.LEFT, padx=(0, 10))
        
        pace_var = tk.StringVar()
        pace_entry = tk.Entry(pace_frame, 
                           textvariable=pace_var, 
                           width=10,
                           bg=self.bg_color,
                           fg=self.text_color,
                           insertbackground=self.text_color,
                           relief="flat",
                           highlightthickness=1,
                           highlightcolor=self.primary_color,
                           highlightbackground=self.accent_color)
        pace_entry.pack(side=tk.LEFT)
        
        pace_example = ttk.Label(pace_frame, 
                              text="Piemērs: 5:30", 
                              font=self.font_small, 
                              foreground=self.text_secondary,
                              style="Card.TLabel")
        pace_example.pack(side=tk.LEFT, padx=10)
        
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
                                   command=lambda: self.calculate_time(distance_var, pace_var))
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, 
                               text="Notīrīt", 
                               command=lambda: self.reset_fields(distance_var, pace_var, self.time_result_label))
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
        
        # Laiks
        time_frame = ttk.Frame(input_frame, style="Card.TFrame")
        time_frame.pack(fill=tk.X, pady=15, padx=20)
        
        time_label = ttk.Label(time_frame, 
                            text="Laiks (mm:ss):", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        time_label.pack(side=tk.LEFT, padx=(0, 10))
        
        time_var = tk.StringVar()
        time_entry = tk.Entry(time_frame, 
                           textvariable=time_var, 
                           width=10,
                           bg=self.bg_color,
                           fg=self.text_color,
                           insertbackground=self.text_color,
                           relief="flat",
                           highlightthickness=1,
                           highlightcolor=self.primary_color,
                           highlightbackground=self.accent_color)
        time_entry.pack(side=tk.LEFT)
        
        time_example = ttk.Label(time_frame, 
                              text="Piemērs: 45:00", 
                              font=self.font_small, 
                              foreground=self.text_secondary,
                              style="Card.TLabel")
        time_example.pack(side=tk.LEFT, padx=10)
        
        # Temps
        pace_frame = ttk.Frame(input_frame, style="Card.TFrame")
        pace_frame.pack(fill=tk.X, pady=15, padx=20)
        
        pace_label = ttk.Label(pace_frame, 
                            text="Temps (min/km):", 
                            width=16, 
                            anchor="w",
                            style="Card.TLabel")
        pace_label.pack(side=tk.LEFT, padx=(0, 10))
        
        pace_var = tk.StringVar()
        pace_entry = tk.Entry(pace_frame, 
                           textvariable=pace_var, 
                           width=10,
                           bg=self.bg_color,
                           fg=self.text_color,
                           insertbackground=self.text_color,
                           relief="flat",
                           highlightthickness=1,
                           highlightcolor=self.primary_color,
                           highlightbackground=self.accent_color)
        pace_entry.pack(side=tk.LEFT)
        
        pace_example = ttk.Label(pace_frame, 
                              text="Piemērs: 5:45", 
                              font=self.font_small, 
                              foreground=self.text_secondary,
                              style="Card.TLabel")
        pace_example.pack(side=tk.LEFT, padx=10)
        
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
                                   command=lambda: self.calculate_distance(time_var, pace_var))
        calculate_button.pack(side=tk.LEFT, padx=5)
        
        reset_button = ttk.Button(button_frame, 
                               text="Notīrīt", 
                               command=lambda: self.reset_fields(time_var, pace_var, self.distance_result_label))
        reset_button.pack(side=tk.LEFT, padx=5)
    
    def calculate_pace(self, distance_var, time_var):
        """Aprēķina tempu"""
        try:
            # Pārbaudīt distanci
            distance_str = distance_var.get().strip().replace(',', '.')
            if not distance_str:
                raise ValueError("Distance nav ievadīta.")
            distance = float(distance_str)
            if distance <= 0:
                raise ValueError("Distancei jābūt pozitīvam skaitlim.")
            
            # Pārbaudīt laiku
            time_str = time_var.get().strip()
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
            self.pace_result_label.config(
                text=f"Jūsu temps: {pace_formatted} min/km", 
                fg=self.primary_color
            )
            
        except ValueError as e:
            messagebox.showerror("Kļūda", str(e))
        except Exception as e:
            messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
    
    def calculate_time(self, distance_var, pace_var):
        """Aprēķina laiku"""
        try:
            # Pārbaudīt distanci
            distance_str = distance_var.get().strip().replace(',', '.')
            if not distance_str:
                raise ValueError("Distance nav ievadīta.")
            distance = float(distance_str)
            if distance <= 0:
                raise ValueError("Distancei jābūt pozitīvam skaitlim.")
            
            # Pārbaudīt tempu
            pace_str = pace_var.get().strip()
            if not pace_str:
                raise ValueError("Temps nav ievadīts.")
            
            # Tempa pārbaude un pārvēršana minūtēs
            pace_in_minutes = self.parse_pace_to_minutes(pace_str)
            if pace_in_minutes <= 0:
                raise ValueError("Tempam jābūt pozitīvam.")
            
            # Aprēķināt laiku
            time_in_minutes = pace_in_minutes * distance
            
            # Formatēt laiku
            time_formatted = self.format_time_for_display(time_in_minutes)
            
            # Parādīt rezultātu
            self.time_result_label.config(
                text=f"Jūsu laiks: {time_formatted}", 
                fg=self.primary_color
            )
            
        except ValueError as e:
            messagebox.showerror("Kļūda", str(e))
        except Exception as e:
            messagebox.showerror("Kļūda", f"Notika kļūda: {e}")
    
    def calculate_distance(self, time_var, pace_var):
        """Aprēķina distanci"""
        try:
            # Pārbaudīt laiku
            time_str = time_var.get().strip()
            if not time_str:
                raise ValueError("Laiks nav ievadīts.")
            
            # Laika pārbaude un pārvēršana minūtēs
            time_in_minutes = self.parse_time_to_minutes(time_str)
            if time_in_minutes <= 0:
                raise ValueError("Laikam jābūt pozitīvam.")
            
            # Pārbaudīt tempu
            pace_str = pace_var.get().strip()
            if not pace_str:
                raise ValueError("Temps nav ievadīts.")
            
            # Tempa pārbaude un pārvēršana minūtēs
            pace_in_minutes = self.parse_pace_to_minutes(pace_str)
            if pace_in_minutes <= 0:
                raise ValueError("Tempam jābūt pozitīvam.")
            
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
    
    def reset_fields(self, var1, var2, result_label):
        """Notīrīt ievades laukus un rezultātu"""
        var1.set("")
        var2.set("")
        result_label.config(
            text="Rezultāts parādīsies šeit", 
            fg=self.text_secondary
        )
    
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
                raise ValueError("Nepareizs laika formāts. Izmantojiet mm:ss vai hh:mm:ss.")
        except Exception:
            raise ValueError("Nepareizs laika formāts. Izmantojiet mm:ss vai hh:mm:ss.")

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
    
    def format_time_for_display(self, minutes):
        """Formatē minūtes kā hh:mm:ss vai mm:ss atkarībā no garuma"""
        total_seconds = int(minutes * 60)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"

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
        
        # Virsraksts ar lieliem burtiem un dzelteno krāsu
        title_label = ttk.Label(title_frame, 
                             text="SKRĒJĒJA KALKULATORS", 
                             font=("Arial", 28, "bold"), 
                             foreground=self.primary_color)
        title_label.pack()
        
        # Skrējēja ikona (emoji)
        icon_label = ttk.Label(main_frame,
                            font=("Arial", 50), 
                            foreground=self.primary_color)
        icon_label.pack(pady=(10, 30))
        
        # Programmas apraksta karte
        card_frame = ttk.Frame(main_frame, style="Card.TFrame")
        card_frame.pack(fill=tk.X, padx=50, pady=10)
        
        intro_text = """
        Vienkāršs un ērts rīks, kas palīdzēs tev plānot skrējienus un sasniegt savus mērķus!
        
        Ar šo kalkulatoru tu vari:
          • Aprēķināt tempu (min/km), ievadot distanci un laiku
          • Aprēķināt laiku, ievadot distanci un tempu
          • Aprēķināt distanci, ievadot laiku un tempu
        """
        
        intro_label = ttk.Label(card_frame, 
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
        
        # Autora informācija apakšā
        author_label = ttk.Label(main_frame, 
                              text="© Skrējēju atbalsta komanda",
                              font=self.font_small, 
                              foreground=self.text_secondary)
        author_label.pack(side=tk.BOTTOM, pady=10)

# Palaist programmu
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleRunnerCalculator(root)
    root.mainloop()