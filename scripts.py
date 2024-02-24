import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import subprocess
import threading
import os

class LibraryInstallerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Instalador de Bibliotecas Python")

        self.libraries = {
            'numpy': '1.21.1',
            'pandas': '1.3.3',
            'matplotlib': '3.4.3',
            'seaborn': '0.11.2',
            'scikit-learn': '0.24.2',
            'tensorflow': '2.6.0',
            'torch': '1.9.0',  # PyTorch
            'keras': '2.6.0',
            'Django': '3.2.8',
            'Flask': '2.0.1',
            'requests': '2.26.0',
            'beautifulsoup4': '4.10.0',
        }

        self.library_vars = {lib: tk.StringVar() for lib in self.libraries}

        self.install_button = None
        self.progress_bar = None
        self.log_text = None
        self.status_label = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Selecione as bibliotecas que deseja instalar:").pack(pady=10)

        for library, version in self.libraries.items():
            tk.Checkbutton(self.master, text=f"{library} ({version})", variable=self.library_vars[library]).pack(anchor=tk.W)

        self.install_button = tk.Button(self.master, text="Instalar Selecionadas", command=self.install_libraries)
        self.install_button.pack(pady=10)

        tk.Button(self.master, text="Atualizar Lista", command=self.update_library_list).pack(pady=5)
        tk.Button(self.master, text="Selecionar Tudo", command=self.select_all).pack(pady=5)
        tk.Button(self.master, text="Desmarcar Tudo", command=self.deselect_all).pack(pady=5)
        tk.Button(self.master, text="Ver Log de Instalação", command=self.view_installation_log).pack(pady=10)
        tk.Button(self.master, text="Sair", command=self.master.quit).pack()

        self.progress_bar = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(self.master, width=80, height=20, wrap=tk.WORD)
        self.log_text.pack(pady=10)

        self.status_label = tk.Label(self.master, text="Status: Pronto")
        self.status_label.pack()

    def install_libraries(self):
        selected_libraries = {lib: version.get() for lib, version in self.library_vars.items() if version.get()}
        
        if not selected_libraries:
            messagebox.showinfo("Nenhuma Biblioteca Selecionada", "Por favor, selecione pelo menos uma biblioteca.")
            return

        self.clear_log()
        self.install_button.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(selected_libraries)

        install_thread = threading.Thread(target=self.run_installation, args=(selected_libraries,))
        install_thread.start()

    def run_installation(self, selected_libraries):
        try:
            self.log("Iniciando instalação das bibliotecas...")
            for i, (library, version) in enumerate(selected_libraries.items()):
                self.show_installation_progress(i + 1, library)
                install_command = ["pip", "install", f"{library}=={version}"]
                process = subprocess.Popen(install_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()
                if process.returncode != 0:
                    self.log(f"Erro durante a instalação de {library}:\n{error}")
                    self.set_status(f"Status: Erro durante a instalação de {library}")
                else:
                    self.log(f"Instalação de {library} concluída com sucesso.")
                    self.set_status(f"Status: Instalação de {library} concluída")
                self.progress_bar["value"] = i + 1

            self.log("Instalação concluída.")
            self.set_status("Status: Todas as bibliotecas foram instaladas com sucesso!")
            messagebox.showinfo("Instalação Concluída", "Todas as bibliotecas foram instaladas com sucesso!")
        finally:
            self.install_button.config(state=tk.NORMAL)

    def show_installation_progress(self, current, library):
        self.progress_bar["value"] = current
        self.log(f"Iniciando instalação de {library}...")

    def update_library_list(self):
        # Adicione aqui a lógica para atualizar a lista de bibliotecas, se necessário
        messagebox.showinfo("Lista Atualizada", "A lista de bibliotecas foi atualizada.")

    def select_all(self):
        for var in self.library_vars.values():
            var.set(1)

    def deselect_all(self):
        for var in self.library_vars.values():
            var.set(0)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def set_status(self, message):
        self.status_label["text"] = message

    def view_installation_log(self):
        with open("installation_log.txt", "w") as log_file:
            log_file.write(self.log_text.get(1.0, tk.END))

        if os.name == 'nt':  # Windows
            subprocess.Popen(["notepad.exe", "installation_log.txt"])
        else:  # Assume sistema baseado em Unix
            subprocess.Popen(["gedit", "installation_log.txt"])

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryInstallerApp(root)
    root.mainloop()
