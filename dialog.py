import pygame


class DialogBox:
    X_POSITION = 590
    Y_POSITION = 940

    def __init__(self):
        self.box = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = ["Bonjour les copains", "ca va ou quoi ?", "J'espère que tu t'amuses bien dans ce monde"]
        self.length_list = len(self.texts)
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('E:/Développement/RPG/0.83/assets/graphics/dialogs/dialog_font.ttf', 20)
        self.reading = False

    def execute(self) :
        if self.reading and self.letter_index >= len(self.texts[self.text_index]) and self.text_index < len(self.texts):
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0


    def render(self, screen):
        if self.reading:
            print("longueur de la liste : ", self.length_list)
            self.letter_index += 1

            if self.letter_index > len(self.texts[self.text_index]):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.execute()

            screen.blit(self.box, (self.X_POSITION , self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0 ,0 ,0))
            screen.blit(text, (self.X_POSITION + 50, self.Y_POSITION + 30))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            self.reading = False
            self.text_index = 0
            self.letter_index = self.letter_index
