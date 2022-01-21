import sys


def main(output_path, *db_paths):
    print(db_paths)
    print(output_path)


if __name__ == "__main__":
    main(sys.argv[-1], *sys.argv[1:-1])
