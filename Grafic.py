import tkinter as tk
import pygame
import os
import sys
from random import randint
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move, game_score

BOT_DELAY = 700
ATTACK_DELAY, ATTACK_DELAY_SHAG = 200, 20
BURST_DELAY, BURST_DELAY_AFTER= 50, 1000
ATTACK_DELAY_BOT, ATTACK_DELAY_SHAG_BOT = 100, 500
ITOG_START_DELAY = 1000
DELAY_HIDE = 3000
hm = None
Play_score = 0
Bote_score = 0
Tota_score = 0

def get_resource_path(relavite_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.argv[0])
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relavite_path)

def on_click(event):
    player_move = event.widget.name
    if event.widget.after_clickable == True:
        pass
    else:
        if player_move == "new_game":
            player_health.config(width=200)
            bot_health.config(width=200)
            new_game_widget.place_forget()
            scissors_widget.after_clickable = False
            stone_widget.after_clickable = False
            paper_widget.after_clickable = False
            slova("Player win!", x=575, y=225, width=150, height=100, de=False)
        else:
            item = label_hide(root, objects, player_move)
            bot_move = bot_chose_animation(bot_label=bot_label)
            play_sound('intriga', 'ch3')
            burst_animation()
            winner = move_result(player_move, bot_move)
            attack(item)
            attack_up(bot_label, target_y=200, win=True, delay_True=250)
            after_win(bot_label, item, winner)

def play_sound(sound_name, sound_channel):
    sound = soundse[sound_name]
    channels[sound_channel].play(pygame.mixer.Sound(sound))

root = tk.Tk()
root.geometry("800x600")
root.title("Камень/Ножницы/Бумага")

pygame.mixer.init()
pygame.mixer.set_num_channels(8)

soundse = {"boom": get_resource_path('sounds/sound-effects-library-explosion-short-explosion-with-glass-debris-crash-explosions-bombs.mp3'),
          "bot_win": get_resource_path('sounds/66dc9666f919d55.mp3'),
          "player_win": get_resource_path('sounds/win31.mp3'),
          "intriga": get_resource_path('sounds/intriga.mp3')}

channels = {"ch1": pygame.mixer.Channel(0),
          "ch2": pygame.mixer.Channel(1),
            "ch3": pygame.mixer.Channel(2)}
