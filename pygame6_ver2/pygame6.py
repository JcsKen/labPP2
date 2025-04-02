import pygame
import tkinter as tk
from tkinter import colorchooser

def pick_color():
    root = tk.Tk()
    root.withdraw()
    color_code = colorchooser.askcolor(title="Choose color")[0]
    return (int(color_code[0]), int(color_code[1]), int(color_code[2])) if color_code else None

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    radius = 15
    mode = 'blue'
    draw_mode = 'line'
    points = []
    shapes = []  # Store drawn shapes
    custom_color = (0, 0, 255)
    
    # Load tool images
    eraser_icon = pygame.image.load("eraser.png")
    rectangle_icon = pygame.image.load("rectangle.png")
    circle_icon = pygame.image.load("circle.png")
    square_icon = pygame.image.load("square.png")
    triangle_icon = pygame.image.load("triangle.png")
    rhombus_icon = pygame.image.load("rhombus.png")
    
    eraser_icon = pygame.transform.scale(eraser_icon, (50, 50))
    rectangle_icon = pygame.transform.scale(rectangle_icon, (50, 50))
    circle_icon = pygame.transform.scale(circle_icon, (50, 50))
    square_icon = pygame.transform.scale(square_icon, (50, 50))
    triangle_icon = pygame.transform.scale(triangle_icon, (50, 50))
    rhombus_icon = pygame.transform.scale(rhombus_icon, (50, 50))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Check if tool icons are clicked
                if 10 <= mouse_x <= 60:
                    if 10 <= mouse_y <= 60:
                        draw_mode = 'eraser'
                    elif 70 <= mouse_y <= 120:
                        draw_mode = 'rect'
                    elif 130 <= mouse_y <= 180:
                        draw_mode = 'circle'
                    elif 190 <= mouse_y <= 240:
                        draw_mode = 'square'
                    elif 250 <= mouse_y <= 300:
                        draw_mode = 'triangle'
                    elif 310 <= mouse_y <= 360:
                        draw_mode = 'rhombus'
                else:
                    start_pos = event.pos
                    
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.pos
                if draw_mode == 'rect':
                    shapes.append(('rect', start_pos, mouse_pos, custom_color if mode == 'custom' else (255, 255, 255)))
                elif draw_mode == 'circle':
                    radius = int(((mouse_pos[0] - start_pos[0]) ** 2 + (mouse_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    shapes.append(('circle', start_pos, radius, custom_color if mode == 'custom' else (255, 255, 255)))
                elif draw_mode == 'square':
                    side = abs(mouse_pos[0] - start_pos[0])
                    shapes.append(('square', start_pos, side, custom_color if mode == 'custom' else (255, 255, 255)))
                elif draw_mode == 'triangle':
                    x, y = start_pos
                    shapes.append(('triangle', [(x, y), (x - 40, y + 60), (x + 40, y + 60)], custom_color if mode == 'custom' else (255, 255, 255)))
                elif draw_mode == 'rhombus':
                    x, y = start_pos
                    shapes.append(('rhombus', [(x, y), (x + 40, y + 30), (x, y + 60), (x - 40, y + 30)], custom_color if mode == 'custom' else (255, 255, 255)))
                elif draw_mode == 'eraser':
                    shapes.append(('eraser', mouse_pos, radius, (0, 0, 0)))  # Draw black circles as an eraser
        
        screen.fill((0, 0, 0))
        
        for shape in shapes:
            if shape[0] == 'rect':
                pygame.draw.rect(screen, shape[3], (*shape[1], shape[2][0] - shape[1][0], shape[2][1] - shape[1][1]), 2)
            elif shape[0] == 'circle':
                pygame.draw.circle(screen, shape[3], shape[1], shape[2], 2)
            elif shape[0] == 'square':
                pygame.draw.rect(screen, shape[3], (*shape[1], shape[2], shape[2]), 2)
            elif shape[0] == 'triangle':
                pygame.draw.polygon(screen, shape[2], shape[1], 2)
            elif shape[0] == 'rhombus':
                pygame.draw.polygon(screen, shape[2], shape[1], 2)
            elif shape[0] == 'eraser':
                pygame.draw.circle(screen, (0, 0, 0), shape[1], shape[2])  # Erase by drawing black circles
        
        # Draw tool icons
        screen.blit(eraser_icon, (10, 10))
        screen.blit(rectangle_icon, (10, 70))
        screen.blit(circle_icon, (10, 130))
        screen.blit(square_icon, (10, 190))
        screen.blit(triangle_icon, (10, 250))
        screen.blit(rhombus_icon, (10, 310))
        
        pygame.display.flip()
        clock.tick(60)

main()
