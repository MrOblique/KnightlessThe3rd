import pygame

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

viewSights = True # view a line between player and enemies

def hCollisionHandler(player, enemies, projectiles):
    # we initialise hitboxes and hurtboxes to empty lists since we are updating them
    # and may be created or destroyed at any frame

    hitboxes = []
    hurtboxes = []

    # HITBOXES
    # player hitbox
    if player.hitbox_active:
        hitboxes.append(("player", player, player.hitbox))
    # enemy hitboxes
    for enemy in enemies:
        if enemy.hitbox_active:
            hitboxes.append(("enemy", enemy, enemy.hitbox))
    # projectiles
    for proj in projectiles:
        if proj.hitbox_active:
            hitboxes.append(("projectile", proj, proj.rect))

    # HURTBOXES
    # player hurtbox
    hurtboxes.append(("player", player, player.rect))
    # enemy hurtbox
    for enemy in enemies:
        # making sure enemy is alive
        if enemy.state != "Dead":
            hurtboxes.append(("enemy", enemy, enemy.rect))
    # HITBOXES
    # player hitbox
    hitboxes.append(("player", player, player.hitbox))
    # enemy hitbox
    for enemy in enemies:
        if enemy.state != "Dead":
            if enemy.hitbox_active:
                hitboxes.append(("enemy", enemy, enemy.hitbox))
    #  COLLISION HANDLER
    for hitbox in hitboxes:
        for hurtbox in hurtboxes:
            if hitbox[2] and hurtbox[2]:
                if hitbox[2].colliderect(hurtbox[2]):
                    if hitbox[0] != hurtbox[0]:
                        print(hitbox[0])
                        print(hurtbox[0])
                        hurtbox[1].state = "Hurt"
                        hurtbox[1].hurt_cd = 100
                        pass

