import tkinter as tk
from random import randint
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move

def on_click(event):
    player_move = event.widget.name
    move_result(player_move, bot_turn(possible_move))

root = tk.Tk()
root.geometry("800x600")
root.title("Камень/Ножницы/Бумага")

def create_widget(root, img_path, x, y, name, clickable=True):

    img = PILImage.open(img_path)
    scaled = img.resize((200, 200), PILImage.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(scaled)

    label = tk.Label(root, image=photo)
    label.image = photo
    label.name = name
    label.place(x=x, y=y)
    if clickable:
        label.configure(cursor="hand2")
        label.bind("<Button-1>", on_click)
    return label

def bot_chose_animation(bot_label, total_delay=700):
    image_paths = (r"imageee/1scissors.webp", r"imageee/1scala.png", r"imageee/1quest.webp")
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
            step_delay = total_delay // bot_move_number
            bot_label.after(step_delay, step)

    step()
    return bot_chose

create_widget(root, r"imageee/1scissors.webp", 50, 50, "scissors")
create_widget(root, r"imageee/1scala.png", 300, 350, "stone")
create_widget(root, r"imageee/1magabum.png", 550, 50, "paper")
bot_label = create_widget(root, r"imageee/1quest.webp", 300, 170, "?", False)
bot_move = bot_chose_animation(bot_label=bot_label)
print(bot_move)

root.mainloop()