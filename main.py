import pygame
import random
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        self.isBossRoom = False
        self.isMainRoom = True
        self.isBossRoomLoaded = False
        self.hasWin = False
        self.hasLost = False
        self.reset = False
        self.room_state = "main"
        self.title = pygame.display.set_caption("Dungeon Fighter")
        self.running = True
        self.FRAME_LIMIT = 30
        self.WIDTH = 800
        self.HEIGHT = 600
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

    def event_handler(self):
        keys = pygame.key.get_pressed()
        if player.isIdle:
            player.isMovingLeft = False
            player.isMovingRight = False
            player.isMovingDown = False
            player.isMovingUp = False
        if keys[K_DOWN] and player.yPos < game.HEIGHT - player.HEIGHT - player.velocity - 70:
            player.move_down()
        if keys[K_UP] and player.yPos > player.velocity:
            player.move_up()
        if keys[K_LEFT] and game.room_state == "main" and player.xPos > player.velocity + 10:
            player.move_left()
        elif keys[K_LEFT] and game.room_state == "boss" and player.xPos > 450:
            player.move_left()
        if keys[K_RIGHT] and player.xPos < game.WIDTH - player.WIDTH - player.velocity - 10:
            player.move_right()
        else:
            player.isIdle = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    if player.canShoot:
                        if len(fireballs) < 1:
                            player.attack()
                            temp_fireball = Fireball()
                            fireballs.append(temp_fireball)
                if event.key == K_RETURN and level.isDoorOpen:
                    game.room_state = "boss"
                    game.isBossRoom = True
                    game.isMainRoom = False
                if event.key == K_r and self.hasLost:
                    self.reset = True

    def main_room(self):
        self.window.blit(level.mainBase, (0, 0))
        self.event_handler()
        if not self.hasLost:
            player.animation_counter(), player.collision(), player.animation(), player.death(), player.display_health()
            for ogre in ogres:
                ogre.display(), ogre.movement(), ogre.collision(), ogre.display_health()
                if not ogres[0].isAlive and not ogres[1].isAlive and not ogres[2].isAlive:
                    redFlask.canPickUp = True
                    redFlask.display_red_flask()
                if ogre.isLast:
                    key.display(ogre.xPos, ogre.yPos)
            for fireball in fireballs:
                player.attack()
                player.canMove = False
                fireball.animation_counter(), fireball.shoot(), fireball.collision()
                if abs(player.xPos - fireball.xPos) > 100 or len(fireballs) == 0:
                    player.canMove, player.isAttacking, player.isIdle = True, False, True
        else:
            player.canMove, player.canShoot = False, False
            self.window.blit(level.loseLabel, (150, 50))
        pygame.display.update()

    def boss_room(self):
        self.window.blit(level.bossBase, (0, 0))
        self.isBossRoomLoaded = True
        self.event_handler()
        if not self.hasLost:
            player.animation_counter(), player.animation(), player.collision(), player.death()
            for fireball in fireballs:
                player.attack()
                player.canMove = False
                fireball.animation_counter()
                fireball.shoot()
                fireball.collision()
                if abs(player.xPos - fireball.xPos) > 100 or len(fireballs) == 0:
                    player.canMove = True
                    player.isAttacking = False
                    player.isIdle = True
            boss.shoot(), boss.display(), boss.movement(), boss.display_health()
            for tear in tears:
                tear.display(), tear.collision()
            player.display_health()
        else:
            player.canMove = False
            player.canShoot = False
            self.window.blit(level.loseLabel, (150, 0))
        if self.hasWin:
            game.window.blit(level.winLabel, (150, 0))
        pygame.display.update()


