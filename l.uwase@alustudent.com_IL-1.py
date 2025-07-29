import string
from collections import Counter


class PlagiarismDetector:

    def __init__(self, file1_path, file2_path):

        self.words1 = self._read_and_clean(file1_path)
        self.words2 = self._read_and_clean(file2_path)

        self.initialized = False

        if self.words1 is not None and self.words2 is not None:
            self.counter1 = Counter(self.words1)
            self.counter2 = Counter(self.words2)
            self.unique_words1 = set(self.words1)
            self.unique_words2 = set(self.words2)
            self.initialized = True

        else:
            print("\nERROR: could not initialize the detector due to file reading errors")

    def _read_and_clean(self, file_path):
        """reads a text file and converts it to lowercase and remove punctuation and returns a list of words"""

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read().lower()
                # creating a translation to remove the punctuation characters.
                translator = str.maketrans('', '', string.punctuation)
                clean_text = text.translate(translator)
                return clean_text.split()

            # error handling
        except FileNotFoundError:
            print(f"ERROR: The file '{file_path}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file '{file_path}': {e}")
            return None

    def plagiarism_percentage(self):

        if not self.initialized:
            return

        intersection = self.unique_words1.intersection(self.unique_words2)
        union = self.unique_words1.union(self.unique_words2)

        if not union:
            percentage = 0.0

        else:
            percentage = (len(intersection) / len(union)) * 100

        print("\n--- PLAGIARISM ANALYSIS ---")
        print(f"Unique words in Essay 1: {len(self.unique_words1)}")
        print(f"Unique words in Essay 2: {len(self.unique_words2)}")
        print(f"Common words (intersection): {len(intersection)}")
        print(f"Total unique words (Union): {len(union)}")
        print(f"\nFormula: (intersection / union) * 100")
        print(f"Plagiarism Percentage: {percentage:.2f}%")

        print("\n--- Final Decision ---")
        if percentage >= 50:
            print(f"Result: Plagiarism DETECTED (Score is >= 50%).")
        else:
            print(f"Result: No Plagiarism Detected (Score is < 50%).")

    def find_common_words(self):
        """ identify common words in both word1 and word2"""
        if not self.is_initialized:
            return

        print("\n-----finding common words-----")
        common_words = self.unique_words1.intersection(self.unique_words2)

        if not common_words:
            print("\nNo common words were found.")
            return
        print(f"found {len(common_words)} common words: \n")

    def search_for_word(self):
        """
          Prompts the user to enter a word and displays its frequency in both essays.
          """
        if not self.is_initialized:
            return

        word = input("\nEnter a word to search for: ").strip().lower()

        if not word:
            print("Error: Please enter a valid word to search.")
            return False

        count1 = self.counter1.get(word, 0)
        count2 = self.counter2.get(word, 0)

        print("\n--- SEARCH RESULTS ---")

        if count1 == 0 and count2 == 0:

            print(f"The word '{word}' was not found in either essay.")
            return False
        else:
            print(f"The word '{word}' appears:")
            print(f"- {count1} time(s) in Essay 1.")
            print(f"- {count2} time(s) in Essay 2.")
            return True


if __name__ == "__main__":

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
    if detector.is_initialized:
        detector.calculate_plagiarism_percentage()
        detector.find_common_words()
        detector.search_for_word()

