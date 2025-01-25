from pygame import *
from random import randint
from time import time as timer

# Ініціалізація шрифтів і текстів
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
font2 = font.Font(None, 36)

# Ініціалізація музики
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire_sound = mixer.Sound('fire.ogg')

# Зображення
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bullet = 'bullet.png'
img_enemy = 'ufo.png'
img_ast = 'asteroid.png'
img_bust = 'upgrade.png'
img_upgrade = 'upgradee.png'
img_fon = 'menu_fonn.jpeg'  # Використовуємо .jpg замість .avif
new_rocket = 'new_rocket.png'



# Початкові значення
score = 0
goal = 20
lost = 0
max_lost = 3
life = 3

# Клас для спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Клас гравця
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.speed_original = player_speed
        self.speed_boosted = player_speed * 2
        self.boost_time = 0
        self.boost_duration = 5
        self.shield = False
        self.shield_time = 0
        self.shield_duration = 5
        self.asteroid_busting_time = 0
        self.asteroid_busting_duration = 10
        self.asteroid_busting_enabled = False
        self.hit_counter = 0  # Лічильник зіткнень


    def update(self):
        if self.shield and timer() - self.shield_time >= self.shield_duration:
            self.shield = False  # Вимикаємо щит після закінчення часу

        if self.boost_time > 0 and timer() - self.boost_time >= self.boost_duration:
            self.speed = self.speed_original
            self.boost_time = 0

        if self.asteroid_busting_time > 0 and timer() - self.asteroid_busting_time >= self.asteroid_busting_duration:
            self.asteroid_busting_enabled = False
            self.asteroid_busting_time = 0

        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

    def activate_boost(self):
        self.speed = self.speed_boosted
        self.boost_time = timer()

    def activate_asteroid_busting(self):
        if not self.asteroid_busting_enabled:
            self.asteroid_busting_time = timer()
            self.asteroid_busting_enabled = True

    def activate_shield(self):
        self.shield = True
        self.shield_time = timer()

    def add_asteroid_busting_upgrade(self):
        self.asteroid_busting_enabled = True
        self.asteroid_busting_time = timer()

# Клас ворогів
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

    
class upgrrade(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

# Клас кулі
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



# Клас для просунутих ворогів
class AdvancedEnemy(Enemy):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.direction = 1

    def update(self):
        if self.direction == 1:
            self.rect.x += self.speed
            if self.rect.x > win_width - self.rect.width:
                self.direction = -1
        else:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.direction = 1
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

# Ініціалізація вікна
win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Створення гравця
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

# Створення груп ворогів
monsters = sprite.Group()
for i in range(1, 4):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
    monsters.add(monster)

advanced_enemies = sprite.Group()
for i in range(1, 3):
    advanced_enemy = AdvancedEnemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
    advanced_enemies.add(advanced_enemy)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 70, 50, randint(1, 7))
    asteroids.add(asteroid)

upgrades = sprite.Group()
for i in range(1, 3):
    upgrade = Enemy(img_bust, randint(30, win_width - 30), -40, 70, 50, randint(1, 5))
    upgrades.add(upgrade)

upgrades2 = sprite.Group()
for i in range(1, 3):
    upgrade2 = Enemy(img_upgrade, randint(30, win_width - 30), -40, 70, 50, randint(1, 5))
    upgrades2.add(upgrade2)

bullets = sprite.Group()