class Player:
    def __init__(self):
        self.WIDTH = 50
        self.HEIGHT = 80
        self.xPos = 100
        self.yPos = 100
        self.velocity = 5
        self.hasKey = False
        self.health = [True, True, True]
        self.canMove = True
        self.canShoot = True
        self.isIdle = True
        self.isMovingRight = False
        self.isMovingLeft = False
        self.isMovingUp = False
        self.isMovingDown = False
        self.isFacingRight = True
        self.isFacingLeft = False
        self.isAttacking = False
        self.rightIdleAnimationCounter = 0
        self.leftIdleAnimationCounter = 0
        self.moveRightAnimationCounter = 0
        self.moveLeftAnimationCounter = 0
        self.moveUpRightAnimationCounter = 0
        self.moveUpLeftAnimationCounter = 0
        self.moveDownRightAnimationCounter = 0
        self.moveDownLeftAnimationCounter = 0
        self.hitBox = (self.xPos, self.yPos, self.WIDTH, self.HEIGHT)
        self.hitBoxRect = pygame.Rect(self.hitBox)
        self.moveRightAnimation = [
            pygame.transform.scale(pygame.image.load('assets/player/run/' + str(i) + '.png'),
                                   (self.WIDTH, self.HEIGHT)) for i in range(4)]

        self.moveLeftAnimation = [pygame.transform.flip(self.moveRightAnimation[i], True, False) for i in range(4)]

        self.rightIdleAnimation = [
            pygame.transform.scale(pygame.image.load('assets/player/idle/' + str(i) + '.png'),
                                   (self.WIDTH, self.HEIGHT)) for i in range(4)]
        self.leftIdleAnimation = [pygame.transform.flip(self.rightIdleAnimation[i], True, False) for i in range(4)]

        self.rightAttackAnimation = pygame.transform.scale(pygame.image.load('assets/player/hit/0.png')
                                                           .convert_alpha(), (self.WIDTH, self.HEIGHT))
        self.leftAttackAnimation = pygame.transform.flip(self.rightAttackAnimation, True, False)

        self.fullHealthIndicator = pygame.transform.scale(
            pygame.image.load('assets/player/playerHealth/full_heart.png'), (40, 40))
        self.emptyHealthIndicator = pygame.transform.scale(
            pygame.image.load('assets/player/playerHealth/empty_heart.png'), (40, 40))
        self.healthIndicatorX = 20
        self.healthIndicatorY = 15

    def display_health(self):
        if self.health[0]:
            game.window.blit(self.fullHealthIndicator, (self.healthIndicatorX, self.healthIndicatorY))
        else:
            game.window.blit(self.emptyHealthIndicator, (self.healthIndicatorX, self.healthIndicatorY))
        if self.health[1]:
            game.window.blit(self.fullHealthIndicator, (self.healthIndicatorX + 40, self.healthIndicatorY))
        else:
            game.window.blit(self.emptyHealthIndicator, (self.healthIndicatorX + 40, self.healthIndicatorY))
        if self.health[2]:
            game.window.blit(self.fullHealthIndicator, (self.healthIndicatorX + 80, self.healthIndicatorY))
        else:
            game.window.blit(self.emptyHealthIndicator, (self.healthIndicatorX + 80, self.healthIndicatorY))

    def animation_counter(self):
        if self.rightIdleAnimationCounter >= 3:
            self.rightIdleAnimationCounter = 0
        if self.leftIdleAnimationCounter >= 3:
            self.leftIdleAnimationCounter = 0
        if self.moveRightAnimationCounter >= 3:
            self.moveRightAnimationCounter = 0
        if self.moveLeftAnimationCounter >= 3:
            self.moveLeftAnimationCounter = 0
        if self.moveUpRightAnimationCounter >= 3:
            self.moveUpRightAnimationCounter = 0
        if self.moveUpLeftAnimationCounter >= 3:
            self.moveUpLeftAnimationCounter = 0
        if self.moveDownRightAnimationCounter >= 3:
            self.moveDownRightAnimationCounter = 0
        if self.moveDownLeftAnimationCounter >= 3:
            self.moveDownLeftAnimationCounter = 0

    def animation(self):
        if self.isMovingUp:
            if self.isFacingRight:
                game.window.blit(self.moveRightAnimation[round(self.moveUpRightAnimationCounter)],
                                 (self.xPos, self.yPos))
                self.moveUpRightAnimationCounter += 0.2
            elif self.isFacingLeft:
                game.window.blit(self.moveLeftAnimation[round(self.moveUpLeftAnimationCounter)], (self.xPos, self.yPos))
                self.moveUpLeftAnimationCounter += 0.2
        elif self.isMovingDown:
            if self.isFacingRight:
                game.window.blit(self.moveRightAnimation[round(self.moveDownRightAnimationCounter)],
                                 (self.xPos, self.yPos))
                self.moveDownRightAnimationCounter += 0.2
            elif self.isFacingLeft:
                game.window.blit(self.moveLeftAnimation[round(self.moveDownLeftAnimationCounter)],
                                 (self.xPos, self.yPos))
                self.moveDownLeftAnimationCounter += 0.2
        elif self.isMovingRight:
            game.window.blit(self.moveRightAnimation[round(self.moveRightAnimationCounter)], (self.xPos, self.yPos))
            self.moveRightAnimationCounter += 0.2
        elif self.isMovingLeft:
            game.window.blit(self.moveLeftAnimation[round(self.moveLeftAnimationCounter)], (self.xPos, self.yPos))
            self.moveLeftAnimationCounter += 0.2
        elif self.isAttacking:
            if self.isFacingRight:
                game.window.blit(player.rightAttackAnimation, (player.xPos, player.yPos))
            else:
                game.window.blit(player.leftAttackAnimation, (player.xPos, player.yPos))
        else:
            if player.isFacingRight:
                game.window.blit(self.rightIdleAnimation[round(self.rightIdleAnimationCounter)], (self.xPos, self.yPos))
                self.rightIdleAnimationCounter += 0.15
            else:
                game.window.blit(self.leftIdleAnimation[round(self.leftIdleAnimationCounter)], (self.xPos, self.yPos))
                self.leftIdleAnimationCounter += 0.15

    def move_up(self):
        if self.canMove:
            self.yPos -= self.velocity
            self.isIdle = False
            self.isMovingLeft = False
            self.isMovingDown = False
            self.isMovingUp = True
            self.isAttacking = False
            self.rightIdleAnimationCounter = 0
            self.leftIdleAnimationCounter = 0

    def move_down(self):
        if self.canMove:
            self.yPos += self.velocity
            self.isIdle = False
            self.isMovingRight = False
            self.isMovingLeft = False
            self.isMovingDown = True
            self.isMovingUp = False
            self.isAttacking = False
            self.rightIdleAnimationCounter = 0
            self.leftIdleAnimationCounter = 0

    def move_right(self):
        if self.canMove:
            self.xPos += self.velocity
            self.isFacingRight = True
            self.isFacingLeft = False
            self.isIdle = False
            self.isMovingRight = True
            self.isMovingLeft = False
            self.isAttacking = False
            self.rightIdleAnimationCounter = 0
            self.leftIdleAnimationCounter = 0

    def move_left(self):
        if self.canMove:
            self.xPos -= self.velocity
            self.isFacingLeft = True
            self.isFacingRight = False
            self.isIdle = False
            self.isMovingRight = False
            self.isMovingLeft = True
            self.isAttacking = False
            self.rightIdleAnimationCounter = 0
            self.leftIdleAnimationCounter = 0

    def attack(self):
        self.isAttacking = True
        self.isIdle = False
        self.isMovingRight = False
        self.isMovingLeft = False
        self.isMovingUp = False
        self.isMovingDown = False

    def collision(self):
        self.hitBox = (self.xPos + 5, self.yPos + 40, self.WIDTH - 10, self.HEIGHT - 40)
        self.hitBoxRect = pygame.Rect(self.hitBox)
        if self.hitBoxRect.colliderect(redFlask.redFlaskHitBoxRect) and game.isMainRoom and redFlask.canPickUp:
            if redFlask.redFlaskIsAlive:
                self.health = [True, True, True]
                redFlask.redFlaskIsAlive = False
        if game.room_state == "main":
            if self.hitBoxRect.colliderect(key.hitBox):
                self.hasKey = True
                key.isAlive = False
            if self.hitBoxRect.colliderect(level.doorHitBox) and self.hasKey:
                level.isDoorOpen = True
                level.doorOpen = True
                game.window.blit(level.openDoor, (470, 14))
            else:
                game.window.blit(level.closedDoor, (470, 14))
                level.isDoorOpen = False
                level.doorOpen = False

    def death(self):
        if not self.health[0] and not self.health[1] and not self.health[2]:
            game.hasLost = True


