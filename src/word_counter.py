# src/word_counter.py
def count_characters(word):
    return len(word)

def main():
    word = input("Enter a word: ")
    char_count = count_characters(word)
    print(f"The word '{word}' has {char_count} characters.")

if __name__ == "__main__":
    main()