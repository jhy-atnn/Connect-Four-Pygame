import pygame
import sys
import random
from settings import Settings
from confetti import show_confetti

# Colors
RED = ("#8f1414")
YELLOW = ("#f2b705")

class ConnectFour:
    def __init__(self, settings, player1="Player 1", player2="Player 2"):
        self.settings = settings
        self.ROW_COUNT = settings.ROW_COUNT
        self.COLUMN_COUNT = settings.COLUMN_COUNT
        self.SQUARESIZE = settings.SQUARESIZE
        self.RADIUS = settings.RADIUS

        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h

        self.BG = pygame.image.load(settings.BG_IMAGE)
        self.BG = pygame.transform.scale(self.BG, (self.width, self.height))

        self.board = self.create_board()
        self.game_over = False
        self.turn = 0

        self.player1 = player1.title()
        self.player2 = player2.title()

        self.x_offset = (self.width - self.COLUMN_COUNT * self.SQUARESIZE) // 2
        self.y_offset = (self.height - (self.ROW_COUNT + 1) * self.SQUARESIZE) // 2

        # Set custom font for all text
        self.font = pygame.font.Font(settings.GAME_FONT_PATH, 60)
        self.draw_board()
        pygame.display.update()

        # Bomb feature
        self.bomb_used = [False, False]
        self.bomb_mode = False
        # Load bomb image
        self.bomb_img = pygame.image.load(settings.BOMB_IMAGE)
        self.bomb_img = pygame.transform.scale(self.bomb_img, (50, 50))

        # Load yay sound
        self.yay_sound = pygame.mixer.Sound(settings.YAY_SOUND)

        # Load bomb sound
        self.bomb_sound = pygame.mixer.Sound(settings.BOMB_SOUND)
        self.drop_sound = pygame.mixer.Sound(settings.DROP_SOUND)

    def create_board(self):
        return [[0 for _ in range(self.COLUMN_COUNT)] for _ in range(self.ROW_COUNT)]

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
        

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def winning_move(self, piece):
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if all(self.board[r][c+i] == piece for i in range(4)):
                    return True
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if all(self.board[r+i][c] == piece for i in range(4)):
                    return True
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if all(self.board[r+i][c+i] == piece for i in range(4)):
                    return True
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if all(self.board[r-i][c+i] == piece for i in range(4)):
                    return True
        return False

    def is_board_full(self):
        return all(self.board[self.ROW_COUNT - 1][c] != 0 for c in range(self.COLUMN_COUNT))
    
    # Pixelated yung board drawing
    def draw_board(self):
        pixel_factor = 0.25
        small_width = int(self.width * pixel_factor)
        small_height = int(self.height * pixel_factor)
        small_surface = pygame.Surface((small_width, small_height))

        small_surface.blit(pygame.transform.scale(self.BG, (small_width, small_height)), (0, 0))
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                # Yung Board Squares
                pygame.draw.rect(
                    small_surface, pygame.Color(self.settings.PINK),
                    (
                        int((self.x_offset + c * self.SQUARESIZE) * pixel_factor),
                        int((self.y_offset + r * self.SQUARESIZE + self.SQUARESIZE) * pixel_factor),
                        int(self.SQUARESIZE * pixel_factor),
                        int(self.SQUARESIZE * pixel_factor)
                    )
                )
                # Eto yung Empty Slots
                pygame.draw.circle(
                    small_surface, pygame.Color(self.settings.PURPLE),
                    (
                        int((self.x_offset + c * self.SQUARESIZE + self.SQUARESIZE / 2) * pixel_factor),
                        int((self.y_offset + r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2) * pixel_factor)
                    ),
                    int(self.RADIUS * pixel_factor)
                )
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(
                        small_surface, pygame.Color(self.settings.RED),
                        (
                            int((self.x_offset + c * self.SQUARESIZE + self.SQUARESIZE / 2) * pixel_factor),
                            int((self.y_offset + (self.ROW_COUNT - r) * self.SQUARESIZE + self.SQUARESIZE / 2) * pixel_factor)
                        ),
                        int(self.RADIUS * pixel_factor)
                    )
                elif self.board[r][c] == 2:
                    pygame.draw.circle(
                        small_surface, pygame.Color(self.settings.YELLOW),
                        (
                            int((self.x_offset + c * self.SQUARESIZE + self.SQUARESIZE / 2) * pixel_factor),
                            int((self.y_offset + (self.ROW_COUNT - r) * self.SQUARESIZE + self.SQUARESIZE / 2) * pixel_factor)
                        ),
                        int(self.RADIUS * pixel_factor)
                    )

        # Stand nung Board
        stand_color = self.settings.STAND
        board_left = int(self.x_offset * pixel_factor)
        board_top = int((self.y_offset + self.SQUARESIZE) * pixel_factor)
        board_width = int(self.COLUMN_COUNT * self.SQUARESIZE * pixel_factor)
        board_height = int(self.ROW_COUNT * self.SQUARESIZE * pixel_factor)
        stand_height = int(40 * pixel_factor)
        stand_rect = pygame.Rect(
            board_left,
            board_top + board_height,
            board_width,
            stand_height
        )
        pygame.draw.rect(small_surface, stand_color, stand_rect)

        pixelated_surface = pygame.transform.scale(small_surface, (self.width, self.height))
        self.screen.blit(pixelated_surface, (0, 0))

    def run(self):
        winner = None
        turn_start_time = pygame.time.get_ticks()
        turn_limit = 11000 
        mouse_pos = None

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_b and not self.bomb_used[self.turn]:
                        self.bomb_mode = True

                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = (posx - self.x_offset) // self.SQUARESIZE
                    if 0 <= col < self.COLUMN_COUNT:
                        if self.bomb_mode and not self.bomb_used[self.turn]:
                            for r in range(self.ROW_COUNT):
                                self.board[r][col] = 0
                            self.bomb_used[self.turn] = True
                            self.bomb_mode = False
                            self.bomb_sound.play() 
                            self.turn = (self.turn + 1) % 2
                            turn_start_time = pygame.time.get_ticks()
                        elif self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, self.turn + 1)
                            self.drop_sound.play()  # Play drop sound here
                            if self.winning_move(self.turn + 1):
                                winner = self.player1 if self.turn == 0 else self.player2
                                self.game_over = True
                            elif self.is_board_full():
                                winner = "Draw Game"
                                self.game_over = True
                            self.turn = (self.turn + 1) % 2
                            turn_start_time = pygame.time.get_ticks()
                            if self.game_over:
                                self.draw_board()
                                pygame.display.update()
                                self.yay_sound.play()  # Play yay sound
                                show_confetti(self.screen, self.BG, duration=2)
                                if winner == "Draw Game":
                                    win_color = (255, 255, 255)
                                else:
                                    win_color = RED if winner == self.player1 else YELLOW
                                winner_font = pygame.font.Font("img\Blockblueprint-LV7z5.ttf", 100)  # Adjust size as needed
                                label = winner_font.render(f"{winner}!", 1, win_color)
                                label_rect = label.get_rect(center=(self.width // 2, self.height // 2))
                                self.screen.blit(label, label_rect)

                                info_font = pygame.font.Font("img\Blockblueprint-LV7z5.ttf", 40)
                                info_label = info_font.render("[Click anywhere to Play Again]", 1, (255, 255, 255))
                                info_rect = info_label.get_rect(center=(self.width // 2, self.height // 2 + 120))
                                self.screen.blit(info_label, info_rect)
                                pygame.display.update()

                                # Wait for any mouse click or key press
                                waiting = True
                                while waiting:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                                            waiting = False
                                return

            # Timer check random drop ng piece sa board
            if not self.game_over:
                time_passed = pygame.time.get_ticks() - turn_start_time
                if time_passed >= turn_limit:
                    valid_cols = [c for c in range(self.COLUMN_COUNT) if self.is_valid_location(c)]
                    if valid_cols:
                        col = random.choice(valid_cols)
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, self.turn + 1)
                        if self.winning_move(self.turn + 1):
                            winner = self.player1 if self.turn == 0 else self.player2
                            self.game_over = True
                        elif self.is_board_full():
                            winner = "Draw Game"
                            self.game_over = True
                        self.turn = (self.turn + 1) % 2
                        turn_start_time = pygame.time.get_ticks()
                        if self.game_over:
                            self.draw_board()
                            if winner == "Draw Game":
                                win_color = (255, 255, 255)
                            else:
                                win_color = RED if winner == self.player1 else YELLOW
                            label = self.font.render(f"{winner}!", 1, win_color)
                            label_rect = label.get_rect(center=(self.width // 2, self.y_offset // 2 + 30))
                            self.screen.blit(label, label_rect)
                            pygame.display.update()
                            pygame.time.wait(3000)
                            return

            if mouse_pos:
                posx = mouse_pos[0]
                if not (self.x_offset <= posx < self.x_offset + self.COLUMN_COUNT * self.SQUARESIZE):
                    mouse_pos = None

            self.draw_board()

            if mouse_pos:
                posx = mouse_pos[0]
                color = RED if self.turn == 0 else YELLOW
                pygame.draw.circle(
                    self.screen, color,
                    (posx, self.y_offset + self.SQUARESIZE // 2),
                    self.RADIUS
                )

            # Draw turn label and timer
            if not self.game_over:
                bomb_icon_size = 50
                if self.turn == 0:
                    # Player 1 (left)
                    p1_label = self.font.render(f"{self.player1}'s Turn", 1, RED)
                    self.screen.blit(p1_label, (40, self.y_offset // 2 + 30))
                    bomb_x = 40
                    bomb_y = self.y_offset // 2 + 110
                    label_x = bomb_x + bomb_icon_size + 10
                    bomb_text_align = "left"
                else:
                    # Player 2 (right)
                    p2_label = self.font.render(f"{self.player2}'s Turn", 1, YELLOW)
                    p2_rect = p2_label.get_rect(topright=(self.width - 40, self.y_offset // 2 + 30))
                    self.screen.blit(p2_label, p2_rect)
                    bomb_x = self.width - 40 - bomb_icon_size
                    bomb_y = self.y_offset // 2 + 110
                    label_x = bomb_x - 180  # adjust as needed
                    bomb_text_align = "right"

                # Draw bomb icon and label under current player
                if not self.bomb_used[self.turn]:
                    self.screen.blit(self.bomb_img, (bomb_x, bomb_y))
                    bomb_text = self.font.render("Bomb (Type B)", 1, ("#5A5B6C"))
                else:
                    bomb_img_gray = pygame.Surface(self.bomb_img.get_size(), pygame.SRCALPHA)
                    bomb_img_gray.blit(self.bomb_img, (0,0))
                    bomb_img_gray.fill((128,128,128,180), special_flags=pygame.BLEND_RGBA_MULT)
                    self.screen.blit(bomb_img_gray, (bomb_x, bomb_y))
                    bomb_text = self.font.render("Bomb Used", 1, (128,128,128))

                bomb_text_rect = bomb_text.get_rect()
                if self.turn == 0:
                    bomb_text_rect.topleft = (label_x, bomb_y + 10)
                else:
                    bomb_text_rect.topright = (bomb_x - 10, bomb_y + 10)
                self.screen.blit(bomb_text, bomb_text_rect)

                time_left = max(0, turn_limit - (pygame.time.get_ticks() - turn_start_time)) // 1000
                timer_label = self.font.render(f"Time: {time_left}", 1, (255,255,255))
                timer_rect = timer_label.get_rect(center=(self.width // 2, self.y_offset // 2 + 30))
                self.screen.blit(timer_label, timer_rect)

            pygame.display.update()

if __name__ == "__main__":
    settings = Settings()
    game = ConnectFour(settings)
    game.run()