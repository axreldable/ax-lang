def get_grade(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


grade1 = get_grade(95)
grade2 = get_grade(75)
grade3 = get_grade(55)

print(grade1, grade2, grade3)
print()
