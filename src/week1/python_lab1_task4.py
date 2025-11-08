"""
Task 4 – Text-based Arithmetic Analyzer
--------------------------------------
Create a text-based analyzer that:
1. Counts non-space characters.
2. Counts words.
3. Extracts numbers and computes their sum and average.
Use helper functions:
- count_characters(text)
- count_words(text)
- extract_numbers(text)
- analyze_text(text)
Print formatted summary in main.
"""

def count_characters(text):
    """Count non-space characters in a string."""
    return len(text.replace(" ", ""))

def count_words(text):
    """Count number of words in a string."""
    return len(text.split())

def extract_numbers(text):
    """Return list of integers found in text."""
    numbers = []
    for part in text.split():
        if part.isdigit():    # only collects pure integer words
            numbers.append(int(part))
    return numbers

def analyze_text(text):
    """Perform text-based arithmetic analysis."""
    chars = count_characters(text)
    words = count_words(text)
    nums = extract_numbers(text)

    total = sum(nums) if nums else 0
    average = total / len(nums) if nums else 0

    return chars, words, nums, total, average

if __name__ == "__main__":
    text_input = input("Enter text to analyze: ")

    chars, words, nums, total, average = analyze_text(text_input)

    print("\n--- Analysis Summary ---")
    print(f"Non-space characters: {chars}")
    print(f"Word count: {words}")
    print(f"Numbers found: {nums}")
    print(f"Sum of numbers: {total}")
    print(f"Average of numbers: {average:.2f}")
