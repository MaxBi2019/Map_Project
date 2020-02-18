"""
Maksym Bilyk -- All __modules reserved__
"""


def to_end():
    """
    Returns
    -------
    bool
    Provides with quit control
    """
    first = True
    while True:
        if first:
            print("Do you want to exit? [y/n]")
            first = False
        inp = input(">>> ").lower().split()
        inp = "" if not inp else inp[0]
        if inp in ["yes", "y", "no", "n"]:
            if inp in ["yes", "y"]:
                print("How pity")
                return True
            print("Great, lets do a new research\n")
            return False
        print("I didn't get it just type yes or no")