def create_img(img_path):
    img = PILImage.open(img_path)
    if img_path == r"imageee/1burst.webp":
        scaled = img.resize((600, 300), PILImage.Resampling.LANCZOS)
        scaled = scaled.crop((0, 50, 600, 300))
    else:
        scaled = img.resize((200, 200), PILImage.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(scaled)
    return photo
def create_widget(root, img_path, x, y, name, clickable=True, default_img_path=None, invision=False, after_clickable=False):
    photo_obj = create_img(img_path)
    label = tk.Label(root, image=photo_obj)
    if default_img_path is not None:
        default_img_obj = create_img(default_img_path)
        label.default_image = default_img_obj
    label.image = photo_obj
    label.name = name
    label.after_clickable = after_clickable
    label.x = x
    label.y = y
    label.place(x=x, y=y)
    if invision:
        label.place_forget()
    if clickable:
        label.configure(cursor="hand2")
        label.bind("<Button-1>", on_click)
    return label

def bot_chose_animation(bot_label):
    image_paths = (r"imageee/1scissors.webp", r"imageee/1scala.png", r"imageee/1magabum.png")
    images = []
    for path in image_paths:
        img = PILImage.open(path).resize((200, 200), PILImage.Resampling.LANCZOS)
        images.append(ImageTk.PhotoImage(img))
    bot_move_number = randint(9, 11)
    hodi = ['scissors', 'stone', 'paper']
    bot_chose = hodi[bot_move_number % 3]
    current_step = 0

    def step():
        nonlocal current_step
        idx = current_step % 3
        image = images[idx]
        bot_label.configure(image=image)
        bot_label.image = image
        current_step += 1
        if current_step <= bot_move_number:
            step_delay = BOT_DELAY // bot_move_number
            bot_label.after(step_delay, step)
    step()
    return bot_chose

def label_hide(root, list_obj_labels, name_label_to_show):
    hodi = ['scissors', 'stone', 'paper']
    b = 0
    for i in range(3):
        if list_obj_labels[i].name == "?":
            continue
        if name_label_to_show != hodi[i]:
            list_obj_labels[i].place_forget()
        else:
            b = i
    root.after(DELAY_HIDE, label_none_hide, list_obj_labels)
    return list_obj_labels[b]
def label_none_hide(list_obj_labels):
    for item in list_obj_labels:
        if item.name == "?":
            item.configure(image=item.default_image)
            item.image = item.default_image
        if item.name == "burst":
            item.place_forget()
        else:
            item.place(x=item.x, y=item.y)

def attack(item):
    current_x = item.winfo_x()
    current_y = item.winfo_y()
    step_y = (current_y - 200) / 21
    step_x = (current_x - 300) / 21
    def step():
        nonlocal current_x, current_y
        if item.name == 'paper':
            current_x -= step_x
            current_y -= step_y
            item.place(x=current_x, y=current_y)
            if current_x > 300 and current_y > 200:
                item.after(ATTACK_DELAY_SHAG, step)
        elif item.name == 'stone':
            current_y -= step_y
            item.place(x=current_x, y=current_y)
            if current_y > 200:
                item.after(ATTACK_DELAY_SHAG, step)
        elif item.name == 'scissors':
            current_x -= step_x
            current_y -= step_y
            item.place(x=current_x, y=current_y)
            if current_x < 300 and current_y < 400:
                item.after(ATTACK_DELAY_SHAG, step)
    item.after(ATTACK_DELAY, step)

def burst_animation():
    def burst_delay():
        root.after(BURST_DELAY, burst_widget.place_forget())
        burst_widget.place(x=100, y=150)
        play_sound('boom', 'ch1')
    root.after(BURST_DELAY_AFTER, burst_delay)

def after_win(bot_label, player_move, win):
    global Tota_score, Play_score, Bote_score
    def attack_delay():
        if win == 'net':
            pass
        elif win == 'bot':
            attack_up(bot_label)
        else:
            attack_from_niz(player_move)
    root.after(1000, health, win)
    root.after(ATTACK_DELAY_BOT, attack_delay)
    if player_health.winfo_width() <= 50 and win == 'bot':
        slova("Bot win!", x=575, y=225, fg="Red", width=150, height=100, win=win)
        scissors_widget.after_clickable = True
        stone_widget.after_clickable = True
        paper_widget.after_clickable = True
    elif bot_health.winfo_width() <= 50 and win == 'player':
        scissors_widget.after_clickable = True
        stone_widget.after_clickable = True
        paper_widget.after_clickable = True
        slova("Player win!", x=575, y=225, width=150, height=100, win=win)

def attack_up(item, target_y = 400, win=False, delay_True=0):
    current_y = item.winfo_y()
    current_x = item.winfo_x()
    step_delay = ATTACK_DELAY_SHAG_BOT // 7
    if win == False:
        step_y = (target_y - current_y) / 24
    else:
        step_y = (target_y - current_y) / 11
    def step():
        nonlocal current_y, current_x, step_y
        current_y += step_y
        bot_label.place(x=current_x, y=current_y)
        if current_y < target_y:
            bot_label.after(step_delay, step)
    root.after(delay_True, step)

def attack_from_niz(item, target_y = 0):
    current_y = 200
    step_y = (current_y - target_y) / 24
    current_x = 300
    step_delay = ATTACK_DELAY_SHAG_BOT // 7
    def step():
        nonlocal current_y, current_x
        current_y -= step_y
        item.place(x=current_x, y=current_y)
        if current_y > target_y:
            item.after(step_delay, step)
    root.after(ATTACK_DELAY_BOT + 290, step)

def create_healthbar(root, x, y, width, height, out_color='red', inner_color='green'):
    outer = tk.Frame(root, bg=out_color, width=width, height=height)
    outer.place(x=x, y=y)
    outer.update_idletasks()
    inner = tk.Frame(root, bg=inner_color, width=width, height=height)
    inner.place(x=x, y=y)
    inner.update_idletasks()
    return inner

def health(win):
    if win == "player":
        new_width = bot_health.winfo_width() - 50
        bot_health.config(width=new_width)
    elif win == "bot":
        new_width = player_health.winfo_width() - 50
        player_health.config(width=new_width)
    else:
        pass

def slova(text, fg="Blue", x=0, y=0, width=0, height=0, de=True, win=None):
    texttt = tk.Label(root, text=text, font=("Arial", 16, "bold"), fg=fg)
    global hm
    skip = 0
    if de == False:
        skip = 1000
    def wrapper(de=de):
        global hm, Tota_score, Bote_score, Play_score
        if de == True:
            hm = texttt
            Tota_score += 1
            scor_t = tk.Label(root, text=f"Total score: {Tota_score}", font=("Arial", 16, "bold"), fg="Black")
            texttt.place(x=x, y=y, width=width, height=height)
            scor_t.place(x=0, y=100, width=150, height=100)
            if win == "player":
                play_sound('player_win', 'ch2')
                Play_score += 1
                scor_p = tk.Label(root, text=f"Player score: {Play_score}", font=("Arial", 16, "bold"), fg="Blue")
                scor_p.place(x=0, y=200, width=150, height=100)
            else:
                play_sound('bot_win', 'ch2')
                Bote_score += 1
                scor_b = tk.Label(root, text=f"Bot score: {Bote_score}", font=("Arial", 16, "bold"), fg="Red")
                scor_b.place(x=0, y=300, width=150, height=100)
        else:
            hm.destroy()
    def refresh():
        label = new_game_widget
        label.place(x=550, y=25)
    root.after(ITOG_START_DELAY - skip, wrapper)
    if de == True:
        root.after(ITOG_START_DELAY + 1900, refresh)
name_health_bot = tk.Label(root, text="Bot health", font=("Arial", 16, "bold"), fg="Black")
name_health_bot.place(x=0, y=25, width=150, height=50)
name_health_player = tk.Label(root, text="Your health", font=("Arial", 16, "bold"), fg="Black")
name_health_player.place(x=470, y=575, width=150, height=25)
scissors_widget = create_widget(root, r"imageee/1scissors.webp", 50, 370, "scissors", after_clickable=False)
stone_widget = create_widget(root, r"imageee/1scala.png", 300, 370, "stone", after_clickable=False)
paper_widget = create_widget(root, r"imageee/1magabum.png", 550, 350, "paper",  after_clickable=False)
bot_label = create_widget(root, r"imageee/1quest.webp", 300, 0, "?", False, default_img_path=r"imageee/1quest.webp")
burst_widget = create_widget(root, r"imageee/1burst.webp", 0, 0, "burst", False, invision=True)
new_game_widget = create_widget(root, r"imageee/refresh.png", 500, 225, "new_game", True, invision=True)
bot_health = create_healthbar(root, 0, 0, 200, 40, out_color='red', inner_color='green')
player_health = create_healthbar(root, 600, 560, 200, 40, out_color='red', inner_color='green')
objects = [scissors_widget, stone_widget, paper_widget, bot_label, burst_widget]

root.mainloop()