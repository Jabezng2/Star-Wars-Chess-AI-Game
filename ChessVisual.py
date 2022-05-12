import pygame as p
import sys
# designing menu interface

class ChessVisual():
    def __init__(self):
        p.init()
        self.BOARD_WIDTH = self.BOARD_HEIGHT = 512
        self.MOVE_LOG_PANEL_WIDTH = 250
        self.MOVE_LOG_PANEL_HEIGHT = self.BOARD_HEIGHT
        self.DIMENSION = 8
        self.SQUARE_SIZE = self.BOARD_HEIGHT // self.DIMENSION
        self.MAX_FPS = 15
        self.IMAGES = {}
        self.screen = p.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        self.click = False
        self.buttons = {"buttonPlayAsLightSide": p.Rect(56, 120, 400, 56),
                        "buttonPlayAsDarkSide": p.Rect(56, 240, 400, 56),
                        "buttonCredits": p.Rect(56, 360, 400, 56)}
        self.mainClock = p.time.Clock()
        self.font_name = '8-BIT WONDER.TTF'
        self.font = p.font.Font(self.font_name, 20) # second parameter is text size
        self.mid_w, self.mid_h = self.BOARD_WIDTH/2, self.BOARD_HEIGHT/2
        # 3 buttons texts
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.creditBK = p.image.load("creditBK.png")
        self.menuBk = p.image.load("menuBK.png")

    def loadImages(self):
        """
        Initialize a global directory of images.
        This will be called exactly once in the main.
        """
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = p.transform.smoothscale(p.image.load("images/" + piece + ".png"),
                                                         (self.SQUARE_SIZE, self.SQUARE_SIZE))

    def drawBoard(self, screen):
        """
        Draw the squares on the board.
        The top left square is always light.
        """
        global colors
        colors = [p.Color("white"), p.Color("light blue")]
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                color = colors[((row + column) % 2)]
                p.draw.rect(screen, color, p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                                       self.SQUARE_SIZE, self.SQUARE_SIZE))

    def drawPieces(self, screen, board):
        """
        Draw the pieces on the board using the current game_state.board
        """
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = board[row][column]
                if piece != "--":
                    screen.blit(self.IMAGES[piece], p.Rect(column * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                                           self.SQUARE_SIZE, self.SQUARE_SIZE))

    def drawEndGameText(self, screen, text):
        font = p.font.SysFont("Helvetica", 32, True, False)
        text_object = font.render(text, False, p.Color("gray"))
        text_location = p.Rect(0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT).move(self.BOARD_WIDTH / 2 - text_object.get_width() / 2,
                                                                     self.BOARD_HEIGHT / 2 - text_object.get_height() / 2)
        screen.blit(text_object, text_location)
        text_object = font.render(text, False, p.Color('black'))
        screen.blit(text_object, text_location.move(2, 2))

    def drawMenuText(self, text, font, x, y):
        font = p.font.Font(self.font_name, font) # added in parameter for text size so easier to handle
        text_surface = font.render(text, True, p.Color("white"))
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.screen.blit(text_surface, text_rect)

    def mainMenu(self):
        while True and self.click == False:
            self.screen.fill(p.Color("white"))  # screen color
            self.screen.blit(self.menuBk, (6, 0))
            self.drawMenuText("Star Wars Chess", 30, self.BOARD_WIDTH/2, self.BOARD_HEIGHT/2 - 190)
            for button in self.buttons:
                p.draw.rect(self.screen, p.Color("dark grey"), self.buttons[button])  # button color comes out as white
            # outline for button !!can make a button class for better encapsulation!!
            x = 120
            for i in range(3):
                p.draw.line(self.screen, (255, 255, 255), (56, x), (56 + 400, x), 2)
                p.draw.line(self.screen, (255, 255, 255), (56, x), (56, x + 56), 2)
                p.draw.line(self.screen, (0, 0, 0), (56, x + 56), (56 + 400, x + 56), 2)
                p.draw.line(self.screen, (0, 0, 0), (56 + 400, x), (56 + 400, x + 56), 2)
                x += 120
            self.drawMenuText("Light Side", 20, self.BOARD_WIDTH / 2, self.BOARD_HEIGHT / 2 - 110)
            self.drawMenuText("Dark Side", 20, self.BOARD_WIDTH / 2, self.BOARD_HEIGHT / 2 + 10)  # 120 difference
            self.drawMenuText("Credits", 20, self.BOARD_WIDTH / 2, self.BOARD_HEIGHT / 2 + 130)
            # need this after the button so it doesnt get covered by button
            self.click = False
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        p.quit()
                        sys.exit()
                if event.type == p.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
            p.display.update()
            self.mainClock.tick(60)

    def creditsMenu(self):
        while True:
            # settle the screen color
            self.screen.fill(p.Color(128, 0 , 0))
            # background must be here
            self.screen.blit(self.creditBK, (0, -70))
            # no buttons but if further features want to be added can add here
            self.drawMenuText("Made by Jabez Ng", 30, self.BOARD_WIDTH /2 , self.BOARD_HEIGHT / 2 - 10)
            self.drawMenuText("Inspired by Eddie Sharick", 20, self.BOARD_WIDTH/2, self.BOARD_HEIGHT / 2 + 20)
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        p.quit()
                        sys.exit()
                if event.type == p.MOUSEBUTTONDOWN:
                        self.click = False
                        return
            p.display.update()
            self.mainClock.tick(60)

    def optionsMenu(self):
        while True:
            self.screen.fill(p.Color(128, 0, 0))
            # back ground image here
