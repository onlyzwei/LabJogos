import pygame

screen_width, screen_height = 1000, 1000


class Menu:
    def __init__(self, options):
        self.options = options
        self.font = pygame.font.SysFont('Futura', 40)
        self.selected_option = 0

    def draw(self, screen):
        for i in range(len(self.options)):
            option = self.options[i]
            text = self.font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 50))
            screen.blit(text, text_rect)

            if i == self.selected_option:
                pygame.draw.rect(screen, (255, 0, 0), text_rect, 2)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]

        return None


def show_menu(screen):
    menu_options = ["Start Game", "Quit"]
    menu = Menu(menu_options)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            selected_option = menu.handle_event(event)
            if selected_option:
                return selected_option

        screen.fill((0, 0, 0))
        menu.draw(screen)
        pygame.display.update()


