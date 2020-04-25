import pygame, sys, os



class SlidePuzzle:
    def __init__(self,gs,ts,ms):  #gridSize, size of tiles, margin size
        self.gs, self.ts, self.ms = gs,ts,ms

        #create grid

        self.tiles_len  = gs[0]*gs[1]-1 
        self.tiles = [(x,y) for y in range (gs[1]) for x in range(gs[0])] 
        #array for coord on screen for the grid
        self.tilepos = { (x,y): (x*(ts+ms)+ms, y*(ts+ms)+ms) for y in range (gs[1]) for x in range(gs[0])} 

        #text 
        font = pygame.font.Font(None, 120)
        self.images = []
        for i in range (self.tiles_len): 
            image = pygame.Surface((ts,ts))
            image.fill((0,167,201))
            text = font.render(str(i+1), 2, (0,0,0))
            w,h = text.get_size()
            image.blit(text, ((ts-w)/2, (ts-h)/2))
            self.images+=[image]

        self.switch((0,0))


    def getBlank(self): 
        return self.tiles[-1]
    def setBlank(self, pos): 
        self.tiles[-1] = pos  
    opentile= property(getBlank, setBlank)
    
    def switch(self, tile): 
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]

    def in_grid(self, tile ): 
        return tile[0]>=0 and tile[0]< self.gs[0] and tile[1]>=0 and tile[0]< self.gs[1]

    def adjacent(self): 
        x,y = self.opentile
        return (x-1,y), (x+1,y),(x,y-1), (x,y+1)

    def update(self,dt): 
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()

        if mouse[0]:

            x, y  = mpos[0]%(self.ts+self.ms), mpos[0]%(self.ts+self.ms)
            if x>self.ms and y>self.ms:
                tile = mpos[0]//self.ts, mpos[1]//self.ts
                if self.in_grid(tile):
                    if tile in self.adjacent():
                        self.switch(tile)

    def draw(self, screen):
        for i in range (self.tiles_len): 
            x,y = self.tilepos[self.tiles[i]]
            screen.blit(self.images[i], (x,y))

def main(): 
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('SMART CITY: Bicycle Parking Problem')
    screen = pygame.display.set_mode((800,600))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle((3,3), 160, 5)


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