#import from the configuration file all variables and libraries
from utilities import *

class Wall:
    def __init__(self, hits, color, position):
        self.hits = hits
        self.color = color
        self.position = position
    
    def status(self):
        return self.hits
    
    def get_color(self):
        return self.color

    def get_hits(self):
        return self.hits

    def get_position(self):
        return self.position


#DRAW

#draw window of the game, red and yellow rapresent the two ships
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, ammo_red, ammo_yellow, walls_red, walls_yellow ):
    
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    r_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE) 
    y_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, WHITE) 
    
    WIN.blit(r_health_text, (10, 10))
    WIN.blit(y_health_text, (WIDTH - y_health_text.get_width() - 10, 10 ))

    r_score = HEALTH_FONT.render("SCORE: " + str(red_score), 1, WHITE)
    y_score = HEALTH_FONT.render("SCORE: " + str(yellow_score),1, WHITE)

    WIN.blit(r_score, (10 + r_health_text.get_width() + 50,10))
    WIN.blit(y_score, (WIDTH - y_health_text.get_width() - y_score.get_width() - 50,10))

    red_ammunitions = HEALTH_FONT.render("AMMO: " + str(MAX_BULLETS_RED), 1, WHITE)
    yellow_ammunitions = HEALTH_FONT.render("AMMO: " + str(MAX_BULLETS_YELLOW),1, WHITE)

    WIN.blit(red_ammunitions, (10 + r_health_text.get_width() + r_score.get_width() + 100, 10))
    WIN.blit(yellow_ammunitions, (WIDTH - y_health_text.get_width() -  y_score.get_width() - yellow_ammunitions.get_width() - 100 , 10))
    
    #i can access to x and y because yellow and red are rectangles
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for ammo in ammo_red:
        WIN.blit(BULLET_SCALE, (ammo.x, ammo.y))
        
    for ammo in ammo_yellow:
        WIN.blit(BULLET_SCALE, (ammo.x, ammo.y))

    for wall in walls_red:
        pygame.draw.rect(WIN, wall.get_color(), wall.get_position())
    
    for wall in walls_yellow:
        pygame.draw.rect(WIN, wall.get_color(), wall.get_position())
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

#change color of the wall when is hit
def set_wall_color(walls_red, walls_yellow):
    for wall in walls_red:
        if wall.hits == 1:
            wall.color = ORANGE
        elif wall.hits == 2:
            wall.color = YELLOW
        elif wall.hits == 3:
            walls_red.remove(wall)

    for wall in walls_yellow:
        if wall.hits == 1:
            wall.color = ORANGE
        elif wall.hits == 2:
            wall.color = YELLOW
        elif wall.hits == 3:
            walls_yellow.remove(wall)

#draw who is the winner
def draw_winner(text):
    win_text = WINNER_FONT.render(text, 1, PURPLE)
    WIN.blit(win_text, (WIDTH/2 - win_text.get_width() / 2, HEIGHT/2 - win_text.get_height() / 2))
    pygame.display.update()
    WIN_SOUND.play()
    pygame.time.delay(4000)
    pygame.event.clear()
    main_menu()


#COLLISION

#check collision between walls and players
def wall_collision_player(red, yellow, walls_red, walls_yellow):
    
    for wall in walls_red:
        if abs(red.top - wall.position.bottom) < COLLISION_TOLERANCE:
            while red.colliderect(wall.position):
                red.y += 1

        if abs(red.bottom - wall.position.top) < COLLISION_TOLERANCE:
            while red.colliderect(wall.position):
                red.y -= 1
                
        if abs(red.right - wall.position.left) < COLLISION_TOLERANCE:
            rect = pygame.Rect(wall.position.x - 10, wall.position.y, 10, wall.position.height)
            while red.colliderect(rect):
                red.x -= 1

        if abs(red.left - wall.position.right) < COLLISION_TOLERANCE:
            while red.colliderect(wall.position):
                red.x += 1

    
    for wall in walls_yellow:
        if abs(yellow.top - wall.position.bottom) < COLLISION_TOLERANCE:
            while yellow.colliderect(wall.position):
                yellow.y += 1

        if abs(yellow.bottom - wall.position.top) < COLLISION_TOLERANCE:
            while yellow.colliderect(wall.position):
                yellow.y -= 1

        if abs(yellow.right - wall.position.left) < COLLISION_TOLERANCE:
            while yellow.colliderect(wall.position):
                yellow.x -= 1

        if abs(yellow.left - wall.position.right) < COLLISION_TOLERANCE:
            while yellow.colliderect(wall.position):
                yellow.x += 1

#check collision between walls and bullets
def wall_collision_bullet(red_bullets, yellow_bullets, walls_red, walls_yellow):
   
    for wall in walls_red:
        for bullet in red_bullets:
            if bullet.colliderect(wall.position):
                wall.hits += 1
                red_bullets.remove(bullet)
    
    for wall in walls_red:
        for bullet in yellow_bullets:
            if bullet.colliderect(wall.position):
                wall.hits += 1
                yellow_bullets.remove(bullet)
                
    
    for wall in walls_yellow:
        for bullet in yellow_bullets:
            if bullet.colliderect(wall.position):
                wall.hits += 1
                yellow_bullets.remove(bullet)

    for wall in walls_yellow:
        for bullet in red_bullets:
            if bullet.colliderect(wall.position):
                wall.hits += 1 
                red_bullets.remove(bullet)

