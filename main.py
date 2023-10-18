import time
from random import randint
from kivy.clock import Clock

import kivy
import self as self
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup

Check = False
VsComputer = [True, True]
Count = 0

#add a alpha beta prunning function to the game to make it unbeatable
#do it write here


class ButtonGrid(GridLayout):
    def __init__(self, **kwargs):
        super(ButtonGrid, self).__init__(**kwargs)
        self.cols = 3  # Set the number of columns in the grid layout
        self.rows = 4  # Set the number of rows in the grid layout
        self.buttons = [[None for _ in range(3)] for _ in range(3)]  # Initialize 2D list for buttons

        # Create buttons and add them to the grid layout
        for i in range(3):
            for j in range(3):
                button = Button()
                button.bind(on_press=self.on_button_press)  # Bind a function to button press event
                button.pos_hint = {'row': i, 'col': j}  # Set position hint for the button
                self.add_widget(button)  # Add button to the grid layout
                self.buttons[i][j] = button  # Add button to the 2D list

    def alpha_beta_pruning(self, is_maximizing_player, depth):
        global buttonJ, buttonI
        VAL, best_move = self.max_alpha_beta(float("-inf"), float("inf"), depth)
        return best_move

    def max_alpha_beta(self, alpha, beta, depth):
        if depth == 0 or self.check_winner():
            return self.evaluate(), None

        max_eval = float("-inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text == "":
                    self.buttons[i][j].text = "O"  # Make a hypothetical move
                    eval, VAL = self.min_alpha_beta(alpha, beta, depth - 1)  # Evaluate the move
                    self.buttons[i][j].text = ""  # Undo the hypothetical move
                    if eval > max_eval:
                        max_eval = eval
                        best_move = (i, j)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval, best_move

    def min_alpha_beta(self, alpha, beta, depth):
        if depth == 0 or self.check_winner():
            return self.evaluate(), None

        min_eval = float("inf")
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text == "":
                    self.buttons[i][j].text = "X"  # Make a hypothetical move
                    eval, VAL = self.max_alpha_beta(alpha, beta, depth - 1)  # Evaluate the move
                    self.buttons[i][j].text = ""  # Undo the hypothetical move
                    if eval < min_eval:
                        min_eval = eval
                        best_move = (i, j)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval, best_move


    def PlayVsComputer(self):
        global Check
        # Create a list of tuples representing unclicked buttons
        # arr = []
        # for i in range(0):
        #     for j in range(0):
        #         if self.buttons[i][j].text == "":
        #             arr.append((i, j))

        # Check if there are any available moves
        # if arr:
        #     # Pick a random button from the available moves
        #     buttonI, buttonJ = arr[randint(0, len(arr) - 1)]

        if VsComputer[1] != False:
            best_moveI,best_moveJ = self.alpha_beta_pruning(True)
        else:
            best_moveI,best_moveJ = self.alpha_beta_pruning(False)

        buttonI = best_moveI
        buttonJ = best_moveJ

        if VsComputer[1] != False:
            self.buttons[buttonI][buttonJ].text = "O"
            self.buttons[buttonI][buttonJ].font_size = 120
            self.buttons[buttonI][buttonJ].color = (0, 0, 1, 1)  # Set text color to blue (RGBA format)
            self.buttons[buttonI][buttonJ].disabled = True
            Check = False
        else:
            self.buttons[buttonI][buttonJ].text = "X"
            self.buttons[buttonI][buttonJ].font_size = 120
            self.buttons[buttonI][buttonJ].color = (1, 0, 0, 1)  # Set text color to red (RGBA format)
            self.buttons[buttonI][buttonJ].disabled = True
            Check = True
        self.check_winner()

    def on_button_press(self, instance):
        global Check  # Declare Check as a global variable
        if Check == False:
            if (VsComputer[0] == True) and (VsComputer[1] == True):
                instance.text = "X"
                instance.font_size = 120
                instance.color = (1, 0, 0, 1)  # Set text color to red (RGBA format)
                instance.disabled = True
                Check = True
        else:
            if (VsComputer[0] == True) and (VsComputer[1] == False):
                instance.text = "O"
                instance.font_size = 120
                instance.color = (0, 0, 1, 1)  # Set text color to blue (RGBA format)
                instance.disabled = True
                Check = False
        gameOver = self.check_winner()
        # Schedule a callback after 1 second to execute the computer's move
        if not gameOver:
            Clock.schedule_once(self.play_computer_move, 0.5)

    def play_computer_move(self, dt):
        self.PlayVsComputer()

    def evaluate(self):
        winner = self.check_winner()
        if winner == "Player X WON":
            return -1
        elif winner == "Player O WON":
            return 1
        elif winner == "It's a Tie":
            return 0
        else:
            # Game still ongoing, return an appropriate heuristic value
            return 0  # You can adjust this value based on your game's strategy

    def check_winner(self):
        global Count
        # Check rows and columns for "X" or "O" wins
        for i in range(3):
            # Check rows for "X" or "O" wins
            if self.buttons[i][0].text == self.buttons[i][1].text == self.buttons[i][2].text == "X":
                self.show_popup(Winner="Player X WON")
                return True, "Player X WON"
            if self.buttons[i][0].text == self.buttons[i][1].text == self.buttons[i][2].text == "O":
                self.show_popup(Winner="Player O WON")
                return True, "Player O WON"
            # Check columns for "X" or "O" wins
            if self.buttons[0][i].text == self.buttons[1][i].text == self.buttons[2][i].text == "X":
                self.show_popup(Winner="Player X WON")
                return True, "Player X WON"
            if self.buttons[0][i].text == self.buttons[1][i].text == self.buttons[2][i].text == "O":
                self.show_popup(Winner="Player O WON")
                return True, "Player O WON"

        # Check diagonals for "X" or "O" wins
        if self.buttons[0][0].text == self.buttons[1][1].text == self.buttons[2][2].text == "X":
            self.show_popup(Winner="Player X WON")
            return True, "Player X WON"
        if self.buttons[0][0].text == self.buttons[1][1].text == self.buttons[2][2].text == "O":
            self.show_popup(Winner="Player O WON")
            return True, "Player O WON"
        if self.buttons[0][2].text == self.buttons[1][1].text == self.buttons[2][0].text == "X":
            self.show_popup(Winner="Player X WON")
            return True, "Player X WON"
        if self.buttons[0][2].text == self.buttons[1][1].text == self.buttons[2][0].text == "O":
            self.show_popup(Winner="Player O WON")
            return True, "Player O WON"

        Count = 0
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text == "X" or self.buttons[i][j].text == "O":
                    Count += 1
        if Count == 9:
            self.show_popup(Winner="It's a Tie")
            return True, "It's a Tie"

        return None



    def show_popup(self, Winner):
        show1 = Button(text='Restart Game')
        show2 = Button(text='Play vs Computer')
        popupWindow = Popup(title=Winner, content=show1, size_hint=(None, None), size=(400, 400))
        show1.bind(on_press=popupWindow.dismiss)
        popupWindow.open()

        # Reset the game
        global Count
        global Check
        global VsComputer
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].text = ""
                self.buttons[i][j].disabled = False
                Check = False
                VsComputer = [True, True]
                Count = 0
  
class ButtonApp(App):
    def build(self):
        return ButtonGrid()

# Run the app
if __name__ == '__main__':
    ButtonApp().run()
