import customtkinter as ctk
from tkinter import messagebox
from data_manager import DataManager
from engine_auditor import EngineAuditor

class GuildMasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ DATA GUILD MASTER v2.0")
        self.geometry("600x500")
        
        self.auditor = EngineAuditor("BlueTwenty", "DataGuildMaster") # Cambia por tu User
        self.data = DataManager.cargar_json("progreso.json")
        self.nivel = self.data.get('mision_actual', 1)
        self.info = self.auditor.obtener_info_mision(self.nivel)

        # UI
        ctk.CTkLabel(self, text=f"👤 {self.data.get('nombre')} | LVL: {self.nivel}", font=("Consolas", 14)).pack(pady=10)
        
        self.f = ctk.CTkFrame(self, fg_color="#161b22")
        self.f.pack(pady=10, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(self.f, text=self.info['titulo'], font=("Arial", 20, "bold"), text_color="#FFCC00").pack(pady=10)
        ctk.CTkLabel(self.f, text=self.info['obj'], wraplength=400).pack(pady=10)

        ctk.CTkButton(self, text="📥 1. GENERAR RETO", fg_color="#7952b3", command=self.gen).pack(pady=5)
        ctk.CTkButton(self, text="💡 VER PISTA", fg_color="#e3b341", text_color="black", command=lambda: messagebox.showinfo("Tip", self.info['tip'])).pack(pady=5)
        ctk.CTkButton(self, text="☁️ 2. SUBIR A GITHUB", fg_color="#1f6feb", command=self.sync).pack(pady=5)
        ctk.CTkButton(self, text="✅ 3. VALIDAR", fg_color="#238636", command=self.val).pack(pady=5)

    def gen(self):
        try:
            # Llamamos a generar_excel, que es el nombre que definimos arriba
            ok, m = self.auditor.generar_excel(self.nivel)
            if ok:
                messagebox.showinfo("Sistema", m)
            else:
                messagebox.showwarning("Error", m)
        except Exception as e:
            print(f"ERROR CRÍTICO AL GENERAR: {e}")
            messagebox.showerror("Error", f"No se pudo generar: {e}")

    def sync(self):
        ok, m = self.auditor.subir_github()
        messagebox.showinfo("Git", m)

    def val(self):
        ok, m = self.auditor.validar_remoto(self.info)
        if ok:
            self.data['mision_actual'] += 1
            self.data['exp'] += 100 * self.nivel
            DataManager.guardar_progreso(self.data)
            messagebox.showinfo("ÉXITO", "¡Nivel Superado! Reiniciando...")
            self.destroy()
        else: messagebox.showerror("Fallo", m)

if __name__ == "__main__":
    app = GuildMasterApp()
    app.mainloop()