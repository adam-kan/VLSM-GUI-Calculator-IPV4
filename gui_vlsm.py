import customtkinter as ctk
from tkinter import messagebox
from vlsm_logic import calcul_vlsm, filtrer_et_rectifier_ip, verifier_sous_reseaux


def lancer_gui():
    ctk.set_appearance_mode("Dark")

    app = ctk.CTk()
    app.title(" VLSM Calculator")
    app.geometry("1200x800")
    app.configure(bg="#0F0F0F")  # unified dark tone

    container = ctk.CTkFrame(app, fg_color="#1A1A1A", corner_radius=12)
    container.pack(pady=30, padx=40)

    for i in range(4):
        container.grid_columnconfigure(i, weight=1)

    label_net = ctk.CTkLabel(container, text="Adresse Réseau :", font=("Segoe UI", 12), text_color="#F1F5F9")
    label_net.grid(row=0, column=0, padx=5, pady=8, sticky="e")

    entry_ip = ctk.CTkEntry(container, width=180, placeholder_text="192.168.1.0")
    entry_ip.grid(row=0, column=1, padx=5, pady=8)

    slash_label = ctk.CTkLabel(container, text="/", font=("Segoe UI", 14, "bold"), text_color="#F1F5F9")
    slash_label.grid(row=0, column=2, padx=4, pady=8)

    entry_mask = ctk.CTkEntry(container, width=50, placeholder_text="24")
    entry_mask.grid(row=0, column=3, padx=5, pady=8)

    label_count = ctk.CTkLabel(container, text="Nombre de sous-réseaux :", font=("Segoe UI", 12), text_color="#F1F5F9")
    label_count.grid(row=1, column=0, padx=5, pady=8, sticky="e")

    entry_count = ctk.CTkEntry(container, width=80, placeholder_text="ex: 3")
    entry_count.grid(row=1, column=1, padx=5, pady=8, sticky="w")

    subnet_entries = []

    def ajouter_champs():
        nonlocal subnet_entries
        for entry in subnet_entries:
            entry.destroy()
        subnet_entries.clear()

        try:
            count = int(entry_count.get())
            for i in range(count):
                ent = ctk.CTkEntry(container, width=120, placeholder_text=f"Sous-réseau {i+1}")
                ent.grid(row=2 + i // 4, column=i % 4, padx=5, pady=5)
                subnet_entries.append(ent)
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour les sous-réseaux.")

    btn_add_subnets = ctk.CTkButton(container, text="+ Ajouter Sous-Réseaux", command=ajouter_champs,
                                    fg_color="#7C3AED", hover_color="#A855F7", text_color="#FFFFFF",
                                    font=("Segoe UI Semibold", 12), corner_radius=8)
    btn_add_subnets.grid(row=1, column=2, columnspan=2, padx=5, pady=8)

    def afficher_resultats():
        try:
            ip_saisie = entry_ip.get()
            CIDR = int(entry_mask.get())   
            ip_debut = filtrer_et_rectifier_ip(ip_saisie, CIDR)  

            sous_reseaux = [int(ent.get()) for ent in subnet_entries if ent.get().isdigit()]
            verifier_sous_reseaux(sous_reseaux, CIDR)
            resultats = calcul_vlsm(ip_debut, sous_reseaux)

            for widget in result_frame.winfo_children():
                widget.destroy()

            headers = ["Sous-réseau", "Adresse réseau", "Masque", "Premier Adresse", "Dernier Adresse", "Diffusion", "Hôtes"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(result_frame, text=header, font=("Segoe UI", 13, "bold"), text_color="#F1F5F9", width=150)
                label.grid(row=0, column=i, padx=2, pady=6, sticky="nsew")

            for index, res in enumerate(resultats):
                values = [index + 1, res['add'], res['/CIDR'], res['padd'], res['dadd'], res['adddif'], res['n_hotes']]
                bg = "#1A1A1A" if index % 2 == 0 else "#222222"

                for i, val in enumerate(values):
                    label = ctk.CTkLabel(result_frame, text=str(val), font=("Segoe UI", 12), fg_color=bg,
                                          text_color="#F1F5F9", corner_radius=6, width=150)
                    label.grid(row=index + 1, column=i, padx=1, pady=1, sticky="nsew")

        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    ctk.CTkButton(app, text="🚀 Calculer", command=afficher_resultats, fg_color="#06B6D4",
                  hover_color="#0EA5E9", text_color="#0F172A", font=("Segoe UI Semibold", 12), corner_radius=10,
                  width=180, height=40).pack(pady=20)

    result_frame = ctk.CTkFrame(app, fg_color="#0F0F0F")
    result_frame.pack(pady=10, fill="both", expand=True)
    result_frame.pack_propagate(False)
    result_frame.configure(height=400)

    app.mainloop()


if __name__ == "__main__":
    lancer_gui()
