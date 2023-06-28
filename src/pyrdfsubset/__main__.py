import sys
from pyrdfsubset import rdfsubset

def main():
    if len(sys.argv) > 1:
        shex2dot.main(sys.argv[1:])
    else:
        print("Usage: rdfsubset <shexfile> <rdffile>")

if __name__ == "__main__":
    main()