class Flask:
    def __init__(self):
        self.redFlaskX = 300
        self.redFlaskY = 300
        self.WIDTH = 40
        self.HEIGHT = 40
        self.redFlaskIsAlive = True
        self.canPickUp = False
        self.redFlaskHitBox = (self.redFlaskX + 5, self.redFlaskY + 10, self.WIDTH - 10, self.HEIGHT - 10)
        self.redFlaskHitBoxRect = pygame.Rect(self.redFlaskHitBox)
        self.redFlask = pygame.transform.scale(pygame.image.load('assets/flask/0.png'),
                                               (self.WIDTH, self.HEIGHT))

    def display_red_flask(self):
        if self.redFlaskIsAlive:
            game.window.blit(self.redFlask, (self.redFlaskX, self.redFlaskY))


class Level:
    def __init__(self):
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.isDoorOpen = False
        self.mainBase = pygame.transform.scale(pygame.image.load('assets/level/surroundings/base.png'),
                                               (game.WIDTH, game.HEIGHT))
        self.bossBase = pygame.transform.scale(pygame.image.load('assets/level/surroundings/bossBase.png'),
                                               (game.WIDTH, game.HEIGHT))
        self.openDoor = pygame.transform.scale(pygame.image.load('assets/level/doors/doorOpen.png'), (80, 65))
        self.closedDoor = pygame.transform.scale(pygame.image.load('assets/level/doors/doorClosed.png'), (80, 65))
        self.doorHitBox = pygame.Rect(470, 14, 80, 65)
        self.winLabel = pygame.transform.scale(pygame.image.load('assets/level/win.png'), (500, 500))
        self.loseLabel = pygame.transform.scale(pygame.image.load('assets/level/lose.png'), (500, 500))


