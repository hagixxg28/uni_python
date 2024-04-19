from typing import Optional


def add(num1, num2):
    val = 0
    for item in range(num2):
        val += num1
    print(val)


add(2, 5)


def greetings(first_name: Optional[str] = None,
              last_name: Optional[str] = None):
    if first_name is None and last_name is None:
        print("Hello world")
        return
    if first_name is None or last_name is None:
        print("bad bad")
    print('Hello', first_name, last_name)


def average_grades(grades: list[float]) -> [float, float]:
    grades_sum = sum(grades)
    grades_average = grades_sum / len(grades)
    return grades_sum, grades_average


def analyze_class(grades: list[float]) -> [float, float, int]:
    _, grades_average = average_grades(grades=grades)
    max_grade = max(grades)
    max_index = grades.index(max_grade)
    return grades_average, max_grade, max_index
