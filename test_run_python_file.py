from functions.run_python_file import run_python_file

# Should print the calculator's usage
print("Result for main.py:")
print(run_python_file("calculator", "main.py"))

# Should run the calculator, gives nasty rendered result
print("Result for main.py with args:")
print(run_python_file("calculator", "main.py", ["3 + 5"]))

# Should run the calculator's tests successfully
print("Results for tests.py:")
print(run_python_file("calculator", "tests.py"))

# Should return an error
print("Results for ../main.py:")
print(run_python_file("calculator", "../main.py"))

# Should return an error
print("Results for nonexistent.py:")
print(run_python_file("calculator", "nonexistent.py"))

# Should return an error, file doesn't end in ".py"
print("Results for lorem.txt:")
print(run_python_file("calculator", "lorem.txt"))