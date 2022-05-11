import argparse
from src.data_ingest import load_from_file, save_to_file
from src.preprocessing import (
    remove_tabs, replace_break_line)
from src.transform import greedy_wrap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", default="input.txt", help="File to process")
    parser.add_argument("-o", default="output.txt", help="file to output")
    parser.add_argument("-c", default=40, help="character limit", type=int)
    parser.add_argument(
        "--justify", default=False, help="Justify text", action="store_true")
    args = parser.parse_args()
    input_file = args.i
    output_file = args.o
    character_limit = args.c
    justify = args.justify
    print("\n")
    print("Info:")
    print("-------")
    print(f"\tInput file: {input_file}")
    print(f"\tOutput file: {output_file}")
    print(f"\tCharacter limit: {character_limit}")
    print(f"\tJustify: {justify}")
    print("\n")
    file_txt = load_from_file(input_file)
    print("Original txt")
    print("------------")
    print("\n")
    print(file_txt)
    print("\n")
    print("Preprocessed txt")
    print("----------------")
    print("\n")
    preprocessed_txt = remove_tabs(file_txt)
    preprocessed_txt = replace_break_line(preprocessed_txt)
    print(preprocessed_txt)
    print("\n")
    print("Wrapped txt")
    print("------------")
    print("\n")
    wrapped_txt = greedy_wrap(preprocessed_txt, character_limit, justify)
    print(wrapped_txt)
    print("\n")

    save_to_file(output_file, wrapped_txt)


if __name__ == "__main__":
    main()