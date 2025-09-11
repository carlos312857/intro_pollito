import tkinter as tk
import random

# -----------------------
# Configuración
# -----------------------
WIDTH, HEIGHT = 800, 600
PLAYER_STEP = 20
LIVES = 3
car_speed = 5   # velocidad inicial de los carros
GAME_SPEED = 40

# -----------------------
# Variables globales
# -----------------------
carros = []
vidas = LIVES
puntos = 0

# -----------------------
# Funciones
# -----------------------
def mover_jugador(dx, dy):
    global puntos
    canvas.move(pollito, dx, dy)
    x1, y1, x2, y2 = canvas.coords(pollito)
    # Si llega arriba -> punto y vuelve al inicio
    if y1 < 0:
        puntos += 1
        canvas.itemconfig(txt_puntos, text=f"Puntos: {puntos}")
        canvas.coords(pollito, WIDTH//2-15, HEIGHT-40, WIDTH//2+15, HEIGHT-10)

def crear_carro():
    y = random.choice([160, 210, 260, 310])  # carriles
    if random.choice([True, False]):
        x, dx = -60, car_speed   # izquierda → derecha
    else:
        x, dx = WIDTH+60, -car_speed  # derecha → izquierda
    carro = canvas.create_rectangle(x, y, x+60, y+30, fill=random.choice(["red","blue","green","purple"]))
    carros.append((carro, dx))

def mover_carros():
    global vidas, car_speed
    for carro, dx in list(carros):
        canvas.move(carro, dx, 0)
        x1, y1, x2, y2 = canvas.coords(carro)
        if x2 < 0 or x1 > WIDTH:  # fuera de pantalla
            canvas.delete(carro)
            carros.remove((carro, dx))
        # colisión
        if colision(carro, pollito):
            vidas -= 1
            car_speed += 1   # 🚀 aumenta la velocidad de los carros
            canvas.itemconfig(txt_vidas, text=f"Vidas: {vidas}")
            canvas.coords(pollito, WIDTH//2-15, HEIGHT-40, WIDTH//2+15, HEIGHT-10)
            if vidas <= 0:
                game_over()

def colision(obj1, obj2):
    x1, y1, x2, y2 = canvas.coords(obj1)
    a1, b1, a2, b2 = canvas.coords(obj2)
    return not (x2 < a1 or a2 < x1 or y2 < b1 or b2 < y1)

def game_over():
    canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER", fill="white", font=("Arial", 30))

def loop():
    mover_carros()
    if random.random() < 0.03:  # probabilidad de que aparezca un carro
        crear_carro()
    if vidas > 0:
        root.after(GAME_SPEED, loop)

# -----------------------
# Ventana y escenario
# -----------------------
root = tk.Tk()
root.title("Pollito cruzando la avenida")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="gray20")
canvas.pack()

# Césped
canvas.create_rectangle(0,0,WIDTH,150, fill="green", outline="")
canvas.create_rectangle(0,450,WIDTH,HEIGHT, fill="green", outline="")
canvas.create_text(WIDTH//2, 50, text="META", font=("Arial", 20,"bold"))

# Jugador
pollito = canvas.create_oval(WIDTH//2-15, HEIGHT-40, WIDTH//2+15, HEIGHT-10, fill="yellow")

# Texto
txt_vidas = canvas.create_text(10,10, anchor="nw", text=f"Vidas: {vidas}", font=("Arial",14))
txt_puntos = canvas.create_text(WIDTH-10,10, anchor="ne", text=f"Puntos: {puntos}", font=("Arial",14))

# Controles
root.bind("<Left>", lambda e: mover_jugador(-PLAYER_STEP, 0))
root.bind("<Right>", lambda e: mover_jugador(PLAYER_STEP, 0))
root.bind("<Up>", lambda e: mover_jugador(0, -PLAYER_STEP))
root.bind("<Down>", lambda e: mover_jugador(0, PLAYER_STEP))

# Iniciar juego
loop()
root.mainloop()
