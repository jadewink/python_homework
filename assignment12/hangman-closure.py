# Task 4: Closure Practice
def make_hangman(secret_word):
    guesses = [' ']  # Start with space as a "guessed" character

    def hangman_closure(letter):
        if letter not in guesses:
            guesses.append(letter)

        displayed = ''.join(
            letter if letter in guesses else '_'
            for letter in secret_word
        )
        print(displayed)

        # Only require guessing actual letters (ignore spaces)
        return all(
            letter in guesses or letter == ' '
            for letter in secret_word
        )

    return hangman_closure

# Game Loop
def main():
    secret_word = input("Enter the secret word: ").lower()
    print("\n" * 50)  # Hide the secret word from the guesser

    game = make_hangman(secret_word)

    print("Start guessing letters!")
    while True:
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabetical character.")
            continue

        finished = game(guess)
        if finished:
            print("Congratulations! You guessed the word.")
            break

if __name__ == "__main__":
    main()
