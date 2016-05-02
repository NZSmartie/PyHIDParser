import hidparser

if __name__ is '__main__':
    # dumped from a real DS3 controllser
    ds3_desc = bytes([5, 1, 9, 4, 161, 1, 161, 2, 133, 1, 117, 8, 149, 1, 21, 0, 38, 255, 0, 129, 3, 117, 1, 149, 19,
                      21, 0, 37, 1, 53, 0, 69, 1, 5, 9, 25, 1, 41, 19, 129, 2, 117, 1, 149, 13, 6, 0, 255, 129, 3, 21,
                      0, 38, 255, 0, 5, 1, 9, 1, 161, 0, 117, 8, 149, 4, 53, 0, 70, 255, 0, 9, 48, 9, 49, 9, 50, 9, 53,
                      129, 2, 192, 5, 1, 117, 8, 149, 39, 9, 1, 129, 2, 117, 8, 149, 48, 9, 1, 145, 2, 117, 8, 149, 48,
                      9, 1, 177, 2, 192, 161, 2, 133, 2, 117, 8, 149, 48, 9, 1, 177, 2, 192, 161, 2, 133, 238, 117, 8,
                      149, 48, 9, 1, 177, 2, 192, 161, 2, 133, 239, 117, 8, 149, 48, 9, 1, 177, 2, 192, 192])

    ds3 = hidparser.parse(ds3_desc)

    # Print the report groups for the device (which includes input, output and feature collections and their reports
    print(ds3)

    # The pass is for me to set a break point, so i can inspect the ds3 object with my debugger
    pass

