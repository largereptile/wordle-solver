from wordle import Wordle
from solver import WordleSolver

if __name__ == "__main__":
    wordlist = [line.strip() for line in open('5letters.txt')]
    total = 0
    failures = 0
    for word in wordlist:
        wordle = Wordle(word)
        solver = WordleSolver(wordle)
        _, guesses = solver.solve()
        if guesses == 7:
            failures += 1
        else:
            total += guesses

    print(f"Solved {((len(wordlist) - failures)/len(wordlist))*100}% (failed {failures}/{len(wordlist)})")
    print(f"Average guesses for successes: {total/len(wordlist)}")
