import pymorphy2
import csv
import string
import os
import importlib.resources as resources

class Borrowed:
    def __init__(self, words, found_borrowed):
        self._dict = dict(sorted(found_borrowed.items(), key=lambda x: x[1].get("Repeats", 1), reverse=True))  # order by repeats
        self._len = len(words)
        self._bor = sum(len(value["Instances"]) for value in found_borrowed.values())
        self._percent = round(self._bor / self._len * 100, 2)

    @property
    def dict(self):
        return self._dict

    @property
    def len(self):
        return self._len

    @property
    def bor(self):
        return self._bor

    @property
    def percent(self):
        return self._percent


def extract(the_text=None, output_file=None):    
    words = [] # read words from the original text file
    words = read_txt(the_text) if the_text.endswith(".txt") else read_str(the_text)

    # normalize words
    normalized_words = normalize(words)

    # read and store borrowed words from the CSV file
    borrowed_words = load_borrowed()

    # check if normalized word is present in borrowed_words
    found_borrowed = find_borrowed(normalized_words, borrowed_words)

    ready_dictionary = Borrowed(words, found_borrowed) #create instance

    if output_file:
        expanded_output_path = os.path.expanduser(output_file)
        if output_file.endswith(".txt"):
            output_file_txt(expanded_output_path, ready_dictionary)

        elif output_file.endswith(".csv"):
            output_file_csv(expanded_output_path, ready_dictionary)

        else: 
            raise ValueError("Invalid output file format. Supported formats are .txt and .csv.")

    return ready_dictionary


def read_txt(text_file):
    words_from_file = []
    expanded_file_path = os.path.expanduser(text_file)
    with open(expanded_file_path, "r") as file:
        for line in file:
            cleaned_line = ''
            for char in line.replace('ё', 'е'): #pymorphy dictionary not using ё!
                if char.isalnum() or char == '-': #keep alphanumeric or '-' as it might be part of a word
                    cleaned_line += char
                else:
                    cleaned_line += ' '
            words_from_file.extend(cleaned_line.split())
    return words_from_file


def read_str(text_string):
    words_from_string = []
    cleaned_text = the_text.replace('ё', 'е')  # replace 'ё' with 'е'
    cleaned_text = cleaned_text.translate(str.maketrans('', '', string.punctuation.replace('-', '')))  # remove punctuation, excluding '-'
    words_from_string.extend(cleaned_text.split())
    return words_from_string


def normalize(words):
    morph = pymorphy2.MorphAnalyzer()
    normalized_words = {}
    for word in words:
        normalized_word = morph.parse(word)[0].normal_form.lower()
        normalized_words.setdefault(normalized_word, []).append(word)
    return normalized_words


def load_borrowed():
    borrowed_dictionary = resources.files(__name__) / 'borrowed_dictionary.csv'
    borrowed_words = {}
    with open(borrowed_dictionary, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            borrowed_words[row["Key"].lower()] = {"Value": row["Value"], "Origin": row["Origin"], "Repeats": 0}
    return borrowed_words


def find_borrowed(normalized_words, borrowed_words):
    found_borrowed = {}  
    for word, instances in normalized_words.items():
        if word in borrowed_words:
            repeats = len(instances) # count how many times the word is repeated in the text
            borrowed_words[word]["Repeats"] = repeats # add value "Repeats" to key,value pair in borrowed_words
            found_borrowed[word] = borrowed_words[word] 
            found_borrowed[word]["Instances"] = instances #save the list of prenormalized words
    return found_borrowed


def output_file_txt(expanded_output_path, ready_dictionary):
    with open(expanded_output_path, "w", encoding="utf-8") as formatted_file:
        formatted_file.write(f"Out of a total of {ready_dictionary.len} words, {ready_dictionary.bor} are borrowed, comprising {ready_dictionary.percent}% of the total.\n\n")
        for key, value in ready_dictionary.dict.items():
            formatted_file.write(f"{value['Repeats']}x: {key} {value['Value']} – {value['Origin']}.\nВ тексте встречается: {', '.join(value['Instances'])}\n\n")


def output_file_csv(expanded_output_path, ready_dictionary):
    with open(expanded_output_path, "w", encoding="utf-8", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Word", "Value", "Origin", "Repeats", "Instances"])
        for key, value in ready_dictionary.dict.items():
            csv_writer.writerow([key, value["Value"], value["Origin"], value["Repeats"], value["Instances"]])








