import pygame
import random
import sys
import string

# --- Configurações Gerais ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Cores - Tema Hacker
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
DARK_GREEN = (0, 120, 40)
GRAY = (40, 40, 40)
DARK_GRAY = (20, 20, 20)
RED = (255, 60, 60)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
PURPLE = (150, 0, 255)

# --- Classes do Jogo ---
class Button:
    def __init__(self, rect, text, font, color, hover_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        # Fundo do botão
        pygame.draw.rect(surface, DARK_GRAY, self.rect, border_radius=6)
        pygame.draw.rect(surface, color, self.rect, 2, border_radius=6)
        # Texto
        txt = self.font.render(self.text, True, WHITE)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.hovered and mouse_pressed[0]

class Hero:
    def __init__(self, name, max_hp, attack, color):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.color = color
        self.alive = True
        self.anim_offset = 0
        self.anim_dir = 1

    def draw(self, surface, x, y):
        # Corpo
        pygame.draw.rect(surface, self.color, (x, y + self.anim_offset, 50, 70), border_radius=12)
        # Cabeça
        pygame.draw.circle(surface, self.color, (x+25, y-15 + self.anim_offset), 20)
        # Olhos
        pygame.draw.circle(surface, BLACK, (x+18, y-18 + self.anim_offset), 3)
        pygame.draw.circle(surface, BLACK, (x+32, y-18 + self.anim_offset), 3)
        # Sombra
        pygame.draw.ellipse(surface, DARK_GRAY, (x+5, y+70 + self.anim_offset, 40, 10))

    def animate(self):
        if self.alive:
            self.anim_offset += self.anim_dir
            if abs(self.anim_offset) > 6:
                self.anim_dir *= -1
        else:
            if self.anim_offset < 50:
                self.anim_offset += 3

class Enemy(Hero):
    def draw(self, surface, x, y):
        # Corpo
        pygame.draw.rect(surface, self.color, (x, y + self.anim_offset, 50, 70), border_radius=12)
        # Cabeça
        pygame.draw.circle(surface, self.color, (x+25, y-15 + self.anim_offset), 20)
        # Olhos
        pygame.draw.circle(surface, BLACK, (x+18, y-18 + self.anim_offset), 4)
        pygame.draw.circle(surface, BLACK, (x+32, y-18 + self.anim_offset), 4)
        # Sombra
        pygame.draw.ellipse(surface, DARK_GRAY, (x+5, y+70 + self.anim_offset, 40, 10))
        # Efeito glitch/hacker
        if not self.alive:
            for _ in range(6):
                ox = random.randint(-8, 8)
                oy = random.randint(-8, 8)
                pygame.draw.circle(surface, YELLOW, (x+25+ox, y-15+oy+self.anim_offset), 4, 1)

# --- Funções Auxiliares ---
def draw_bar(surface, x, y, w, h, pct, color, border=BLACK):
    pygame.draw.rect(surface, DARK_GRAY, (x-1, y-1, w+2, h+2), border_radius=4)
    pygame.draw.rect(surface, color, (x, y, int(w*pct), h), border_radius=4)

def draw_hacker_bg(surface):
    font = pygame.font.SysFont('consolas', 18)
    for i in range(0, WIDTH, 28):
        for j in range(0, HEIGHT, 28):
            if random.random() < 0.15:
                char = random.choice('01$#@%&*')
                color = (0, random.randint(150,200), 0)
                txt = font.render(char, True, color)
                surface.blit(txt, (i, j))

def generate_password(difficulty):
    if difficulty == 'Fácil':
        chars = string.ascii_letters + string.digits
        length = 6
    elif difficulty == 'Média':
        chars = string.ascii_letters + string.digits + '!@#$%'
        length = 10
    else:
        chars = string.ascii_letters + string.digits + '!@#$%&*()-_'
        length = 16
    return ''.join(random.choice(chars) for _ in range(length))

# --- Função para copiar senha ---
def copy_to_clipboard(text):
    try:
        import subprocess
        import platform
        if platform.system() == 'Windows':
            cmd = f'echo {text.strip()}| clip'
            subprocess.run(cmd, shell=True, check=True)
        elif platform.system() == 'Darwin':
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
            p.communicate(input=text.encode())
        else:
            p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
            p.communicate(input=text.encode())
    except Exception as e:
        print('Erro ao copiar:', e)

# --- Estados do Jogo ---
MENU, SELECT, BATTLE, WIN, LOSE = 'MENU', 'SELECT', 'BATTLE', 'WIN', 'LOSE'

# --- Função Principal ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Secure Pass RPG - Hacker Edition')
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('consolas', 24)
    small_font = pygame.font.SysFont('consolas', 16)
    big_font = pygame.font.SysFont('consolas', 36, bold=True)
    tiny_font = pygame.font.SysFont('consolas', 12)

    # --- Menu ---
    btn_jogar = Button((WIDTH//2-80, HEIGHT//2-30, 160, 40), 'INICIAR', font, GREEN, (0,200,0))
    btn_sair = Button((WIDTH//2-80, HEIGHT//2+20, 160, 40), 'SAIR', font, RED, (200,80,80))
    btns_menu = [btn_jogar, btn_sair]

    # --- Seleção de Dificuldade ---
    btn_facil = Button((WIDTH//2-180, HEIGHT//2-30, 120, 40), 'Fácil', font, RED, (200,80,80))
    btn_media = Button((WIDTH//2-50, HEIGHT//2-30, 120, 40), 'Média', font, YELLOW, (200,200,0))
    btn_dificil = Button((WIDTH//2+80, HEIGHT//2-30, 120, 40), 'Difícil', font, GREEN, (0,200,0))
    btns_dif = [btn_facil, btn_media, btn_dificil]

    # --- Estados ---
    state = MENU
    difficulty = None
    password = ''
    msg = ''
    turn = 'hero'
    anim_timer = 0
    show_password = False
    credits_offset = 0
    credits_dir = 1

    # --- Personagens ---
    hero = None
    enemies = []
    current_enemy = None
    enemy_idx = 0

    # --- Botão copiar senha ---
    btn_copiar = Button((WIDTH//2-80, HEIGHT-100, 160, 35), 'Copiar senha', small_font, GREEN, (0,180,60))
    senha_copiada = False

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        screen.fill(BLACK)

        # Animar créditos
        credits_offset += credits_dir * 0.3
        if abs(credits_offset) > 8:
            credits_dir *= -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == SELECT and event.type == pygame.MOUSEBUTTONDOWN:
                if btn_facil.rect.collidepoint(event.pos):
                    difficulty = 'Fácil'
                    pygame.time.wait(200)
                elif btn_media.rect.collidepoint(event.pos):
                    difficulty = 'Média'
                    pygame.time.wait(200)
                elif btn_dificil.rect.collidepoint(event.pos):
                    difficulty = 'Difícil'
                    pygame.time.wait(200)
            if state == BATTLE and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and turn == 'hero' and current_enemy and hero and current_enemy.alive and hero.alive:
                    # Ataque do herói
                    current_enemy.hp -= hero.attack
                    if current_enemy.hp <= 0:
                        current_enemy.hp = 0
                        current_enemy.alive = False
                        anim_timer = pygame.time.get_ticks()
                        msg = f'{current_enemy.name} derrotado!'
                    else:
                        turn = 'enemy'
            if state == WIN or state == LOSE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    state = SELECT
                    senha_copiada = False
                    difficulty = None
                    hero = None
                    enemies = []
                    current_enemy = None
                    enemy_idx = 0

        # --- MENU PRINCIPAL ---
        if state == MENU:
            # Título principal
            title = big_font.render('SECURE PASS RPG', True, CYAN)
            screen.blit(title, title.get_rect(center=(WIDTH//2, 100)))
            subtitle = small_font.render('Hacker Edition', True, GREEN)
            screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, 140)))
            
            # Créditos no canto inferior direito
            credits = tiny_font.render('Desenvolvido por Rafael Oliveira', True, GRAY)
            screen.blit(credits, (WIDTH - credits.get_width() - 15, HEIGHT - 30 + credits_offset))
            version = tiny_font.render('v2.0', True, YELLOW)
            screen.blit(version, (WIDTH - version.get_width() - 15, HEIGHT - 15 + credits_offset))
            
            for btn in btns_menu:
                btn.update(mouse_pos)
                btn.draw(screen)
            if btn_jogar.is_clicked(mouse_pos, mouse_pressed):
                state = SELECT
                pygame.time.wait(200)
            if btn_sair.is_clicked(mouse_pos, mouse_pressed):
                running = False

        # --- SELEÇÃO DE DIFICULDADE ---
        elif state == SELECT:
            draw_hacker_bg(screen)
            txt = font.render('Selecione a segurança da senha:', True, WHITE)
            screen.blit(txt, (WIDTH//2-txt.get_width()//2, 100))
            for btn in btns_dif:
                btn.update(mouse_pos)
                btn.draw(screen)
            
            # Se uma dificuldade foi selecionada, inicializar o jogo
            if difficulty:
                # Inicializa personagens
                if difficulty == 'Fácil':
                    hero = Hero('Herói', 100, 15, CYAN)
                    enemies = [Enemy('Trasher', 120, 25, MAGENTA)]
                elif difficulty == 'Média':
                    hero = Hero('Herói', 100, 20, CYAN)
                    enemies = [Enemy('Trasher', 80, 15, MAGENTA), Enemy('Hacker', 150, 30, DARK_GREEN)]
                else:
                    hero = Hero('Herói', 120, 35, CYAN)
                    enemies = [Enemy('Trasher', 80, 20, MAGENTA), Enemy('Hacker', 100, 25, DARK_GREEN)]
                enemy_idx = 0
                current_enemy = enemies[enemy_idx]
                password = generate_password(difficulty)
                msg = ''
                turn = 'hero'
                show_password = True
                senha_copiada = False
                state = BATTLE

        # --- BATALHA ---
        elif state == BATTLE:
            if not hero or not current_enemy:
                pygame.display.flip()
                clock.tick(FPS)
                continue
            # HUD
            pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, 70))
            pygame.draw.line(screen, GREEN, (0, 70), (WIDTH, 70), 2)
            txt = small_font.render(f'Batalha: {hero.name} vs {current_enemy.name}', True, WHITE)
            screen.blit(txt, txt.get_rect(center=(WIDTH//2, 15 + txt.get_height()//2)))
            draw_bar(screen, 20, 45, 180, 15, hero.hp/hero.max_hp, CYAN)
            draw_bar(screen, WIDTH-200, 45, 180, 15, current_enemy.hp/current_enemy.max_hp, current_enemy.color)
            hptxt = small_font.render(f'HP: {hero.hp}/{hero.max_hp}', True, WHITE)
            screen.blit(hptxt, (20, 25))
            hptxt2 = small_font.render(f'HP: {current_enemy.hp}/{current_enemy.max_hp}', True, WHITE)
            screen.blit(hptxt2, (WIDTH-200, 25))
            # Personagens
            hero.draw(screen, 150, 300)
            current_enemy.draw(screen, WIDTH-200, 300)
            hero.animate()
            current_enemy.animate()
            # Mensagem
            if msg:
                m = small_font.render(msg, True, YELLOW)
                screen.blit(m, (WIDTH//2-m.get_width()//2, 150))
            # Senha
            if show_password:
                ptxt = small_font.render(f'Senha: {password}', True, WHITE)
                screen.blit(ptxt, (WIDTH//2-ptxt.get_width()//2, HEIGHT-50))
            # Turno
            ttxt = small_font.render(f'Turno: {"Você" if turn=="hero" else current_enemy.name}', True, WHITE)
            screen.blit(ttxt, (WIDTH//2-ttxt.get_width()//2, 85))
            # Instrução
            if turn == 'hero' and current_enemy.alive and hero.alive:
                inst = small_font.render('Pressione ESPAÇO para atacar!', True, WHITE)
                screen.blit(inst, (WIDTH//2-inst.get_width()//2, HEIGHT-80))
            # Lógica de turnos
            if turn == 'enemy' and current_enemy.alive and hero.alive:
                pygame.time.wait(600)
                hero.hp -= current_enemy.attack
                if hero.hp <= 0:
                    hero.hp = 0
                    hero.alive = False
                    msg = 'Você foi derrotado!'
                    anim_timer = pygame.time.get_ticks()
                turn = 'hero'
            # Troca de inimigo
            if not current_enemy.alive and pygame.time.get_ticks() - anim_timer > 900:
                enemy_idx += 1
                if enemy_idx < len(enemies):
                    current_enemy = enemies[enemy_idx]
                    msg = ''
                    turn = 'hero'
                else:
                    state = WIN
            # Derrota
            if not hero.alive and pygame.time.get_ticks() - anim_timer > 1200:
                state = LOSE

        # --- TELA DE VITÓRIA ---
        elif state == WIN:
            # Fundo escuro
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Card central
            card_rect = pygame.Rect(WIDTH//2-180, HEIGHT//2-120, 360, 240)
            pygame.draw.rect(screen, DARK_GRAY, card_rect, border_radius=12)
            pygame.draw.rect(screen, GREEN, card_rect, 3, border_radius=12)
            
            t = font.render('VITÓRIA!', True, GREEN)
            screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2-90)))
            m = small_font.render('Senha segura! Todos os inimigos derrotados.', True, WHITE)
            screen.blit(m, m.get_rect(center=(WIDTH//2, HEIGHT//2-50)))
            
            # Senha
            ptxt = small_font.render(f'Senha: {password}', True, WHITE)
            screen.blit(ptxt, (WIDTH//2-ptxt.get_width()//2, HEIGHT//2-10))
            
            # Botão copiar
            btn_copiar.update(mouse_pos)
            btn_copiar.draw(screen)
            if btn_copiar.is_clicked(mouse_pos, mouse_pressed) and not senha_copiada:
                copy_to_clipboard(password)
                senha_copiada = True
            if senha_copiada:
                ok = small_font.render('Senha copiada!', True, GREEN)
                screen.blit(ok, (WIDTH//2-ok.get_width()//2, HEIGHT//2+30))
            
            inst = small_font.render('Pressione ENTER para jogar novamente.', True, WHITE)
            screen.blit(inst, inst.get_rect(center=(WIDTH//2, HEIGHT//2+70)))

        # --- TELA DE DERROTA ---
        elif state == LOSE:
            # Fundo escuro
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # Card central
            card_rect = pygame.Rect(WIDTH//2-180, HEIGHT//2-120, 360, 240)
            pygame.draw.rect(screen, DARK_GRAY, card_rect, border_radius=12)
            pygame.draw.rect(screen, RED, card_rect, 3, border_radius=12)
            
            t = font.render('DERROTA!', True, RED)
            screen.blit(t, t.get_rect(center=(WIDTH//2, HEIGHT//2-90)))
            m = small_font.render('Senha comprometida. Tente novamente!', True, WHITE)
            screen.blit(m, m.get_rect(center=(WIDTH//2, HEIGHT//2-50)))
            
            # Senha
            ptxt = small_font.render(f'Senha: {password}', True, WHITE)
            screen.blit(ptxt, (WIDTH//2-ptxt.get_width()//2, HEIGHT//2-10))
            
            # Botão copiar
            btn_copiar.update(mouse_pos)
            btn_copiar.draw(screen)
            if btn_copiar.is_clicked(mouse_pos, mouse_pressed) and not senha_copiada:
                copy_to_clipboard(password)
                senha_copiada = True
            if senha_copiada:
                ok = small_font.render('Senha copiada!', True, GREEN)
                screen.blit(ok, (WIDTH//2-ok.get_width()//2, HEIGHT//2+30))
            
            inst = small_font.render('Pressione ENTER para jogar novamente.', True, WHITE)
            screen.blit(inst, inst.get_rect(center=(WIDTH//2, HEIGHT//2+70)))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 