class Fireball:
    def __init__(self):
        self.WIDTH = 80
        self.HEIGHT = 50
        if player.isFacingRight:
            self.xPos = player.xPos + 20
            self.isMovingRight = True
            self.isMovingLeft = False
        elif player.isFacingLeft:
            self.xPos = player.xPos - 20
            self.isMovingLeft = True
            self.isMovingRight = False
        self.yPos = player.yPos + 30
        self.velocity = 10
        self.hitBox = (self.xPos, self.yPos, self.WIDTH, self.HEIGHT)
        self.hitBoxRect = pygame.Rect(self.hitBox)
        self.rightAnimationCounter = 0
        self.leftAnimationCounter = 0
        self.rightAnimation = [
            pygame.transform.scale(pygame.image.load('assets/fireball/' + str(i) + '.png').convert_alpha(),
                                   (self.WIDTH, self.HEIGHT)) for i in range(15)]

        self.leftAnimation = [pygame.transform.flip(self.rightAnimation[i], True, False) for i in range(15)]

    def animation_counter(self):
        if self.rightAnimationCounter >= 14:
            self.rightAnimationCounter = 0
        if self.leftAnimationCounter >= 14:
            self.leftAnimationCounter = 0

    def shoot(self):
        if player.canShoot:
            if self.isMovingRight:
                if self.xPos < game.WIDTH - self.WIDTH - self.velocity:
                    game.window.blit(self.rightAnimation[self.rightAnimationCounter],
                                     (self.xPos, self.yPos))
                    self.xPos += self.velocity
                    self.rightAnimationCounter += 1
                else:
                    fireballs.remove(self)
            if self.isMovingLeft:
                if self.xPos > self.velocity + 25:
                    game.window.blit(self.leftAnimation[self.leftAnimationCounter],
                                     (self.xPos - 30, self.yPos))
                    self.xPos -= self.velocity
                    self.leftAnimationCounter += 1
                else:
                    fireballs.remove(self)

    def collision(self):
        if self.isMovingRight:
            self.hitBox = (self.xPos, self.yPos + 15, self.WIDTH - 5, self.HEIGHT - 25)
            self.hitBoxRect = pygame.Rect(self.hitBox)
        elif self.isMovingLeft:
            self.hitBox = (self.xPos - 20, self.yPos + 15, self.WIDTH - 5, self.HEIGHT - 25)
            self.hitBoxRect = pygame.Rect(self.hitBox)
        if game.room_state == "main":
            for ogre in ogres:
                if self.hitBoxRect.colliderect(ogre.hitBoxRect):
                    if ogre.isAlive:
                        fireballs.remove(self)
                        ogre.hitCounter += 1
                        break
        elif game.room_state == "boss":
            if self.hitBoxRect.colliderect(boss.hitBox):
                if boss.isAlive:
                    fireballs.remove(self)
                    boss.hitCounter += 1


