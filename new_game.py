import random
import pygame
from pygame.display import toggle_fullscreen

from pygame.time import Clock

class que_item:
    #initial variables
    completed = False
    i = 0
    #iniitializes the que_item class
    def __init__(self, square, new_vel):
        self.square = square
        self.new_vel = new_vel
    
    #updates the the i'th square's position and increments the counter
    def advance(self):
        if (len(self.square) <= self.i):
            self.completed = True
        else:
            self.square[self.i].vel[0] = self.new_vel[0]
            self.square[self.i].vel[1] = self.new_vel[1]
        self.i += 1
    
    #deletes the item after it has been completed
    def clean_up(self, snake):
        if self.completed:
            snake.action_que.pop(0)

class Square:
    #initializes the square class
    def __init__(self, pos=[0,0],velocity=[0,0], color = (255,0,0), focused = False):
        self.pos = pos
        self.vel = velocity
        self.color = color
        self.focused = focused
    
    #updates the poisition of the square according to its velocity
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
    
    #draws the square if it is within the view range
    def draw(self, surface):
        dist = width // rows
        x = self.pos[0] + cam_coords[0]
        y = self.pos[1] + cam_coords[1]
        if x >= 0 and x < 20 and y >= 0 and y < 20:
            pygame.draw.rect(surface, self.color, (x*dist+1, y*dist+1, dist-1, dist-1))
   
class Snake:
    #initialize the snake class
    def __init__(self, pos=[10,10],velocity=[0,0], color = (0,255,0), isPlayer = True):
        self.head = Square(pos, velocity, color, isPlayer)
        self.vel = velocity
        self.color = color
        self.isPlayer = isPlayer
        self.body = []
        self.action_que = []

    #runs every frame
    def update(self):
        #calls the ai script
        if not self.isPlayer:
            self.AI_update()

        #updates each square in the snake
        self.head.update()
        for square in self.body:
            square.update()
        
    #returns the position of the object nearest to the snake it's called from
    def findNearestObject(self):    
        dis = abs(objects[0].pos[0] - self.head.pos[0]) + abs(objects[0].pos[1] - self.head.pos[1])
        nearest_object = objects[0]
        for object in objects:
            if abs(object.pos[0] - self.head.pos[0]) + abs(object.pos[1] - self.head.pos[1]) < dis:
                dis = abs(object.pos[0] - self.head.pos[0]) + abs(object.pos[1] - self.head.pos[1])
                nearest_object = object
        return nearest_object

    #controls the ai of the non-player snakes
    def AI_update(self):

        new_vel = self.vel
        #directs the snake to the nearest point object
        nearest_object = self.findNearestObject()
        if abs(nearest_object.pos[0] - self.head.pos[0]) > abs(nearest_object.pos[1] - self.head.pos[1]):
            if (nearest_object.pos[0] - self.head.pos[0]) > 0:
                new_vel = [1,0]
            else:
                new_vel = [-1,0]
        else:
            if (nearest_object.pos[1] - self.head.pos[1]) > 0:
                new_vel = [0,1]
            else:
                new_vel = [0,-1]

        self.set_vel(new_vel)

        #diverts the snake if it will intersect its self next frame
        pos = self.head.pos.copy()
        vel = self.vel

        for sq in self.body:
            if (self.head.pos[0] + self.vel[0] == sq.pos[0] and self.head.pos[1] + self.vel[1] == sq.pos[1]):
                if (not self.head.vel[0] == 0):
                    for _sq in self.body:
                        if (self.head.pos[0] + self.vel[0] == _sq.pos[0] and self.head.pos[1] + 1 == _sq.pos[1]):
                            self.set_vel([0,-1])
                        else:
                            self.set_vel([0,1])
                else:
                    for _sq in self.body:
                        if (self.head.pos[0] + 1 == _sq.pos[0] and self.head.pos[1] + self.vel[1] == _sq.pos[1]):
                            self.set_vel([-1,0])
                        else:
                            self.set_vel([1,0])

    #calls draw on each square of the snake
    def draw(self, surface):
        self.head.draw(surface)
        for square in self.body:
            square.draw(surface)
    
    #adds a new square to the snake's body
    def add_body(self):
        #adds a square opposite to the head's velocity
        if len(self.body) == 0:
            spawn_pos = [self.head.pos[0] - self.vel[0],self.head.pos[1] - self.vel[1]]
            spawn_vel = [self.vel[0],self.vel[1]]
            new = Square(spawn_pos, spawn_vel, self.color)
        #adds a square opposite to the last body element's velocity
        else:
            spawn_pos = [self.body[-1].pos[0] - self.body[-1].vel[0],self.body[-1].pos[1] - self.body[-1].vel[1]]
            spawn_vel = [self.body[-1].vel[0], self.body[-1].vel[1]]
            new = Square(spawn_pos, spawn_vel, self.color)
            #adds new square to all existing ques in the snake's action que
            if (len(self.action_que) > 0):
                for que in self.action_que:
                    que.square.append(new)
        
        self.body.append(new)
    
    #sets the velocity of the snake's head
    def set_vel(self, vel):
        self.vel[0] = vel[0]
        self.vel[1] = vel[1]

        #adds new list of squares to the snake's action que
        if len(self.body) > 0:
            self.action_que.append(que_item(self.body.copy(), vel))

