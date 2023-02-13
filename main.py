import pgzrun, random

WIDTH = 800
HEIGHT = 600

TITLE = "Torches and Shields"

FPS = 30

wall = Actor("wall")
torch = Actor("torch")
shield = Actor("shield")

button_pvp = Actor("btn", center = (400, 250))
button_pvb = Actor("btn", center = (400, 400))

game_buttons =[]
for i in range(3):
    for j in range(3):
        game_button = Actor("game_number", center = ((j * 100) + 300, (i * 100) + 250))
        game_button.used = 0
        game_buttons.append(game_button)

player_turn = 0
mode = "menu"
win = None

shields = []
torches = []

def go_to_menu():
    global mode
    mode = "menu"

def check_win():
    global mode, win
    soln = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for combine in soln:
        if game_buttons[combine[0]].used != 0 and game_buttons[combine[0]].used == game_buttons[combine[1]].used == game_buttons[combine[2]].used:
            mode = "win"
            win = game_buttons[combine[0]].used
            clock.schedule(go_to_menu, 3)
            shields.clear()
            torches.clear()

def create_bg():
    for i in range(0, 9):
        for j in range(0, 7):
            wall.x = i * 100
            wall.y = j * 100
            wall.draw()

    torch.center = (100, 100)
    torch.draw()

    shield.center = (720, 100)
    shield.draw()

def create_game_table():
    screen.draw.line((350, 200), (350, 500), "#FFFFFF")
    screen.draw.line((351, 200), (351, 500), "#FFFFFF")
    screen.draw.line((349, 200), (349, 500), "#FFFFFF")

    screen.draw.line((450, 200), (450, 500), "#FFFFFF")
    screen.draw.line((451, 200), (451, 500), "#FFFFFF")
    screen.draw.line((449, 200), (449, 500), "#FFFFFF")

    screen.draw.line((250, 300), (550, 300), "#FFFFFF")
    screen.draw.line((250, 301), (550, 301), "#FFFFFF")
    screen.draw.line((250, 299), (550, 299), "#FFFFFF")

    screen.draw.line((250, 400), (550, 400), "#FFFFFF")
    screen.draw.line((250, 401), (550, 401), "#FFFFFF")
    screen.draw.line((250, 399), (550, 399), "#FFFFFF")

def draw():
    create_bg()

    screen.draw.text("Torches and Shields", color = "#FFFFFF", center = (400, 100), fontsize = 64, fontname = "orpheus")

    if mode == 'menu':
        button_pvb.draw()
        button_pvp.draw()
        screen.draw.text("PVP", color = "#FFFFFF", center = (400, 250), fontsize = 64, fontname = "orpheus")
        screen.draw.text("PVBot", color = "#FFFFFF", center = (400, 400), fontsize = 64, fontname = "orpheus")
    
    if mode == "pvp":
        for cell in game_buttons:
            cell.draw()
        for shield in shields:
            shield.draw()
        for torch in torches:
            torch.draw()
        
        create_game_table()
    
    if mode == "win":
        screen.draw.text(f"Player {win} win!", color = "#FFFFFF", center = (400, 250), fontsize = 72, fontname = "orpheus")
    
    if mode == "pvbot":
        for cell in game_buttons:
            cell.draw()
        for shield in shields:
            shield.draw()
        for torch in torches:
            torch.draw()
        
        create_game_table()
        

def on_mouse_down(button, pos):
    global mode, player_turn
    if mode == "menu":
        if button_pvp.collidepoint(pos) and button == mouse.LEFT:
            mode = "pvp"
            player_turn = 1
            for btn in game_buttons:
                btn.used = 0

        if button_pvb.collidepoint(pos) and button == mouse.LEFT:
            mode = "pvbot"
            player_turn = 1
            for btn in game_buttons:
                btn.used = 0

    elif mode == "pvp":
        for btn in game_buttons:
            if btn.collidepoint(pos) and not btn.used and player_turn == 1:
                shields.append(Actor("shield", btn.center))
                btn.used = 1
                check_win()
                player_turn = 2
                
            elif btn.collidepoint(pos) and not btn.used and player_turn == 2:
                shields.append(Actor("torch", btn.center))
                btn.used = 2
                check_win()
                player_turn = 1
    
    elif mode == "pvbot":
        for btn in game_buttons:
            if btn.collidepoint(pos) and not btn.used and player_turn == 1:
                shields.append(Actor("shield", btn.center))
                btn.used = 1
                check_win()
                player_turn = "bot"

def update(dt):
    global player_turn
    if player_turn == "bot":
        while True:
            cell = random.randint(0, 8)

            if not game_buttons[cell].used:
                shields.append(Actor("torch", game_buttons[cell].center))
                game_buttons[cell].used = "bot"
                check_win()
                player_turn = 1
                break
        
pgzrun.go()