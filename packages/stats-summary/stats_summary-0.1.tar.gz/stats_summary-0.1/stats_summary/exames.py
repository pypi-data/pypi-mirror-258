from .exams.second_exam import content as second_exam
from .exams.first_exam import content as first_exam
from .exams.first_list import content as first_list
from .exams.second_list import content as second_list

exams = {
    'first': first_exam,
    'second': second_exam,
    'list1': first_list,
    'list2': second_list,
}
