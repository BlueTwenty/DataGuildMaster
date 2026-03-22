import sys
import os

# Agregamos la carpeta 'Scripts' al camino de búsqueda
script_dir = os.path.join(os.path.dirname(__file__), 'Scripts')
sys.path.insert(0, script_dir)

from interface_gui import GuildMasterApp

if __name__ == "__main__":
    app = GuildMasterApp()
    app.mainloop()