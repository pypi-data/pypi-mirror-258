class ProductFilter:
    OPERATORS = ["lt", "le", "gt", "ge", "eq", "ne"]
    LOGICAL_OPERATORS = ["and", "or"]
    DATE_FUNCTIONS = ["year", "month", "day", "hour", "minute", "second"]
    MATH_FUNCTIONS = ["floor", "ceiling"]

    def __init__(self):
        self.filter = ""

    def add_filter(self, attribute: str, operator: str, value: str, logical_operator="and", quote_value=True):
        if operator not in self.OPERATORS:
            raise ValueError(f"Invalid operator {operator}. Must be one of {self.OPERATORS}")

        if logical_operator not in self.LOGICAL_OPERATORS:
            raise ValueError(f"Invalid logical operator {logical_operator}. Must be one of {self.LOGICAL_OPERATORS}")

        # Wrap value with single quotes if quote_value is True
        value = f"'{value}'" if quote_value else value

        if self.filter:
            self.filter += f" {logical_operator} {attribute} {operator} {value}"
        else:
            self.filter += f"{attribute} {operator} {value}"


    def add_date_function_filter(self, function_name: str, attribute: str, value: str, logical_operator="and"):
        if function_name not in self.DATE_FUNCTIONS:
            raise ValueError(f"Invalid date function {function_name}. Must be one of {self.DATE_FUNCTIONS}")

        if logical_operator not in self.LOGICAL_OPERATORS:
            raise ValueError(f"Invalid logical operator {logical_operator}. Must be one of {self.LOGICAL_OPERATORS}")       

        if self.filter:
            self.filter += f" {logical_operator} {function_name}({attribute}) eq {value}"
        else:
            self.filter += f"{function_name}({attribute}) eq {value}"

    def add_math_function_filter(self, function_name: str, attribute: str, value: str, logical_operator="and"):
        if function_name not in self.MATH_FUNCTIONS:
            raise ValueError(f"Invalid math function {function_name}. Must be one of {self.MATH_FUNCTIONS}")

        if logical_operator not in self.LOGICAL_OPERATORS:
            raise ValueError(f"Invalid logical operator {logical_operator}. Must be one of {self.LOGICAL_OPERATORS}")

        if self.filter:
            self.filter += f" {logical_operator} {function_name}({attribute}) eq {value}"
        else:
            self.filter += f"{function_name}({attribute}) eq {value}"

    def get_filter(self) -> str:
        return self.filter
