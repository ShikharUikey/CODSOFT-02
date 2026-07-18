import customtkinter as ctk
import random
import time

# ----------------------------
# Theme & Config
# ----------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_COLOR = "#0F172A"
PANEL_COLOR = "#1E293B"
TEXT_COLOR = "#F8FAFC"
X_COLOR = "#38BDF8"       # Light blue for X
O_COLOR = "#F43F5E"       # Pink/Red for O
HOVER_COLOR = "#334155"

class TicTacToeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tic Tac Toe - AI Edition")
        self.geometry("550x750")
        self.configure(fg_color=BG_COLOR)
        
        # ----------------------------
        # State
        # ----------------------------
        self.player_score = 0
        self.ai_score = 0
        self.board = [""] * 9
        self.game_over = False
        self.difficulty = ctk.StringVar(value="Hard (Unbeatable)")

        self.setup_ui()

    def setup_ui(self):
        # Header
        self.title_label = ctk.CTkLabel(
            self, 
            text="TIC TAC TOE", 
            font=("Helvetica", 32, "bold"),
            text_color=X_COLOR
        )
        self.title_label.pack(pady=(30, 10))

        # Score Board
        self.score_frame = ctk.CTkFrame(self, fg_color=PANEL_COLOR, corner_radius=15)
        self.score_frame.pack(pady=10, padx=40, fill="x")
        
        self.score_label = ctk.CTkLabel(
            self.score_frame, 
            text=f"Player (X): {self.player_score}    AI (O): {self.ai_score}", 
            font=("Helvetica", 18, "bold"),
            text_color=TEXT_COLOR
        )
        self.score_label.pack(pady=15)

        # Status & Difficulty
        self.status_label = ctk.CTkLabel(
            self, 
            text="Your Turn", 
            font=("Helvetica", 18),
            text_color="#10B981" # Green
        )
        self.status_label.pack(pady=10)

        self.difficulty_menu = ctk.CTkOptionMenu(
            self, 
            values=["Easy", "Medium", "Hard (Unbeatable)"],
            variable=self.difficulty,
            fg_color=PANEL_COLOR,
            button_color=PANEL_COLOR,
            button_hover_color=HOVER_COLOR,
            font=("Helvetica", 14),
            command=self.reset_game
        )
        self.difficulty_menu.pack(pady=10)

        # Game Board
        self.board_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.board_frame.pack(pady=20)
        
        self.buttons = []
        for i in range(9):
            btn = ctk.CTkButton(
                self.board_frame, 
                text="", 
                width=100, 
                height=100,
                corner_radius=15,
                font=("Helvetica", 48, "bold"),
                fg_color=PANEL_COLOR,
                hover_color=HOVER_COLOR,
                command=lambda idx=i: self.player_move(idx)
            )
            row, col = divmod(i, 3)
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.buttons.append(btn)

        # Restart Button
        self.restart_btn = ctk.CTkButton(
            self, 
            text="Restart Game", 
            width=200, 
            height=45,
            corner_radius=20,
            font=("Helvetica", 16, "bold"),
            fg_color="#475569",
            hover_color="#64748B",
            command=self.reset_game
        )
        self.restart_btn.pack(pady=20)

    # ----------------------------
    # Game Logic
    # ----------------------------
    def check_winner(self, temp_board):
        wins = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], # Cols
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        for combo in wins:
            a, b, c = combo
            if temp_board[a] != "" and temp_board[a] == temp_board[b] == temp_board[c]:
                return temp_board[a], combo
        
        if "" not in temp_board:
            return "Draw", None
        return None, None

    def minimax(self, temp_board, is_maximizing):
        winner, _ = self.check_winner(temp_board)
        if winner == "O": return 1
        elif winner == "X": return -1
        elif winner == "Draw": return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if temp_board[i] == "":
                    temp_board[i] = "O"
                    score = self.minimax(temp_board, False)
                    temp_board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if temp_board[i] == "":
                    temp_board[i] = "X"
                    score = self.minimax(temp_board, True)
                    temp_board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def ai_move(self):
        if self.game_over: return
        
        mode = self.difficulty.get()
        available_moves = [i for i, spot in enumerate(self.board) if spot == ""]
        
        move = None
        
        if mode == "Easy":
            # 100% Random
            move = random.choice(available_moves) if available_moves else None
            
        elif mode == "Medium":
            # 50% chance of random, 50% optimal
            if random.random() < 0.5:
                move = random.choice(available_moves) if available_moves else None
        
        if move is None: # Hard mode or Medium fallback
            best_score = -float('inf')
            for i in available_moves:
                self.board[i] = "O"
                score = self.minimax(self.board, False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    move = i

        if move is not None:
            self.board[move] = "O"
            self.buttons[move].configure(text="O", text_color=O_COLOR)
            
        self.evaluate_board()

    def player_move(self, index):
        if self.game_over or self.board[index] != "":
            return

        # Player move
        self.board[index] = "X"
        self.buttons[index].configure(text="X", text_color=X_COLOR)
        
        winner, _ = self.check_winner(self.board)
        if winner:
            self.evaluate_board()
            return
            
        self.status_label.configure(text="AI Thinking...", text_color="#F59E0B") # Yellow
        self.update()
        
        # Small delay for realism
        self.after(400, self.ai_move)

    def evaluate_board(self):
        winner, combo = self.check_winner(self.board)
        
        if not winner:
            self.status_label.configure(text="Your Turn", text_color="#10B981")
            return
            
        self.game_over = True
        
        if winner == "X":
            self.player_score += 1
            self.status_label.configure(text="You Win! 🎉", text_color=X_COLOR)
            self.highlight_win(combo, X_COLOR)
        elif winner == "O":
            self.ai_score += 1
            self.status_label.configure(text="AI Wins! 🤖", text_color=O_COLOR)
            self.highlight_win(combo, O_COLOR)
        else:
            self.status_label.configure(text="It's a Draw! 🤝", text_color="#94A3B8")
            
        self.score_label.configure(text=f"Player (X): {self.player_score}    AI (O): {self.ai_score}")

    def highlight_win(self, combo, color):
        if not combo: return
        for idx in combo:
            # Highlight the winning buttons
            self.buttons[idx].configure(fg_color="#334155")

    def reset_game(self, _=None):
        self.board = [""] * 9
        self.game_over = False
        
        for btn in self.buttons:
            btn.configure(text="", fg_color=PANEL_COLOR)
            
        self.status_label.configure(text="Your Turn", text_color="#10B981")

if __name__ == "__main__":
    app = TicTacToeApp()
    app.mainloop()