class Entity(pygame.sprite.Sprite):
    def __init__(self, name, x, y, width, height, x_velocity, y_velocity, x_acceleration, y_acceleration, max_x_velocity, colour, sprites, animation_number, class_name):
        # call super constructor
        pygame.sprite.Sprite.__init__(self, all_sprites)
        self.sprites = sprites
        self.animation_number = animation_number  # idle animation
        self.frame_number = 0  # starting frame of animation
        self.image = self.sprites[self.animation_number][self.frame_number%len(self.sprites[self.animation_number])]
        self.name = name # name of object
        self.class_name = class_name # subclass of object
        self.x = x # x-position
        self.y = y # y-position
        self.rect = pygame.Rect(self.x-(width/2), self.y-(height/2), width, height) # object rect
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.x_acceleration = x_acceleration
        self.y_acceleration = y_acceleration
        self.max_x_velocity = max_x_velocity
        self.grounded = False # is object touching ground
        self.isAttacking = False # is the object attacking
        self.attack_cd = 0  # attack cooldown
        self.hurt_cd = 0  # hurt duration stun
        self.state = "Patrol"  # dictate the action the entity will do
        self.hitbox = None
        self.hitbox_active = False
        self.direction = 1
        self.is_jumping = True
        self.shot = False
        self.state_change = False

        self.image_offset = (0, 0)
    def draw(self, screen):
        screen.blit(self.image,(self.rect.x + self.image_offset[0], self.rect.y + self.image_offset[1]))
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        pygame.draw.circle(screen, (0, 255, 0), self.rect.center, 5)
        if self.hitbox_active:
            print("Drawing hitboxxxxx")
            pygame.draw.rect(screen, (0, 0, 255), self.hitbox, 2)
    def updateAnimation(self):
        if self.class_name == "Knight":
            # (0,Attack1), (1,Attack2), (2,Attack3), (3,Dead), (4,Hurt), (5,Idle), (6,Jump), (7,Run), (8,Walk)
            # if not attacking, there should be no hitboxes active
            if not self.state == "Attack":
                self.hitbox_active = False
            # set animation to appropiate animation number relative to state
            if self.state == "Dead":
                self.animation_number = 3
            elif self.state == "Hurt":
                self.animation_number = 4
                self.frame_number = 0
            # cycles between different attack cycles
            # if not in attack animation and is attacking, switch to attack animation
            elif self.state == "Attack":
                print("Play attack")
                if self.animation_number == 0 and int(self.frame_number) == 5:
                    self.animation_number = 1
                    self.frame_number = 0
                    self.isAttacking = False
                elif self.animation_number == 1 and int(self.frame_number) == 4:
                    self.animation_number = 2
                    self.frame_number = 0
                    self.isAttacking = False
                elif self.animation_number == 2 and int(self.frame_number) == 4:
                    self.animation_number = 0
                    self.frame_number = 0
                    self.isAttacking = False
                elif not (self.animation_number == 0 or self.animation_number == 1 or self.animation_number == 2):
                    self.animation_number = 0
                    self.frame_number = 0
            elif self.state == "Jump":
                self.animation_number = 6
            elif self.state == "Run":
                self.animation_number = 7
            elif self.state == "Walk":
                self.animation_number = 8
            elif self.state == "Idle":
                self.animation_number = 5
        if self.class_name == "GangsterMelee":
            # (0,Attack1), (1,Dead), (2,Hurt), (3,Idle), (4,Run), (5,Walk)
            # if not attacking, there should be no hitboxes active
            if not self.state == "Attack":
                self.hitbox_active = False
            if self.state == "Dead":
                self.animation_number = 1
            elif self.state == "Hurt":
                self.animation_number = 2
            elif self.state == "Attack":
                self.animation_number = 0
            elif self.state == "Chase":
                self.animation_number = 4
            elif self.state == "Patrol":
                self.animation_number = 5
            elif self.state == "Idle":
                self.animation_number = 3
        if self.class_name == "GangsterRanged":
            # (0,Dead), (1,Hurt), (2,Idle), (3,Run), (4,Shoot), (5,Walk)
            # if not shooting
            if not self.state == "Shoot":
                self.shot = False
            if self.state == "Dead":
                self.animation_number = 0
            elif self.state == "Hurt":
                self.animation_number = 1
            elif self.state == "Shoot":
                self.animation_number = 4
                # once animation has looped
                if int(self.frame_number) >= 5:
                    self.frame_number = 0
                    self.shot = False
            elif self.state == "Chase":
                self.animation_number = 3
            elif self.state == "Patrol":
                self.animation_number = 5
            elif self.state == "Idle":
                self.animation_number = 2

    def update(self, key_pressed, mouse_pressed, tiles, player, screen, dt):
        # initialise state_change for current frame
        self.state_change = self.state
        dt *= 0.1
        # detect player controls and stops when runs out of lives
        if self.name == "Player":
            if self.lives > 0:
                self.control(key_pressed, mouse_pressed)
            else:
                self.state = "Dead"
                self.x_velocity = 0
                return "Dead"
        elif self.name == "Enemy":
            # if enemy dead, then can't move
            if self.hp > 0:
                # does enemy validation
                self.validate(tiles, player, screen, dt)
            else:
                self.state = "Dead"
                self.x_velocity = 0
        # decrement attack cd each pass
        #if self.attack_cd > 0:
        #    self.attack_cd -= 1

        self.x += self.x_velocity * dt * 2
        self.rect.centerx = self.x
        # we check collisions after movement
        # for now we check x, then check y later
        for tile in tiles:
            # if entity is within a tile's rect
            # update self.x otherwise don't
            if self.rect.colliderect(tile):
                if self.name == "Projectile":
                    self.kill()
                    self.hitbox_active = False
                # if enemy and patrolling, switch directions when hitting wall
                if self.name == "Enemy" and self.state == "Patrol":
                    self.direction *= -1
                # player moves right so must be colliding to left of tile
                if self.x_velocity > 0:
                    self.rect.right = tile.left
                # and vice versa
                elif self.x_velocity < 0:
                    self.rect.left = tile.right
                # after adjusting to collision, set x-velocity and acceleration to 0
                # and reposition the position of the rect
                self.x = self.rect.centerx
                self.x_velocity = 0
                self.x_acceleration = 0
        # we update velocity after since it could flip to 0 due to acceleration
        self.x_velocity += self.x_acceleration * dt
        if self.class_name == "Knight":
            print(self.max_x_velocity)
        if self.x_velocity > self.max_x_velocity:
            self.x_velocity = self.max_x_velocity
        if self.x_velocity < self.max_x_velocity * -1:
            self.x_velocity = self.max_x_velocity * -1
        if 0.2 > self.x_velocity > -0.2:
            self.x_acceleration = 0
            self.x_velocity = 0
        # Remove effects of gravity to projectile
        if self.name == "Projectile":
            # if projectile is alive, decrease lifespan
            if self.lifespan > 0:
                self.lifespan -= 1 * dt * 0.02
            # kill projectile if dead
            if self.lifespan <= 0:
                self.kill()
                self.hitbox_active = False
            self.y_velocity = 0
            self.y_acceleration = 0

        self.y += self.y_velocity * dt * 10
        self.rect.centery = self.y
        self.grounded = False
        # we check collisions after movement
        for tile in tiles:
            # if entity is within a tile's rect
            # update self.y otherwise don't
            if self.rect.colliderect(tile):
                # player moves down so must be colliding with top of tile
                if self.y_velocity > 0:
                    self.rect.bottom = tile.top
                    # touching ground since player is above
                    self.grounded = True
                # and vice versa
                elif self.y_velocity < 0:
                    self.rect.top = tile.bottom
                # after adjusting to collision, set y-velocity to 0
                # and reposition the position of the rect
                self.y = self.rect.centery
                self.y_velocity = 0
        self.y_velocity += self.y_acceleration * dt * 15
        if not self.grounded:
            self.y_acceleration = 0.002
        else:
            self.y_acceleration = 0
        # if state has changed, we will set the current frame to 0
        if self.state_change != self.state:
            self.frame_number = 0
        self.updateAnimation()
        self.image = self.sprites[self.animation_number][
            int(self.frame_number) % len(self.sprites[self.animation_number])]
        # if moving left, reflect the sprite
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = -1
            # offsetting certain sprites
            if self.class_name == "Knight":
                if self.animation_number == 0:
                    self.image_offset = (128 - self.image.get_width(), -128)
                else:
                    self.image_offset = (128 - 32 - self.image.get_width(), -128)
        else:
            # offsetting certain sprites
            if self.class_name == "Knight":
                if self.animation_number == 0:
                    self.image_offset = (-64, -128)
                else:
                    self.image_offset = (-32, -128)
        self.frame_number += 0.05 * dt
        print(f"State of {self.class_name} : {self.state}")
    def getProperties(self):
        return self.x, self.y, self.rect.width, self.rect.height

