import tkinter as tk
from random import randint
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move

def on_click(event):
    player_move = event.widget.name
    item = label_hide(root, objects, player_move)
    attack(item)
    bot_move = bot_chose_animation(bot_label=bot_label)
    attack(bot_label)
    move_result(player_move, bot_move)

root = tk.Tk()
root.geometry("800x600")
root.title("Камень/Ножницы/Бумага")


def create_img(img_path):
    img = PILImage.open(img_path)
    scaled = img.resize((200, 200), PILImage.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(scaled)
    return photo
def create_widget(root, img_path, x, y, name, clickable=True, default_img_path=None):
    photo_obj = create_img(img_path)

    label = tk.Label(root, image=photo_obj)
    if default_img_path is not None:
        default_img_obj = create_img(default_img_path)
        label.default_image = default_img_obj
    label.image = photo_obj
    label.name = name
    label.x = x
    label.y = y
    label.place(x=x, y=y)
    if clickable:
        label.configure(cursor="hand2")
        label.bind("<Button-1>", on_click)
    return label

def bot_chose_animation(bot_label, total_delay=700):
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
            step_delay = total_delay // bot_move_number
            bot_label.after(step_delay, step)

    step()
    return bot_chose

def label_hide(root, list_obj_labels, name_label_to_show, delay=2000):
    hodi = ['scissors', 'stone', 'paper']
    b = 0
    for i in range(3):
        if list_obj_labels[i].name == "?":
            continue
        if name_label_to_show != hodi[i]:
            list_obj_labels[i].place_forget()
        else:
            b = i
    root.after(delay, label_none_hide, list_obj_labels, root)
    return list_obj_labels[b]
def label_none_hide(list_obj_labels, root):
    for item in list_obj_labels:
        if item.name == "?":
            item.configure(image=item.default_image)
            item.image = item.default_image
        item.place(x=item.x, y=item.y)

def attack(item):
    current_x = item.winfo_x()
    current_y = item.winfo_y()
    def step():
        nonlocal current_x, current_y
        step_y = (current_y - 200) / 7
        step_x = (current_x - 300) / 7
        if str(item) == '.!label3':
            current_x -= step_x
            current_y -= step_y
            item.place(x=current_x, y=current_y)
            if current_x > 300 and current_y > 200:
                item.after(100, step)
        elif str(item) == '.!label2':
            current_y -= step_y
            item.place(x=current_x, y=current_y)
            if current_y > 200:
                item.after(10, step)
        elif str(item) == '.!label':
            current_x -= step_x
            current_y -= step_y
            item.place(x=current_x, y=current_y)
            if current_x < 300 and current_y < 400:
                item.after(100, step)
    item.after(100, step())
scissors_widget = create_widget(root, r"imageee/1scissors.webp", 50, 370, "scissors")
stone_widget = create_widget(root, r"imageee/1scala.png", 300, 370, "stone")
paper_widget = create_widget(root, r"imageee/1magabum.png", 550, 370, "paper")
bot_label = create_widget(root, r"imageee/1quest.webp", 300, 0, "?", False, default_img_path=r"imageee/1quest.webp")
objects = [scissors_widget, stone_widget, paper_widget, bot_label]

root.mainloop()