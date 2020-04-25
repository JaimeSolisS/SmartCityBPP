import pygame, sys, os



class SlidePuzzle:
    def __init__(self,gs,ts,ms):  #gridSize, size of tiles, margin size
        self.gs, self.ts, self.ms = gs,ts,ms

        #create grid
        self.tiles_len  = gs[0]*gs[1]-1 
        self.tiles = [(x,y) for y in range (gs[1]) for x in range(gs[0])] 
        #array for coord on screen for the grid
        self.tilepos = { (x,y): (x*(ts+ms)+ms, y*(ts+ms)+ms) for y in range (gs[1]) for x in range(gs[0])} 

    def update(self,dt): 
        pass

    def draw(self, screen):
        for i in range (self.tiles_len): 
            x,y = self.tilepos[self.tiles[i]]
            pygame.draw.rect(screen, (0,167,201), (x,y, self.ts, self.ts))



def main(): 
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('SMART CITY: Bicycle Parking Problem')
    screen = pygame.display.set_mode((800,600))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle((3,3), 100, 5)


    while True: 
        dt = fpsclock.tick()/1000

        screen.fill((0,0,0,))
        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

        program.update(dt)


if __name__ == "__main__": 
     main()