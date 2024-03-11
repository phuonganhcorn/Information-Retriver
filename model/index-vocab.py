import os
import re
from collections import defaultdict

def index_corpus(corpus_dir, output_file):
    # Initialize vocabulary and posting lists
    vocabulary = set()
    posting_lists = defaultdict(list)

    # Regular expression pattern to match special characters
    special_characters_pattern = r'[!?.,$;\'-[\]><&{}@\(\)\"]'

    # Iterate through each document in the corpus directory
    for filename in os.listdir(corpus_dir):
        with open(os.path.join(corpus_dir, filename), 'r', encoding='latin-1') as file:
            content = file.read().lower().split()  # Read content and convert to lowercase
            doc_id = filename.split('.')[0]  # Extract document ID from filename

            # Update vocabulary and posting lists
            for token in content:
                # Remove special characters from the token
                token = re.sub(special_characters_pattern, '', token)
                if token:
                    vocabulary.add(token)
                    posting_lists[token].append(doc_id)

    # Sort vocabulary alphabetically
    sorted_vocabulary = sorted(vocabulary)

    # Write posting lists to the output file
    with open(output_file, 'w') as outfile:
        for token in sorted_vocabulary:
            posting = ' '.join(posting_lists[token])
            outfile.write(f"{token}\t{posting}\n")

def search(index, term):
    if term in index:
        return index[term]
    else:
        return []

def search_and(index, term1, term2):
    posting1 = set(search(index, term1))
    posting2 = set(search(index, term2))
    result = posting1.intersection(posting2)
    return sorted(list(result))

def search_or(index, term1, term2):
    posting1 = set(search(index, term1))
    posting2 = set(search(index, term2))
    result = posting1.union(posting2)
    return sorted(list(result))

def search_and_not(index, term1, term2):
    posting1 = set(search(index, term1))
    posting2 = set(search(index, term2))
    result = posting1.difference(posting2)
    return sorted(list(result))

def search_or_not(index, term1, term2):
    posting1 = set(search(index, term1))
    posting2 = set(search(index, term2))
    result = posting1.symmetric_difference(posting2)
    return sorted(list(result))


if __name__ == "__main__":
    # Define input and output paths
    dir = "/home/phanh/Downloads/study/ir" # Change this with your own directory
    corpus_directory = f"{dir}/reuters/test"
    index_file = f"{dir}/index.txt"

    # Index the corpus and generate the posting lists
    index_corpus(corpus_directory, index_file)
    print("Indexing completed. Posting lists saved to index.txt")

    index = {}
    with open(index_file, 'r') as file:
        for line in file:
            term, postings = line.strip().split('\t')
            index[term] = postings.split()

    # Perform searches based on different query types
    print("Single-term Query:")
    print("america:", search(index, 'america'))

    print("\nTwo-term Query with AND:")
    print("america AND oil:", search_and(index, 'america', 'oil'))

    print("\nTwo-term Query with OR:")
    print("america OR oil:", search_or(index, 'america', 'oil'))

    print("\nTwo-term Query with AND and NOT:")
    print("america AND (NOT oil):", search_and_not(index, 'america', 'oil'))

    print("\nTwo-term Query with OR and NOT:")
    print("america OR (NOT oil):", search_or_not(index, 'america', 'oil'))
