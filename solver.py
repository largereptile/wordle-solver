from collections import defaultdict


class WordleSolver:
    def __init__(self, wordle):
        self.wordlist = [line.strip() for line in open('5letters.txt')]
        self.wordle = wordle
        self.starting_word = "salet"
        self.most_common = [defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)]
        self.analyse_words()
        self.correct_positions = set()
        self.incorrect_positions = set()
        self.incorrect_letters = set()
        # self.confirmed_letter_counts = defaultdict(int)

    def analyse_words(self):
        for word in self.wordlist:
            for i in range(5):
                self.most_common[i][word[i]] += 1

    def solve(self):
        self.correct_positions = set()
        self.incorrect_positions = set()
        self.incorrect_letters = set()

        guesses = 0
        guess_results = self.wordle.guess_word(self.starting_word)
        while guesses < 6:
            guesses += 1
            pos = 0

            # parse results
            for letter, status in guess_results:
                if status == 2:
                    self.correct_positions.add((pos, letter))
                elif status == 1:
                    self.incorrect_positions.add((pos, letter))
                else:
                    self.incorrect_letters.add((pos, letter))
                pos += 1

            # end if correct
            if len(self.correct_positions) == 5:
                return self.correct_positions, guesses

            # find extra constraints from incorrect letters that are present before
            self.wordlist = self.filter_wordlist(guess_results)

            # choose new word from list based on common letter heuristics
            scores = []
            for word in self.wordlist:
                score = 0
                for pos, letter in enumerate(word):
                    score += self.most_common[pos][letter]
                scores.append((word, score))

            sorted_words = list(sorted(scores, key=lambda x: x[1], reverse=True))
            word_to_guess = ""
            best_score = 99999999999999
            for word, _ in sorted_words[:40]:
                score = self.inner_solve(word)
                if score < best_score:
                    word_to_guess = word
                    best_score = score

            guess_results = self.wordle.guess_word(word_to_guess)

        return [], 7

    def filter_wordlist(self, guess_results):
        for letter, status in guess_results:
            if (letter in list(map(lambda x: x[1], self.correct_positions)) or letter in list(
                    map(lambda x: x[1], self.incorrect_positions))) and status == 0:
                count = 0
                for _, c_letter in self.correct_positions:
                    if c_letter == letter:
                        count += 1
                for _, i_letter in self.incorrect_positions:
                    if i_letter == letter:
                        count += 1

        # remove words from wordlist that break constraints
        new_wordlist = []
        for word in self.wordlist:
            correct_word = word == self.wordle.word
            add = True
            # remove any without correct letters
            for pos, letter in self.correct_positions:
                if word[pos] != letter:
                    add = False

            # remove any with incorrect positions
            for pos, letter in self.incorrect_positions:
                if word[pos] == letter or letter not in word:
                    add = False

            for pos, letter in self.incorrect_letters:
                if word[pos] == letter:
                    add = False

            if add:
                new_wordlist.append(word)
        return new_wordlist

    # take word, assume it is wrong, return length of new wordlist with those constraints
    def inner_solve(self, word):
        answer = []
        for i, letter in enumerate(word):
            if (letter, i) in self.correct_positions:
                answer.append((letter, 2))
            elif (letter, i) in self.incorrect_positions:
                answer.append((letter, 1))
            else:
                answer.append((letter, 0))

        wordlist = self.filter_wordlist(answer)
        return len(wordlist)
