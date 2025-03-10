from game_controller import GameController
from ai_engine import AIEngine

def print_welcome():
    """Print welcome message and basic instructions."""
    print("\nWelcome to Chess Bot!")
    print("\nOptions:")
    print("1. Play against AI (as White)")
    print("2. Play against AI (as Black)")
    print("3. Human vs Human")
    print("\nIn-game commands:")
    print("- Enter moves in the format: e2 e4")
    print("- Type 'quit' to exit")
    print("- Type 'display' to show the current board\n")

def get_game_mode() -> str:
    """Get the game mode from user input."""
    while True:
        choice = input("Choose option (1-3): ").strip()
        if choice == '1':
            return 'black'  # AI plays as black
        elif choice == '2':
            return 'white'  # AI plays as white
        elif choice == '3':
            return None     # Human vs Human
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

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
    ai_player = get_game_mode()
    game = GameController()
    
    # Set up AI if playing against computer
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