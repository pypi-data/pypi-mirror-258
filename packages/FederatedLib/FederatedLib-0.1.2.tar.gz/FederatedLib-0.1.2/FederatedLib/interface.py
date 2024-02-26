import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")  # Utilisez l'interface graphique Tkinter pour afficher les graphiques
from tkinter import messagebox, Toplevel, Label, Button, StringVar
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import Compose, ToTensor, Normalize
from torch.utils.data import DataLoader, random_split, Subset
from torchvision.datasets import CIFAR10
import paramiko
import io
import pkg_resources
import concurrent.futures
import random
import re
import numpy as np
import matplotlib.pyplot as plt
import os
import ssl
from functools import partial
from .base import Client, Server
import importlib
import sys
import time
import inspect
# Désactive verification ssl
ssl._create_default_https_context = ssl._create_unverified_context
# Choisi GPU ou CPU. Gpu si il est disponible
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class ClientManager:
    def __init__(self):
        # Initialise une liste vide pour stocker les informations des clients
        self.clients = []
        # Charge les clients
        self.load_clients_from_file()
        
    # Charge les clients depuis un fichier lors de la création du gestionnaire de clients
    def load_clients_from_file(self):
        try:
            # Tente d'ouvrir le fichier 'config.txt' et de lire les informations des clients
            with open('config.txt', 'r') as file:
                for line in file:
                    # Divise chaque ligne en informations sur le client et convertit en dictionnaire
                    client_info = line.strip().split(':')
                    self.clients.append({
                        'ID': int(client_info[0]),
                        'IP': client_info[1],
                        'username': client_info[2],
                        'password': client_info[3],
                        'path': client_info[4],
                        'python_version': client_info[5]
                    })
        except FileNotFoundError:
            pass

    # Sauvegarde les clients dans le config.txt
    def save_clients_to_file(self):
        with open('config.txt', 'w') as file:
            for client in self.clients:
                file.write(f"{client['ID']}:{client['IP']}:{client['username']}:{client['password']}:{client['path']}:{client['python_version']}\n")

    # Ajoute un client dans le fichier config
    def add_client(self, client_info):
        max_id = max([client['ID'] for client in self.clients], default=0)
        client_info['ID'] = max_id + 1
        self.clients.append(client_info)
        self.save_clients_to_file()

    # Retire un client de la classe et réécrit config.txt
    def remove_client(self, client_id):
        self.clients = [client for client in self.clients if client['ID'] != client_id]
        self.save_clients_to_file()

