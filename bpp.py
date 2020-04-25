import pygame, sys, os

def main(): 
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('SMART CITY: Bicycle Parking Problem')
    screen = pygame.display.set_mode((800,600))
    fpsclock = pygame.time.Clock()

    while True: 
        screen.fill((0,0,0,))
        pygame.display.flip()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

 
if __name__ == "__main__": 
    main() 