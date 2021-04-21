import json, csv, sys, os


def main():
    if len(sys.argv) <= 1:
        raise Exception("No file was provided")

    file_path = os.path.realpath(sys.argv[1])
    output_file = file_path[:-6] + ".csv"

    if not os.path.exists(os.path.dirname(output_file)):
        try:
            os.makedirs(os.path.dirname(output_file))
        except Exception as e:
            print(e)

    # Read jsonl code and convert to rows
    with open(file_path) as f:
        lines = [json.loads(line) for line in f.readlines()]

    fields = list(lines[0].keys())
    rows = [list(line.values()) for line in lines]

    with open(output_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(rows)

    print("Output file: " + output_file)


if __name__ == "__main__":
    main()