# Створення меню
def show_menu():
    menu_font = font.Font(None, 100)
    play_text = menu_font.render('Play', True, (255, 255, 255))
    skins_text = menu_font.render('Skins', True, (255, 255, 255))  # Додано текст для кнопки скіни
    play_rect = play_text.get_rect(center=(win_width // 2, win_height // 2))
    skins_rect = skins_text.get_rect(center=(win_width // 2, win_height // 2 + 100))  # Позиція кнопки скіни

    # Завантаження фону меню
    menu_background = transform.scale(image.load(img_fon), (win_width, win_height))

    # Малюємо фон і кнопки
    window.blit(menu_background, (0, 0))
    window.blit(play_text, play_rect)
    window.blit(skins_text, skins_rect)  # Малюємо кнопку скіни
    display.update()

    waiting_for_input = True
    while waiting_for_input:
        for e in event.get():
            if e.type == QUIT:
                return False
            elif e.type == MOUSEBUTTONDOWN:
                if play_rect.collidepoint(e.pos):
                    return "play"  # Повертаємо "play" якщо натиснута кнопка Play
                elif skins_rect.collidepoint(e.pos):
                    return "skins"  # Повертаємо "skins" якщо натиснута кнопка Skins
    return False


def show_skin_menu():
    menu_font = font.Font(None, 80)
    default_skin_text = menu_font.render('Default Skin', True, (255, 255, 255))
    new_skin_text = menu_font.render('New Skin', True, (255, 255, 255))  # Текст для новго скіна
    back_text = menu_font.render('Back', True, (255, 255, 255))  # Кнопка "Назад"

    default_skin_rect = default_skin_text.get_rect(center=(win_width // 2, win_height // 2 - 50))
    new_skin_rect = new_skin_text.get_rect(center=(win_width // 2, win_height // 2 + 50))
    back_rect = back_text.get_rect(center=(win_width // 2, win_height // 2 + 150))

    window.fill((0, 0, 0))  # Заповнюємо екран чорним кольором
    window.blit(default_skin_text, default_skin_rect)
    window.blit(new_skin_text, new_skin_rect)
    window.blit(back_text, back_rect)
    display.update()

    waiting_for_input = True
    while waiting_for_input:
        for e in event.get():
            if e.type == QUIT:
                return False
            elif e.type == MOUSEBUTTONDOWN:
                if default_skin_rect.collidepoint(e.pos):
                    ship.image = transform.scale(image.load('rocket.png'), (80, 100))  # Вибір стандартного скіна
                    return "play"
                elif new_skin_rect.collidepoint(e.pos):
                    ship.image = transform.scale(image.load('new_rocket.png'), (80, 100))  # Вибір нового скіна
                    return "play"
                elif back_rect.collidepoint(e.pos):
                    return "back"
    return False

# Основний цикл гри
finish = False
run = True
rel_time = False
num_fire = 0

# Показуємо меню перед початком гри
if not show_menu():
    run = False


menu_result = show_menu()
if menu_result == "skins":
    menu_result = show_skin_menu()

if menu_result == "play":
    while run:
        # Основна логіка гри
        ...

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and not rel_time:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and not rel_time:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0, 0))

        ship.update()
        monsters.update()
        advanced_enemies.update()
        bullets.update()
        asteroids.update()
        upgrades.update()
        upgrades2.update()

        ship.reset()
        monsters.draw(window)
        advanced_enemies.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        upgrades.draw(window)
        upgrades2.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        # Перевірка на зіткнення з монстрами
        collisions = sprite.groupcollide(monsters, bullets, True, True)
        for c in collisions:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if lost >= 20:
            finish = True
            window.blit()

        # Перевірка на зіткнення гравця з ворогами
        collisions_with_monsters = sprite.spritecollide(ship, monsters, True)
        for monster in collisions_with_monsters:
            if not ship.shield:  # Якщо щит не активний
                life -= 1
            if life == 0 or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))

        # Перевірка на зіткнення з астероїдами
        collisions_with_asteroids = sprite.spritecollide(ship, asteroids, True)
        for asteroid in collisions_with_asteroids:
            life -= 1
            asteroid = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
            asteroids.add(asteroid)
            if life == 0 or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))

        # Перевірка на зіткнення з UFO
        collisions_advanced = sprite.groupcollide(advanced_enemies, bullets, True, True)
        for c in collisions_advanced:
            score += 2
            advanced_enemy = AdvancedEnemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
            advanced_enemies.add(advanced_enemy)

        # Перевірка на зіткнення гравця з ворогами
        collisions_with_advanced = sprite.spritecollide(ship, advanced_enemies, False)
        for advanced_enemy in collisions_with_advanced:
            life -= 1
            advanced_enemy.rect.x = randint(80, win_width - 80)  # Випадкове нове положення
            advanced_enemy.rect.y = -40  # Повертаємо наверх



            if life == 0 or lost >= max_lost:
                finish = True
                window.blit(lose, (200, 200))

        # Перевірка на зіткнення з апгрейдами
        if sprite.spritecollide(ship, upgrades, True):
            ship.activate_boost()

        if sprite.spritecollide(ship, upgrades2, True):
            ship.add_asteroid_busting_upgrade()

        # Перевірка на можливість ламати астероїди
        if ship.asteroid_busting_enabled:
            collisions = sprite.groupcollide(asteroids, bullets, True, True)
            for c in collisions:
                score += 1

        # Перевірка на досягнення цілі
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font2.render("Рахунок:" + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # Виведення активних бустів і залишковий час
        boosts_text = ""
        if ship.boost_time > 0 and timer() - ship.boost_time < ship.boost_duration:
            remaining_boost_time = ship.boost_duration - (timer() - ship.boost_time)
            boosts_text += f"Speed boost {int(remaining_boost_time)}s left\n"
        
        if ship.shield and timer() - ship.shield_time < ship.shield_duration:
            remaining_shield_time = ship.shield_duration - (timer() - ship.shield_time)
            boosts_text += f"Shield: {int(remaining_shield_time)}s left\n"

        if ship.asteroid_busting_enabled and ship.asteroid_busting_time > 0 and timer() - ship.asteroid_busting_time < ship.asteroid_busting_duration:
            remaining_asteroid_busting_time = ship.asteroid_busting_duration - (timer() - ship.asteroid_busting_time)
            boosts_text += f"Destroy boost: {int(remaining_asteroid_busting_time)}s left\n"

        boosts_display = font2.render(boosts_text, 1, (255, 255, 255))
        window.blit(boosts_display, (10, 80))

        life_color = (0, 150, 0) if life == 3 else (150, 150, 0) if life == 2 else (150, 0, 0)
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for ae in advanced_enemies:
            ae.kill()
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        for u in upgrades:
            u.kill()
        for t in upgrades2:
            t.kill()

        time.delay(3000)
        for i in range(1, 4):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(2, 5))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 70, 50, randint(1, 7))
            asteroids.add(asteroid)
        for i in range(1, 3):
            upgrade = Enemy(img_bust, randint(30, win_width - 30), -40, 70, 50, randint(2, 4))
            upgrades.add(upgrade)
        for i in range(1, 3):
            upgrade2 = Enemy(img_upgrade, randint(30, win_width - 30), -40, 70, 50, randint(2, 4))
            upgrades2.add(upgrade2)

    time.delay(50)