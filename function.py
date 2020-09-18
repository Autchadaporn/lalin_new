def tranformgrade(grade):
    if grade == "A":
        return 4.00
    if grade == "B+":
        return 3.50
    if grade == "B":
        return 3.00
    if grade == "C+":
        return 2.50
    if grade == "C":
        return 2.00
    if grade == "D+":
        return 1.50
    if grade == "D":
        return 1.00
    if grade == "F":
        return 0.00
    if grade == "W":
        return -1.00
    if grade == 0:
        return 0