#check collisions between ammunitions and players
def ammo_collision(ammo_red, ammo_yellow, red, yellow):
    global MAX_BULLETS_RED, MAX_BULLETS_YELLOW
    for ammo in ammo_red:
        if red.colliderect(ammo):
            MAX_BULLETS_RED += 5
            GET_AMMO_SOUND.play()
            ammo_red.remove(ammo)
    for ammo in ammo_yellow:
        if yellow.colliderect(ammo):
            MAX_BULLETS_YELLOW += 5
            GET_AMMO_SOUND.play()
            ammo_yellow.remove(ammo)


#MOVEMENT

#handle movement of red player
def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - SPEED > 0: #left
        red.x -= SPEED
    if keys_pressed[pygame.K_d] and red.x + red.width < BORDER.x : #right
        red.x += SPEED
    if keys_pressed[pygame.K_w] and red.y - SPEED > 0: #up
        red.y -= SPEED
    if keys_pressed[pygame.K_s] and red.y + SPEED + red.height < HEIGHT - SPEED*3 : #down
        red.y += SPEED

#handle movement of yellow player
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - SPEED > BORDER.x + SPEED*3: #left
        yellow.x -= SPEED
    if keys_pressed[pygame.K_RIGHT] and yellow.x - SPEED < WIDTH - SPACESHIP_WIDTH: #right
        yellow.x += SPEED
    if keys_pressed[pygame.K_UP] and yellow.y - SPEED > 0: #up
        yellow.y -= SPEED
    if keys_pressed[pygame.K_DOWN] and yellow.y + SPEED + yellow.height < HEIGHT - SPEED*3: #down
        yellow.y += SPEED

#handle movement of bullets
def bullets_movement(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


#handle loop of the game
def main():
    red = pygame.Rect(150, 350, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(1200, 350,SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    ammo_red = []                        
    ammo_yellow = []                       
    
    red_bullets = []
    yellow_bullets = []
    
    walls_red = []
    walls_yellow = []

    red_health = 3
    yellow_health = 3
    global MAX_BULLETS_YELLOW, MAX_BULLETS_RED
    MAX_BULLETS_RED = 5
    MAX_BULLETS_YELLOW = 5

    count = 0
    #set the speed of the loop (60 times per second)
    clock = pygame.time.Clock()
    run = True
    #infinite loop, ends when the game finishes or the user quits the game    

    while run:
        clock.tick(FPS)
        
        if count % (FPS*10) == 0:
            r_ammo = pygame.Rect(random.randint(0,WIDTH/2 - 50), random.randint(50, HEIGHT - 50), BULLET_WIDTH, BULLET_HEIGHT)
            y_ammo = pygame.Rect(random.randint(WIDTH/2 + 50, WIDTH - 50), random.randint(50, HEIGHT - 50), BULLET_WIDTH, BULLET_HEIGHT)

            ammo_red.append(r_ammo)
            ammo_yellow.append(y_ammo)

        if count % (FPS*20) == 0:
            r_wall = Wall(0, RED, pygame.Rect(random.randint(50, WIDTH/2 - 50), random.randint(20, HEIGHT - 50), WALL_WIDTH, random.randint(MIN_WALL_HEIGHT, MAX_WALL_HEIGHT)))
            y_wall = Wall(0, RED, pygame.Rect(random.randint(WIDTH/2 + 50, WIDTH - 50), random.randint(20, HEIGHT - 50), WALL_WIDTH, random.randint(MIN_WALL_HEIGHT, MAX_WALL_HEIGHT)))
            
            walls_red.append(r_wall)
            walls_yellow.append(y_wall)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and MAX_BULLETS_RED > 0:
                    MAX_BULLETS_RED -= 1
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height/2 - BULLET_HEIGHT/2 , BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and MAX_BULLETS_YELLOW > 0:
                    MAX_BULLETS_YELLOW -= 1
                    bullet = pygame.Rect(yellow.x , yellow.y + yellow.height/2 - BULLET_HEIGHT/2 , BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_q:
                    run = False
                    pygame.quit()
            
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()


        winner = ""
        if red_health <= 0:
            winner = "YELLOW WINS!"
            global yellow_score
            yellow_score += 1

        if yellow_health <= 0:
            winner = "RED WINS!"
            global red_score
            red_score += 1

        if winner != '':
            red_bullets.clear()
            yellow_bullets.clear()
            ammo_red.clear()
            ammo_yellow.clear()
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, ammo_red, ammo_yellow, walls_red, walls_yellow)
            draw_winner(winner)
            break
        
    
        count += 1
        #moovment
        keys_pressed = pygame.key.get_pressed()

        red_movement(keys_pressed, red)
        yellow_movement(keys_pressed, yellow)
        bullets_movement(red_bullets, yellow_bullets, red, yellow)
        
        wall_collision_bullet(red_bullets, yellow_bullets, walls_red, walls_yellow)
        ammo_collision(ammo_red, ammo_yellow, red, yellow)
        wall_collision_player(red, yellow, walls_red, walls_yellow)
        
        set_wall_color(walls_red, walls_yellow)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, ammo_red, ammo_yellow, walls_red, walls_yellow)


def main_menu():
    init = True
    pygame.event.clear()
    while init:
        WIN.blit(SPACE, (0,0))
        shoot_me = SHOOT_ME_FONT.render("SHOOT ME!!", 1, GREEN)
        WIN.blit(shoot_me, (WIDTH/2 - shoot_me.get_width() / 2,  shoot_me.get_height()))

        text = INIT_FONT.render("Press any key to play...", 1, WHITE)
        WIN.blit(text, (WIDTH/2 - text.get_width() / 2, HEIGHT/2))
        pygame.display.update()
        pygame.time.delay(1500)

        WIN.blit(SPACE, (0,0))
        pygame.display.update()
        pygame.time.delay(500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                init = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                pygame.KEYDOWN
                main()


main_menu()

