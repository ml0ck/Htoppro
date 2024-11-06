import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Importer Pillow pour gérer l'image
import psutil

# Fonction pour afficher les processus
def afficher_processus():
    """Affiche les processus en cours dans la fenêtre scrollable."""
    for i in tree.get_children():
        tree.delete(i)

    processus = []
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_info']):
        try:
            processus.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'username': proc.info['username'],
                'cpu': proc.info['cpu_percent'],
                'memory': proc.info['memory_info'].rss / (1024 * 1024)  # Convertir la mémoire en MB
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass  # Ignorer les processus que l'on ne peut pas accéder

    # Ajouter chaque processus dans la table
    for p in processus:
        tree.insert('', 'end', values=(p['pid'], p['name'], p['username'], f"{p['cpu']}%", f"{p['memory']:.2f} MB"))

    # Rafraîchir la liste des processus toutes les 2 secondes
    root.after(2000, afficher_processus)

# Fonction pour tuer le processus sélectionné
def tuer_procesus():
    """Tuer le processus sélectionné."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a process to kill.")
        return

    pid = tree.item(selected_item, 'values')[0]  # Obtenir le PID du processus sélectionné
    try:
        process = psutil.Process(int(pid))
        process.terminate()  # Terminer le processus
        messagebox.showinfo("Success", f"Process with PID {pid} has been terminated.")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        messagebox.showerror("Error", "Could not terminate the process. The process may be protected or no longer exists.")
    except ValueError:
        messagebox.showerror("Error", "Invalid PID value.")

# Fonction pour quitter le programme
def quitter():
    """Quitter le programme."""
    root.quit()

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("System Process Manager")

# Définir la taille de la fenêtre
root.geometry("900x650")
root.config(bg="#f5f5f5")  # Couleur de fond claire

# Ajouter l'image en haut de la fenêtre avec Pillow
try:
    img = Image.open("tag.png")  # Charger l'image avec Pillow
    img = img.resize((900, 150), Image.ANTIALIAS)  # Redimensionner si nécessaire
    img = ImageTk.PhotoImage(img)  # Convertir en format compatible avec tkinter

    label_img = tk.Label(root, image=img, bg="#f5f5f5")
    label_img.image = img  # Garder une référence pour éviter que l'image soit détruite
    label_img.pack(side="top", pady=10)  # Placer l'image en haut de la fenêtre
except Exception as e:
    print(f"Error loading image: {e}")

# Frame contenant le menu
frame_menu = tk.Frame(root, bg="#f5f5f5")
frame_menu.pack(fill="x", pady=10)

# Menu principal
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Sous-menu "View"
menu_affichage = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=menu_affichage)
menu_affichage.add_command(label="Show Processes", command=afficher_processus)
menu_affichage.add_separator()
menu_affichage.add_command(label="Quit", command=quitter)

# Frame pour l'affichage des processus
frame_processus = tk.Frame(root, bg="#f5f5f5")
frame_processus.pack(padx=10, pady=10, fill="both", expand=True)

# Créer un Treeview pour afficher les processus sous forme de tableau
tree = ttk.Treeview(frame_processus, columns=("PID", "Name", "User", "CPU", "Memory"), show="headings")
tree.pack(fill="both", expand=True)

# Définir les en-têtes du tableau
tree.heading("PID", text="PID")
tree.heading("Name", text="Name")
tree.heading("User", text="User")
tree.heading("CPU", text="CPU")
tree.heading("Memory", text="Memory")

# Définir la largeur des colonnes
tree.column("PID", width=80, anchor="center")
tree.column("Name", width=200, anchor="w")
tree.column("User", width=150, anchor="w")
tree.column("CPU", width=100, anchor="center")
tree.column("Memory", width=120, anchor="center")

# Style du Treeview pour un affichage plus joli
style = ttk.Style()
style.configure("Treeview",
                background="#f9f9f9",
                foreground="black",
                rowheight=25,
                fieldbackground="#f9f9f9")
style.map('Treeview', background=[('selected', '#4CAF50')])

# Zone pour entrer le PID du processus à tuer
frame_pid = tk.Frame(root, bg="#f5f5f5")
frame_pid.pack(pady=10)

label_pid = tk.Label(frame_pid, text="Enter PID to Kill:", font=("Verdana", 10), bg="#f5f5f5")
label_pid.pack(side="left", padx=10)

entry_pid = tk.Entry(frame_pid, font=("Verdana", 10), width=15)
entry_pid.pack(side="left")

# Bouton pour tuer le processus
btn_kill = tk.Button(frame_pid, text="Kill Process", font=("Verdana", 10), command=tuer_procesus)
btn_kill.pack(side="left", padx=10)

# Titre de la fenêtre
titre_label = tk.Label(root, text="System Process Manager", font=("Verdana", 16, "bold"), fg="#4CAF50", bg="#f5f5f5")
titre_label.pack(pady=20)

# Lancer l'application
root.after(2000, afficher_processus)  # Initialiser le rafraîchissement des processus
root.mainloop()
