from mazegenerator.Mazegenerator import MazeGenerator

def main():
    test = MazeGenerator()
    test.generate(42)
    print(test.maze)


main()