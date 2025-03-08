import pygame
from director import Director
from scenes.startMenu import StartMenu
import tkinter as tk
from tkinter import messagebox

if __name__ == "__main__":

    messagebox.showwarning(
        "Que guay!", "Acabas de instalar el nuevo Troyano 2.1, disfrutalo! :D"
    )
    messagebox.showinfo(
        "Que poca seguridad!", "No deberias haber instalado el Troyano 2.1"
    )
    messagebox.showinfo(
        "",
        "Es coña, pero vigila que pulleas, que no es plan de que te metan un troyano de verdad\n"
        "Besos, Fer",
    )

    pygame.init()
    director = Director()
    first_scene = StartMenu(director)
    director.stack_scene(first_scene)
    director.run()
    pygame.quit()
