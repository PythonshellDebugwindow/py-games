from game import die, main

if __name__ == "__main__":
    try:
        main()
        die()
    except Exception as e:
        print("ERROR", e)
        print("TYPE", type(e))
        die()
    finally:
        print("Bye Bye")
        die()
