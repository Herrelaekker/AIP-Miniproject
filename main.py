import pygame
import a_star_pathfinding as a_star
import state_machine as sm


def grid(window):
    distanceBtwRows = size // rows
    x = 0
    y = 0
    for l in range(rows):
        x += distanceBtwRows
        y += distanceBtwRows
        pygame.draw.line(window, (0,0,0),  (x,0), (x,size))
        pygame.draw.line(window, (0,0,0),  (0,y), (size,y))


def draw_enemy(window, enm):
    x = enm[0]
    y = enm[1]
    pygame.draw.rect(window, (255, 0, 0), (x*rectSize + 1, y*rectSize + 1, rectSize - 1, rectSize - 1))


def draw_obstacle(window, obs):
    x = obs[0]
    y = obs[1]
    pygame.draw.rect(window, (0, 0, 0), (x*rectSize + 1, y*rectSize + 1, rectSize - 1, rectSize - 1))


def draw_speaker(window, spk):
    x = spk[0]
    y = spk[1]
    pygame.draw.rect(window, (0, 0, 255), (x*rectSize + 1, y*rectSize + 1, rectSize - 1, rectSize - 1))


def redraw(window):
    window.fill((255,255,255))
    grid(window)

    for o in obstacles:
        draw_obstacle(window, o)

    if speaker:
        draw_speaker(window, speaker)

    pygame.draw.rect(window, (0,255,0), (posX*rectSize+1, posY*rectSize+1, rectSize -1, rectSize-1))

    for e in enemies:
        draw_enemy(window, e)

    pygame.display.update()


def tile_has_obstacle(square):
    for o in obstacles:
        if o == square:
            return True
    return False


def can_move_to_tile(direction):
    if direction == "Left":
        if posX - 1 >= 0 and not tile_has_obstacle(tuple((posX-1, posY))):
            return True
        else:
            return False
    elif direction == "Right":
        if posX + 1 < rectSize and not tile_has_obstacle(tuple((posX+1, posY))):
            return True
        else:
            return False
    elif direction == "Up":
        if posY - 1 >= 0 and not tile_has_obstacle(tuple((posX, posY - 1))):
            return True
        else:
            return False
    elif direction == "Down":
        if posY + 1 < rectSize and not tile_has_obstacle(tuple((posX, posY + 1))):
            return True
        else:
            return False


def create_obstacle(pos):
    obstaclePosX = int(pos[0]/rectSize)
    obstaclePosY = int(pos[1]/rectSize)
    obstacle = tuple((obstaclePosX, obstaclePosY))
    if not tile_has_obstacle(obstacle):
        obstacles.append(tuple(obstacle))


def destroy_obstacle(pos):
    obstaclePosX = int(pos[0] / rectSize)
    obstaclePosY = int(pos[1] / rectSize)
    obstacle = tuple((obstaclePosX, obstaclePosY))
    if tile_has_obstacle(obstacle):
        obstacles.remove(tuple(obstacle))


def create_speaker(pos):
    speakerPosX = int(pos[0])
    speakerPosY = int(pos[1])
    global speaker
    speaker = (tuple((speakerPosX, speakerPosY)))


def main():
    pygame.init()
    global size, rows
    size = 900
    rows = 30

    global posX, posY, rectSize
    posX = 8
    posY = 4
    rectSize = size/rows

    global obstacles
    obstacles = []

    global enemies
    enemies = [(0,0)]

    global speaker
    speaker = None

    window = pygame.display.set_mode((size, size))

    play = True

    MOVE_TIME = 500
    enemy_move = pygame.USEREVENT +1

    pygame.time.set_timer(enemy_move, MOVE_TIME)

    destroySpeakertimer = 2
    enemySM = sm.EnemySM(destroySpeakertimer)
    enemyInitialPos = enemies[0]

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if can_move_to_tile("Left"):
                        posX -= 1
                if event.key == pygame.K_RIGHT:
                    if can_move_to_tile("Right"):
                        posX += 1
                if event.key == pygame.K_UP:
                    if can_move_to_tile("Up"):
                        posY -= 1
                if event.key == pygame.K_DOWN:
                    if can_move_to_tile("Down"):
                        posY += 1
                if event.key == pygame.K_SPACE:
                    if speaker is None:
                        create_speaker((posX, posY))
                        enemySM.speaker_spawned()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    create_obstacle(pos)
                if event.button == 3:
                    pos = pygame.mouse.get_pos()
                    destroy_obstacle(pos)
            if event.type == enemy_move:
                enemySM.update()
                if enemySM.get_state() == enemySM.goToSpeaker:
                    state_path = a_star.search(enemies[0], speaker, obstacles, rows)
                    print(state_path)
                    print(len(state_path))
                    if len(state_path) > 1:
                        enemies[0] = state_path[1]
                    else:
                        enemySM.speaker_reached()
                if enemySM.get_state() == enemySM.goBackToIdle:
                    if speaker is not None:
                        speaker = None
                    state_path = a_star.search(enemies[0], enemyInitialPos, obstacles, rows)
                    print(state_path)
                    print(len(state_path))
                    if len(state_path) > 1:
                        enemies[0] = state_path[1]
                    else:
                        enemySM.spawn_point_reached()


        redraw(window)


main()
