import os
import time
import threading
import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import random
import pygame
import tkinter.messagebox as messagebox
pygame.init()
pygame.mixer.init()
shot_sound = pygame.mixer.Sound('C:/Users/muha/Desktop/directory warrior/sounds/GE_Silencer.wav')
reload_sound = pygame.mixer.Sound('C:/Users/muha/Desktop/directory warrior/sounds/AK47_Reload.wav')
explosion_sound = pygame.mixer.Sound('C:/Users/muha/Desktop/directory warrior/sounds/mixkit-explosion-hit-1704.wav')
folder_path = ''
ammo = 10
addspeed = 100
score = 0
game_active = True
def play_shot_sound():
    shot_sound.play()
def play_reload_sound():
    reload_sound.play()
def play_e_sound():
    explosion_sound.play()

def delete_folders_after_game_ending(path, folder):
    for folder_name in os.listdir(path):
        if folder_name.startswith(folder):
            full_path = os.path.join(path, folder_name)
            if os.path.isdir(full_path):
                try:
                    os.rmdir(full_path)
                    print(f'{folder_name} removed')
                except OSError:
                    print(f'Error removing {folder_name}')
def enemy_folder(path):
    global game_active
    count = 0
    delay = 3
    start_time = time.time()
    while game_active:
        try:
            os.mkdir(os.path.join(path, f'enemy_{count}'))
            print(f'Enemies coming from {os.path.join(path, f"enemy_{count}")}')
            count += 1
            current_time = time.time()
            time_a = current_time - start_time
            delay_effect = max(0.5, delay - time_a / addspeed)
            time.sleep(delay_effect)
        except FileExistsError:
            continue
def create_explosion_folder(path, interval=25):
    global game_active
    while game_active:
        time.sleep(interval)
        name = 'explosion'
        e_path = os.path.join(path, name)
        if not os.path.exists(e_path):
            os.mkdir(e_path)
            print(f'explosion created at {e_path}')
def delete_random_folders_in_game_directory(path, number=5):
    entries = os.listdir(path)
    folders = [f for f in entries if os.path.isdir(os.path.join(path, f))]
    for folder in random.sample(folders, min(number, len(folders))):
        os.rmdir(os.path.join(path, folder))
        print(f'{folder} was removed')
def create_ammo_folder(path, interval=20):
    global game_active
    while game_active:
        count = 0
        time.sleep(interval)
        foldet_name = f'ammo_{count}'
        folder_path = os.path.join(path, foldet_name)
        os.mkdir(folder_path)
        print(f'Ammo created at {folder_path}')
        threading.Timer(10, lambda: delete_folder_if_exists(folder_path)).start()
        count += 1
def delete_folder_if_exists(folder_path):
    if os.path.exists(folder_path):
        os.rmdir(folder_path)
        print(f'{folder_path} was removed')
def start_enemy_creation(path):
   threading.Thread(target=enemy_folder, args=(path,)).start()
   threading.Thread(target=create_ammo_folder, args=(path,)).start()
   threading.Thread(target=create_explosion_folder, args=(path,)).start()
def delete_enemy():
    global ammo, ammo_holder, folder_path, score
    if ammo > 0:
        entries = os.listdir(folder_path)
        enemies = [f for f in entries if f.startswith('enemy')]
        ammo_folders = [f for f in entries if f.startswith('ammo')]
        explosions = [f for f in entries if f == 'explosion']
        targets = enemies + ammo_folders + explosions
        if targets:
            target = simpledialog.askstring("Target", "choose target:")
            if target in enemies:
                os.rmdir(os.path.join(folder_path, target))
                print(f'Deleted: {target}')
                ammo -= 1
                score += 1
                play_shot_sound()
            elif target in ammo_folders:
                os.rmdir(os.path.join(folder_path, target))
                ammo += 3
                play_reload_sound()
                print(f'reloaded from {target}')
            elif target in explosions:
                os.rmdir(os.path.join(folder_path, target))
                delete_random_folders_in_game_directory(folder_path)
                play_e_sound()
                score += 5
            ammo_holder.config(text=f' bullet remains: {ammo}')
            score_holder.config(text=f'score: {score}')
        else:
            game_over()
def end_game(root):
    global score, username, game_active
    game_active = False
    with open(os.path.join(folder_path, f'{username}_score.txt'), 'w') as file:
        file.write(f'Player: {username}\nscore: {score}')
    delete_folders_after_game_ending(folder_path, 'enemy')
    delete_folders_after_game_ending(folder_path, 'ammo')
    delete_folders_after_game_ending(folder_path, 'explosion')
    game_over()
    root.destroy()

def start_game():
    global username
    username = simpledialog.askstring("Имя")





def game_over():
    ammo_holder.config(text="game over")

def game_directory():
    global folder_path
    folder_path = filedialog.askdirectory()
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    gui()


def exit_game(root):
    answer = messagebox.askquestion( "Выход","Вы точно хотите выйти?")
    if answer == 'да!':
        root.destroy()

# интерфейс


def gui():
    global  ammo_holder, username, score_holder
    root = tk.Tk()
    root.title('directory warrior')
    username = simpledialog.askstring("Name", "Choose your name: ")
    if username is None:
        username = "Anonymous"
    else:
        start_enemy_creation(folder_path)
    ammo_holder = tk.Label(root, text=f'bullet remains {ammo}')
    ammo_holder.pack(pady=20)
    score_holder = tk.Label(root, text=f'score: {score}')
    score_holder.pack(pady=20)
    shoot = tk.Button(root, text="shoot", command=delete_enemy)
    shoot.pack(pady=20)
    root.after(60000, lambda: end_game(root))
    root.mainloop()
game_directory()




if not os.path.exists(folder_path):
    os.makedirs(folder_path)


gui()
