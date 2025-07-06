import tkinter as tk
from tkinter import ttk, messagebox


class ThunderarApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_main_window()
        self.show_login()
        self.root.mainloop()

    def setup_main_window(self):
        self.root.title("Thunderar")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        tk.Label(main_frame, text="⚡", font=("Arial", 48), bg="#ffffff").pack(pady=(10, 20))
        tk.Label(main_frame, text="Thunderar", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333").pack()
        tk.Label(main_frame, text="Iniciar Sesión", font=("Arial", 14), bg="#ffffff", fg="#666666").pack(pady=(0, 30))

        self.user_entry = self.create_input_field(main_frame, "Usuario:")
        self.pass_entry = self.create_input_field(main_frame, "Contraseña:", True)

        self.create_button(main_frame, "INGRESAR", "#3B4FFF", self.login, pady=(20, 10))
        self.create_button(main_frame, "REGISTRARSE", "#4CAF50", self.show_register, pady=(5, 15))
        self.create_button(main_frame, "ACCESO CLIENTE", "#FFC107", self.client_access, pady=(5, 0))

        tk.Label(main_frame, text="Thunderar v2.0", bg="#ffffff", fg="#999999", font=("Arial", 8)).pack(side="bottom",
                                                                                                        pady=(20, 0))

    def create_input_field(self, parent, label, is_password=False):
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(fill="x", pady=(0, 15))
        tk.Label(frame, text=label, bg="#ffffff", fg="#555555").pack(anchor="w")
        entry = ttk.Entry(frame, font=("Arial", 12))
        if is_password:
            entry.config(show="•")
        entry.pack(fill="x", pady=(5, 0), ipady=5)
        return entry

    def create_button(self, parent, text, bg, command, **pack_args):
        btn = tk.Button(
            parent,
            text=text,
            bg=bg,
            fg="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            command=command,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        btn.pack(fill="x", **pack_args)
        return btn

    def login(self):
        if not self.validate_fields():
            return
        self.show_main_menu()

    def client_access(self):
        self.show_sales_screen(access_type="Cliente")

    def show_register(self):
        RegisterDialog(self.root, self)

    def validate_fields(self):
        if not self.user_entry.get() or not self.pass_entry.get():
            messagebox.showerror("Error", "Complete todos los campos")
            return False
        return True

    def show_main_menu(self):
        self.clear_window()
        MainMenu(self.root, self)

    def show_sales_screen(self, access_type="Usuario"):
        self.clear_window()
        SalesScreen(self.root, self, access_type)

    def show_user_profile(self):
        self.clear_window()
        UserProfile(self.root, self)


class RegisterDialog(tk.Toplevel):
    def __init__(self, parent, app):
        super(ThunderarApp).__init__(parent)
        self.app = app
        self.setup_dialog()
        self.create_widgets()

    def setup_dialog(self):
        self.title("Thunderar - Registro")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(bg="#ffffff")
        self.grab_set()

    def create_widgets(self):
        tk.Label(self, text="⚡", font=("Arial", 48), bg="#ffffff").pack(pady=(10, 5))
        tk.Label(self, text="Registro de Usuario", font=("Arial", 18, "bold"), bg="#ffffff", fg="#333333").pack(
            pady=(0, 20))

        self.entries = []
        fields = [
            ("Nombre Completo", False),
            ("Correo Electrónico", False),
            ("Teléfono", False),
            ("Usuario", False),
            ("Contraseña", True),
            ("Confirmar Contraseña", True)
        ]

        for field, is_password in fields:
            frame = tk.Frame(self, bg="#ffffff")
            frame.pack(fill="x", padx=20, pady=5)
            tk.Label(frame, text="{field}:", bg="#ffffff", fg="#555555").pack(anchor="w")
            entry = ttk.Entry(frame, font=("Arial", 12))
            if is_password:
                entry.config(show="•")
            entry.pack(fill="x", pady=(2, 0), ipady=5)
            self.entries.append(entry)

        tk.Button(
            self,
            text="REGISTRAR",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            command=self.register,
            padx=20,
            pady=10
        ).pack(fill="x", padx=40, pady=(20, 10))

    def register(self):
        if not all(entry.get() for entry in self.entries):
            messagebox.showerror("Error", "Complete todos los campos")
            return
        if self.entries[4].get() != self.entries[5].get():
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        messagebox.showinfo("Éxito", "Registro completado")
        self.destroy()
        self.app.show_login()


class MainMenu:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Thunderar - Menú Principal")
        self.root.geometry("800x600")

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        header_frame = tk.Frame(main_frame, bg="#ffffff")
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="Thunderar", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333").pack(
            side="left")
        tk.Label(header_frame, text="Menú Principal", font=("Arial", 16), bg="#ffffff", fg="#666666").pack(side="left",
                                                                                                           padx=10)

        # BOTÓN "Usuario" actualizado
        tk.Button(
            header_frame,
            text="Usuario",
            bg="#FFEB3B",
            fg="black",
            font=("Arial", 10, "bold"),
            borderwidth=1,
            relief="solid",
            command=self.app.show_user_profile,
            padx=10,
            pady=2
        ).pack(side="right", padx=5)

        options_frame = tk.Frame(main_frame, bg="#ffffff")
        options_frame.pack(expand=True, fill="both", pady=(20, 0))

        options = [
            {"name": "Comunidad", "icon": "👥",
             "command": lambda: messagebox.showinfo("Comunidad", "Acceso a Comunidad")},
            {"name": "Ventas", "icon": "💰", "command": lambda: self.app.show_sales_screen()},
            {"name": "Logística", "icon": "🚚",
             "command": lambda: messagebox.showinfo("Logística", "Acceso a Logística")},
            {"name": "Reportes", "icon": "📊", "command": lambda: messagebox.showinfo("Reportes", "Acceso a Reportes")}
        ]

        for i, option in enumerate(options):
            row, col = divmod(i, 2)
            self.create_menu_option(options_frame, option, row, col)

    def create_menu_option(self, parent, option, row, col):
        def on_click(event):
            option["command"]()

        btn_frame = tk.Frame(parent, bg="#ffffff", highlightbackground="#e0e0e0", highlightthickness=1, cursor="hand2")
        btn_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew", ipadx=20, ipady=20)
        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)
        icon_label = tk.Label(btn_frame, text=option["icon"], font=("Arial", 48), bg="#ffffff")
        icon_label.pack(pady=(10, 5))
        tk.Label(btn_frame, text=option["name"], font=("Arial", 14), bg="#ffffff").pack(pady=(0, 10))
        btn_frame.bind("<Button-1>", on_click)
        icon_label.bind("<Button-1>", on_click)


