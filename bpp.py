import pygame, sys, os, random

#A* Used for getting path to target while avoiding other tiles
def AStar (start, end, walls, size): 
    
    cells = {(x,y) : {'pos' : (x,y), 'parent': None, 'g': 0, 'h': max(abs(x-end[0]), abs(y-end[1])), 'wall': (x,y) in walls} for y in range(size[1]) for x in range(size[0])}
    opened = [cells[start]] 
    closed = []
    path =[]
    
    while opened:
        
        current = min(opened, key=lambda i: i['g']+i['h'])
        closed.append(current) 
        opened.remove(current)
        
        if current['pos']==end:
            while current['parent']: 
                path.append(current['pos'])
                current=current['parent']
            return path[::-1]

        for dx,dy in ((-1,0), (1,0), (0,-1), (0,1)):
            x,y = current['pos'][0]+dx, current['pos'][1]+dy
            if x<0 or y<0 or x>=size[0] or y>=size[1]: 
                continue
            adj = cells[(x,y)] 
            if adj['wall'] or adj in closed: 
                continue
            new_g = current['g']+1
            new_cell = adj not in opened
            if new_cell or new_g<adj['g']: 
                adj['parent'] = current 
                adj['g'] = new_g
            if new_cell: 
                opened.append(adj)

    return path
    
class Simulator: 

    previous = None 
    moves = None
    speed = 500

    def __init__(self, gs,ts,ms):  #gridSize, size of tiles, margin size
        self.size, self.ts, self.ms = gs,ts,ms
        self.width = self.size[0]
        self.heigth = self.size[1]
        self.walls = [(x,y) for y in range(self.heigth-2) for x in range(self.-2)]

        #create grid
        self.tiles_len  = self.width * self.heigth-1 
        self.tiles = [(x,y) for y in range (self.heigth) for x in range(self.width)] 
        self.tiles.append(self.tiles.pop(self.tiles.index((1,0))))    

        #We have to identical array of tile pos to use one to slide them to the new position
        self.tilepos=[(x*(ts+ms)+ms, y*(ts+ms)+ms) for y in range (self.heigth) for x in range(self.width)] #actual position on screen
        #array for coord on screen for the grid
        self.tilePOS = { (x,y): (x*(ts+ms)+ms, y*(ts+ms)+ms) for y in range (self.heigth) for x in range(self.width)} #the place they slide to

        self.images = []
        #text 
        font = pygame.font.Font(None, 20)
        
        for i in range (self.tiles_len): 
            x,y = self.tilepos[i]
            image = pygame.Surface((ts,ts))
            if i == 0 or i ==7:
                image.fill((255,0,0))
            elif i == 34:
                image.fill((0,255,0))
            else:
                image.fill((0,167,201))
            text = font.render(str(i+1), 2, (0,0,0))
            w,h = text.get_size()
            image.blit(text, ((ts-w)/2, (ts-h)/2))
            self.images+=[image]

    

    def getBlank(self): 
        return self.tiles[-1]
    def setBlank(self, pos): 
        self.tiles[-1] = pos  
    opentile= property(getBlank, setBlank)
    
    def switch(self, tile): 
        self.tiles[self.tiles.index(tile)], self.opentile, self.prev = self.opentile, tile, self.opentile

    def in_grid(self, tile ): 
        return tile[0]>=0 and tile[0]< self.width and tile[1]>=0 and tile[1]< self.heigth

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
                    print(self.tiles)

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
    screen = pygame.display.set_mode((400,700))
    fpsclock = pygame.time.Clock()
    program = Simulator((8,15), 40, 5)


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




        

    

        