class Ogre:
    def __init__(self, x_pos, y_pos):
        self.WIDTH = 100
        self.HEIGHT = 100
        self.xPos = x_pos
        self.yPos = y_pos
        self.velocity = 1
        self.isPrimary = True
        self.isSecondary = False
        self.isTertiary = False
        self.isPrimaryAlive = True
        self.isSecondaryAlive = True
        self.isTertiaryAlive = True
        self.canMove = True
        self.isAlive = True
        self.isMovingLeft = True
        self.isMovingRight = False
        self.isAttacking = False
        self.isHit = False
        self.isLast = False
        self.secondaryIsDoneUp = False
        self.secondaryIsDoneLeft = False
        self.secondaryIsDoneDown = False
        self.secondaryIsDoneRight = False
        self.tertiaryIsDoneUp = False
        self.tertiaryIsDoneLeft = False
        self.tertiaryIsDoneDown = False
        self.tertiaryIsDoneRight = False
        self.hitCounter = 0
        self.attackCounter = 2
        self.hitBox = (self.xPos, self.yPos, self.WIDTH, self.HEIGHT)
        self.hitBoxRect = pygame.Rect(self.hitBox)
        self.attackRange = (self.xPos, self.yPos, self.WIDTH, self.HEIGHT)
        self.attackRangeRect = pygame.Rect(self.attackRange)
        self.moveRightAnimationCounter = 0
        self.moveLeftAnimationCounter = 0
        self.rightAttackAnimationCounter = 0
        self.leftAttackAnimationCounter = 0
        self.rightAttackAnimation = [pygame.transform.scale(pygame.image.load('assets/ogre/attack/' + str(i) + '.png'),
                                                            (self.WIDTH, self.HEIGHT)) for i in range(3)]
        self.leftAttackAnimation = [pygame.transform.flip(self.rightAttackAnimation[i], True, False) for i in range(3)]
        self.moveRightAnimation = [pygame.transform.scale(pygame.image.load('assets/ogre/walk/' + str(i) + '.png'),
                                                          (self.WIDTH, self.HEIGHT)) for i in range(4)]
        self.moveLeftAnimation = [pygame.transform.flip(self.moveRightAnimation[i], True, False) for i in range(4)]
        self.healthIndicator = [pygame.transform.scale(pygame.image.load
                                                       ('assets/ogre/health/' + str(i) + '.png').convert_alpha(),
                                                       (self.WIDTH, 40)) for i in range(5)]
        self.healthIndicatorX = self.xPos
        self.healthIndicatorY = self.yPos - 15

    def display(self):
        if self.hitCounter >= 5:  # if ogre dies
            if self == ogres[1] and self.isPrimaryAlive:
                if self.isSecondaryAlive:
                    ogres[0].isPrimary, ogres[0].isSecondary = True, False
                elif self.isTertiaryAlive:
                    ogres[2].isPrimary, ogres[2].isTertiary = True, False
                self.isPrimaryAlive = False

                if not ogres[0].isAlive and not ogres[2].isAlive:
                    self.isLast = True

            elif self == ogres[0] and self.isSecondaryAlive:
                if self.isTertiaryAlive:
                    ogres[2].isPrimary, ogres[2].isTertiary = True, False
                elif self.isPrimaryAlive:
                    ogres[1].isPrimary = True
                self.isSecondaryAlive = False

                if not ogres[1].isAlive and not ogres[2].isAlive:
                    self.isLast = True

            elif self == ogres[2] and self.isTertiaryAlive:
                if self.isPrimaryAlive:
                    ogres[1].isPrimary = True
                else:
                    ogres[0].isPrimary, ogres[0].isSecondary = True, False
                self.isTertiaryAlive = False

                if not ogres[0].isAlive and not ogres[1].isAlive:
                    self.isLast = True

            self.isAlive = False

        if self.isAlive:
            if self.moveRightAnimationCounter >= 3:
                self.moveRightAnimationCounter = 0
            if self.moveLeftAnimationCounter >= 3:
                self.moveLeftAnimationCounter = 0
            if self.rightAttackAnimationCounter >= 2:
                self.isHit = True
                self.rightAttackAnimationCounter = 0
            if self.leftAttackAnimationCounter >= 2:
                self.isHit = True
                self.leftAttackAnimationCounter = 0
            if self.isHit:
                player.health[self.attackCounter] = False
                self.attackCounter -= 1
                if self.attackCounter < 0:
                    self.attackCounter = 0
                self.isHit = False
            if self.isMovingLeft:
                if self.isAttacking:
                    game.window.blit(self.leftAttackAnimation[round(self.leftAttackAnimationCounter)],
                                     (self.xPos, self.yPos))
                    self.leftAttackAnimationCounter += 0.1
                else:
                    game.window.blit(self.moveLeftAnimation[round(self.moveLeftAnimationCounter)],
                                     (self.xPos, self.yPos))
                    self.moveLeftAnimationCounter += 0.2
                    self.rightAttackAnimationCounter = 0
                    self.leftAttackAnimationCounter = 0
            elif self.isMovingRight:
                if self.isAttacking:
                    game.window.blit(self.rightAttackAnimation[round(self.rightAttackAnimationCounter)],
                                     (self.xPos, self.yPos))
                    self.rightAttackAnimationCounter += 0.1
                else:
                    game.window.blit(self.moveRightAnimation[round(self.moveRightAnimationCounter)],
                                     (self.xPos, self.yPos))
                    self.rightAttackAnimationCounter = 0
                    self.leftAttackAnimationCounter = 0
                    self.moveRightAnimationCounter += 0.2

    def movement(self):
        if self.isPrimary:
            if self.isAlive and self.canMove:
                if self.xPos > player.xPos:
                    self.isMovingLeft = True
                    self.isMovingRight = False
                    self.xPos -= self.velocity
                    if self.yPos < player.yPos:
                        self.yPos += self.velocity
                    elif self.yPos > player.yPos:
                        self.yPos -= self.velocity
                elif self.xPos < player.xPos:
                    self.isMovingLeft = False
                    self.isMovingRight = True
                    self.xPos += self.velocity
                    if self.yPos < player.yPos:
                        self.yPos += self.velocity
                    elif self.yPos > player.yPos:
                        self.yPos -= self.velocity
                elif self.xPos == player.xPos:
                    if self.yPos < player.yPos:
                        self.yPos += self.velocity
                    elif self.yPos > player.yPos:
                        self.yPos -= self.velocity

        if self.isSecondary:
            if self.isAlive and self.canMove:
                if self.yPos > self.velocity + 30 and not self.secondaryIsDoneUp:
                    self.yPos -= self.velocity
                    if self.yPos <= self.velocity + 30:
                        self.secondaryIsDoneUp = True
                        self.secondaryIsDoneLeft = False
                elif self.xPos > self.velocity + 15 and not self.secondaryIsDoneLeft:
                    self.xPos -= self.velocity
                    if self.xPos <= self.velocity + 15:
                        self.secondaryIsDoneLeft = True
                        self.secondaryIsDoneDown = False
                elif self.yPos < game.HEIGHT - self.HEIGHT - 80 and not self.secondaryIsDoneDown:
                    self.yPos += self.velocity
                    if self.yPos >= game.HEIGHT - self.HEIGHT - 80:
                        self.secondaryIsDoneDown = True
                        self.secondaryIsDoneRight = False
                elif self.xPos < game.WIDTH - self.WIDTH - 10 and not self.secondaryIsDoneRight:
                    self.xPos += self.velocity
                    if self.xPos >= game.WIDTH - self.WIDTH - 10:
                        self.secondaryIsDoneRight = True
                        self.secondaryIsDoneUp = False

        if self.isTertiary:
            if self.isAlive and self.canMove:
                if self.xPos < game.WIDTH - self.WIDTH - 10 and not self.tertiaryIsDoneRight:
                    self.xPos += self.velocity
                    if self.xPos >= game.WIDTH - self.WIDTH - 10:
                        self.tertiaryIsDoneRight = True
                        self.tertiaryIsDoneDown = False
                elif self.yPos < game.HEIGHT - self.HEIGHT - 80 and not self.tertiaryIsDoneDown:
                    self.yPos += self.velocity
                    if self.yPos >= game.HEIGHT - self.HEIGHT - 80:
                        self.tertiaryIsDoneDown = True
                        self.tertiaryIsDoneLeft = False
                elif self.xPos > self.velocity + 15 and not self.tertiaryIsDoneLeft:
                    self.xPos -= self.velocity
                    if self.xPos <= self.velocity + 15:
                        self.tertiaryIsDoneLeft = True
                        self.tertiaryIsDoneUp = False
                elif self.yPos > self.velocity + 30 and not self.tertiaryIsDoneUp:
                    self.yPos -= self.velocity
                    if self.yPos <= self.velocity + 30:
                        self.tertiaryIsDoneUp = True
                        self.tertiaryIsDoneRight = False

    def display_health(self):
        self.healthIndicatorX = self.xPos
        self.healthIndicatorY = self.yPos - 15
        if self.isAlive:
            game.window.blit(self.healthIndicator[self.hitCounter],
                             (self.healthIndicatorX, self.healthIndicatorY))

    def collision(self):
        if self.isAlive:
            if self.isMovingLeft:
                self.hitBox = (self.xPos, self.yPos + 15, self.WIDTH - 10, self.HEIGHT - 10)
                self.hitBoxRect = pygame.Rect(self.hitBox)
                self.attackRange = (self.xPos, self.yPos + 55, self.WIDTH - 60, self.HEIGHT - 85)
                self.attackRangeRect = pygame.Rect(self.attackRange)
            else:
                self.hitBox = (self.xPos + 10, self.yPos + 15, self.WIDTH - 10, self.HEIGHT - 10)
                self.hitBoxRect = pygame.Rect(self.hitBox)
                self.attackRange = (self.xPos + 60, self.yPos + 55, self.WIDTH - 60, self.HEIGHT - 85)
                self.attackRangeRect = pygame.Rect(self.attackRange)
            for ogre in ogres:
                if player.hitBoxRect.colliderect(ogre.attackRangeRect):
                    ogre.isAttacking = True
                    ogre.canMove = False
                    break
                else:
                    ogre.isHit = False
                    ogre.isAttacking = False
                    ogre.canMove = True