class Character(Entity):
    def __init__(self, lives, souls, base_dmg, base_speed, base_attack_speed, sprites, animation_number, class_name):
        self.lives = lives # no. of player lives
        self.souls = souls # no. of player souls
        self.base_dmg = base_dmg # player's base atk dmg
        self.base_speed = base_speed # player's base movement speed
        self.base_attack_speed = base_attack_speed # player's base attack speed
        Entity.__init__(self, "Player", 700, 550, 64, 128, 0, 0,
                        0, 0, 1,(0, 255, 0), sprites, animation_number, class_name)
        self.image_offset = (-32, -128)
    def control(self, key_pressed, mouse_pressed):
        self.max_x_velocity = 1
        # if hurt, take dmg for 1 intance, stop moving and reduc stun every update
        if self.hurt_cd > 0 and self.state == "hurt":
            self.hurt_cd -= 1
        if self.grounded and not self.isAttacking:
            self.state = "Idle"
        if key_pressed[pygame.K_d]: # moving right
            self.x_velocity = self.base_speed
            self.x_acceleration = -1
            self.direction = 1
            if self.grounded:
                self.state = "Walk"
        if key_pressed[pygame.K_a]: # moving left
            self.x_velocity = -self.base_speed
            self.x_acceleration = 1
            self.direction = -1
            if self.grounded and not self.isAttacking:
                self.state = "Walk"
        if key_pressed[pygame.K_LSHIFT]: # sprinting
            self.max_x_velocity *= 2
            self.x_velocity *= 2
            print(f"x velocity ================================== {self.x_velocity}")
            if self.grounded and not self.isAttacking:
                self.state = "Run"
        if key_pressed[pygame.K_SPACE] and self.grounded: # jumping
            self.y_velocity = -1
            self.grounded = False
            if not self.isAttacking:
                self.state = "Jump"
        if mouse_pressed[0] == 1 or self.isAttacking: # attacking
            print("attacking")
            self.state = "Attack"
            # attack hitbox
            # hitbox will only be active for certain frames
            if self.animation_number == 0:
                if int(self.frame_number) == 4:
                    if self.direction == 1:
                        self.hitbox = pygame.Rect(self.rect.right, self.rect.y, self.rect.width, self.rect.height)
                    else:
                        self.hitbox = pygame.Rect(self.rect.left-self.rect.width, self.rect.y, self.rect.width, self.rect.height)
                    self.hitbox_active = True
                else:
                    self.hitbox_active = False
            elif self.animation_number == 1:
                if 2 <= int(self.frame_number) <= 3:
                    if self.direction == 1:
                        self.hitbox = pygame.Rect(self.rect.right, self.rect.y, self.rect.width, self.rect.height)
                    else:
                        self.hitbox = pygame.Rect(self.rect.left - self.rect.width, self.rect.y, self.rect.width,
                                                  self.rect.height)
                    self.hitbox_active = True
                else:
                    self.hitbox_active = False
            elif self.animation_number == 2:
                if 2 <= int(self.frame_number) <= 3:
                    if self.direction == 1:
                        self.hitbox = pygame.Rect(self.rect.right, self.rect.y, self.rect.width, self.rect.height)
                    else:
                        self.hitbox = pygame.Rect(self.rect.left - self.rect.width, self.rect.y, self.rect.width,
                                                  self.rect.height)
                    self.hitbox_active = True
                else:
                    self.hitbox_active = False
            else:
                self.hitbox_active = False
            self.isAttacking = True

        if key_pressed[pygame.K_y]:
            self.lives = 0