class GUI:
    # Root = fenêtre
    def __init__(self, root, Net, dependances, fonction_choix, fonction_average, directory):
        self.root = root
        self.root.title("Client Manager")
        self.Net = Net
        self.root.geometry("1400x820")  
        self.root.minsize(1400, 820)    
        self.client_manager = ClientManager()
        self.choix_utilisateur = "nouveau"
        self.fonction_choix = fonction_choix
        self.fonction_average = fonction_average
        self.dependances = dependances
        self.directory = directory
        self.creer_carre_blanc()

        

        
        self.create_table()

    # Créer un tableau avec les informations clients
    def create_table(self):
        columns = ["ID", "IP", "Username", "Password", "Path", "Python Version"]
        
        self.table = tk.ttk.Treeview(self.root, columns=columns, show='headings')
        for col, width in zip(columns, [100, 100, 100, 100, 170, 100]):
            self.table.heading(col, text=col)
            self.table.column(col, width=width, anchor='center')

        for client in self.client_manager.clients:
            self.table.insert("", "end", values=(client['ID'], client['IP'], client['username'], client['password'], client['path'], client['python_version']))
        
        

        self.table.grid(row=0, column=0, padx=10, pady=2, sticky="nw")
        grille = tk.Frame(self.root)
        grille.grid(row=1, column=0)
        # Bouton Modifier
        modify_button = tk.Button(grille, text="Modify", command=self.modify_client)
        modify_button.grid(row=0, column=0, padx=5, pady=2)
        

        # Bouton Supprimer
        delete_button = tk.Button(grille, text="Delete", command=self.delete_client)
        delete_button.grid(row=0, column=1, padx=5, pady=2)

        # Bouton Ajoute un Client
        add_button = tk.Button(self.root, text="Add Client", command=self.open_add_client_window)
        add_button.grid(row=2, column=0, columnspan=1, pady=2)

        # Emplacement du serveur
        self.input_frame = tk.LabelFrame(self.root, text="Serveur")
        self.input_frame.grid(row=3, column=0, padx=10, pady=3)

        # LabelFrames pour regrouper chaque paire d'étiquette et d'entrée
        labels = ["IP Address", "Username", "Password"]
        self.entry_widgets = []

        for label_text in labels:
            label_frame = tk.LabelFrame(self.input_frame, text=label_text)
            label_frame.grid(row=labels.index(label_text) * 2, column=0, padx=10, pady=3, sticky="w")

            entry_widget = tk.Entry(label_frame)
            entry_widget.grid(row=0, column=0, padx=5, pady=3)

            self.entry_widgets.append(entry_widget)
        # Crée en emplacement pour les infos du FL
        grille2 = tk.Frame(self.root)
        grille2.grid(row=4, column=0)
        # Infos FL
        label1 = tk.Label(grille2, text="nb_Clients:")
        label2 = tk.Label(grille2, text="Rounds:")
        label3 = tk.Label(grille2, text="Epochs:")

        # Créez trois Spinboxs pour les entiers avec une plage de valeurs de 0 à 100
        self.spinbox1 = tk.Spinbox(grille2, from_=2, to=100, width=3)
        self.spinbox2 = tk.Spinbox(grille2, from_=1, to=100, width=3)
        self.spinbox3 = tk.Spinbox(grille2, from_=1, to=100, width=3)

        label1.grid(row=0, column=0, padx=5, pady=3)
        self.spinbox1.grid(row=0, column=1, padx=5, pady=3)

        label2.grid(row=0, column=2, padx=5, pady=3)
        self.spinbox2.grid(row=0, column=3, padx=5, pady=3)

        label3.grid(row=0, column=4, padx=5, pady=3)
        self.spinbox3.grid(row=0, column=5, padx=5, pady=3)

        grille3 = tk.Frame(self.root)
        grille3.grid(row=5, column=0)
        # Création des Label widgets pour afficher le texte non modifiable
        self.client_choice_label = tk.Label(grille3, text="client choice function: {}".format(self.fonction_choix.__name__))
        self.client_choice_label.grid(row=0, column=0, padx=5)

        self.averaging_label = tk.Label(grille3, text="averaging function: {}".format(self.fonction_average.__name__))
        self.averaging_label.grid(row=0, column=1, padx=5)

        add_button = tk.Button(self.root, text="Run", command=self.run_server)
        add_button.grid(row=6, column=0, columnspan=1, pady=3)

    
    # Fonction qui execute le federated learning
    def run_server(self):
        # Récupère les entrées de l'utilisateur dans l'interface
        nb_clients_str = self.spinbox1.get()
        rounds_str = self.spinbox2.get()
        epochs_str = self.spinbox3.get()
        nb_clients = int(nb_clients_str)
        rounds = int(rounds_str)
        epochs = int(epochs_str)
        ip_address = self.entry_widgets[0].get()
        username = self.entry_widgets[1].get()
        password = self.entry_widgets[2].get()
       
        print(f'test GUI : { self.directory}')
        # Instancie la classe server
        server = Server(ip_address, username, password, self.directory)
        # Instancie la classe FederatedLearning
        fl = FederatedLearning.with_server(self.Net, server)
        # Si un modèle existe déjà, demande pour le supprimer ou le garder.
        fichier_existe = os.path.exists(self.directory+"/m.pt")
        if(fichier_existe):
            def on_button_click(response):
                # Fonction appelée lorsqu'un bouton est cliqué
                self.choix_utilisateur = response
                #messagebox.showinfo("Réponse", "Vous avez choisi : {}".format(response))
                root.destroy()  # Ferme la fenêtre après avoir affiché la réponse
                root.after(100)
                results_table, comp_evolution = fl.federatedLearning(nb_clients, epochs, rounds, server, self.choix_utilisateur, self.dependances ,averaging_function=self.fonction_average, client_choice_function=self.fonction_choix)
                self.afficher_graphe(results_table, comp_evolution)

            # Création de la fenêtre principale
            root = tk.Tk()
            root.title("Question")

            # Texte de la question
            question_label = tk.Label(root, text="m.pt exsiste, \n Continuer avec ou créer un nouveau modèle ?")
            question_label.pack(pady=10)

            # Boutons avec les réponses possibles
            button1 = tk.Button(root, text="continuer", command=lambda: on_button_click("continuer"))
            button1.pack(side=tk.LEFT, padx=10)

            button2 = tk.Button(root, text="nouveau", command=lambda: on_button_click("nouveau"))
            button2.pack(side=tk.RIGHT, padx=10)

            # Lancement de la boucle
            root.mainloop()
        else:
            # Recupere les résultats et affiche le graphe
            results_table, comp_evolution = fl.federatedLearning(nb_clients, epochs, rounds, server, self.choix_utilisateur, self.dependances ,averaging_function=self.fonction_average, client_choice_function=self.fonction_choix)
            self.afficher_graphe(results_table, comp_evolution)
        
        
    
    # Fonction qui permet de modifier les informations d'un client dans l'interface
    def modify_client(self):
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showinfo("Erreur", "Choisissez un client à modifier")
            return
        # Récupère le client id qui servira à determiner quelle ligne il faut modifier dans le fichier config
        client_id = int(self.table.item(selected_item, 'values')[0])
        client_to_modify = next(client for client in self.client_manager.clients if client['ID'] == client_id)

        # Crée une fenêtre de modification similaire à la fenêtre d'ajout
        modify_client_window = tk.Toplevel(self.root)
        modify_client_window.title("Modify Client")

        entry_labels = ["IP", "username", "password", "path", "python_version"]
        entries = {}
        for i, label in enumerate(entry_labels):
            tk.Label(modify_client_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            
            entries[label] = tk.Entry(modify_client_window)
            entries[label].insert(0, str(client_to_modify.get(label, '')))
            entries[label].grid(row=i, column=1, padx=10, pady=5)

        # Met à jour les modifications
        def apply_modification():
            for label in entry_labels:
                client_to_modify[label] = entries[label].get()
            # Sauvegarde 
            self.client_manager.save_clients_to_file()
            # Supprime la fenêtre
            modify_client_window.destroy()
            # Met à jour le tableau
            self.update_table()


        # Bouton appliquer
        apply_button = tk.Button(modify_client_window, text="Apply", command=apply_modification)
        apply_button.grid(row=len(entry_labels), columnspan=2, pady=10)
    # Fonction d'ajout de client dans le tableau et le fichier config.
    def open_add_client_window(self):
        add_client_window = tk.Toplevel(self.root)
        add_client_window.title("Add Client")
        # Affichage colonnes
        entry_labels = ["IP", "Username", "Password", "Path", "Python Version"]
        entries = {}

        for i, label in enumerate(entry_labels):
            tk.Label(add_client_window, text=label).grid(row=i, column=0, padx=10, pady=5)
            
            entries[label] = tk.Entry(add_client_window)
            entries[label].grid(row=i, column=1, padx=10, pady=5)

        # Recupere les entrées de l'utilisateur
        def add_client():
            client_info = {
                'IP': entries['IP'].get(),
                'username': entries['Username'].get(),
                'password': entries['Password'].get(),
                'path': entries['Path'].get(),
                'python_version': entries['Python Version'].get()
            }
            # Ajout le client à la classe client_manager
            self.client_manager.add_client(client_info)
            # Destruiction de la fenêtre
            add_client_window.destroy()
            # Mise à jour du tableau
            self.update_table()

        # Boutton ajouter
        add_button = tk.Button(add_client_window, text="Add", command=add_client)
        add_button.grid(row=len(entry_labels), columnspan=2, pady=10)

    # Fonction pour supprimer un client du fichier config et du tableau de l'interface
    def delete_client(self):
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showinfo("Erreur", "Choisissez un client à supprimer.")
            return
        # Recupere id client
        client_id = int(self.table.item(selected_item, 'values')[0])
        # Supprime du fichier config
        self.client_manager.remove_client(client_id)
        # Met à jour le tableau
        self.update_table()

    # Fonction pour mettre à jour les valeurs du client sélectionné dans le tableau
    def update_table(self):
        # Supprime toutes les lignes
        for row in self.table.get_children():
            self.table.delete(row)
        # Ecrit tout les clients dans le tableau
        for client in self.client_manager.clients:
            self.table.insert("", "end", values=(client['ID'], client['IP'], client['username'], client['password'], client['path'], client['python_version']))

    # Crée une zone pour afficher les graphiques
    def creer_carre_blanc(self):
        self.carre = tk.Frame(self.root, bg="white", width=650, height=750)
        self.carre.grid(row=0, column=1, rowspan=7, padx=30, pady=30)

        # Zone où on peut scroll
        canvas = tk.Canvas(self.carre, bg="white", width=650, height=750, scrollregion=(0, 0, 650, 750))
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar 
        scrollbar = tk.Scrollbar(self.carre, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Sous zone pour le graphe
        self.graph_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=self.graph_frame, anchor="nw")

        # Permet de scroll avec la molette de la souris
        self.graph_frame.bind("<MouseWheel>", lambda event: self.on_mousewheel(event, canvas))

    def on_mousewheel(self, event, canvas):
        # Cette fonction gère l'événement de la molette de la souris pour le défilement
        if event.delta:
            # Si il y a un evenement, ajoute la position du défilement
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Affichage des graphes à partir des résultats du federated learning
    def afficher_graphe(self, results_tables, comp_evolution):
        num_columns = len(results_tables[0][0]) - 1  
        # Creation des graphes
    
        graph_frame_height = 330*len(results_tables) + 700

        # Ajustement de la hauteur minimale du cadre des graphes
        if graph_frame_height < 750:
            graph_frame_height = 750

        # Configuration du canvas pour permettre le défilement vertical
        canvas = self.graph_frame.master
        canvas.config(scrollregion=(0, 0, 650, graph_frame_height))
        # Nom des colonnes
        column_names = ['id', 'loss', 'accuracy', 'train_time', 'test_time']
        # Sous graphes avec les résultats
        fig, axs = plt.subplots(len(results_tables), len(column_names) - 1, figsize=(7, 3*len(results_tables)), sharex=True)
        fig.subplots_adjust(top=1-(260/graph_frame_height))
        fig.suptitle("Performance Metrics")
             
        for i, results_table in enumerate(results_tables):
            
            for j in range(1, len(column_names)):
                row = i
                col = j - 1

                data = results_table[:, j]
                if len(results_tables) == 1:
                    # Si un seul résultat (1 seul client), crée un sous-graphe de barres pour la colonne actuelle
                    axs[col].bar(np.arange(len(results_table)), data, color='blue', alpha=0.7)
                    axs[col].set_title(column_names[j])
                else:
                    # Si plusieurs résulats, crée un sous-graphe de barres pour chaque table et chaque colonne
                    axs[row, col].bar(np.arange(len(results_table)), data, color='blue', alpha=0.7)
                    axs[row, col].set_title(column_names[j])
    
        # Ajustement de l'espacement vertical entre les sous-graphes
        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=0.5) 
        # largeur minimale 
        min_width = len(comp_evolution) - 1
        # Sépare les graphes
        fig_line, axs_line = plt.subplots(2, 1, figsize=(7, 6))
        fig_line.suptitle("Évolution du Modèle")

        
        loss_curve = [entry[0] for entry in comp_evolution]
        accuracy_curve = [entry[1] for entry in comp_evolution]

        axs_line[0].plot(loss_curve, label="Loss")
        axs_line[0].set_xlim(0, min_width)  
        axs_line[0].set_xlabel("Round")
        axs_line[0].set_ylabel("Loss")

        axs_line[1].plot(accuracy_curve, label="Accuracy")
        axs_line[1].set_xlim(0, min_width)  
        axs_line[1].set_xlabel("Round")
        axs_line[1].set_ylabel("Accuracy")

        # Espacement
        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=0.5)

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Affichage
        self.figure = fig
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top")
        canvas_line = FigureCanvasTkAgg(fig_line, master=self.graph_frame)
        canvas_line.draw()
        canvas_line.get_tk_widget().pack(side="top")