class Boss:
    def __init__(self):
        self.WIDTH = 200
        self.HEIGHT = 200
        self.xPos = 300
        self.yPos = 175
        self.velocity = 3
        self.isAlive = True
        self.isDoneUp = False
        self.isDoneDown = False
        self.isDoneLeft = False
        self.hitCounter = 0
        self.healthIndicatorX = self.xPos
        self.healthIndicatorY = self.yPos - 15
        self.hitBox = pygame.Rect(self.xPos, self.yPos, self.WIDTH, self.HEIGHT)
        self.animation = [pygame.transform.scale(pygame.image.load('assets/boss/' + str(i) + '.png'),
                                                 (self.WIDTH, self.HEIGHT)) for i in range(5)]
        self.animationCounter = 0
        self.healthIndicator = [pygame.transform.scale(pygame.image.load
                                                       ('assets/ogre/health/' + str(i) + '.png').convert_alpha(),
                                                       (self.WIDTH, 80)) for i in range(5)]

    def display(self):
        if self.isAlive:
            if self.hitCounter >= 5:
                self.isAlive = False
                tears.clear()
                player.canMove = False
                player.canShoot = False
                game.hasWin = True
            if self.animationCounter >= 4:
                self.animationCounter = 0
            game.window.blit(self.animation[round(self.animationCounter)], (self.xPos, self.yPos))
            self.animationCounter += 0.2
            self.hitBox = pygame.Rect(self.xPos + 20, self.yPos + 15, self.WIDTH - 50, self.HEIGHT - 30)

    def shoot(self):
        if self.isAlive:
            if self.isDoneLeft:
                if self.yPos % 7 == 0:
                    tears.append(Tear())

    def movement(self):
        if self.isAlive:
            if self.xPos > self.velocity + 10 and not self.isDoneLeft:
                self.xPos -= self.velocity
                if self.xPos < self.velocity + 10:
                    self.isDoneLeft = True
                    player.canMove = True
            elif self.yPos > self.velocity + 40 and not self.isDoneUp:
                self.yPos -= self.velocity
                if self.yPos <= self.velocity + 40:
                    self.isDoneUp = True
                    self.isDoneDown = False
            elif self.yPos < game.HEIGHT - player.HEIGHT - player.velocity - 195 and not self.isDoneDown:
                self.yPos += self.velocity
                if self.yPos > game.HEIGHT - player.HEIGHT - player.velocity - 195:
                    self.isDoneDown = True
                    self.isDoneUp = False

    def display_health(self):
        if self.isAlive:
            self.healthIndicatorX = self.xPos
            self.healthIndicatorY = self.yPos - 15
            game.window.blit(self.healthIndicator[self.hitCounter],
                             (self.healthIndicatorX + 5, self.healthIndicatorY - 40))


