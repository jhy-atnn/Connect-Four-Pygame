class Settings:
    """A class to hold configuration settings for the Connect Four game."""
    def __init__(self, row_count=6, col_count=7, square_size=100):
        # Board settings
        self.ROW_COUNT = row_count
        self.COLUMN_COUNT = col_count
        self.SQUARESIZE = square_size
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.screen_width = self.COLUMN_COUNT * self.SQUARESIZE
        self.screen_height = (self.ROW_COUNT + 1) * self.SQUARESIZE

        # Colors
        self.PINK = "#8B3883"
        self.PURPLE = "#281244"
        self.RED = "#8f1414"
        self.YELLOW = "#f2b705"
        self.STAND = ("#4C244D")
        self.WHITE = (255, 255, 255)

        # Font
        self.MENU_FONT_PATH = "img\\stytlefont.ttf"
        self.GAME_FONT_PATH = "img\\Blockblueprint-LV7z5.ttf"
        self.FONT_SIZE_LARGE = 190
        self.FONT_SIZE_MEDIUM = 75
        self.FONT_SIZE_SMALL = 55
        self.FONT_SIZE_INPUT = 40

        # Images
        self.BG_IMAGE = "img\\BGGGG.png"
        self.CONFOUR_IMAGE = "img\\confourcircle.png"
        self.PLAY_BUTTON_IMAGE = "img\\Play Rect.png"
        self.BOMB_IMAGE = "img\\bomb.png"

        # Sounds
        self.BG_MUSIC = "img\\Sakura-Girl-Yay-chosic.com_.mp3"
        self.YAY_SOUND = "img\\children-saying-yay-praise-and-worship-jesus-299607.wav"
        self.BOMB_SOUND = "img\\Bad-Explosion-chosic.com_.mp3"
        self.DROP_SOUND = "img\dropsound.WAV"
        self.CLICK_SOUND = "img\clicksound.WAV"

        # Button colors
        self.PLAY_BUTTON_COLOR = "#07c917"
        self.QUIT_BUTTON_COLOR = "#fec107"
        self.BUTTON_HOVER_COLOR = "White"
        self.BUTTON_TEXT_COLOR = "#f2b705"