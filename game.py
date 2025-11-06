# create a sinple rock, paper, scissors gane
# provide a welcone nessage
# get the user"s choice
# get the corputer's choice
# compare the two choices
# print the results
# ask the user if they want to play again
# say goodbye and end the gane
# use one function for the game logic
import random

choices = ["rock", "paper", "scissors"]

def play_rps():
    """Run the rock-paper-scissors game loop."""
    print("Welcome to Rock, Paper, Scissors!")
    try:
        while True:
            user = input("Enter rock, paper, or scissors (or 'quit' to exit): ").strip().lower()
            if not user:
                print("Please enter a choice.")
                continue
            if user in ("quit", "q", "exit"):
                print("Thanks for playing. Goodbye!")
                break
            if user in ("r", "p", "s"):
                user = {"r": "rock", "p": "paper", "s": "scissors"}[user]
            if user not in choices:
                print("Invalid choice. Please try again.")
                continue

            comp = random.choice(choices)
            print(f"You chose: {user}. Computer chose: {comp}.")

            if user == comp:
                print("It's a tie!")
            elif (user == "rock" and comp == "scissors") or \
                 (user == "paper" and comp == "rock") or \
                 (user == "scissors" and comp == "paper"):
                print("You win!")
            else:
                print("You lose!")

            again = input("Play again? [Y/n]: ").strip().lower()
            if again and again[0] == "n":
                print("Thanks for playing. Goodbye!")
                break
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")

if __name__ == "__main__":
    play_rps()
