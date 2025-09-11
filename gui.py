import tkinter as tk
from tkinter import ttk, messagebox
import operaciones
import utilidades as u

# Paleta definida en el requerimiento
COLOR_PRIMARIO_PRESSED = "#6A1B9A"
COLOR_PRIMARIO_BASE = "#7E57C2"
COLOR_PRIMARIO_HOVER = "#3949AB"
COLOR_ACTIVO = "#5C6BC0"
COLOR_SUAVE = "#7BBBC4"
COLOR_FONDO = "#FFFFFF"
COLOR_PANEL = "#F7F7FB"
COLOR_BORDES = "#E3E5F0"
COLOR_TEXTO = "#1F2233"
COLOR_TEXTO_SEC = "#5A6079"


def crear_estilo():
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    fuente_base = ("Segoe UI", 10)
    style.configure("TFrame", background=COLOR_PANEL)
    style.configure("TLabel", background=COLOR_PANEL, foreground=COLOR_TEXTO, font=fuente_base)
    style.configure("Secondary.TLabel", foreground=COLOR_TEXTO_SEC, background=COLOR_PANEL, font=("Segoe UI", 9))
    style.configure("Title.TLabel", font=("Segoe UI", 12, "bold"), foreground=COLOR_PRIMARIO_BASE, background=COLOR_PANEL)

    style.configure("Primary.TButton",
                    background=COLOR_PRIMARIO_BASE,
                    foreground="#FFFFFF",
                    font=fuente_base,
                    padding=6,
                    borderwidth=0)
    style.map("Primary.TButton",
              background=[("active", COLOR_PRIMARIO_HOVER), ("pressed", COLOR_PRIMARIO_PRESSED)],
              relief=[("pressed", "sunken"), ("!pressed", "flat")])

    style.configure("TButton", padding=5, font=fuente_base)

    # Entry / Combobox
    style.configure("TEntry", fieldbackground=COLOR_FONDO, background=COLOR_FONDO, foreground=COLOR_TEXTO, bordercolor=COLOR_BORDES, lightcolor=COLOR_ACTIVO)
    style.configure("TCombobox", fieldbackground=COLOR_FONDO, background=COLOR_FONDO, foreground=COLOR_TEXTO)

    # Notebook
    style.configure("TNotebook", background=COLOR_PANEL, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(12, 6), font=fuente_base)
    style.map("TNotebook.Tab", background=[("selected", COLOR_FONDO)], foreground=[("selected", COLOR_PRIMARIO_BASE)])

    return style


def matriz_a_texto(M):
    """Devuelve representación alineada de la matriz aumentada usando utilidades."""
    if not M:
        return "[ ]"
    filas = len(M)
    cols_total = len(M[0])
    cols_A = cols_total - 1
    anchos = []
    for c in range(cols_total):
        max_len = 0
        for f in range(filas):
            t = u.texto_fraccion(M[f][c])
            if len(t) > max_len:
                max_len = len(t)
        anchos.append(max_len)
    lineas = []
    for f in range(filas):
        izquierda = []
        for c in range(cols_A):
            txt = u.texto_fraccion(M[f][c])
            izquierda.append(txt.rjust(anchos[c]))
        txt_b = u.texto_fraccion(M[f][cols_A]).rjust(anchos[cols_A])
        lineas.append("[ " + "  ".join(izquierda) + " | " + txt_b + " ]")
    return "\n".join(lineas)


class AlgebraLinealApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Álgebra Lineal")
        self.configure(bg=COLOR_PANEL)
        self.minsize(980, 640)
        crear_estilo()
        self._construir_ui()

    # UI
    def _construir_ui(self):
        cont = ttk.Frame(self, padding=10)
        cont.pack(fill="both", expand=True)

        header = ttk.Frame(cont)
        header.pack(fill="x")
        ttk.Label(header, text="Resolución de Sistemas Lineales", style="Title.TLabel").pack(side="left")

        form = ttk.Frame(cont)
        form.pack(fill="x", pady=(10, 10))

        # Método
        ttk.Label(form, text="Método:").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        self.metodo_var = tk.StringVar(value="Gauss")
        self.combo_metodo = ttk.Combobox(form, textvariable=self.metodo_var, state="readonly", width=28,
                                         values=["Eliminación de Gauss (forma escalonada)", "Gauss-Jordan (forma escalonada reducida por filas)"])
        self.combo_metodo.grid(row=0, column=1, sticky="w", pady=2)

        # Dimensiones
        ttk.Label(form, text="Ecuaciones (m):").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=2)
        self.m_var = tk.StringVar(value="3")
        self.e_m = ttk.Entry(form, width=8, textvariable=self.m_var)
        self.e_m.grid(row=1, column=1, sticky="w", pady=2)

        ttk.Label(form, text="Incógnitas (n):").grid(row=1, column=2, sticky="w", padx=(18, 6), pady=2)
        self.n_var = tk.StringVar(value="3")
        self.e_n = ttk.Entry(form, width=8, textvariable=self.n_var)
        self.e_n.grid(row=1, column=3, sticky="w", pady=2)

        self.btn_generar = ttk.Button(form, text="Generar matriz", style="Primary.TButton", command=self.generar_matriz)
        self.btn_generar.grid(row=0, column=3, sticky="e", padx=(18, 0))

        self.mostrar_pasos_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(form, text="Mostrar pasos", variable=self.mostrar_pasos_var).grid(row=0, column=4, padx=(25, 0))

        form.columnconfigure(5, weight=1)

        # Contenedor matriz
        matriz_frame_outer = ttk.LabelFrame(cont, text="Matriz aumentada [A|b]", padding=10)
        matriz_frame_outer.pack(fill="x")
        self.matriz_frame = ttk.Frame(matriz_frame_outer)
        self.matriz_frame.pack(fill="x")

        # Botón resolver
        acciones = ttk.Frame(cont)
        acciones.pack(fill="x", pady=(10, 4))
        self.btn_resolver = ttk.Button(acciones, text="Resolver", style="Primary.TButton", command=self.resolver)
        self.btn_resolver.pack(side="left")

        # Notebook resultados
        notebook = ttk.Notebook(cont)
        notebook.pack(fill="both", expand=True, pady=(8,0))
        self.tab_resultado = ttk.Frame(notebook)
        self.tab_pasos = ttk.Frame(notebook)
        notebook.add(self.tab_resultado, text="Resultado")
        notebook.add(self.tab_pasos, text="Pasos")

        # Resultado
        self.text_resultado = tk.Text(self.tab_resultado, wrap="word", height=18, font=("Consolas", 10), background=COLOR_FONDO, borderwidth=1, relief="solid")
        self.text_resultado.pack(fill="both", expand=True, padx=6, pady=6)

        # Pasos
        self.text_pasos = tk.Text(self.tab_pasos, wrap="none", font=("Consolas", 10), background=COLOR_FONDO, borderwidth=1, relief="solid")
        sx = ttk.Scrollbar(self.tab_pasos, orient="horizontal", command=self.text_pasos.xview)
        sy = ttk.Scrollbar(self.tab_pasos, orient="vertical", command=self.text_pasos.yview)
        self.text_pasos.configure(xscrollcommand=sx.set, yscrollcommand=sy.set)
        self.text_pasos.grid(row=0, column=0, sticky="nsew", padx=(6,0), pady=6)
        sy.grid(row=0, column=1, sticky="ns", pady=6)
        sx.grid(row=1, column=0, sticky="ew", padx=(6,0))
        self.tab_pasos.rowconfigure(0, weight=1)
        self.tab_pasos.columnconfigure(0, weight=1)

        # Inicial
        self.entries = []  # grid de entries
        self.generar_matriz()

    # Lógica GUI
    def limpiar_matriz(self):
        for fila in self.entries:
            for e in fila:
                e.destroy()
        self.entries = []

    def generar_matriz(self):
        try:
            m = int(self.m_var.get())
            n = int(self.n_var.get())
            if m <= 0 or n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "m y n deben ser enteros positivos.")
            return
        self.limpiar_matriz()
        for i in range(m):
            fila_entries = []
            for j in range(n + 1):
                e = ttk.Entry(self.matriz_frame, width=8, font=("Segoe UI", 10))
                e.grid(row=i, column=j, padx=3, pady=3)
                e.insert(0, "0")
                fila_entries.append(e)
            self.entries.append(fila_entries)

    def _leer_matriz_desde_entries(self):
        M = []
        for fila_entries in self.entries:
            fila = []
            for e in fila_entries:
                txt = e.get().strip()
                if txt == "":
                    txt = "0"
                try:
                    fr = u.crear_fraccion_desde_cadena(txt)
                except Exception:
                    raise ValueError(f"Valor inválido: '{txt}'")
                fila.append(fr)
            M.append(fila)
        return M

    def resolver(self):
        try:
            M = self._leer_matriz_desde_entries()
        except ValueError as ex:
            messagebox.showerror("Error de datos", str(ex))
            return
        metodo_texto = self.metodo_var.get()
        usar_gauss = metodo_texto.startswith("Eliminación")
        if usar_gauss:
            R, pivotes, pasos = operaciones.eliminacion_gauss(M)
            info = operaciones.analizar_solucion_gauss(R, pivotes)
        else:
            R, pivotes, pasos = operaciones.gauss_jordan(M)
            info = operaciones.analizar_solucion(R, pivotes)
        self.mostrar_resultado(R, info)
        if self.mostrar_pasos_var.get():
            self.mostrar_pasos(pasos)
        else:
            self.text_pasos.delete("1.0", tk.END)
            self.text_pasos.insert(tk.END, "(Pasos ocultos)\n")

    # Resultados
    def mostrar_resultado(self, R, info):
        self.text_resultado.delete("1.0", tk.END)
        tipo = info.get("tipo_forma", "")
        solucion = info.get("solucion", "")
        self.text_resultado.insert(tk.END, f"Tipo de solución: {solucion}\n")
        if solucion == "INCONSISTENTE":
            self.text_resultado.insert(tk.END, "Sistema inconsistente.\n\n")
        else:
            sp = info.get("solucion_particular", [])
            if sp:
                self.text_resultado.insert(tk.END, "Variables (fracción = decimal):\n")
                for i, fr in enumerate(sp, start=1):
                    self.text_resultado.insert(tk.END, f"x{i} = {u.texto_fraccion(fr)} = {u.texto_decimal(fr)}\n")
                self.text_resultado.insert(tk.END, "\n")
            libres = info.get("libres", [])
            if libres:
                vars_libres = ", ".join(f"x{c+1}" for c in libres)
                self.text_resultado.insert(tk.END, f"Variables libres: {vars_libres}\n\n")
        etiqueta = "Forma escalonada reducida por filas" if tipo == "ESCALONADA_REDUCIDA" else "Forma escalonada"
        self.text_resultado.insert(tk.END, etiqueta + " final ([A|b]):\n")
        self.text_resultado.insert(tk.END, matriz_a_texto(R) + "\n")

    def mostrar_pasos(self, pasos):
        self.text_pasos.delete("1.0", tk.END)
        if not pasos:
            self.text_pasos.insert(tk.END, "No hubo operaciones (matriz ya estaba reducida).\n")
            return
        for idx, paso in enumerate(pasos, start=1):
            if isinstance(paso, dict):
                self.text_pasos.insert(tk.END, f"{idx:02d}) {paso.get('operacion','')}\n")
                self.text_pasos.insert(tk.END, matriz_a_texto(paso.get("matriz", [])) + "\n")
                self.text_pasos.insert(tk.END, "-" * 42 + "\n")
            else:
                self.text_pasos.insert(tk.END, f"{idx:02d}) {paso}\n")

def run_gui():
    app = AlgebraLinealApp()
    app.mainloop()

if __name__ == "__main__":
    run_gui()
