'''
This is a program that grades tests from a text file and outputs
the first name, last name, test score, and letter grade to a 
new text file.
'''
import os

ERROR_FILE = 'errors.txt'
GRADE_FILE = 'grades.txt'
TESTS_FILE = 'input_files/tests.txt'
STUDENTS_FILE = 'input_files/students.txt'
GRADE_OUTPUT_TEMPLATE = '{first:15s} {last:15s} {score:5s}  {grade:2s}\n'


def delete_file_if_exists(file_name):
    '''
    Deletes a file if it already exists.
    Input: file_name, the file name to delete
    Output: none
    '''
    if os.path.exists(file_name):
        os.remove(file_name)


def letter_grade(score):
    '''
    Determines the grade of associated with the core that is
    passed as an argument and returns the grade.
    '''
    grade = ''

    grade_scale = {score > 46: 'A', 44 <= score < 46: 'A-',
                   42 <= score < 44: 'B+', 40 <= score < 42: 'B',
                   38 <= score < 40: 'B-', 36 <= score < 38: 'C+',
                   34 <= score < 36: 'C', 32 <= score < 34: 'C-',
                   30 <= score < 32: 'D', score < 30: 'F'}

    for grade_item in grade_scale:
        if grade_item:
            grade = grade_scale[grade_item]

    return grade


def calculate_score(score, formatted_answers, answer_key, index_counter1, index_counter2):
    '''
    Calculates the score by looping over each answer in the list
    and returns the score and counter.
    '''
    correct = 1
    incorrect = -0.25
    empty = 0

    for grade_item in answer_key:
        if grade_item == formatted_answers[index_counter1][1][index_counter2]:
            score += correct
            index_counter2 += 1

        elif formatted_answers[index_counter1][1][index_counter2] == ' ':
            score += empty
            index_counter2 += 1

        else:
            score += incorrect
            index_counter2 += 1

    return score, index_counter2


def format_list_answers(test_answers, formatted_answers):
    '''
    Formats the answers by removing the newline and splitting
    the list at the colon and every comma
    '''
    counter = 0

    while counter < len(test_answers):
        test_answers[counter] = test_answers[counter].rstrip('\n')
        test_answers[counter] = test_answers[counter].split(';')
        counter += 1
    return test_answers, formatted_answers


def format_list_students(students):
    '''
    Formats the student file by putting each item in the file
    into a list as a list item
    '''
    counter = 0

    while counter < len(students):
        students[counter] = students[counter].rstrip('\n')
        students[counter] = students[counter].split(' ')
        counter += 1
    return students


def write_to_grade_file(formatted_students, formatted_answers, grade_infile,
                        error_infile, answer_key, score, message):
    '''
    loops over every item in the list of formatted answers
    and changes the index of list. Then writes the Names, score, and grade to the file.
    '''
    counter = 0
    stud_counter = 0

    index_counter1 = 1
    index_counter2 = 0

    while counter < len(formatted_answers):
        answer_items = 0

        while answer_items < len(formatted_answers):
            score, index_counter2 = calculate_score(
                score, formatted_answers, answer_key, index_counter1, index_counter2)
            if index_counter1 < len(formatted_answers)-1:
                index_counter1 += 1
            index_counter2 = 0
            grade = letter_grade(score)

            if stud_counter < len(formatted_students):

                first_name = formatted_students[stud_counter][1]
                last_name = formatted_students[stud_counter][2]
                score = str(score)

                grade_infile.writelines(GRADE_OUTPUT_TEMPLATE.format(
                    first=first_name, last=last_name, score=str(score), grade=grade))
                score = 0
                stud_counter += 1

            answer_items += 1

            counter += 1
    error_infile.writelines(message)  # write errors to file.
    grade_infile.close()
    return formatted_students, answer_key, score


def validate_id(formatted_students, message):
    '''
    Validates the student's ID. if Id is not valid, it will be saved
    and written to the error.txt file. Checks entire file for errors before
    writing to files.
    '''
    counter = 0
    stud_id = []

    while counter < len(formatted_students):
        stud_id = [i for i in formatted_students[counter][0]]

        if stud_id == formatted_students[counter]:
            message += formatted_students[counter][0]

        if len(formatted_students[counter][0]) != 6:
            message += formatted_students[counter][0] + \
                ' is invalid: ID is not 6 characters in length.\n'

        if not (stud_id[0].isalpha() and stud_id[1].isalpha()):
            message += formatted_students[counter][0] + \
                ' is invalid: The first two characters must be letters.\n'

        digit_counter = 2
        while digit_counter < len(stud_id):
            if not stud_id[digit_counter].isdigit():
                message += formatted_students[counter][0] + \
                    ' is invalid: The last four characters must be numbers.\n'
                digit_counter += len(stud_id)
            digit_counter += 1

        unique_char = list(dict.fromkeys(stud_id))

        if unique_char != stud_id:
            message += formatted_students[counter][0] + \
                ' is invalid: The characters in the ID are not unique.\n'

        counter += 1
    return message


def open_error_file():
    '''
    Checks if file is already created and deletes it if it is.
    Creates and opens the errors file to write to it.
    '''
    delete_file_if_exists(ERROR_FILE)

    error_infile = open(ERROR_FILE, 'w')

    return error_infile


def open_tests_file():
    '''
    Opens tests file
    '''
    infile = open(TESTS_FILE, 'r')
    test_answers = infile.readlines()

    infile.close()

    return test_answers


def open_students_file():
    '''
    Opens students file
    '''
    student_infile = open(STUDENTS_FILE, 'r')
    students = student_infile.readlines()

    student_infile.close()

    return students


def open_grade_file():
    '''
    Checks if file is already created and deletes it if it is.
    Creates and opens the grade file to write to it.
    '''
    delete_file_if_exists(GRADE_FILE)

    grade_infile = open(GRADE_FILE, 'w')

    grade_infile.writelines(GRADE_OUTPUT_TEMPLATE.format(
        first='First Name', last='Last Name', score='Score', grade='Grade'))

    grade_infile.writelines('============================================\n')
    return grade_infile


def main():
    '''
    Controls the process of grading student tests.
    '''
    score = 0.0

    test_answers = open_tests_file()
    formatted_answers = []

    format_list_answers(test_answers, formatted_answers)

    formatted_answers = test_answers

    answer_key = formatted_answers[0][1]

    grade_infile = open_grade_file()

    students = open_students_file()

    formatted_students = []

    format_list_students(students)

    formatted_students = students

    error_infile = open_error_file()

    message = ''

    message = validate_id(formatted_students, message)

    write_to_grade_file(formatted_students, formatted_answers, grade_infile, error_infile,
                        answer_key, score, message)


if __name__ == '__main__':
    main()
