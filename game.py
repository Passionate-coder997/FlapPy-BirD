import pygame, sys, random
def draw_base():
    screen.blit(base_img,(base_x_pos,450))
    screen.blit(base_img,(base_x_pos+288,450))

def create_pipe():
    pipe_pos = random.choice(pipe_h)
    top_pipe = top_pipe_img.get_rect(midbottom=(350,pipe_pos-200))
    top_pipe = pipe_img.get_rect(midbottom=(350,pipe_pos-200))
    new_pipe = pipe_img.get_rect(midtop=(350,pipe_pos))
    return new_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 1         #controls gameplay
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=512:
            screen.blit(pipe_img,pipe)
        else:
            flip_pipe = pygame.transform.flip(top_pipe_img,False,True)
            screen.blit(flip_pipe,pipe)

def collision_detect(pipes):
    global sc_point
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            collision_sound.play()
            sc_point = True
            return False

    if bird_rect.top <= -50 or bird_rect.bottom >= 500:
        collision_sound.play()
        sc_point = True
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3,1)
    return new_bird
def bird_animate():
    new_bird = bird_frame[bird_frameid]
    new_bird_rect = new_bird.get_rect(center=(50,bird_rect.centery))
    return new_bird, new_bird_rect
def disp_score(game_state):
    if game_state == 'current_game':
        score_surface = game_font.render(str(score),True,(255,150,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score:{score}',True,(255,150,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score:{int(high_score)}',True,(255,150,255))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
def score_check():
    global score, sc_point

    if pipe_lst:
        for pipe in pipe_lst:
            if 47.5 < pipe.centerx < 52.5 and sc_point:
                score += 1
                score_sound.play()
                sc_point = False
            if pipe.centerx < 0:
                sc_point = True

#pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)

pygame.init()

icon = pygame.image.load('assets/main.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

gravity = 0.15
bird_movement = 0
game_on = True
score = 0
high_score = 0
sc_point = True

bg = pygame.image.load('assets/background-day.png').convert()
base_img = pygame.image.load('assets/base.png')
base_x_pos=0

bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frame = [bird_upflap, bird_midflap, bird_downflap]
bird_frameid = 0
bird_img = bird_frame[bird_frameid]
bird_rect = bird_img.get_rect(center=(50,256))

bird_flaps = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flaps,200)

#bird_img = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_rect = bird_img.get_rect(center=(50,256))
#to scale image to screen dimensions
#bg = pygame.transform.scale2x(bg)
pipe_img = pygame.image.load('assets/pipe-green.png').convert()
top_pipe_img = pygame.image.load('assets/pipe-red.png').convert()
pipe_lst = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_h = [200,300,400]

game_over_surface = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(144,256))

flap_sound=pygame.mixer.Sound('sound/sfx_wing.wav')
collision_sound=pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound=pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_count=100

#SCOREVENT = pygame.USEREVENT+2
#pygame.time.set_timer(SCOREVENT,100)

#Game Loop
while True:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif events.type == pygame.KEYDOWN:
            if events.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE and game_on:
                bird_movement = 0
                bird_movement -= 7     #value can be altered for moving bird upwards
                flap_sound.play()
            if events.key == pygame.K_SPACE and game_on == False:
                game_on = True
                pipe_lst.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0
        if events.type == SPAWNPIPE:
            pipe_lst.extend(create_pipe())
        if events.type == bird_flaps:
            if bird_frameid < 2:
                bird_frameid += 1
            else:
                bird_frameid = 0

        bird_img,bird_rect = bird_animate()

    screen.blit(bg,(0,0))

    if game_on:
    #Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_img)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        game_on = collision_detect(pipe_lst)
    #Pipes
        pipe_lst = move_pipe(pipe_lst)
        draw_pipe(pipe_lst)
    #Score
        score_check()
        disp_score('current_game')

    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        disp_score('game_over')

    base_x_pos -= 1
    
    draw_base()
    
    if base_x_pos<=-288:
        base_x_pos=0
    
    pygame.display.update()
    
    clock.tick(120)