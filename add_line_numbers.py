def add_line_numbers(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for index, line in enumerate(infile, start=1):
            outfile.write(f"{index}: {line}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file.py> <output_file.txt>")
        exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    add_line_numbers(input_file, output_file)
    print(f"Line numbers have been added to '{output_file}'")