class SalesScreen:
    def __init__(self, root, app, access_type):
        self.root = root
        self.app = app
        self.access_type = access_type
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Thunderar - Ventas ({self.access_type})")
        self.root.geometry("800x600")

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        header_frame = tk.Frame(main_frame, bg="#ffffff")
        header_frame.pack(fill="x", pady=(0, 20))
        tk.Label(header_frame, text="Thunderar", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333").pack(
            side="left")
        tk.Label(header_frame, text="Ventas ({self.access_type})", font=("Arial", 16), bg="#ffffff",
                 fg="#666666").pack(side="left", padx=10)

        tk.Button(
            header_frame,
            text="Regresar",
            bg="#FF5722",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.app.show_main_menu if self.access_type == "Usuario" else self.app.show_login,
            padx=10,
            pady=2
        ).pack(side="right", padx=5)

        tk.Label(
            main_frame,
            text="Pantalla de Ventas\n\nFuncionalidades disponibles para clientes",
            font=("Arial", 14),
            bg="#ffffff",
            justify="center"
        ).pack(expand=True)


class UserProfile:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        self.root.title("Thunderar - Perfil de Usuario")
        self.root.geometry("800x600")

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#ffffff")
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(frame, text="👤", font=("Arial", 64), bg="#ffffff").pack(pady=20)
        tk.Label(frame, text="Perfil de Usuario", font=("Arial", 24, "bold"), bg="#ffffff", fg="#333333").pack(
            pady=(0, 10))
        tk.Label(frame, text="Esta es una vista de prueba del perfil de usuario.", font=("Arial", 14), bg="#ffffff",
                 fg="#666666").pack(pady=(0, 40))

        tk.Button(
            frame,
            text="Volver al Login",
            bg="#3B4FFF",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.app.show_login,
            padx=20,
            pady=10
        ).pack(pady=(0, 10))

        tk.Button(
            frame,
            text="Cerrar Aplicación",
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.app.root.quit,
            padx=20,
            pady=10
        ).pack()


if __name__ == "__main__":
    ThunderarApp()
