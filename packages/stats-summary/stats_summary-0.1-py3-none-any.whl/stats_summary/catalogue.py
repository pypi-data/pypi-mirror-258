from . import tests 
from . import test_comparison_table
from . import inference_basics
from . import exames
from . import prob_dist_integrals

test_index = tests.tests
comparison_table = test_comparison_table.comparison_table
inference_summary = inference_basics.inferential_stats_summary
tailed_tests_differences = inference_basics.tailed_tests_differences
tailed_tests_separate_examples = inference_basics.tailed_tests_separate_examples
tailed_tests_single_example = inference_basics.tailed_tests_single_example
exames = exames.exams
distributions_integrals = prob_dist_integrals.content

class Catalogue:

    @staticmethod
    def list_tests(parametric_only=False, non_parametric_only=False):
        # Assuming test_index is defined elsewhere and accessible
        if parametric_only:
            return [test for test in test_index.keys() if test_index[test].parametric]
        elif non_parametric_only:
            return [test for test in test_index.keys() if not test_index[test].parametric]
        return list(test_index.keys())

    @staticmethod
    def show_usecases():
        print(comparison_table)

    @staticmethod
    def get_test(test_name):
        test_details = test_index.get(test_name, {})
        if test_details is None:
            print(f'Test {test_name} not found')
            return
        elif type(test_details) == dict:
            for key, value in test_details.items():
                print(f'{key}: {value}')

    @staticmethod
    def get_examples(test_name):
        examples = str(test_index.get(test_name, {}).get('examples', ''))
        print(f'[{test_name.upper()} EXAMPLES]\n{examples}')

    @staticmethod
    def get_description(test_name):
        description = str(test_index.get(test_name, {}).get('description', ''))
        print(f'[{test_name.upper()} DESCRIPTION]\n{description}')

    @staticmethod
    def get_formulas(test_name):
        formulas = test_index.get(test_name, {}).get('formulas', '')
        if type(formulas) == list:
            formulas = "\n".join(formulas)
        print(f'[{test_name.upper()} FORMULAS]\n{formulas}')

    @staticmethod
    def get_use_cases(test_name):
        use_cases = test_index.get(test_name, {}).get('use-cases', '')
        if type(use_cases) == list:
            use_cases = "\n".join(use_cases)
        print(f'[{test_name.upper()} USE CASES]\n{use_cases}')

    @staticmethod
    def get_summary(test_name):
        summary = str(test_index.get(test_name, {}).get('summary', ''))
        print(f'[{test_name.upper()} SUMMARY]\n{summary}')

    @staticmethod
    def get_code_snippets(test_name):
        code_snippets = str(test_index.get(test_name, {}).get('code_snippets', ''))
        print(f'[{test_name.upper()} CODE SNIPPETS]\n{code_snippets}')

    @staticmethod
    def get_thorough_examples(test_name):
        thorough_examples = "\n".join(test_index.get(test_name, {}).get('thorough_examples', []))  # Convert list to string
        print(f"[{test_name.upper()} THOROUGH EXAMPLES]\n{thorough_examples}")

    @staticmethod
    def get_exam(exam_name):
        exam = exames.get(exam_name, '')
        print(f'[{exam_name.upper()} EXAM]\n{exam}')

class BasicInference:

    def get_summary():
        print(inference_summary)

    def get_tailed_tests_difference():
        print(tailed_tests_differences)

    def get_tailed_tests_separate_examples():
        print(tailed_tests_separate_examples)

    def get_tailed_tests_single_example():
        print(tailed_tests_single_example)

    def get_integrals():
        print(distributions_integrals)
