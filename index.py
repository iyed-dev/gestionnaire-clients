import json
import os
import tkinter.filedialog as filedialog
import pandas as pd
import customtkinter as ctk
import tkinter.messagebox as messagebox

DATA_FILE = "clients.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ClientManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Amris Web – Gestion de Prospection")
        self.geometry("1150x700")
        self.minsize(900, 600)

        self.clients = self.load_data()
        self.selected_index = None

        self.create_widgets()
        self.refresh_tree()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump([], f)
        with open(DATA_FILE, 'r') as f:
            return json.load(f)

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.clients, f, indent=4)

    def create_widgets(self):
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(pady=10, fill="x")

        self.name_entry = self._create_labeled_entry(self.form_frame, "Nom", 0)
        self.activity_entry = self._create_labeled_entry(self.form_frame, "Activité", 1)
        self.phone_entry = self._create_labeled_entry(self.form_frame, "Téléphone", 2)
        self.link_entry = self._create_labeled_entry(self.form_frame, "Lien", 3)

        ctk.CTkLabel(self.form_frame, text="Statut").grid(row=0, column=2, padx=10, sticky='w')
        self.status_combobox = ctk.CTkComboBox(self.form_frame, values=["Contacté ✅", "À contacter ☎️", "À relancer ⏳"])
        self.status_combobox.grid(row=0, column=3, padx=10)

        ctk.CTkLabel(self.form_frame, text="Commentaire").grid(row=1, column=2, padx=10, sticky='nw')
        self.comment_entry = ctk.CTkTextbox(self.form_frame, width=250, height=100)
        self.comment_entry.grid(row=1, column=3, padx=10, pady=5)

        ctk.CTkButton(self.form_frame, text="Ajouter le client", command=self.add_client).grid(row=4, column=1, pady=10)
        ctk.CTkButton(self.form_frame, text="Modifier le client", command=self.update_client).grid(row=4, column=2, pady=10)
        ctk.CTkButton(self.form_frame, text="Importer depuis Excel", command=self.import_excel).grid(row=4, column=3, pady=10)

        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=10)
        ctk.CTkLabel(self.search_frame, text="Rechercher :").pack(side="left")
        self.search_entry = ctk.CTkEntry(self.search_frame)
        self.search_entry.pack(side="left", padx=5)
        ctk.CTkButton(self.search_frame, text="OK", command=self.search_clients).pack(side="left")

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(pady=10, fill="both", expand=True)

        self.tree = ctk.CTkScrollableFrame(self.tree_frame)
        self.tree.pack(fill="both", expand=True)
        self.tree_items = []

    def _create_labeled_entry(self, parent, label, row):
        ctk.CTkLabel(parent, text=label).grid(row=row, column=0, padx=10, sticky='w')
        entry = ctk.CTkEntry(parent, width=300)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def add_client(self):
        client = self._get_client_data()
        if not client["Nom"]:
            ctk.CTkMessagebox(title="Erreur", message="Le nom est requis.", icon="warning")
            return
        self.clients.append(client)
        self.save_data()
        self.refresh_tree()
        self.clear_fields()

    def update_client(self):
        if self.selected_index is None:
            ctk.CTkMessagebox(title="Erreur", message="Aucun client sélectionné.", icon="warning")
            return
        self.clients[self.selected_index] = self._get_client_data()
        self.save_data()
        self.refresh_tree()
        self.clear_fields()

    def _get_client_data(self):
        return {
            "Nom": self.name_entry.get(),
            "Activité": self.activity_entry.get(),
            "Téléphone": self.phone_entry.get(),
            "Lien": self.link_entry.get(),
            "Statut": self.status_combobox.get(),
            "Commentaire": self.comment_entry.get("1.0", "end").strip()
        }

    def clear_fields(self):
        self.name_entry.delete(0, "end")
        self.activity_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.link_entry.delete(0, "end")
        self.comment_entry.delete("1.0", "end")
        self.status_combobox.set("")

        self.selected_index = None

    def refresh_tree(self, filtered_clients=None):
        for widget in self.tree.winfo_children():
            widget.destroy()

        clients = filtered_clients if filtered_clients else self.clients
        self.tree_items = []

        for index, c in enumerate(clients):
            container = ctk.CTkFrame(self.tree)
            container.pack(fill="x", padx=5, pady=5)

            info = f"{c['Nom']} | {c['Activité']} | {c['Téléphone']} | {c['Lien']} | {c['Statut']} | {str(c['Commentaire'])[:30]}..."
            label = ctk.CTkLabel(container, text=info, anchor="w")
            label.pack(side="left", fill="x", expand=True, padx=5)

            btn_update = ctk.CTkButton(container, text="Modifier", width=100, command=lambda idx=index: self.load_client(idx))
            btn_update.pack(side="left", padx=5)

            btn_delete = ctk.CTkButton(container, text="Supprimer", width=100, command=lambda idx=index: self.delete_client(idx))
            btn_delete.pack(side="right", padx=5)

            self.tree_items.append(container)

    def load_client(self, index):
        client = self.clients[index]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, client["Nom"])
        self.activity_entry.delete(0, "end")
        self.activity_entry.insert(0, client["Activité"])
        self.phone_entry.delete(0, "end")
        self.phone_entry.insert(0, client["Téléphone"])
        self.link_entry.delete(0, "end")
        self.link_entry.insert(0, client["Lien"])
        self.status_combobox.set(client["Statut"])
        self.comment_entry.delete("1.0", "end")
        self.comment_entry.insert("1.0", client["Commentaire"])
        self.selected_index = index

    def search_clients(self):
        query = self.search_entry.get().lower()
        results = [c for c in self.clients if query in c["Nom"].lower() or query in c["Activité"].lower()]
        self.refresh_tree(results)

    def import_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers Excel", "*.xlsx *.xls")])
        if not file_path:
            return
        try:
            df = pd.read_excel(file_path)
            required_columns = {"Nom", "Activité", "Téléphone", "Lien", "Statut", "Commentaire"}
            if not required_columns.issubset(df.columns):
                ctk.CTkMessagebox(title="Erreur", message="Le fichier doit contenir les colonnes : Nom, Activité, Téléphone, Lien, Statut, Commentaire", icon="cancel")
                return
            for _, row in df.iterrows():
                client = {
                    "Nom": row["Nom"],
                    "Activité": row["Activité"],
                    "Téléphone": str(row["Téléphone"]),
                    "Lien": row["Lien"],
                    "Statut": row["Statut"],
                    "Commentaire": str(row["Commentaire"])
                }
                self.clients.append(client)
            self.save_data()
            self.refresh_tree()
        except Exception as e:
            ctk.CTkMessagebox(title="Erreur", message=f"Impossible d'importer le fichier : {e}", icon="cancel")

    def delete_client(self, index):
        confirm = messagebox.askyesno("Confirmation", "Supprimer ce client ?")
        if confirm:
            del self.clients[index]
            self.save_data()
            self.refresh_tree()
            self.clear_fields()

if __name__ == "__main__":
    app = ClientManagerApp()
    app.mainloop()
