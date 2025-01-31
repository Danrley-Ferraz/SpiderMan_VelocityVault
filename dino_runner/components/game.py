import pygame 
import pygame.mixer


from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, MENU, GAMEOVER, SPIDERVERSE
from dino_runner.components.powerups.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.text_utils import draw_message_component
from dino_runner.components.powerups.power_up_manager import PowerUpManager
from dino_runner.components.soundtrack import Music




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.score = 0
        self.death_count = 0 
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.fade_img = pygame.Surface((1100, 600)).convert_alpha()
        self.fade_img.fill("black")
        self.fade_alpha = 255
        pygame.mixer.music.load("dino_runner/assets/Annihilate.mp3")
        self.game_over_music = pygame.mixer.Sound("dino_runner/assets/canonico.mp3")
        self.game_over_sound_played = False
        self.game_over_music.set_volume(0.2)


    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20
        self.score = 0 
        self.fade_alpha = 255
        self.game_over_sound_played = False
        pygame.mixer.music.play(-1) 

        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)
    
    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5 
    
    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()
    
    def draw_background(self):

         image_width = BG.get_width()
         self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
         self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))

         if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
         self.x_pos_bg -= self.game_speed
        # if self.x_pos_bg <= - image_width:
        #     self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        #     self.x_pos_bg = 400
        # self.x_pos_bg -= self.game_speed

    def draw_score(self):
        draw_message_component(
            f"Pontuação: {self.score}",
            self.screen,
            pos_x_center = 1000,
            pos_y_center = 50
        )

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_timing - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(f"{self.player.type.capitalize()} de Invisibilidade disponivel por {time_to_show:.0f}s", 
                    self.screen,
                    font_size = 18,
                    pos_x_center = 500,
                    pos_y_center = 40,
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               self.playing = False
               self.running = False 

            elif event.type == pygame.KEYDOWN:
                self.run()
                Music.play_music(self)

    
    def show_main_menu(self):
        self.screen.blit(MENU, (self.x_pos_bg, self.y_pos_bg))

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_height = SCREEN_HEIGHT // 2 
        half_screen_width = SCREEN_WIDTH // 2 
        if self.death_count == 0:
            self.show_main_menu()
            

      
        else:
            pygame.mixer.music.stop()
            # game_over = GAMEOVER.get_width()
            self.screen.blit(GAMEOVER, (self.x_pos_bg == 500, self.y_pos_bg))

            if not self.game_over_sound_played:
                self.game_over_music.play()
                self.game_over_sound_played = True

            
            self.fade_alpha -= 1
            self.fade_img.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_img, [0, 0])

            draw_message_component(
               f"{self.score}", self.screen, pos_x_center = 1030, pos_y_center = half_screen_height - 212)

            draw_message_component(
                f"{self.death_count} ", self.screen, pos_x_center = 1040, pos_y_center = half_screen_height - 159
            )


        pygame.display.update()
        self.handle_events_on_menu()