class Tear:
    def __init__(self):
        self.WIDTH = 50
        self.HEIGHT = 40
        self.xPos = 100
        self.yPos = random.randint(boss.yPos + 30, boss.yPos + 150)
        self.velocity = 5
        self.hitBoxRect = pygame.Rect(self.WIDTH, self.HEIGHT, self.xPos, self.yPos)
        self.animation = [pygame.transform.scale(pygame.transform.rotate
                                                 (pygame.image.load('assets/bossAttack/' + str(i) + '.png'), 90),
                                                 (self.WIDTH, self.HEIGHT)) for i in range(5)]
        self.animationCounter = 0

    def display(self):
        if self.animationCounter >= 4:
            self.animationCounter = 0
        game.window.blit(self.animation[self.animationCounter], (self.xPos, self.yPos))
        self.animationCounter += 1
        self.xPos += self.velocity
        self.hitBoxRect = pygame.Rect(self.xPos, self.yPos + 10, self.WIDTH - 10, self.HEIGHT - 20)

    def collision(self):
        if self.hitBoxRect.colliderect(player.hitBoxRect):
            if player.health[2]:
                player.health[2] = False
            elif player.health[1]:
                player.health[1] = False
            elif player.health[0]:
                player.health[0] = False
            tears.remove(self)