class Knight(Character):
    def __init__(self, sprites):
        Character.__init__(self, 3, 0, 10, 1, 1, sprites, 5, "Knight")

class Enemy(Entity):
    def __init__(self, x, y, hp, base_dmg, base_speed, base_attack_speed, sprites, animation_number, class_name):
        pygame.sprite.Sprite.__init__(self, all_sprites, enemies)
        self.hp = hp # enemy's hp
        self.base_dmg = base_dmg  # enemy's base atk dmg
        self.base_speed = base_speed  # enemy's base movement speed
        self.base_attack_speed = base_attack_speed  # enemy's base attack speed
        Entity.__init__(self, "Enemy", x, y, 64, 128, 0, 0,
                        0, 0, 5,(255, 0, 0), sprites, animation_number, class_name)
        self.image_offset = (-32, -128)

    # returns true if tile present ahead
    # otherwise, return false
    def checkEdge(self, tiles):
        # this rect is almost like a "white cane" for the enemy
        # it checks a tiles length into enemy's direction
        next_rect = pygame.Rect(int(self.rect.centerx + self.direction * (self.rect.width//2 + 40)),
                     int(self.rect.bottom + 2), 2,2)
        for tile in tiles:
            if next_rect.colliderect(tile):
                return False
        return True
    def attack(self, class_name):
        if class_name == "GangsterMelee":
            print("Melee Attacking")
            # attack animation hitbox creation
            if self.animation_number == 0:
                if 3 <= int(self.frame_number) % 6 <= 4:
                    if self.direction == 1:
                        self.hitbox = pygame.Rect(self.rect.right, self.rect.y, self.rect.width, self.rect.height)
                    else:
                        self.hitbox = pygame.Rect(self.rect.left - self.rect.width, self.rect.y, self.rect.width,
                                                  self.rect.height)
                    self.hitbox_active = True
                else:
                    self.hitbox_active = False
            else:
                self.hitbox_active = False
        elif class_name == "GangsterRanged":
            print("Ranged Attacking")
            # attack animation hitbox creation
            if self.animation_number == 4:
                print(int(self.frame_number))
                if int(self.frame_number) == 1:
                    # Creates an anonymous bullet
                    if not self.shot:
                        if self.direction == 1:
                            Bullet(self.rect.right, self.rect.centery, self.direction)
                        else:
                            Bullet(self.rect.left, self.rect.centery, self.direction)
                        self.shot = True
    def chase(self, player, move, dt):
        # direction enemy faces before chasing the enemy
        # if player is on the right of enemy
        # direction used to determine where enemy will face
        if player.rect.centerx > self.rect.centerx:
            # face to the right
            self.direction = 1
        else:
            # else face to the left
            self.direction = -1
        self.x_velocity = self.base_speed * self.direction * move * dt * 20
        print("E Chase")
    def patrol(self, tiles, dt):
        # if edge change directions
        if self.checkEdge(tiles):
            self.direction *= -1
        self.x_velocity = self.base_speed * self.direction * dt * 20
        print("E Patrolling")
    def validate(self, tiles, player, screen, dt):
        p = player.rect
        e = self.rect
        clipped_line = True
        for tile in tiles:
            if tile.clipline(e.center, p.center):  # detects if enemy can see player
                clipped_line = False
        if viewSights:
            pygame.draw.line(screen, (255, 255, 255), e.center, p.center)
        # if hurt, take dmg for 1 intance, stop moving and reduc stun every update
        if self.hurt_cd > 0 and self.state == "Hurt":
            self.state = "Hurt"
            self.hurt_cd -= 1
            return
        # distance between player and enemy
        # if y distance is beteen 50 to -150 from the player
        # if x distance less than 200, chase player
        elif clipped_line:
            if -200 < p.centery - e.centery < 50:
                if abs(p.centerx - e.centerx) < 700:
                    print("In range")
                    # enemy moves
                    move = 1
                    if self.class_name == "GangsterMelee":
                        if abs(p.centerx - e.centerx) < 100 and abs(p.centery - e.centery) < p.height / 2:
                            print("Too close")
                            # enemy stops moving
                            # enemy attacks
                            move = 0
                            self.chase(player, move, dt)
                            self.attack(self.class_name)
                            self.state = "Attack"
                        else:
                            self.state = "Chase"
                            self.chase(player,move,dt)
                    elif self.class_name == "GangsterRanged":
                        if abs(p.centerx - e.centerx) < 300 and abs(p.centery - e.centery) < p.height / 2:
                            print("Too close")
                            # enemy stops moving
                            # enemy attacks
                            move = 0
                            self.chase(player,move,dt)
                            self.attack(self.class_name)
                            self.state = "Shoot"
                        else:
                            self.state = "Chase"
                            self.chase(player, move, dt)
                else:
                    self.state = "Patrol"
            else:
                self.state = "Patrol"
        elif not clipped_line:
            self.state = "Patrol"
        if self.state == "Idle":
            print("Idling")
            self.x_velocity = 0
            return
        if self.state == "Patrol":
            # patrol state
            self.patrol(tiles, dt)
            return
class Gangster(Enemy):
    def __init__(self, hp, base_dmg, base_speed, base_attack_speed, sprites, animation_number, class_name):
        Enemy.__init__(self, hp, base_dmg, base_speed, base_attack_speed, sprites, animation_number, class_name)

class GangsterMelee(Enemy):
    def __init__(self, sprites):
        Enemy.__init__(self, 1000, 300, 10, 1, 0.1, 1, sprites, 5, "GangsterMelee")
        self.image_offset = (-100, -128)

class GangsterRanged(Enemy):
    def __init__(self, sprites):
        Enemy.__init__(self, 100, 300, 10, 1, 0.1, 1, sprites, 5, "GangsterRanged")
        self.image_offset = (-100, -128)

class Projectile(Entity):
    def __init__(self, x, y, direction, lifespan, sprites, animation_number, class_name):
        pygame.sprite.Sprite.__init__(self, all_sprites, projectiles)
        self.lifespan = lifespan
        self.hitbox_active = True
        Entity.__init__(self, "Projectile", x, y, 25, 5, 1 * direction, 0, 0,
                        0, 1, (255,255,255), sprites, animation_number, class_name)
        self.image_offset = (0, 0)

class Bullet(Projectile):
    def __init__(self, x, y, direction):
        image = pygame.Surface((25, 5))
        image.fill((255,255,255))
        sprites = [[image]]
        Projectile.__init__(self, x, y, direction, 5 , sprites, 0,"Bullet")

