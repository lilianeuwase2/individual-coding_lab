import string
from collections import Counter


class PlagiarismDetector:
    """
    a class that reads and analyzes two essays for common words and plagiarism.
    """

    def __init__(self, file1_path, file2_path):
        self.words1 = self._read_and_clean(file1_path)
        self.word2 = self._read_and_clean(file2_path)


        if self.words1 and self.word2:
            self.counter1 = Counter(self.words1)
            self.counter2 = Counter(self.word2)
            self.unique1 = set(self.words1)
            self.unique2 = set(self.word2)
            self.initialized = True

        else:
            self.initialized = False
            print("Error. could not initialize due to file reading problems.")



    def _read_and_clean(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text  = f.read().lower()
                translator = str.maketrans('', '', string.punctuation)
                cleaned = text.translate(translator)
                return cleaned.split()

        except Exception as e:
            print(f"failed to read file {file_path}: {e}")
            return None



    def find_common_words(self):
        if not self.initialized:
            return

        print("\n----common words----")
        common = self.unique1.intersection(self.unique2)

        if not common:
            print("no common words found")
            return

        print(f"{len(common)} common words found:\n")
        for word in sorted(common):
            print(f"-'{word}':{self.counter1[word]} time(s) in Essay 1, {self.counter2[word]} time(s) in Essay 2.")


    def search_for_word(self):
        if not self.initialized:
            return
        word = input("\nEnter the word to search: ").strip().lower()

        if not word:
            print("Please enter a valid word.")
            return False

        count1 = self.counter1.get(word, 0)
        count2 = self.counter2.get(word, 0)

        print("\n --- SEARCH RESULTS ---")
        if count1 == o and count2 == 0:
            print("No common words found.")
            return False

        else:
            print(f"the word '{word}' appears: ")
            print(f"- {count1} time(s) in Essay 1.")
            print (f"- {count2} time(s) in Essay 2.")
            return True

    def calculate_plagiarism_percentage(self):
        pass


def calculate_plagiarism_percentage(self):
            if not self.initialized:
                return
            intersection = self.unique1.intersection(self.unique2)
            union = self.unique1.union(self.unique2)

            if not union:
                percentage = 0.0
            else:
                percentage = (len(intersection) / len(union)) * 100


                print("\n--PLAGIARISM ANALYSIS--")
                print(f"unique words in essay 1: {len(self.unique1)}")
                print(f"unique words in essay 2: {len(self.unique2)}")
                print(f"common words: {len(intersection)}")
                print(f"total unique words (union): {len(union)}")
                print(f"\nplagiarism % = ({len(intersection)} / {len(union)}) * 100: {percentage:.2f}%")



            if percentage >= 50:
                print("plagiarism detected.")

            else:
                print("plagiarism not detected.")





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
    print("     PLAGIARISM DETECTOR      ")
    print("==============================")

    detector = PlagiarismDetector("essay1.txt", "essay2.txt")

    if detector.initialized:
        detector.calculate_plagiarism_percentage()
        detector.find_common_words()
        detector.search_for_word()
        


