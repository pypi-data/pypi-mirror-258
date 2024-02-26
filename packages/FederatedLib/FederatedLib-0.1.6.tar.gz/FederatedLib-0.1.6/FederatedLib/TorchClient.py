import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.transforms import Compose, ToTensor, Normalize
from torch.utils.data import DataLoader, random_split, Subset
from torchvision.datasets import CIFAR10
import time
import paramiko
import argparse
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
from torch.utils.data import DataLoader
from neuralNetwork import Net
import os

# Fonction qui garde en mêmoire les performances moyennes d'un client sur celui ci
def save_perf(gain_accuracy, train_time):
    
     # Obtenir le chemin absolu du répertoire du fichier actuel
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Concaténez le chemin absolu du fichier "perf.txt"
    perf_file_path = os.path.join(script_dir, "perf.txt")
    # Vérifier si le fichier existe
    try:
        with open(perf_file_path, "r") as file:
            # Lire les valeurs existantes
            lines = file.readlines()
            if len(lines) >= 3:
                # Mettre à jour les valeurs
                lines[0] = f"{(float(lines[0])+gain_accuracy):.5f}\n"
                lines[1] = f"{(float(lines[1])+train_time):.3f}\n"
                lines[2] = f"{int(lines[2]) + 1}\n"
            else:
                # Le fichier ne contient pas assez de lignes, le corriger manuellement
                print("Le fichier perf.txt ne contient pas assez de lignes. Corrigez-le manuellement.")

    except FileNotFoundError:
        # Le fichier n'existe pas, le créer avec les valeurs spécifiées
        lines = [f"{gain_accuracy:.5f}\n", f"{train_time:.3f}\n", "1\n"]

    # Écrire les valeurs dans le fichier
    with open(perf_file_path, "w") as file:
        file.writelines(lines)
    print("fichier perf.txt bien créé.")


# Fonction utilisé lors du dévelopement pour que chaque client entraine sur un dataset différent
def load_data_diff(repertoire):
    trf = Compose([ToTensor(), Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    dataset = CIFAR10(repertoire+"/data", train=True , download=True, transform=trf)
    testset = CIFAR10(repertoire+"/data", train=False , download=True, transform=trf)

    # calcul la taille de chaque training split
    total_size = len(dataset)
    split_size = total_size // 2

    # création d'indices pour les sous ensembles
    indices = list(range(total_size))
    train_indices_1, train_indices_2= random_split(
        indices, [split_size, split_size]
    )

    # création d'instances de sous ensembles basés sur les indices
    trainset_1 = Subset(dataset, train_indices_1)
    trainset_2 = Subset(dataset, train_indices_2)


    # Affichage de chaque dataset
    print(f"Size of trainset_1: {len(trainset_1)}")
    print(f"Size of trainset_2: {len(trainset_2)}")
    print(f"Size of testset: {len(testset)}")

    # choix du dataset selon le client
    if repertoire == "/home/pi/Desktop/Projet":
        return DataLoader(trainset_1, batch_size=12, shuffle=True), DataLoader(testset)
    else:
        return DataLoader(trainset_2, batch_size=12, shuffle=True), DataLoader(testset)


if __name__ == "__main__":

    # Arguments passé en entrée du fichier quand on l'execute

    parser = argparse.ArgumentParser(description="Script TorchClient.py avec argument de répertoire et nombre d'epochs.")
    parser.add_argument("repertoire", type=str, help="Chemin du répertoire à utiliser.")
    parser.add_argument("--epochs", type=int, default=2, help="Nombre d'epochs pour l'entraînement (par défaut: 2).")
    
    
    parser.add_argument("--ip_address", type=str, help="Adresse IP du serveur.")
    parser.add_argument("--username", type=str, help="Nom d'utilisateur du serveur.")
    parser.add_argument("--password", type=str, help="Mot de passe du serveur.")
    parser.add_argument("--dir", type=str, help="Répertoire du serveur.")
    parser.add_argument("--acc", type=float, help="derniere accuracy")

    args = parser.parse_args()

    

    # Chargement du modèle envoyé par le serveur et adaptation au gpu s'il y en a un
    modele = torch.load(args.repertoire+"/m.pt", map_location=DEVICE)
    modele.to(DEVICE)
    
    # Chargement des données d'entrainement et de test
    trainloader, testloader = Net.load_data(args.repertoire)

    # Entrainement du modèle
    temps_debut_train = time.time()
    modele.train(trainloader, args.epochs, DEVICE)
    temps_fin_train = time.time()

    # Test du modèle
    temps_debut_test = time.time()
    loss, accuracy = modele.test(testloader, DEVICE)
    temps_fin_test = time.time()

    # Calcul des temps d'entrainement et de test
    temps_execution_train = temps_fin_train - temps_debut_train
    temps_execution_test = temps_fin_test - temps_debut_test
    
    # Affichage des performances pour récupération par le serveur
    print(f"Loss: {loss:.5f}, Accuracy: {accuracy:.5f}, Train: {temps_execution_train:.3f} secondes, Test: {temps_execution_test:.3f} secondes")
    
    # Calcul des performances (gain de précision et temps d'entrainement)
    gain_accuracy = (accuracy - args.acc)/float(args.epochs)
    temps = temps_execution_train/args.epochs

    # Sauvegarde des performances
    save_perf(gain_accuracy ,temps)

    # Sauvegarde du modèle entrainé
    torch.save(modele, args.repertoire+"/m.pt")

    # Mise en place du SSH avec paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        
        # Connexion au serveur
        ssh.connect(args.ip_address, username=args.username, password=args.password)
        
        # Création d'un transport SFTP
        sftp = ssh.open_sftp()

        # Lire le fichier ID.txt pour renvoyer le modèle renomé selon l'id attribué au client par le serveur
        with open(args.repertoire+'/ID.txt', 'r') as fichier:
            # Lire le contenu du fichier
            contenu = fichier.read()
            # Convertir le contenu en entier
            entier = int(contenu)


        # Envoyer les fichiers locaux vers le serveur distant
        remote_path = args.dir+"/modeles/m" + str(entier) + ".pt"
        sftp.put(args.repertoire+"/m.pt", remote_path)
        print(f"Le fichier a ete transmis")

        # Fermer la connexion SFTP
        sftp.close()
        

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

    finally:
        # Fermer la connexion SSH
        ssh.close()

    