# 🦖 Dino Game - Q-Learning Agent 🎮🧠

Projet d'application de l'apprentissage par renforcement (Q-learning) dans un environnement 2D simulé avec **Pygame**. Ce projet a été développé dans le cadre d'un projet pédagogique orienté **Systèmes Multi-Agents (SMA)**.

---

## 🚀 Aperçu du Projet

L’objectif de ce projet est de démontrer le fonctionnement d’un agent autonome dans un environnement dynamique avec obstacles, où l’agent apprend à atteindre une cible en évitant des dangers à travers un apprentissage itératif basé sur **Q-Learning**.

📌 Le jeu propose **3 niveaux de difficulté** (facile, moyen, difficile) et affiche :
- Le score
- L'épisode actuel
- L'epsilon
- Les logs d’apprentissage

---

## 🖥️ Interface Utilisateur (Pygame)

- Menu principal interactif avec choix de la difficulté.
- Grille de jeu dynamique : chaque niveau présente un environnement différent en termes d'obstacles.
- Agent (représenté par un carré vert) navigue vers une cible (bleue) en évitant les obstacles (rouges).

---

## 📁 Structure du Projet


---

## ⚙️ Installation

### 1. Clonage du dépôt

```bash
git clone https://github.com/motawakil/Dino_game.git
cd Dino_game

Création d’un environnement virtuel (optionnel mais recommandé)
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/macOS

pip install -r requirements.txt

Lancer le Jeu

python main.py



