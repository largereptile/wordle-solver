import random


class Wordle:
    def __init__(self, word):
        self.word = word
        self.last_guess = ""
        self.guesses_left = 6

    @staticmethod
    def create_wordle():
        wordlist = [line.strip() for line in open('5letters.txt')]
        return Wordle(random.choice(wordlist))

    def guess_word(self, guess):
        if len(guess) != 5 or self.guesses_left == 0:
            print("you have lost sorry no more guesses")
            return ()
        self.guesses_left -= 1
        answer = []
        already_guessed = ""
        out = ""
        # correct pass
        correct = []
        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                correct.append((letter, i))

        # incorrect pass

        incorrect = []
        for i, letter in enumerate(guess):
            if letter in self.word and letter != self.word[i]:
                target = self.word.count(letter)
                correct_count = 0
                for correct_letter, _ in correct:
                    if letter == correct_letter:
                        correct_count += 1
                if target > correct_count:
                    incorrect.append((letter, i))

        # construct output
        for i, letter in enumerate(guess):
            if (letter, i) in correct:
                answer.append((letter, 2))
                out += f"\033[0;32m{guess[i]}\033[0m"
            elif (letter, i) in incorrect:
                answer.append((letter, 1))
                out += f"\033[0;33m{guess[i]}\033[0m"
            else:
                answer.append((letter, 0))
                out += letter

        print(f"{out}")
        return answer
