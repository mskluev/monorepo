import sys
from data_core import process_data

def main():
    print("Starting fanout app...")
    result = process_data("sample input")
    print(result)

if __name__ == "__main__":
    main()
