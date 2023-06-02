import pygame

pygame.init()
sc = pygame.display.set_mode((600, 600))

grass = pygame.image.load('TEXTURES/GROUND_TEXTURES/grass.png').convert_alpha()

building1 = pygame.image.load('TEXTURES/BUILDING_TEXTURES/building1.png').convert_alpha()
roof1 = pygame.image.load('TEXTURES/BUILDING_TEXTURES/roof1.png').convert_alpha()
forge = pygame.image.load('TEXTURES/BUILDING_TEXTURES/forge.png').convert_alpha()
forgeBuiltStay = pygame.image.load('TEXTURES/BUILDING_TEXTURES/forgeBuildedStay.png').convert_alpha()

playerStay = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerStay.png').convert_alpha()
playerWalk1 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk1.png').convert_alpha()
playerWalk2 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk2.png').convert_alpha()
playerWalk3 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk3.png').convert_alpha()
playerWalk4 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk4.png').convert_alpha()
playerWalk5 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk5.png').convert_alpha()
playerWalk6 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk6.png').convert_alpha()
playerWalk7 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk7.png').convert_alpha()
playerWalk8 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk8.png').convert_alpha()
playerWalk9 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk9.png').convert_alpha()
playerWalk10 = pygame.image.load('TEXTURES/PLAYER_TEXTURES/playerWalk10.png').convert_alpha()

zombieStay = pygame.image.load('TEXTURES/ZOMBIE_TEXTURES/NORMAL_ZOMBIE_TEXTURES/zombieStay.png').convert_alpha()

bossStay1 = pygame.image.load('TEXTURES/ZOMBIE_TEXTURES/BOSS_ZOMBIE_TEXTURES/bossStay1.png').convert_alpha()

glockStay = pygame.image.load('TEXTURES/WEAPON_TEXTURES/GLOCK_TEXTURES/glockStay.png').convert_alpha()

bulletStay = pygame.image.load('TEXTURES/WEAPON_TEXTURES/BULLET_TEXTURES/bulletStay.png').convert_alpha()
grenadeStay = pygame.image.load('TEXTURES/WEAPON_TEXTURES/BULLET_TEXTURES/grenadeStay.png').convert_alpha()

metal = pygame.image.load('TEXTURES/MATERIAL_TEXTURES/metal1.png').convert_alpha()
wood = pygame.image.load('TEXTURES/MATERIAL_TEXTURES/wood.png').convert_alpha()
rubber = pygame.image.load('TEXTURES/MATERIAL_TEXTURES/rubber.png').convert_alpha()
stone = pygame.image.load('TEXTURES/MATERIAL_TEXTURES/stone.png').convert_alpha()
