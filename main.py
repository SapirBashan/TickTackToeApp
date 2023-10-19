import time
from random import randint
from typing import Union, List, Any, Tuple
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
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
        global buttonI, buttonJ
        best_move = self.max_alpha_beta(float("-inf"), float("inf"), depth, is_maximizing_player)
        return best_move

    def max_alpha_beta(self, alpha: int, beta: int, depth: int, is_maximizing_player: bool):
        if depth == 0:
            return self.evaluate(), None

        max_eval = float("-inf")
        best_move = None
        available_moves = []

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text == "":
                    available_moves.append((i, j))

        if not available_moves:
            return 0, None

        for move in available_moves:
            i, j = move
            self.buttons[i][j].text = "O"  # Make a hypothetical move
            eval, _ = self.min_alpha_beta(alpha, beta, depth - 1, not is_maximizing_player)  # Evaluate the move
            self.buttons[i][j].text = ""  # Undo the hypothetical move

            if eval > max_eval:
                max_eval = eval
                best_move = (i, j)

            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return max_eval, best_move

    def min_alpha_beta(self, alpha, beta, depth, is_maximizing_player):
        if depth == 0:
            return self.evaluate(), None

        min_eval = float("inf")
        best_move = None
        available_moves = []

        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text == "":
                    available_moves.append((i, j))

        if not available_moves:
            return 0, None

        for move in available_moves:
            i, j = move
            self.buttons[i][j].text = "X"  # Make a hypothetical move
            eval, _ = self.max_alpha_beta(alpha, beta, depth - 1, not is_maximizing_player)  # Evaluate the move
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
        arr = []
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text == "":
                    arr.append((i, j))

        # # Check if there are any available moves
        # if arr:
        #     # Pick a random button from the available moves
        #     buttonI, buttonJ = arr[randint(0, len(arr) - 1)]

        if VsComputer[1] != False:
            eval, best_move = self.alpha_beta_pruning(True, 5)
        else:
            eval, best_move = self.alpha_beta_pruning(False, 5)

        for i in range(3):
            for j in range(3):
                if (i, j) in arr:
                    var = self.buttons[i][j].text == ""

        if best_move is not None:
            buttonI, buttonJ = best_move
            if VsComputer[1] != False:
                self.buttons[buttonI][buttonJ].text = "O"
                self.buttons[buttonI][buttonJ].font_size = 120
                self.buttons[buttonI][buttonJ].disabled = True
                self.buttons[buttonI][buttonJ].color = (0, 0, 1, 1)  # Set text color to blue (RGBA format)
                Check = False
            else:
                self.buttons[buttonI][buttonJ].text = "X"
                self.buttons[buttonI][buttonJ].font_size = 120
                self.buttons[buttonI][buttonJ].disabled = True
                self.buttons[buttonI][buttonJ].color = (1, 0, 0, 1)  # Set text color to red (RGBA format)
                Check = True

            self.check_winner()
        else:
            print("No valid moves found. It's a tie!")

    def on_button_press(self, instance):
        global Check  # Declare Check as a global variable
        global VsComputer
        if Check == False:
            if (VsComputer[1] == True):
                instance.text = "X"
                instance.font_size = 120
                instance.disabled = True
                Check = True
                instance.color = (1, 0, 0, 1)  # Set text color to red (RGBA format)
                self.check_winner()
            if (VsComputer[0] == True):
                VsComputer[1] = False
                # Schedule a callback after 1 second to execute the computer's move
            elif (VsComputer[0] == False) and (VsComputer[1] == True):
                Clock.schedule_once(self.play_computer_move, 0.5)
        else:
            if (VsComputer[0] == True) and (VsComputer[1] == False):
                instance.text = "O"
                instance.font_size = 120
                instance.disabled = True
                instance.color = (0, 0, 1, 1)  # Set text color to blue (RGBA format)
                Check = False
                VsComputer[1] = True
                self.check_winner()
            elif (VsComputer[0] == False) and (VsComputer[1] == False):
                    Clock.schedule_once(self.play_computer_move, 0.5)

    def play_computer_move(self, dt):
        self.PlayVsComputer()

    def evaluate(self):
        global Count
        for i in range(3):
            # Check rows for "X" or "O" wins
            if self.buttons[i][0].text == self.buttons[i][1].text == self.buttons[i][2].text == "X":
                return -1
            if self.buttons[i][0].text == self.buttons[i][1].text == self.buttons[i][2].text == "O":
                return 1
            # Check columns for "X" or "O" wins
            if self.buttons[0][i].text == self.buttons[1][i].text == self.buttons[2][i].text == "X":
                return -1
            if self.buttons[0][i].text == self.buttons[1][i].text == self.buttons[2][i].text == "O":
                return 1

            # Check diagonals for "X" or "O" wins
        if self.buttons[0][0].text == self.buttons[1][1].text == self.buttons[2][2].text == "X":
            return -1
        if self.buttons[0][0].text == self.buttons[1][1].text == self.buttons[2][2].text == "O":
            return 1
        if self.buttons[0][2].text == self.buttons[1][1].text == self.buttons[2][0].text == "X":
            return -1
        if self.buttons[0][2].text == self.buttons[1][1].text == self.buttons[2][0].text == "O":
            return 1

        Count = 0
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j].text == "X" or self.buttons[i][j].text == "O":
                    Count += 1
        if Count == 9:
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

    def show_popup(self, Winner):
        # Create a layout to hold the label and buttons
        layout = BoxLayout(orientation='vertical')

        # Create a label
        label = Label(text=Winner, size_hint_y=None, height=50)
        layout.add_widget(label)

        # Create buttons
        show1 = Button(text='Play Vs Friend')
        show2 = Button(text='Play Vs Computer')

        def restart_game(instance):
            global VsComputer
            VsComputer = [True, True]
            global Count
            global Check
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].text = ""
                    self.buttons[i][j].disabled = False
                    self.buttons[i][j].color = (1, 1, 1, 1)  # Set text color to white (original color)
            Check = False
            Count = 0
            popupWindow.dismiss()

        def change_game_mode(instance):
            global VsComputer
            VsComputer = [False, True]
            global Count
            global Check
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j].text = ""
                    self.buttons[i][j].disabled = False
                    self.buttons[i][j].color = (1, 1, 1, 1)  # Set text color to white (original color)
            Check = False
            Count = 0
            popupWindow.dismiss()

        # Bind button press to restart the game and dismiss the popup
        show1.bind(on_press=restart_game)
        show2.bind(on_press=change_game_mode)

        # Add buttons to the layout
        layout.add_widget(show1)
        layout.add_widget(show2)

        # Create the Popup with the layout as content
        popupWindow = Popup(title='Popup Title', content=layout, size_hint=(None, None), size=(400, 400))

        # Open the popup
        popupWindow.open()

class ButtonApp(App):
    def build(self):
        return ButtonGrid()


# Run the app
if __name__ == '__main__':
    ButtonApp().run()
