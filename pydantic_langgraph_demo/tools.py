from schema import MathInput

def add_numbers(input: MathInput) -> int:
    return input.a + input.b

def multiply_numbers(input: MathInput) -> int:
    return input.a * input.b
