import tkinter as tk

# ----------------------------
# Window
# ----------------------------

root = tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("500x650")
root.configure(bg="#1e1e1e")

# ----------------------------
# Scores
# ----------------------------

player_score = 0
ai_score = 0

# ----------------------------
# Game Data
# ----------------------------

board = [""] * 9
buttons = []
game_over = False

# ----------------------------
# UI
# ----------------------------

title_label = tk.Label(
    root,
    text="TIC TAC TOE AI",
    bg="#1e1e1e",
    fg="white",
    font=("Helvetica", 22, "bold")
)
title_label.pack(pady=15)

score_label = tk.Label(
    root,
    text="Player (X): 0    AI (O): 0",
    bg="#1e1e1e",
    fg="white",
    font=("Helvetica", 14)
)
score_label.pack()

status_label = tk.Label(
    root,
    text="Your Turn",
    bg="#1e1e1e",
    fg="#00ff99",
    font=("Helvetica", 14, "bold")
)
status_label.pack(pady=10)

board_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)
board_frame.pack(pady=20)

# ----------------------------
# Winner Logic
# ----------------------------

def check_winner_state(temp_board):

    wins = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for combo in wins:

        a,b,c = combo

        if (
            temp_board[a] != "" and
            temp_board[a] == temp_board[b] == temp_board[c]
        ):
            return temp_board[a]

    if "" not in temp_board:
        return "Draw"

    return None

# ----------------------------
# Minimax
# ----------------------------

def minimax(temp_board, is_maximizing):

    result = check_winner_state(temp_board)

    if result == "O":
        return 1

    elif result == "X":
        return -1

    elif result == "Draw":
        return 0

    if is_maximizing:

        best_score = -100

        for i in range(9):

            if temp_board[i] == "":

                temp_board[i] = "O"

                score = minimax(
                    temp_board,
                    False
                )

                temp_board[i] = ""

                best_score = max(
                    score,
                    best_score
                )

        return best_score

    else:

        best_score = 100

        for i in range(9):

            if temp_board[i] == "":

                temp_board[i] = "X"

                score = minimax(
                    temp_board,
                    True
                )

                temp_board[i] = ""

                best_score = min(
                    score,
                    best_score
                )

        return best_score

# ----------------------------
# AI Move
# ----------------------------

def ai_move():

    global game_over

    if game_over:
        return

    best_score = -100
    move = None

    for i in range(9):

        if board[i] == "":

            board[i] = "O"

            score = minimax(
                board,
                False
            )

            board[i] = ""

            if score > best_score:

                best_score = score
                move = i

    if move is not None:

        board[move] = "O"

        buttons[move].config(
            text="O",
            fg="#ff5555"
        )

    result = check_winner_state(board)

    handle_result(result)

# ----------------------------
# Result Handling
# ----------------------------

def handle_result(result):

    global player_score
    global ai_score
    global game_over

    if result is None:

        status_label.config(
            text="Your Turn"
        )
        return

    game_over = True

    if result == "X":

        player_score += 1

        status_label.config(
            text="You Win!"
        )

    elif result == "O":

        ai_score += 1

        status_label.config(
            text="AI Wins!"
        )

    else:

        status_label.config(
            text="It's a Draw!"
        )

    score_label.config(
        text=f"Player (X): {player_score}    AI (O): {ai_score}"
    )

# ----------------------------
# Player Move
# ----------------------------

def button_click(index):

    global game_over

    if game_over:
        return

    if board[index] != "":
        return

    board[index] = "X"

    buttons[index].config(
        text="X",
        fg="#00bfff"
    )

    result = check_winner_state(board)

    if result:

        handle_result(result)
        return

    status_label.config(
        text="AI Thinking..."
    )

    root.after(
        300,
        ai_move
    )

# ----------------------------
# Restart
# ----------------------------

def restart_game():

    global board
    global game_over

    board = [""] * 9

    game_over = False

    for button in buttons:

        button.config(
            text=""
        )

    status_label.config(
        text="Your Turn"
    )

# ----------------------------
# Create Board
# ----------------------------

for row in range(3):

    for col in range(3):

        index = row * 3 + col

        button = tk.Button(
            board_frame,
            text="",
            width=5,
            height=2,
            font=("Helvetica", 28, "bold"),
            bg="#252526",
            fg="white",
            activebackground="#3c3c3c",
            command=lambda idx=index: button_click(idx)
        )

        button.grid(
            row=row,
            column=col,
            padx=6,
            pady=6
        )

        buttons.append(button)

# ----------------------------
# Restart Button
# ----------------------------

restart_button = tk.Button(
    root,
    text="Restart Game",
    command=restart_game,
    bg="#c0392b",
    fg="black",
    font=("rubintek", 12, "bold"),
    width=18
)

restart_button.pack(
    pady=20
)

# ----------------------------
# Run
# ----------------------------

root.mainloop()