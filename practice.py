
"""this script compares two text documents to detect plagiarism.
it calculates similarity score, identifies common words
and allows the user to search for words within the documents"""
import os
import string
from collections import Counter

#added some extremely common words to this list such as a, is, etc. where they don't can unique and can affect the plagiarism score.by removing the score is more accurate

STOP_WORDS = [
    'a', 'an', 'the', 'and', 'or', 'in', 'on', 'at', 'is', 'are', 'was', 'were',
    'it', 'of', 'for', 'to', 'with', 'i', 'you', 'he', 'she', 'they', 'that',
    'but', 'by', 'as', 'if'
]

class PlagiarismDetector:
    """
    class that reads and analyzes two essays for common words and calculates plagiarism.
    """

    def __init__(self, file1_path, file2_path):
        """
        initializes the detector by reading and processing two essay files.
        """
        #read and process each file.
        self.words1 = self._read_and_clean(file1_path)
        self.words2 = self._read_and_clean(file2_path)

        #this flag will track if both files were read successfully.
        self.initialized = False

        if self.words1 is not None and self.words2 is not None:
            #counter is used to efficiently count word frequencies.
            self.counter1 = Counter(self.words1)
            self.counter2 = Counter(self.words2)
            #sets used to store unique words.
            self.unique_words1 = set(self.words1)
            self.unique_words2 = set(self.words2)
            #the flag is set to true showing that setup was successful.
            self.initialized = True

        else:
            print("\nERROR: could not initialize the detector due to file reading errors")

    def _read_and_clean(self, file_path, filter_stop_words):

        """reads a text file and converts it to lowercase and remove punctuation and returns a list of words"""

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read().lower()
                # creating a translation to remove the punctuation characters.
                translator = str.maketrans('', '', string.punctuation)
                clean_text = text.translate(translator)
                words = clean_text.split()

                if filter_stop_words:
                    #using a list for an efficient way to filter the words.
                    words = [word for word in words if word not in STOP_WORDS]
                return words

            # error handling
        except FileNotFoundError:
            print(f"ERROR: The file '{file_path}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file '{file_path}': {e}")
            return None

    def plagiarism_percentage(self):
        """
        Calculate plagiarism based on the formula.
        Formula:(Number of Common Words / Total Unique Words) * 100
        """

        if not self.initialized:
            print("Cannot perform calculation; detector is not initialized.")
            return

        intersection = self.unique_words1.intersection(self.unique_words2)
        union = self.unique_words1.union(self.unique_words2)

        # check to prevent division by zero, Error if both files are empty.
        percentage = (len(intersection) / len(union)) * 100 if union else 0.0

        print("\n--- PLAGIARISM ANALYSIS ---")
        print(f"Unique words in Essay 1: {len(self.unique_words1)}")
        print(f"Unique words in Essay 2: {len(self.unique_words2)}")
        print(f"Common unique words (intersection): {len(intersection)}")
        print(f"Total unique words (Union): {len(union)}")
        print(f"\nFormula: (intersection / union) * 100")
        print(f"Plagiarism Percentage: {percentage:.2f}%")

        print("\n--- CONCLUSION ---")
        if percentage >= 50:
            print(f"Result: Plagiarism DETECTED (Score is >= 50%).")
        else:
            print(f"Result: No Plagiarism Detected (Score is < 50%).")

    def find_common_words(self):
        """ identifies and prints words that appear in both essays."""
        if not self.initialized:
            print("Cannot perform calculation; detector is not initialized.")
            return

        print("\n---COMMON WORDS ANALYSIS---")
        common_words = self.unique_words1.intersection(self.unique_words2)

        if not common_words:
            print("\nNo common words were found between the two essays.")
            return

        print(f"found {len(common_words)} common words:\n")

        #sorting the list to ensure that the output is easy to read.
        for word in sorted(list(common_words)):
            print(f"- '{word}': Appears {self.counter1[word]} time(s) in Essay 1 and {self.counter2[word]} time(s) in Essay 2.")


    def search_for_word(self):
        """
        Prompts the user to enter a word and displays its frequency in both essays.
        """
        if not self.initialized:
            print(f"Can not search for word; detector is not initialized.")
            return

        word_to_search = input("\nEnter a word to search for: ").strip().lower()
        #input validation to ensure that the user entered something.
        if not word_to_search:
            print("Error: No word entered. Please try again.")
            return

        count1 = self.counter1.get(word_to_search, 0)
        count2 = self.counter2.get(word_to_search, 0)

        print("\n--- SEARCH RESULTS ---")

        if count1 == 0 and count2 == 0:

            print(f"The word '{word_to_search}' was not found in either essay.")

        else:
            print(f"The word '{word_to_search}' appears:")
            print(f"- {count1} time(s) in Essay 1.")
            print(f"- {count2} time(s) in Essay 2.")




def get_file_path_from_user(prompt):
    """
    Prompts the user for a file path and validates that the file exists.
    This function will loop until a valid file path is provided.
    """
    while True:
        path = input(prompt)
        # os.path.exists() is a reliable way to check for a file.
        if os.path.exists(path):
            return path
        else:
            # Provides informative feedback to the user.
            print("File not found at that path. Please check the name and try again.")


def main_menu():
    """
    The main function to run the application's command-line interface.
    """
    print("\n" + "="*30)
    print("   PLAGIARISM DETECTOR   ")
    print("="*30)

    # --- Step 1: Get file paths from the user ---
    print("\nPlease provide the file paths for the essays to be compared.")
    file1 = get_file_path_from_user("Enter path for the first essay (e.g., essay1.txt): ")
    file2 = get_file_path_from_user("Enter path for the second essay (e.g., essay2.txt): ")

    # --- Step 2: Ask about stop word filtering ---
    use_stops = input("Do you want to filter out common 'stop words' for higher accuracy? (yes/no): ").strip().lower()
    filter_enabled = use_stops in ['yes', 'y']

    # --- Step 3: Initialize the detector ---
    detector = PlagiarismDetector(file1, file2, use_stop_words=filter_enabled)

    # --- Step 4: Run the main menu loop ---
    if detector.initialized:
        while True:
            print("\n--- MENU ---")
            print("1. Calculate Plagiarism Score")
            print("2. Show Common Words Report")
            print("3. Search for a Specific Word")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                detector.plagiarism_percentage()
            elif choice == '2':
                detector.find_common_words()
            elif choice == '3':
                detector.search_for_word()
            elif choice == '4':
                print("Exiting program. Goodbye!")
                break
            else:
                # Handles invalid menu choices gracefully.
                print("Invalid choice. Please enter a number between 1 and 4.")

    try:
        with open("essay1.txt", "w") as f1:
            f1.write("""Python is a widely-used programming language.
                         It is popular in web development and data science.""")
        with open("essay2.txt", "w") as f2:
            f2.write("""Programming in Python is useful for web development.
                         Python is also widely used in data science projects.""")
    except Exception as e:
        print(f"Could not create demo files: {e}")

    print("\n==============================")
    print("   PLAGIARISM DETECTOR   ")
    print("==============================")

    # Create an instance of the detector.
    detector = PlagiarismDetector("essay1.txt", "essay2.txt")

    # Run the analysis methods only if initialization was successful.
    if detector.initialized:
        detector.plagiarism_percentage()
        detector.find_common_words()
        detector.search_for_word()

# Run the program
if __name__ == "__main__":
    main_menu()
