# calculator_tool.py
class CalculatorToolset:
    def calculate(self, expression: str):
        """
        Evaluates a simple math expression safely.
        Example expression: '2 + 3 * 4'
        """
        try:
            # Only allow safe characters
            allowed_chars = "0123456789+-*/(). "
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression."

            result = eval(expression)  # Use eval safely for controlled input
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception as e:
            return f"Error: {str(e)}"
