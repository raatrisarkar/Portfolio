import random

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I have picked a number between 1 and 100. Can you guess it?")
    
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10 

    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts}: Enter your guess: "))
            attempts += 1

            if guess < 1 or guess > 100:
                print("Please guess a number between 1 and 100.")
            elif guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
                break
        except ValueError:
            print("Invalid input! Please enter a valid number.")

    if attempts == max_attempts and guess != secret_number:
        print(f"Sorry, you've used all your attempts. The number was {secret_number}.")

number_guessing_game()
