import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1100, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("draw/Background_black.PNG")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("draw/font.ttf", size)

def play():
    run = True
    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(30).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(550, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(100, 690), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

    pygame.quit()

  

        

       
def score():
    while True:
        SCORE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0,0))

        OPTIONS_TEXT = get_font(45).render("This is the SCORE screen.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(550, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        try:
            SCORE1 = get_font(50).render(highscore[0], True, "#C9B037")
            SCORE_RECT1 = HIGHSCORE_TEXT.get_rect(center=(650, 200))
            SCORE2 = get_font(50).render(highscore[1], True, "#B4B4B4")
            SCORE_RECT2 = HIGHSCORE_TEXT.get_rect(center=(650, 250))
            SCORE3 = get_font(50).render(highscore[2], True, "#6A3805")
            SCORE_RECT3 = HIGHSCORE_TEXT.get_rect(center=(650, 300))
            SCORE4 = get_font(50).render(highscore[3], True, "#50577A")
            SCORE_RECT4 = HIGHSCORE_TEXT.get_rect(center=(650, 350))
            SCORE5 = get_font(50).render(highscore[4], True, "#50577A")
            SCORE_RECT5 = HIGHSCORE_TEXT.get_rect(center=(650, 400))


            SCREEN.blit(SCORE2, SCORE_RECT2)
            SCREEN.blit(SCORE1,SCORE_RECT1)
            SCREEN.blit(SCORE3, SCORE_RECT3)
            SCREEN.blit(SCORE4, SCORE_RECT4)
            SCREEN.blit(SCORE5, SCORE_RECT5)
        except:
            pass

        SCORE_BACK = Button(image=None, pos=(550, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        SCORE_BACK.changeColor(SCORE_MOUSE_POS)
        SCORE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCORE_BACK.checkForInput(SCORE_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("SPACE SHOOTER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(550, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("draw/Play Rect.png"), pos=(550, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        SCORE_BUTTON = Button(image=pygame.image.load("draw/Options Rect.png"), pos=(550, 400), 
                            text_input="SCORE", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("draw/Quit Rect.png"), pos=(550, 550), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SCORE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    score()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()