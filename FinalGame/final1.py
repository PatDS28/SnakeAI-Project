import pygame
import button

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")


font = pygame.font.SysFont("arialblack", 30)
text_col = (255,255,255)

# game variables
start_key = False

# button images
img = pygame.image.load("assets/start_btn.png").convert_alpha()
img1 = pygame.image.load("assets/start_btn.png").convert_alpha()
img2 = pygame.image.load("assets/start_btn.png").convert_alpha()

img_button = button.Button(260,125, img, 0.5)
img_button1 = button.Button(260,225, img1, 0.5)
img_button2 = button.Button(260,325, img2, 0.5)

def draw_text(text,font,text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

run = True
while run:
    screen.fill((52,78,91))
    if start_key == True:
        img_button.draw(screen)
        img_button1.draw(screen)
        img_button2.draw(screen)
    else:
        draw_text("Press Space to pause", font, text_col, 150,350)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("sada")
                start_key = True
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()