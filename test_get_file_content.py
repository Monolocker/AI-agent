from functions.get_file_content import get_file_content

print("Results for main.py:")
print(get_file_content("calculator", "main.py"))

print("Results for calculator.py:")
print(get_file_content("calculator", "pkg/calculator.py"))

print("Results for cat:")
print(get_file_content("calculator", "/bin/cat"))

print("Results for does_not_exist:")
print(get_file_content("calculator", "pkg/does_not_exist.py"))