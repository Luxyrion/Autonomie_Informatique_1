from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.core.window import Window

class MorpionGame(Widget):

    def __init__(self, **kwargs):
        super(MorpionGame, self).__init__()

        Window.size = (1000, 500)
        self.size = Window.size
        self.grid()
        self.marker()


    def grid(self):
        with self.canvas:
            # Création de la grille
            Color(0.5, 0.5, 0.5)

            #Lignes verticales
            self.v1 = Rectangle(pos=((self.width - 400) / 3 + 200, 0), size=(4, self.height * (3 / 4)))
            self.v2 = Rectangle(pos=((self.width - 400) * (2 / 3) + 200, 0), size=(4, self.height * (3 / 4)))

            #Lignes horizontales
            self.h1 = Rectangle(pos=(200, self.height * (3 / 4)), size=((self.width - 400), 10))
            self.h2 = Rectangle(pos=(200, self.height / 2), size=((self.width - 400), 4))
            self.h3 = Rectangle(pos=(200, self.height / 4), size=((self.width - 400), 4))
            self.h4 = Rectangle(pos=(200, self.top - self.height / 4), size=((self.width - 400), 10))

            #Ligne rouge à gauche de la grille + Player 1 Label
            Color(1, 0, 0)
            self.red = Rectangle(pos=(195, 0), size=(10, self.height))
            self.player1 = Label(font_size=30, center_x=100, top=self.top - 50, text='[color=FF0000]Player 1[/color]',
                                 markup=True)

            #Ligne bleue à droite de la grille + Player 2 Label
            Color(0, 0, 1)
            self.blue = Rectangle(pos=((self.width - 200) - 5, 0), size=(10, self.height))
            self.player2 = Label(font_size=30, center_x=self.width - 100, top=self.top - 50, text='[color=0000FF]Player 2[/color]', markup=True)


    turn = 1
    matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    Color(1, 0, 0)

    def marker(self):
        color = (self.turn % 2, 0, (self.turn + 1) % 2)

        # On indique le tour du Player 1
        if self.turn % 2 == 1:
            with self.canvas:
                Color(*color)
                p1pawn = Ellipse(pos=(100, self.height / 2), size=(10, 10))
                Color(0, 0, 0)
                p2pawn = Ellipse(pos=(self.width - 100, self.height / 2), size=(10, 10))

        # On indique le tour du Player 2
        if self.turn % 2 == 0:
            with self.canvas:
                Color(0, 0, 0)
                p1pawn = Ellipse(pos=(100, self.height / 2), size=(10, 10))
                Color(*color)
                p2pawn = Ellipse(pos=(self.width - 100, self.height / 2), size=(10, 10))

    def on_touch_down(self, touch):

        if touch.x > 200 and touch.x < self.width - 200 and touch.y > 0 and touch.y < self.height - 100 and self.check_victory() == 0 and self.turn <= 9:

            color = (self.turn % 2, 0, (self.turn + 1) % 2)

            # Si le player 1 joue, la couleur est rouge, sinon elle est bleue
            with self.canvas:
                Color(*color)
                d = self.height / 4 - 50

                xpos, ypos = self.trouve_position(touch.x, touch.y)

                if xpos > 0 and ypos > 0 and self.matrix[xpos - 1][ypos - 1] == 0:
                    if self.turn % 2 == 1:
                        self.matrix[xpos - 1][ypos - 1] = 1
                    else:
                        self.matrix[xpos - 1][ypos - 1] = 2
                    Ellipse(pos=(50 + (self.width - 400) * (xpos / 3) + (d / 3),
                                 (self.height * (3 - ypos) / 4 + self.height / 8) - (d / 3)), size=(d, d))
                    self.turn += 1

            self.marker()
            self.print_winner()


    def print_winner(self):
        if self.check_victory() ==1:
            with self.canvas:
                Color(1, 0, 0)
                Label(font_size=30, center_x=self.width / 2, top=self.height - 50,
                                     text='[color=FF0000]Player 1 wins[/color]',
                                     markup=True)

        if self.check_victory() == 2:
            with self.canvas:
                Label(font_size=30, center_x=self.width / 2, top=self.height - 50,
                                     text='[color=0000FF]Player 2 wins[/color]',
                                     markup=True)

        if self.check_victory() == 0 and self.turn > 9:
            with self.canvas:
                Label(font_size=30, center_x=self.width / 2, top=self.height - 50,
                                     text='[color=AAAAAA]Draw[/color]',
                                     markup=True)

    def trouve_position(self, x, y):
        """
        Permet  de trouver la position du pion dans la grille du morpion en fonction de l'endroit où le joueur a cliqué.

        :param x: float abscisse du clic
        :param y: float ordonnée du clic
        :return xpos and ypos: la position du pion dans la grille
        """

        xpos = 0
        ypos = 0

        # xpos est la position en x dans la grille
        if (x > 200) and (x < (self.width - 400) / 4 + 200):
            xpos = 1
        if (x > (self.width - 400) / 3 + 200) and (x < (self.width - 400) * 2 / 3 + 200):
            xpos = 2
        if (x > (self.width - 400) * 2 / 3 + 200) and (x < self.width - 200):
            xpos = 3

        # ypos est la position en y dans la grille
        if (y > 0) and (y < self.height / 4):
            ypos = 3

        if (y > self.height / 4) and (y < self.height / 2):
            ypos = 2

        if (y > self.height / 2) and (y < self.height * 3 / 4):
            ypos = 1

        return xpos, ypos

    def check_victory(self):
        """
        On regarde si un joueur a gagné.

        :return: 1 si P1 a gagné, 2 si P2 a gagné, 0 sinon
        """
        winner = 0

        # On regarde d'abord les colonnes
        for i in range(3):
            check = self.matrix[i][0]

            for j in range(1, 3):
                check = check * self.matrix[i][j]
                winner = self.who_wins(check)

            if winner != 0:
                return winner

        # On regarde les lignes
        for i in range(3):
            check = self.matrix[0][i]

            for j in range(1, 3):
                check = check * self.matrix[j][i]
                winner = self.who_wins(check)

            if winner != 0:
                return winner

        # On regarde les diagonales
        check = self.matrix[0][0]
        for i in range(1, 3):
            check = check * self.matrix[i][i]
            winner = self.who_wins(check)

        if winner != 0:
            return winner

        check = self.matrix[0][2]
        for i in range(1, 3):
            check = check * self.matrix[i][2 - i]
            winner = self.who_wins(check)
        return winner

    def who_wins(self, check):
        """
        Permet de connaître le gagnant
        :param check: int
        :return:
        """
        if check == 1:
            return 1

        elif check == 8:
            return 2

        else:
            return 0



class MorpionApp(App):
    def build(self):
        parent = Widget()
        self.morpion = MorpionGame()
        parent.add_widget(self.morpion)
        return parent


if __name__ == '__main__':
    MorpionApp().run()
