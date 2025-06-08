# Vestigium - Versión 2D

Esta es la versión 2D del videojuego Vestigium, creada con **Pygame**. Es una experiencia de plataformas narrativa y atmosférica centrada en el sigilo y la evasión de la luz.

## ⚙️ Requisitos

- Python 3.10+
- Pygame (`pip install pygame`)
- Archivos `.tmx` para los niveles

## 🎮 Jugabilidad

Controlas a una sombra que debe:

- Evitar cualquier fuente de luz
- Rebotar sobre setas y escalar paredes
- Nadar bajo el agua
- Resolver minijuegos y recoger objetos

### Controles

| Acción          | Tecla        |
|----------------|--------------|
| Mover          | Flechas ← →  |
| Saltar         | Espacio      |
| Nadar / Minijuego | Flechas ← ↑ ↓ → |
| Pausar         | ESC          |

## 🧩 Niveles

1. **Cementerio** – Evade faroles y al enterrador.
2. **Minijuego** – Inserta la llave mientras esquivas luciérnagas.
3. **Árbol del bosque** – Plataformas con setas que iluminan al saltar.
4. **Lago subacuático** – Niveles acuáticos con medusas y peces linterna.

## 💡 Mecánica principal

> La luz es letal. Cualquier contacto implica la muerte instantánea y el regreso al último punto de control.

## 📸 Capturas

*Próximamente...*

## 🐞 Reporte de bugs

- [ ] Transiciones de fade a veces se solapan
- [ ] Colisión con ciertas luces no se detecta correctamente
- [ ] Optimización de carga de mapas

## 🛠️ Mejores prácticas

- Modularidad por escena
- Sistema de gestión de recursos centralizado
- Motor de transiciones y sonidos desacoplado