# Main classe du federated learning à instancier pour faire du fl
class FederatedLearning:
    def __init__(self, net_class):
        self.net_class = net_class
        self.choix_utilisateur = "nouveau"
        frame_info = inspect.stack()[1]
        chemin_fichier = os.path.abspath(frame_info[1])
        self.chemin_du_fichier = os.path.dirname(chemin_fichier)
        
       
    @classmethod
    def with_server(cls, net_class, server):
        instance = cls(net_class)
        instance.server = server
        return instance
    # Function pour trouver la chemin d'une librairie
    def find_module_path(self, module_name):
        try:
            module_spec = importlib.util.find_spec(module_name)
            if module_spec is not None:
                return module_spec.origin
        except ImportError:
            pass

        return None
    # Affiche le chemin de la librairie
    def afficher(self):
        module_name = "FederatedLib.TorchClient"
        module_path = self.find_module_path(module_name)

        if module_path is not None:
            print(f"Le chemin vers le module '{module_name}' est : {module_path}")
        else:
            print(f"Le module '{module_name}' n'a pas été trouvé.")

    # Créer et retourne une liste de client lu à partir du fichier config.txt
    def lire_config(self, file_path):
        clients = []

        with open(file_path, 'r') as file:
            for line in file:
                # Supprimer les espaces et diviser la ligne en fonction du caractère ":"
                values = line.strip().split(':')

                # Créer un objet Client à partir des valeurs lues
                client = Client(*values)

                # Ajouter le client à la liste
                clients.append(client)

        return clients


    # Affiche les poids d'un model, sert simplement de debug
    def afficher_poids(self, model):
        for nom_couche, parametre in model.named_parameters():
            if parametre.requires_grad:
                print(f"{nom_couche}: {parametre.data}")


   # Fonction qui permet d'executer toutes les commmandes nécessaires via une connection SSH et SFTP
    def ssh_upload(self, hostname, username, password, local_files, remote_directory, command_to_execute, id, python, epochs, server, dependances):
        # Créer une instance SSH client
        ssh = paramiko.SSHClient()
        # Ajoute automatiquement la clé d'hôte au serveur
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Se connecte au client en ssh
            ssh.connect(hostname, username=username, password=password)
            # Execute une commande dans le cmd du client pour installer toutes les dépendances
            command = python + " -m pip install cryptography torch torchvision paramiko numpy pandas 'portalocker>=2/0.0'"
            for dependance in dependances:
                command += f" {dependance}"
            print(command)
            stdin, stdout, stderr = ssh.exec_command(command)
            print("Installation des librairies necessaire ...")
            # Affiche la sortie de la commande
            stdout = io.TextIOWrapper(stdout, encoding='utf-8', errors='replace')
            for line in stdout:
                if "Requirement already satisfied" not in line:
                    print(line)
            # Créer un transport SFTP
            sftp = ssh.open_sftp()

            stdin, stdout, stderr = ssh.exec_command(f'[ -d "{remote_directory}" ] && echo "True" || echo "False"')

            # Lire la sortie pour savoir si le répertoire existe
            directory_exists = stdout.read().decode().strip() == "True"

            # Si le répertoire n'existe pas, le créer
            if not directory_exists:
                ssh.exec_command(f'mkdir {remote_directory}')
                print(f"Le répertoire {remote_directory} a été créé avec succès")

            # Envoie un fichier id.txt avec l'id du client vers le client
            with sftp.file(remote_directory + '/ID.txt', 'w') as fichier:
                fichier.write(str(id))
            print(f"Le fichier ID.txt a été envoyé avec succès vers {remote_directory}")

            # Envoyer les fichiers nécessaires au federated vers le client
            for local_file in local_files:
                remote_path = remote_directory + '/' + local_file
                if local_file == "m.pt" or local_file == "neuralNetwork.py":
                    sftp.put(server.dir+"/"+local_file, remote_path)
                else:
                    sftp.put(pkg_resources.resource_filename('FederatedLib', local_file), remote_path)
                print(f"Le fichier {local_file} a été envoyé avec succès vers {remote_path}")
                
            # Fermer la connexion SFTP
            sftp.close()
            
            # Créer une commande dans le cmd pour l'entrainement du modèle chez le client et envoie des informations du serveur
            command_to_execute = python + " " + command_to_execute + ' "' + remote_directory + '" --epochs ' + str(epochs) + ' --ip_address ' + server.ip_address +" --username " + server.username+" --password "+server.password+" --dir "+server.dir+" --acc "+str(self.last_accuracy)
            print(command_to_execute)
            # Exécute la commande et affiche la sortie
            stdin, stdout, stderr = ssh.exec_command(command_to_execute)
            print("Sortie de la commande:")
            
            stdout = io.TextIOWrapper(stdout, encoding='utf-8', errors='replace')
            # Retourne les résultats de l'entrainement
            for line in stdout:
                
                if("Accuracy" in line or "Loss" in line or "Train" in line or "Test" in line) :
                    print(line)
                    # Regex pour attribuer les valeurs aux bonnes variables
                    match = re.search(r'Loss: ([\d.]+), Accuracy: ([\d.]+), Train: ([\d.]+) secondes, Test: ([\d.]+) secondes', line)
                    if match:
                        loss = float(match.group(1))
                        accuracy = float(match.group(2))
                        train_time = float(match.group(3))
                        test_time = float(match.group(4))
                    else:
                        print("Aucune correspondance trouvée.")
                    return loss, accuracy, train_time, test_time, id
           
              
                
        except Exception as e:
            print(f"Une erreur s'est produite : {str(e)}")

        finally:
            # Fermer la connexion SSH
            ssh.close()
    # Fonction qui exécute le federated learning sur un client (Devra être utiliser avec des threads)
    def executer_en_parallele(self, client, epochs, server, dependances):
        print("epochs : "+str(epochs))
        command_to_execute = client.dir + "/TorchClient.py"
        result = self.ssh_upload(client.ip_address, client.username, client.password,["m.pt", "TorchClient.py", "neuralNetwork.py"], client.dir, command_to_execute, client.client_id, client.python, epochs, server, dependances)
        return result
    # Politique de choix des clients aléatoires
    def choix_client_alea(self, nb_client, tableau_client):
        # Choisi un nombre nb_clients de clients aléatoires dans la liste 
        clients_choisis = random.sample(tableau_client, nb_client)
        print("Clients choisis:")
        for client in clients_choisis:
            print("ID du client:", client.client_id)
                # Vous pouvez remplacer "id" par le nom de l'attribut qui stocke l'ID du client dans votre tableau_client
            
        return clients_choisis
                

    def plot_data(self, results_table):
        # Récupérer les données pour chaque colonne
        id_clients = results_table[:, 0]
        loss_values = results_table[:, 1]
        accuracy_values = results_table[:, 2]
        train_time_values = results_table[:, 3]
        test_time_values = results_table[:, 4]

        title = np.array(["Loss", "Accuracy", "Train time", "Test time"])
        # Convertir les valeurs des ID clients en entiers
        id_clients = id_clients.astype(int)

        # Nombre de lignes dans le tableau
        num_rows = results_table.shape[0]

        # Calculer le nombre de colonnes pour les sous-graphiques
        num_cols = 4  # Vous pouvez ajuster cela en fonction du nombre de colonnes que vous souhaitez afficher

        # Créer 4 graphiques distincts
        plt.figure(figsize=(12, 8))

        # Palette de couleurs
        colors = plt.cm.viridis(np.linspace(0, 1, len(id_clients)))

        for i in range(num_cols):
            plt.subplot(num_rows//2, num_cols, i+1)
            plt.bar(id_clients, results_table[:, i+1], color=colors)
            plt.title(title[i])
            plt.xlabel('id_client')
            plt.ylabel(title[i])
            plt.xticks(id_clients)

        plt.tight_layout()  # Pour améliorer la mise en page

        #plt.show()

    def plot_evolution(self, data):
        # Transposer le tableau pour obtenir des listes distinctes de loss et d'accuracy
        data_transposed = np.array(data).T

        # Récupérer la loss et l'accuracy
        loss = data_transposed[0]
        accuracy = data_transposed[1]

        # Créer un tableau d'index pour l'axe des x
        index = np.arange(len(loss))

        # Tracer la courbe de la loss
        plt.figure(figsize=(10, 5))  # Créer une nouvelle figure
        plt.subplot(1, 2, 1)  # Diviser la figure en 1 ligne et 2 colonnes, sélectionner la première colonne
        plt.plot(index, loss, label='Loss', marker='o')
        plt.xlabel('Round')
        plt.ylabel('Loss')
        plt.title('Évolution de la Loss')
        plt.legend()

        # Tracer la courbe de l'accuracy
        plt.subplot(1, 2, 2)  # Sélectionner la deuxième colonne
        plt.plot(index, accuracy, label='Accuracy', marker='o')
        plt.xlabel('Round')
        plt.ylabel('Accuracy')
        plt.title('Évolution de l\'Accuracy')
        plt.legend()

        # Ajuster la disposition pour éviter les chevauchements
        plt.tight_layout()

        # Afficher les graphiques
        #plt.show()

    # Exemple d'utilisation avec votre tableau


    # Permet de récuperer les temps d'éxecutions et performance d'un client
    def get_perfs(self):
        config_file = './config.txt'
        clients = self.lire_config(config_file)

        # Liste pour stocker les lignes de chaque client
        all_perfs = []

        def process_client(client):
            perfs = []  # Liste pour stocker les lignes du client actuel
            try:
                # Établir une connexion SSH
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(client.ip_address, username=client.username, password=client.password)

                # Lire le fichier perf.txt
                perf_file_path = f"{client.dir}/perf.txt"
                with ssh.open_sftp().file(perf_file_path, 'r') as perf_file:
                    # Ajouter chaque ligne du fichier perf.txt à la liste perfs
                    perfs.append(client.client_id)
                    perfs.extend(perf_file.read().splitlines())
                    

                # Fermer la connexion SSH
                ssh.close()

            except Exception as e:
                print(f"Erreur lors de la connexion au client {client.client_id}: {e}")

            # Ajouter la liste perfs à la liste all_perfs
            all_perfs.append(perfs)

        # Utiliser ThreadPoolExecutor pour le traitement en parallèle
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_client, clients)

        tableau = [[0 for _ in range(3)] for _ in range(len(all_perfs))]
        # Utiliser la liste all_perfs comme nécessaire dans votre code
        for perfs in all_perfs:
            if len(perfs) >= 4:
                client_id = perfs[0]
                accuracy = float(perfs[1])
                temps = float(perfs[2])
                div = float(perfs[3])
                
                # Calculer les valeurs nécessaires et les afficher
                accuracy_divided = accuracy / div
                temps_divided = temps / div

                tableau[int(client_id)-1][0] = int(client_id)
                tableau[int(client_id)-1][1] = accuracy_divided
                tableau[int(client_id)-1][2] = temps_divided

        return tableau


    def running_model_avg(self, current, next, scale):
            # Calcul de la moyenne pondérée des modèles actuel et suivant
            if current == None:
                # Si le modèle actuel n'est pas défini, initialise le modèle suivant multiplié par scale
                current = next
                for key in current:
                    current[key] = current[key] * scale
            else:
                for key in current:
                    current[key] = current[key] + (next[key] * scale)
            return current
    
    # Fonction qui permet la fusion des modèles avec average
    def average_models(self, folder_path):
        
        #  Recupere les modèles (fichiers terminant .pt)
        file_list = [f for f in os.listdir(folder_path) if f.endswith('.pt')]
        # Initialise le modèle de base
        global_model = self.net_class()
        # Comptage du nombre de fichiers
        num_files = len(file_list)

        if num_files == 0:
            print("Aucun fichier .pt trouvé dans le dossier.")
            return None


        running_avg = None
        for index, filename in enumerate(file_list):
                print("Chargement du fichier")
                print(filename)
                model_path = os.path.join(folder_path, filename)
                local_model = torch.load(model_path, map_location=DEVICE) 
                local_model.to(DEVICE)

                # average des modeles
                running_avg = self.running_model_avg(running_avg, local_model.state_dict(), 1/num_files)
        # Chargement et sauvegarde du modèle average
        global_model.load_state_dict(running_avg)
        torch.save(global_model, "./m.pt")
        return global_model
    
    # Fonction qui supprime tout les modèles
    def reset_modeles(self, server):
        dossier_modeles = server.dir+"/modeles"

        # Vérifier si le dossier existe
        if os.path.exists(dossier_modeles):
            # Liste tous les fichiers dans le dossier
            fichiers = os.listdir(dossier_modeles)

            # Parcourir tous les fichiers et les supprimer un par un
            for fichier in fichiers:
                chemin_fichier = os.path.join(dossier_modeles, fichier)
                try:
                    # Supprimer le fichier
                    os.remove(chemin_fichier)
                    print(f"Fichier supprimé : {chemin_fichier}")
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier {chemin_fichier}: {e}")
        else:
            print(f"Le dossier {dossier_modeles} n'existe pas.")
    # Sauvegarde résultat 
    def sauvegarder_dans_fichier(self, tableau, nom_fichier):
        with open(nom_fichier, 'w') as fichier:
            for ligne in tableau:
                fichier.write(','.join(map(str, ligne)) + '\n')

    # Recupere et retourne les valeurs dans le fichier dans un tableau
    def recuperer_de_fichier(self, nom_fichier):
        tableau = []
        try:
            with open(nom_fichier, 'r') as fichier:
                for ligne in fichier:
                    valeurs = list(map(float, ligne.strip().split(',')))
                    tableau.append(valeurs)
            return tableau
        except FileNotFoundError:
            print(f"Le fichier {nom_fichier} n'existe pas.")
            return None
        except Exception as e:
            print(f"Une erreur s'est produite lors de la récupération du fichier : {e}")
            return None

    # recupere le dernier nombre pour l'accuracy
    def get_last_number_from_file(self, file_path):
        try:
            with open(file_path+"/evolution.txt", 'r') as file:
                # Lire toutes les lignes du fichier
                lines = file.readlines()

                # Vérifier si le fichier contient au moins une ligne
                if lines:
                    # Récupérer la dernière ligne
                    last_line = lines[-1]

                    # Diviser la dernière ligne en fonction de la virgule et récupérer le dernier nombre
                    last_number = float(last_line.strip().split(',')[-1])

                    return last_number
                else:
                    print("Le fichier est vide.")
                    return None

        except FileNotFoundError:
            print(f"Le fichier {file_path} n'existe pas.")
            return None

    
    
    # Fonction principale pour lancer le fedeated learning
    def federatedLearning(self, nb_client, epochs, round, server, choix, dependances, averaging_function, client_choice_function):
    
        
        print(choix)
        # Créer le dossier modeles
        folder_path = server.dir+"/modeles"
        if not os.path.exists(folder_path):
            try:
                # Créer le dossier s'il n'existe pas
                os.makedirs(folder_path)
                print(f"Dossier '{folder_path}' créé avec succès.")
            except OSError as e:
                print(f"Erreur lors de la création du dossier '{folder_path}': {e}")
        
        self.reset_modeles(server)
        
        
        # Chargement des ensembles de données d'entraînement et de test
        trainloader, testloader = self.net_class.load_data(server.dir)
        # Créer un nouveau modèle par défaut
        if choix == "nouveau":   
            modele = self.net_class()
            torch.save(modele, "m.pt")
            comp_table = []
            print("Test start model ...")
            loss, self.last_accuracy = modele.test(testloader, DEVICE)
            print(f"Loss: {loss:.5f}, Accuracy: {self.last_accuracy:.5f}")
            ligne = [loss, self.last_accuracy]
            comp_table.append(ligne)
        else:
            # Charge le modèle
            modele = torch.load(server.dir+"/m.pt", map_location=DEVICE) 
            # Vérification que le modèle n'a pas changé
            if str(modele) == str(self.net_class()):
                print("Le modèle n'as pas changé.")
                comp_table = self.recuperer_de_fichier(server.dir+"/evolution.txt")
            else:
                messagebox.showinfo("Information", "Le modèle a changé, vous ne pouvez pas utiliser m.pt, créez en un nouveau")
                sys.exit()
        # Créer le fichier config.txt si pas déjà fait 
        config_file = server.dir+'/config.txt'
        # Créer la liste de clients à partir du fichier config.txt
        liste_clients = self.lire_config(config_file)

        

        clients_choisis = client_choice_function(nb_client, liste_clients) # Minimum 2 clients sinon problèmes avec le plot
        

        results_tables = []
        for i in range(round):
            if i > 0:
                time.sleep(0.1)
                self.last_accuracy = self.get_last_number_from_file(server.dir)
                print(self.last_accuracy)
            if choix == "continuer":
                time.sleep(0.1)
                self.last_accuracy = self.get_last_number_from_file(server.dir)
            results_table = np.zeros((len(clients_choisis), 5))  # 5 columns for id, loss, accuracy, train_time, test_time
            print("\n\nRound " + str(i+1)+" :")
            if i > 0:
                modele = torch.load(server.dir+"/m.pt", map_location=DEVICE) 
            # Crée une nouvelle fonction avec epochs fixée en utilisant functools.partial
            executer_en_parallele_with_epochs = partial(self.executer_en_parallele, epochs=epochs, server=server, dependances=dependances)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Utilisez executor.map pour exécuter la fonction pour chaque client en parallèle
                results = list(executor.map(executer_en_parallele_with_epochs, clients_choisis))

            for i, result in enumerate(results):
                if result is not None:
                    loss, accuracy, train_time, test_time, id = result
                    results_table[i, 0] = id
                    results_table[i, 1] = loss
                    results_table[i, 2] = accuracy
                    results_table[i, 3] = train_time
                    results_table[i, 4] = test_time

            print("Results Table:")
            print(results_table)
            #self.plot_data(results_table)
            results_tables.append(results_table)
            
            folder_path = server.dir+"/modeles"
            averaged_model = averaging_function(folder_path)
            print(averaged_model)
            print("FIN DE AVERAGE")
            if averaged_model is not None:
                print("Test average model ...")
                loss, accuracy = averaged_model.test(testloader, DEVICE)
                print(f"Loss: {loss:.5f}, Accuracy: {accuracy:.5f}") 
                ligne = [loss, accuracy]
                comp_table.append(ligne)
                print(comp_table)
                self.sauvegarder_dans_fichier(comp_table, server.dir+"/evolution.txt")
            else:
                print("Dossier ./modeles vide")
        #self.plot_evolution(comp_table)
        return results_tables, comp_table
        #plt.ioff() 
        #plt.show()
    # Buton run, lance le federated learning
    def run(self, dependances, fonction_choix, fonction_average):
        self.root = tk.Tk()
        app = GUI(self.root, self.net_class, dependances, fonction_choix, fonction_average, self.chemin_du_fichier)
        self.root.mainloop()
    