#runs once per frame
def update_frame(surface):
    #creates game background and grid
    surface.fill((255,255,255))
    pygame.draw.rect(surface, (0,0,0), (0, 0, width, width))
    create_grid(surface)

    #moves the cam coords in the opposite direction of the player to account for the player's movement
    cam_coords[0] -= player.vel[0]
    cam_coords[1] -= player.vel[1]

    #updates and draws each point object
    for object in objects:
        object.update()
        object.draw(surface)
    
    #updates and draws each snake
    for snake in snakes:
        snake.update()
        snake.draw(surface)
    
    #updates each snake's action ques if they contain any
    for snake in snakes:
        if len(snake.action_que) > 0:
            for item in snake.action_que:
                item.advance()
            for item in snake.action_que:
                item.clean_up(snake)

    #checks for snake collision and draws the border
    check_collision()
    draw_border(surface)
    pygame.display.update()

#draws the map grid
def create_grid(surface):
    dist = width // rows

    x = 0
    y = 0

    for i in range(rows):
        x += dist
        y += dist

        pygame.draw.line(surface, (255,255,255), (x,0), (x,width))
        pygame.draw.line(surface, (255,255,255), (0,y), (width,y))
 
#draws the border around the level
def draw_border(surface):
    dist = width // rows

    for x in range(rows):
        for y in range(rows):
            if (x + player.head.pos[0] - 10 < 0 or x + player.head.pos[0] - 10 > map_size or y + player.head.pos[1] - 10 < 0 or y + player.head.pos[1] - 10 > map_size):
                pygame.draw.rect(surface, (255,255,255), (x*dist+1, y*dist+1, dist-1, dist-1))

#runs appropriate responses to pygame events
def get_events():
    dir = ""
    for event in pygame.event.get():
            if event == pygame.QUIT:
                global running
                running = False

            #sets dir to input from this frame
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dir = "left"
                elif event.key == pygame.K_RIGHT:
                    dir = "right"
                elif event.key == pygame.K_UP:
                    dir = "up"
                elif event.key == pygame.K_DOWN:
                    dir = "down"
    #sets player movement to corresponding dir value
    if dir != "":
        if dir == "left":
            player.set_vel([-1,0])
        elif dir == "right":
            player.set_vel([1,0])
        elif dir == "up":
            player.set_vel([0,-1])
        elif dir == "down":
             player.set_vel([0,1])
    dir = ""

#checks if snakes are colliding with themselves, other snakes, or point objects
def check_collision():
    for snake in snakes:
        #checks for collision with point objects
        for object in objects:
            if snake.head.pos[0] == object.pos[0] and snake.head.pos[1] == object.pos[1]:
                snake.add_body()
                objects.remove(object)
                s = Square([random.randrange(0,map_size),random.randrange(0,map_size)])
                objects.append(s)
                while check_objects():
                    objects[-1] = Square([random.randrange(0,map_size),random.randrange(0,map_size)])
        #collision between snakes
        for _snake in snakes:
            for sq in _snake.body:
                if snake.head.pos == sq.pos:
                    die(snake)
                if snake.head.pos == _snake.head.pos and not snake == _snake:
                    die(snake)

        #boundary death
        if (snake.head.pos[0] < 0 or snake.head.pos[0] > map_size or snake.head.pos[1] < 0 or snake.head.pos[1] > map_size):
            die(snake)

#resets the position and body size of the killed snake
def die(snake):
    snake.body.clear()
    loc = [random.randrange(0,map_size), random.randrange(0,map_size)]
    snake.head.pos = loc
    if snake == player:
        print("you died")
        global cam_coords
        cam_coords = [-1 * (loc[0]-(rows/2)),-1 * (loc[1]-(rows/2))]

#checks if any objects are overlapping
def check_objects():
    for obj1 in objects:
        for obj2 in objects:
            if not (obj1 == obj2) and (obj1.pos == obj2.pos):
                return True
    return False

def main() :
    #global variables
    global width, rows, objects, player, cam_coords, snakes, map_size, running
    width = 500
    rows = 20
    map_size = 40
    running = True
    objects = []
    snakes = []

    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((width, width), pygame.RESIZABLE)

    cam_coords = [0,0]
    
    #spawns objects randomly throughout the map
    for i in range(5):
        loc = [random.randrange(0,map_size), random.randrange(0,map_size)]
        s = Square(loc)
        objects.append(s)
    
    #ensures no objects are overlapping
    while check_objects():
        for obj in objects:
            obj.pos = [random.randrange(0,map_size), random.randrange(0,map_size)]

    #creates classes for each snake
    player = Snake([10,10], [0,0], (0,255,0), True)
    p2 = Snake([5,5], [0,-1], (0,255,255), False)
    p3 = Snake([15,5], [0,-1], (255,0,255), False)
    p4 = Snake([5,15], [0,-1], (0,0,255), False)

    #adds each snake class to the snake array to be updated and rendered
    snakes.append(player)
    snakes.append(p2)
    snakes.append(p3)
    snakes.append(p4)

    #main game loop
    while running:
        pygame.time.delay(50)
        clock.tick(10)
        get_events()
        update_frame(surface)


if __name__ == "__main__":
    main()