class Key:
    def __init__(self):
        self.WIDTH = 40
        self.HEIGHT = 40
        self.isAlive = True
        self.hitBox = (0, 0, self.WIDTH, self.HEIGHT)
        self.texture = pygame.transform.scale(pygame.image.load('assets/level/key/0.png'), (self.WIDTH, self.HEIGHT))

    def display(self, x_pos, y_pos):
        if self.isAlive:
            self.hitBox = pygame.Rect(x_pos, y_pos, self.WIDTH, self.HEIGHT)
            game.window.blit(self.texture, (x_pos, y_pos))


game = Game()  # create a game window
player = Player()  # create a player
secondary = Ogre(600, 100)
primary = Ogre(600, 200)
tertiary = Ogre(600, 300)
ogres = [secondary,
         primary,
         tertiary]
ogres[0].isPrimary, ogres[0].isSecondary, ogres[0].isTertiary = False, True, False
ogres[1].isPrimary, ogres[1].isSecondary, ogres[1].isTertiary = True, False, False
ogres[2].isPrimary, ogres[2].isSecondary, ogres[2].isTertiary = False, False, True
redFlask = Flask()
key = Key()
level = Level()
boss = Boss()
fireballs = []
tears = []
# main loop
while game.running:
    game.clock.tick(game.FRAME_LIMIT)
    if game.room_state == "main":
        game.isMainRoom = True
        game.main_room()
    elif game.room_state == "boss":
        if not game.isBossRoomLoaded:
            player.canMove = False
            player.xPos = 470
            player.yPos = 445
        game.isMainRoom = False
        game.isBossRoom = True
        game.boss_room()
    if game.hasLost and game.reset:
        game = Game()
        player = Player()
        secondary = Ogre(600, 100)
        primary = Ogre(600, 200)
        tertiary = Ogre(600, 300)
        ogres = [secondary,
                 primary,
                 tertiary]
        ogres[0].isPrimary, ogres[0].isSecondary, ogres[0].isTertiary = False, True, False
        ogres[1].isPrimary, ogres[1].isSecondary, ogres[1].isTertiary = True, False, False
        ogres[2].isPrimary, ogres[2].isSecondary, ogres[2].isTertiary = False, False, True
        redFlask = Flask()
        key = Key()
        level = Level()
        boss = Boss()
        fireballs = []
        tears = []
        game.isBossRoom = False
        game.isMainRoom = True
        game.hasLost = False
        game.reset = False
        game.main_room()
