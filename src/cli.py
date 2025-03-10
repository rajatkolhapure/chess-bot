from game_controller import GameController
from ai_engine import AIEngine

def print_welcome():
    """Print welcome message and basic instructions."""
    print("\nWelcome to Chess Bot!")
    print("\nOptions:")
    print("1. Play against AI (as White)")
    print("2. Play against AI (as Black)")
    print("3. Human vs Human")
    print("4. AI vs AI")
    print("\nIn-game commands:")
    print("- Enter moves in the format: e2 e4")
    print("- Type 'quit' to exit")
    print("- Type 'display' to show the current board")
    print("- Press Enter to continue AI vs AI game\n")

def get_game_mode() -> tuple:
    """Get the game mode from user input."""
    while True:
        choice = input("Choose option (1-4): ").strip()
        if choice == '1':
            return ('black', False)  # (AI color, is_ai_vs_ai)
        elif choice == '2':
            return ('white', False)
        elif choice == '3':
            return (None, False)
        elif choice == '4':
            return (None, True)      # AI vs AI mode
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

def validate_move_format(move: str) -> bool:
    """Validate the format of the move input."""
    if len(move.split()) != 2:
        return False
    
    from_pos, to_pos = move.split()
    if len(from_pos) != 2 or len(to_pos) != 2:
        return False
    
    # Check if positions are in correct format (e.g., 'e2')
    valid_cols = 'abcdefgh'
    valid_rows = '12345678'
    
    return (from_pos[0].lower() in valid_cols and from_pos[1] in valid_rows and
            to_pos[0].lower() in valid_cols and to_pos[1] in valid_rows)

def main():
    """Main game loop."""
    print_welcome()
    ai_player, is_ai_vs_ai = get_game_mode()
    game = GameController()
    
    if is_ai_vs_ai:
        # Set up two AIs with slightly different personalities
        ai_white = AIEngine(game, 'white')
        ai_white.max_time = 3.0  # Slightly faster for white
        ai_black = AIEngine(game, 'black')
        ai_black.max_time = 4.0  # Slightly slower for black
        
        move_count = 0
        max_moves = 100  # Prevent infinite games
        
        while move_count < max_moves:
            # Display current state
            print(f"\n{game.get_board_str()}")
            current_color = game.get_current_turn()
            print(f"\nMove {move_count + 1}: {current_color.capitalize()}'s turn")
            
            # Set the current AI
            current_ai = ai_white if current_color == 'white' else ai_black
            game.set_ai_player(current_color, current_ai)
            
            print("\nAI is thinking...")
            if not game.make_ai_move():
                print(f"\nGame Over - {current_color} cannot make a valid move!")
                break
            
            move_count += 1
            
            # Check for game end conditions
            if game.is_check(game.get_current_turn()):
                print(f"\n{game.get_current_turn().capitalize()} is in check!")
                if len(game._get_all_valid_moves()) == 0:
                    print(f"\nCheckmate! {game.get_current_turn()} loses!")
                    break
            elif len(game._get_all_valid_moves()) == 0:
                print("\nStalemate! Game is a draw.")
                break
            
            # Pause between moves
            input("\nPress Enter to continue...")
            
    else:
        # Regular human vs AI or human vs human game
        if ai_player:
            ai_engine = AIEngine(game, ai_player)
            game.set_ai_player(ai_player, ai_engine)
        
        # If AI plays as white, make its first move
        if game.is_ai_turn():
            print(f"\n{game.get_board_str()}")
            print("\nAI is thinking...")
            game.make_ai_move()
        
        while True:
            # Display current state
            print(f"\n{game.get_board_str()}")
            print(f"\n{game.get_current_turn().capitalize()}'s turn")
            
            # Handle AI turn
            if game.is_ai_turn():
                print("\nAI is thinking...")
                if not game.make_ai_move():
                    print("\nGame Over - AI cannot make a valid move!")
                    break
                continue
            
            # Get human player move
            move = input("\nEnter your move (e.g., 'e2 e4'): ").strip().lower()
            
            # Handle special commands
            if move == 'quit':
                print("\nThanks for playing!")
                break
            elif move == 'display':
                continue
            
            # Validate move format
            if not validate_move_format(move):
                print("\nInvalid move format. Please use the format: e2 e4")
                continue
            
            # Make the move
            from_pos, to_pos = move.split()
            if not game.make_move(from_pos, to_pos):
                print("\nInvalid move. Please try again.")
                continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")