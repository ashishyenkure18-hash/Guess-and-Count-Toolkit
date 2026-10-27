"""
Guess & Count - Interactive Python Toolkit
===========================================
A menu-driven application combining:
  1. A Number Guessing Game (1-100, 10 attempts, scoring, best score)
  2. A Word Counter for sample.txt (case/punctuation insensitive)

Uses only the Python 3 standard library.
"""

import random
import string
from collections import Counter

# -------------------------
# Named constants (Section 7)
# -------------------------
LOWEST_NUMBER = 1
HIGHEST_NUMBER = 100
MAX_ATTEMPTS = 10
STARTING_SCORE = 100
POINTS_PER_WRONG_GUESS = 10
MIN_SCORE = 0
FILE_NAME = "sample.txt"
ENCODING = "utf-8"
TOP_N_WORDS = 10
MENU_WIDTH = 40


# =========================================================
# NUMBER GUESSING GAME (Sections 1 & 2)
# =========================================================
def calculate_score(attempts_used):
    """Return the score for a win using the given number of valid attempts.

    Score = 100 - 10 * (number of incorrect guesses), with a floor of 0.
    On a win, incorrect guesses = attempts_used - 1.
    """
    incorrect = attempts_used - 1
    score = STARTING_SCORE - (incorrect * POINTS_PER_WRONG_GUESS)
    return max(score, MIN_SCORE)


def get_valid_guess():
    """Prompt until the user enters a whole number between 1 and 100.

    Invalid input never counts as an attempt: this function only returns
    when a valid value has been entered.
    """
    while True:
        raw = input(f"Enter your guess ({LOWEST_NUMBER}-{HIGHEST_NUMBER}): ").strip()

        if raw == "":
            print("  -> Empty input. Please type a whole number.")
            continue

        try:
            guess = int(raw)
        except ValueError:
            print("  -> Invalid input. Please enter a whole number (no letters or decimals).")
            continue

        if guess < LOWEST_NUMBER or guess > HIGHEST_NUMBER:
            print(f"  -> Out of range. Enter a number between {LOWEST_NUMBER} and {HIGHEST_NUMBER}.")
            continue

        return guess


def ask_play_again():
    """Ask whether to play again. Accepts y/yes/n/no (case-insensitive).

    Returns True for yes, False for no. Invalid answers are re-prompted.
    """
    while True:
        answer = input("Play again? (y/yes/n/no): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  -> Please answer y, yes, n, or no.")


def play_guessing_game(best_score):
    """Run one full game of Number Guessing.

    Returns the (possibly updated) best_score. best_score is only updated
    when the player wins with a score higher than the previous best.
    """
    print("\n--- NUMBER GUESSING GAME ---")
    print(f"I'm thinking of a number between {LOWEST_NUMBER} and {HIGHEST_NUMBER}.")
    print(f"You have {MAX_ATTEMPTS} valid attempts. Score starts at {STARTING_SCORE}.")

    # Secret number generated ONCE per game, before the guessing loop.
    secret_number = random.randint(LOWEST_NUMBER, HIGHEST_NUMBER)

    attempts_used = 0
    won = False

    while attempts_used < MAX_ATTEMPTS:
        remaining = MAX_ATTEMPTS - attempts_used
        print(f"\nAttempt {attempts_used + 1}/{MAX_ATTEMPTS} (attempts remaining: {remaining})")

        guess = get_valid_guess()          # invalid input never reaches here
        attempts_used += 1                  # only valid guesses count

        if guess == secret_number:
            won = True
            print("Correct! You guessed the secret number!")
            break
        elif guess > secret_number:
            print("Too high! Try a smaller number.")
        else:
            print("Too low! Try a larger number.")

    # ---------- End-of-game report ----------
    print("\n---------- GAME OVER ----------")
    print(f"Secret number : {secret_number}")

    if won:
        final_score = calculate_score(attempts_used)
        print("Result        : YOU WIN!")
        print(f"Valid attempts: {attempts_used}")
        print(f"Final score   : {final_score}")

        if final_score > best_score:
            best_score = final_score
            print("NEW BEST SCORE!")
        print(f"Best score    : {best_score}")
    else:
        final_score = MIN_SCORE
        print("Result        : YOU LOSE - out of attempts.")
        print(f"Valid attempts: {attempts_used}")
        print(f"Final score   : {final_score}")
        print(f"Best score    : {best_score}")

    return best_score


# =========================================================
# WORD COUNTER (Sections 3, 4 & 5)
# =========================================================
def count_words_in_file(filename):
    """Read filename, clean the text, and return a Counter of words.

    Returns None if the file is missing or cannot be read.
    Uses with-open for safe handling and str.translate for punctuation.
    """
    try:
        with open(filename, "r", encoding=ENCODING) as file:
            text = file.read()
    except FileNotFoundError:
        print(f"\nCould not find '{filename}'. Place the file in the same folder as main.py.")
        return None
    except OSError as error:
        print(f"\nError reading '{filename}': {error}")
        return None

    # 1. Lowercase
    text = text.lower()
    # 2. Remove punctuation using str.translate
    text = text.translate(str.maketrans("", "", string.punctuation))
    # 3. Split into words
    words = text.split()
    # 5. Count frequencies
    return Counter(words)


def display_word_statistics(counter):
    """Display total words, unique words, and top-10 table. Handles empty input."""
    print("\n========== WORD COUNT RESULTS ==========")

    if counter is None:
        return  # error already reported by count_words_in_file

    total_words = sum(counter.values())
    unique_words = len(counter)

    if total_words == 0:
        print("\nThe file contains no words (empty or punctuation only).")
        return

    print(f"\nTotal words: {total_words}")
    print(f"Unique words: {unique_words}")

    print(f"\nTop {TOP_N_WORDS} Most Common Words")
    print("-" * 32)
    print(f"{'Word':<20}{'Count':>12}")
    print("-" * 32)
    for word, count in counter.most_common(TOP_N_WORDS):
        print(f"{word:<20}{count:>12}")
    print("-" * 32)


# =========================================================
# MAIN MENU (Section 6)
# =========================================================
def show_menu():
    """Print the main menu."""
    print("\n" + "=" * MENU_WIDTH)
    print("       GUESS & COUNT TOOLKIT")
    print("=" * MENU_WIDTH)
    print("1. Play Number Guessing Game")
    print("2. Count Words in a Text File")
    print("3. Quit")
    print("=" * MENU_WIDTH)


def main():
    """Entry point: repeating menu loop until the user quits."""
    best_score = 0  # maintained for the whole program session

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "":
            print("  -> Empty input. Please enter 1, 2, or 3.")
            continue

        if choice == "1":
            best_score = play_guessing_game(best_score)
        elif choice == "2":
            counter = count_words_in_file(FILE_NAME)
            display_word_statistics(counter)
        elif choice == "3":
            print("\nThanks for playing! Goodbye.")
            break
        else:
            print("  -> Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()