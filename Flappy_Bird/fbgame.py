import pygame, sys, random 

pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load("assets/Flappy Bird.png")
pygame.display.set_icon(icon)   
pygame.mixer.pre_init(44100, -16, 2, 512)  # Thiết lập âm thanh
pygame.init()
# Hằng số 
weight = 324 
height = 576
TrongLuc = 0.2
clock = pygame.time.Clock()

#biến 
game_active = True
score = 0
high_score = 0

#font chữ 
game_font = pygame.font.Font("04B_19.TTF", 40)


screen = pygame.display.set_mode((weight, height))

# Nền
bg = pygame.image.load("assets/background-night.png").convert()
bg = pygame.transform.scale(bg, (int(bg.get_width()*1.5), int(bg.get_height()*1.5)))

# Sàn
floor = pygame.image.load("assets/floor.png").convert()
floor = pygame.transform.scale(floor, (int(floor.get_width()*1.5), int(floor.get_height()*1.5)))
floor_x_pos = 0

def draw_floor():
    screen.blit(floor, (floor_x_pos, 500))
    screen.blit(floor, (floor_x_pos + weight, 500))

# Tạo chim
bird_downflap = pygame.image.load("assets/yellowbird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("assets/yellowbird-upflap.png").convert_alpha()
bird_list = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird = bird_list[bird_index]
#bird = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
bird_rect = bird.get_rect(center = (75, 300))

bird_movement = 0

# tạo ống
pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale(pipe_surface, (int(pipe_surface.get_width()*1.5), int(pipe_surface.get_height()*1.5)))
pipe_list = []

pipe_gap = random.randint(100,180)  # khoảng cách giữa 2 ống

def create_pipe():
    pipe_center = random.randint(200, 400)  # vị trí trung tâm khoảng trống
    bottom_pipe = pipe_surface.get_rect(midtop=(weight + 50, pipe_center + pipe_gap // 2))
    top_pipe = pipe_surface.get_rect(midbottom=(weight + 50, pipe_center - pipe_gap // 2))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= height:
            screen.blit(pipe_surface, pipe)  # ống dưới
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)  # lật ống trên
            screen.blit(flip_pipe, pipe)

# tạo timer cho ống
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1300) # tạo ống mỗi 1.3 giây

#tạo timer cho chim
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)  # thay đổi hình ảnh chim

# xử lý va chạm 
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= height - 50:  # kiểm tra va chạm với sàn
        die_sound.play()
        return False
    return True

# hiệu ứng chim 
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 6, 1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(bird_rect.centerx, bird_rect.centery))
    return new_bird, new_bird_rect

# Hiển thị điểm số
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(weight // 2, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'main_over':
        high_score_surface = game_font.render(f'High Score: {high_score}', True, (255, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(weight // 2, 50))
        screen.blit(high_score_surface, high_score_rect)

        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 255))
        score_rect = score_surface.get_rect(center=(weight // 2,  475))
        screen.blit(score_surface, score_rect)

# cập nhật điểm
def update_score():
    global score, high_score
    if score > high_score:
        high_score = int(score)
    return high_score

# màn hình kết thúc
game_over_screen = pygame.image.load("assets/message.png").convert_alpha()
game_over_screen = pygame.transform.scale(game_over_screen, (int(game_over_screen.get_width()*1.5), int(game_over_screen.get_height()*1.5)))
game_over_rect = game_over_screen.get_rect(center=(weight // 2, height // 2))

# chèn âm thanh
flap_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
point_sound = pygame.mixer.Sound("sound/sfx_point.wav")
die_sound = pygame.mixer.Sound("sound/sfx_die.wav")
point_sound_count = 100

scored_pipes = []


# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
                flap_sound.play()  # phát âm thanh khi chim bay
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (75, 300)
                bird_movement = 0
            
                if score > high_score:
                    high_score = int(score)
                score = 0

        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())

        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird , bird_rect = bird_animation()
        
    # Vẽ nền
    screen.blit(bg, (0, 0))

    if game_active:
        # Vẽ chim
        
        bird_movement += TrongLuc
        rotated_bird = rotate_bird(bird) #pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
        bird_rect.centery += bird_movement

        screen.blit(rotated_bird, bird_rect)

        game_active = check_collision(pipe_list)

        # vẽ ống
        pipe_list = move_pipes(pipe_list)
        draw_pipe(pipe_list)

        for pipe in pipe_list:
            if pipe.centerx < bird_rect.centerx and pipe not in scored_pipes and pipe.bottom >= height:
                scored_pipes.append(pipe)
                score += 1
                point_sound.play()


        score_display('main_game')

    else:
        screen.blit(game_over_screen, game_over_rect)
        high_score = update_score()
        score_display('main_over')
    # vẽ sàn  

    draw_floor()
    floor_x_pos -= 3
    if floor_x_pos <= -weight:
        floor_x_pos = 0   
    
    screen.blit(floor, (floor_x_pos, 500))

    pygame.display.update()  
    clock.tick(120)
