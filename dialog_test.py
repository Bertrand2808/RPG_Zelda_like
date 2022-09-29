import pygame

class DialogBoxTest:
    X_POSITION = 590
    Y_POSITION = 940

    def __init__(self):
        self.box = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        # self.texts = [f"Tu utilises l'objet {self.item_names[self.selection_index]}"]
        self.text = ["Bonjour les copains", "ca va ou quoi ?", "J'espère que tu t'amuses bien dans ce monde"]
        self.length_list = len(self.text)
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font('E:/Développement/RPG/0.83/assets/graphics/dialogs/dialog_font.ttf', 20)
        self.reading = False

        self.printed = False

    def execute(self) :
        while self.printed == False:
            print("début execute")
            print("début execute : longueur de la liste : ", self.length_list)
            print("début execute : text_index : ", self.text_index)
            print(" début execute : le dialogue est : ", self.text[self.text_index])
            print("début execute : letter_index : ", self.letter_index)
            print("self.reading : ", self.reading)
            self.printed = True

        if self.reading and self.letter_index >= len(self.text[self.text_index]) and self.text_index < len(self.text):
            self.next_text()
            print("go next_text")
        else:
            print("esle execute")
            self.reading = True
            self.text_index = 0
            self.printed = False
            while self.printed == False:
                print("fin execute : longueur de la liste : ", self.length_list)
                print("fin execute : text_index : ", self.text_index)
                print("fin execute : le dialogue est : ", self.text[self.text_index])
                print("def render : la taille est : ", len(self.text[self.text_index]))
                print("fin execute : letter_index : ", self.letter_index)
                print("self.reading : ", self.reading)
                self.printed = True


    def render(self, screen):
        if self.reading:
            self.printed = False
            while self.printed == False:
                print("def render : longueur de la liste : ", self.length_list)
                print("def render : text_index : ", self.text_index)
                print("def render : le dialogue est : ", self.text[self.text_index])
                print("def render : la taille est : ", len(self.text[self.text_index]))
                print("def render : letter_index : ", self.letter_index)
                print("self.reading : ", self.reading)
                self.printed = True

            self.letter_index += 1

            if self.letter_index > len(self.text[self.text_index]):
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            self.execute()

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.text[self.text_index][0:self.letter_index], False, (0 ,0 ,0))
            screen.blit(text, (self.X_POSITION + 50, self.Y_POSITION + 30))

    def next_text(self):
        print("début next_text")
        self.printed = False
        while self.printed == False:
            print("début next_text : longueur de la liste : ", self.length_list)
            print("début next_text : self.text_index : ", self.text_index)
            print("self.reading : ", self.reading)
            self.printed = True

        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.text):
            self.reading = False
            self.text_index = 0
            self.letter_index = self.letter_index

            self.printed = False
            while self.printed == False:
                print("fin next_text : longueur de la liste : ", self.length_list)
                print("fin next_text : self.text_index : ", self.text_index)
                print("self.reading : ", self.reading)
                self.printed = True




