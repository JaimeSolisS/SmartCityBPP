import pygame, sys, os, random

class SlidePuzzle:

    prev = None 
    speed = 500

    def __init__(self,gs,ts,ms):  #gridSize, size of tiles, margin size
        self.gs, self.ts, self.ms = gs,ts,ms

        #create grid

        self.tiles_len  = gs[0]*gs[1]-1 
        self.tiles = [(x,y) for y in range (gs[1]) for x in range(gs[0])] 
       
       #We have to identical array of tile pos to use one to slide them to the new position
        self.tilepos=[(x*(ts+ms)+ms, y*(ts+ms)+ms) for y in range (gs[1]) for x in range(gs[0])] #actual position on screen
        #array for coord on screen for the grid
        self.tilePOS = { (x,y): (x*(ts+ms)+ms, y*(ts+ms)+ms) for y in range (gs[1]) for x in range(gs[0])} #the place they slide to
        

        self.images = []
        #text 
        font = pygame.font.Font(None, 120)
        
        for i in range (self.tiles_len): 
            x,y = self.tilepos[i]
            image = pygame.Surface((ts,ts))
            image.fill((0,167,201))
            text = font.render(str(i+1), 2, (0,0,0))
            w,h = text.get_size()
            image.blit(text, ((ts-w)/2, (ts-h)/2))
            self.images+=[image]

        #self.switch((0,0))


    def getBlank(self): 
        return self.tiles[-1]
    def setBlank(self, pos): 
        self.tiles[-1] = pos  
    opentile= property(getBlank, setBlank)
    
    def switch(self, tile): 
        self.tiles[self.tiles.index(tile)], self.opentile, self.prev = self.opentile, tile, self.opentile

    def in_grid(self, tile ): 
        return tile[0]>=0 and tile[0]< self.gs[0] and tile[1]>=0 and tile[1]< self.gs[1]

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
                if self.in_grid(tile) and tile in self.adjacent():
                    self.switch(tile)

        s = self.speed * dt 
        for i in range (self.tiles_len): 
            x,y = self.tilepos[i] # Current pos
            X,Y = self.tilePOS[self.tiles[i]] #Target pos
            #If the value between the current and target is less than speed, we can just let it jump right into place. 
            #Otherwise, we just need to add/substract in direction
            dx,dy = X-x, Y-y
            self.tilepos[i] = (X if abs(dx)<s else x+s if dx>0 else x-s), (Y if abs(dy)<s else y+s if dy>0 else y-s)



    def draw(self, screen):
        for i in range (self.tiles_len): 
            x,y = self.tilepos[i]
            screen.blit(self.images[i], (x,y))

    def events (self, event): 
        if event.type == pygame.KEYDOWN: 
            for key, dx, dy in ((pygame.K_w,0,-1),(pygame.K_s,0,1),(pygame.K_a,-1,0),(pygame.K_d,1,0)): 
                if event.key == key:
                    x,y = self.opentile
                    tile = x+dx, y+dy
                    if self.in_grid(tile): 
                        self.switch(tile)

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
            program.events(event)

        program.update(dt)


if __name__ == "__main__": 
    main()