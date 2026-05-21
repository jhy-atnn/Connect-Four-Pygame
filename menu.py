import sys
import pygame
import time
import random
from tkinter import *
from button import Button
from settings import Settings
from ConFour import ConnectFour

settings = Settings()

pygame.init()
pygame.mixer.music.load(settings.BG_MUSIC)
pygame.mixer.music.play(-1)
click_sound = pygame.mixer.Sound(settings.CLICK_SOUND)

SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = SCREEN.get_size()
pygame.display.set_caption("Menu")

BG = pygame.image.load(settings.BG_IMAGE)
BG = pygame.transform.scale(BG, (screen_width, screen_height))

def get_font(size):
    return pygame.font.Font(settings.MENU_FONT_PATH, size)

def transition_screen():
    input_boxes = [
        {"rect": pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 100, 400, 60), "color": pygame.Color(settings.RED),
         "text": "", "label": "Player 1 Name"},
        {"rect": pygame.Rect(screen_width // 2 - 200, screen_height // 2 + 80, 400, 60), "color": pygame.Color(settings.YELLOW),
            "text": "", "label": "Player 2 Name",}
    ]
    active_box = None
    font = get_font(settings.FONT_SIZE_INPUT)
    done = False

    while not done:
        SCREEN.blit(BG, (0, 0))
        prompt = get_font(settings.FONT_SIZE_SMALL).render("Enter Player Names", True, "White")
        SCREEN.blit(prompt, prompt.get_rect(center=(screen_width // 2, screen_height // 2 - 280)))
        mouse_pos = pygame.mouse.get_pos()

        # Draw input boxes and labels
        for i, box in enumerate(input_boxes):
            pygame.draw.rect(SCREEN, box["color"], box["rect"], 2)
            label_surface = font.render(box["label"], True, "white")
            label_rect = label_surface.get_rect(center=(box["rect"].centerx, box["rect"].y - 25))
            SCREEN.blit(label_surface, label_rect)
            text_surface = font.render(box["text"], True, "white")
            SCREEN.blit(text_surface, (box["rect"].x + 10, box["rect"].y + 10))
            if active_box == i:
                if int(time.time() * 2) % 2 == 0:
                    cursor_x = box["rect"].x + 10 + text_surface.get_width() + 2
                    cursor_y = box["rect"].y + 12
                    cursor_height = font.get_height() - 10
                    pygame.draw.line(SCREEN, "white", (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        # CONTINUE button (only if both names ay meron)
        if all(box["text"].strip() for box in input_boxes):
            CONTINUE_BUTTON = Button(
                image=None,
                pos=(screen_width // 2, screen_height // 2 + 200),
                text_input="CONTINUE",
                font=get_font(settings.FONT_SIZE_SMALL),
                base_color=settings.BUTTON_TEXT_COLOR,
                hovering_color=settings.BUTTON_HOVER_COLOR
            )
            CONTINUE_BUTTON.changeColor(mouse_pos)
            CONTINUE_BUTTON.update(SCREEN)
        else:
            CONTINUE_BUTTON = None

        # BACK button (dapat nag hhover)
        BACK_BUTTON = Button(
            image=None,
            pos=(screen_width // 2, screen_height // 2 + 300),
            text_input="BACK",
            font=get_font(settings.FONT_SIZE_INPUT),
            base_color=settings.BUTTON_TEXT_COLOR,
            hovering_color=settings.BUTTON_HOVER_COLOR
        )
        BACK_BUTTON.changeColor(mouse_pos)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box["rect"].collidepoint(event.pos):
                        active_box = i
                if CONTINUE_BUTTON and CONTINUE_BUTTON.checkForInput(mouse_pos):
                    click_sound.play() 
                    return "continue", input_boxes[0]["text"], input_boxes[1]["text"]
                if BACK_BUTTON.checkForInput(mouse_pos):
                    click_sound.play()
                    return "back", "", ""
            if event.type == pygame.KEYDOWN and active_box is not None:
                if event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                    click_sound.play()
                elif len(input_boxes[active_box]["text"]) < 15 and event.unicode.isprintable():
                    input_boxes[active_box]["text"] += event.unicode
                    click_sound.play()

        pygame.display.update()

def coin_toss_popup(player1_name, player2_name):
    font = get_font(settings.FONT_SIZE_SMALL)
    small_font = get_font(settings.FONT_SIZE_INPUT)
    toss_screen = True
    winner = None
    toss_result = ""
    while toss_screen:
        SCREEN.blit(BG, (0, 0))
        title = font.render("WHO GOES FIRST? ", True, "white")
        SCREEN.blit(title, title.get_rect(center=(screen_width // 2, screen_height // 2 - 80)))
        toss_button = Button(
            image=None,
            pos=(screen_width // 2, screen_height // 2),
            text_input="CLICK HERE",
            font=small_font,
            base_color=settings.BUTTON_TEXT_COLOR,
            hovering_color=settings.BUTTON_HOVER_COLOR
        )
        mouse_pos = pygame.mouse.get_pos()
        toss_button.changeColor(mouse_pos)
        toss_button.update(SCREEN)
        if toss_result:
            result_label = small_font.render(toss_result, True, "Green")
            SCREEN.blit(result_label, result_label.get_rect(center=(screen_width // 2, screen_height // 2 + 80)))
            continue_label = small_font.render("Click anywhere to continue...", True, "white")
            SCREEN.blit(continue_label, continue_label.get_rect(center=(screen_width // 2, screen_height // 2 + 130)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not toss_result and event.type == pygame.MOUSEBUTTONDOWN:
                if toss_button.checkForInput(pygame.mouse.get_pos()):
                    click_sound.play() 
                    winner = random.choice([1, 2])
                    pname = player1_name if winner == 1 else player2_name
                    toss_result = f"{pname} goes first!"
            elif toss_result and event.type == pygame.MOUSEBUTTONDOWN:
                toss_screen = False
        pygame.display.update()
    return winner

def main_menu():
    confour_img = pygame.image.load(settings.CONFOUR_IMAGE)
    confour_rect = confour_img.get_rect(center=(screen_width // 2, screen_height // 2 + 80))

    while True:
        SCREEN.blit(BG, (0, 0))
        SCREEN.blit(confour_img, confour_rect)
        mouse_pos = pygame.mouse.get_pos()

        MENU_TEXT = get_font(settings.FONT_SIZE_LARGE).render("CONNECT", True, "#ffffff")
        MENU_RECT = MENU_TEXT.get_rect(center=(screen_width // 2, screen_height // 2 - 300))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Button(
            image=pygame.image.load(settings.PLAY_BUTTON_IMAGE),
            pos=(screen_width // 2, screen_height // 2 + 200),
            text_input="PLAY",
            font=get_font(settings.FONT_SIZE_MEDIUM),
            base_color=(settings.PLAY_BUTTON_COLOR),
            hovering_color=settings.BUTTON_HOVER_COLOR
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load(settings.PLAY_BUTTON_IMAGE),
            pos=(screen_width // 2, screen_height // 2 + 350),
            text_input="QUIT",
            font=get_font(settings.FONT_SIZE_MEDIUM),
            base_color=(settings.QUIT_BUTTON_COLOR),
            hovering_color=settings.BUTTON_HOVER_COLOR
        )

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos):
                    click_sound.play()  
                    result, player1, player2 = transition_screen()
                    if result == "continue":
                        winner = coin_toss_popup(player1.title(), player2.title())
                        game = ConnectFour(settings, player1, player2)
                        if winner == 2:
                            game.turn = 1  # dapat Player 2 starts
                        else:
                            game.turn = 0  # dapat Player 1 starts
                        game.run()
                if QUIT_BUTTON.checkForInput(mouse_pos): 
                    click_sound.play()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()