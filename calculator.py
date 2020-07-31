""" S M A R T    C A L C U L A T O R
# Owner            : https://github.com/veena-LINE
# Python build     : 3.8.1
# Last Modified    :
# File Created     : 2020 Jul 29
# File History     : 2020 Jul 29 - File created
"""

import re
from colorama import init, deinit, Fore, Style, Back


class Calculator:
    """ A Smart Calculator that can....
     * Perform arithmetic calculations with/without variables
     * Supports variables assignment
     * Supports parenthesis for more complex calculations
     * Peek at the stored variables
     * Reset memory without quitting the session
     """

    variables = {}  # Memory of assigned variables
    EXIT = '/exit'
    HELP = '/help'
    PROCEED = '/proceed'
    MEMORY = '/m'
    RESET_MEMORY = '/rm'
    __ultimatum = {'/': Fore.RED + "Unknown command",
                   'uc': Fore.RED + "Unknown command",
                   'ie': Fore.RED + "Invalid expression",
                   'uv': Fore.RED + "Unknown variable",
                   'ia': Fore.RED + "Invalid assignment",
                   'ii': Fore.RED + "Invalid identifier",
                   'ma': Fore.RED + "Multiple assignment not supported",
                   'rm': Fore.RED + "! Memory Reset !",
                   'me': Fore.RED + "! Memory Empty !",
                   HELP: f"Assign variables, one at a time ->"
                         f"{Fore.LIGHTBLUE_EX + Style.BRIGHT} x = 1{Style.RESET_ALL}"
                         f" and not {Fore.LIGHTBLUE_EX + Style.BRIGHT}x = 1, y = 2{Style.RESET_ALL}\n"
                         f"  Variable names allowed are English Alphabet only ->"
                         f"{Fore.LIGHTBLUE_EX + Style.BRIGHT} two = 2{Style.RESET_ALL}"
                         f" and not {Fore.LIGHTBLUE_EX + Style.BRIGHT}var2 = 2{Style.RESET_ALL}\n"
                         f"  Variable to variable assignment ->"
                         f"{Fore.LIGHTBLUE_EX + Style.BRIGHT} x = y{Style.RESET_ALL}\n"
                         f"  Parenthesis are permitted ->"
                         f"{Fore.LIGHTBLUE_EX + Style.BRIGHT} 10 * (60 + 40){Style.RESET_ALL}"
                         f" and not {Fore.LIGHTBLUE_EX + Style.BRIGHT}10 (60 + 40){Style.RESET_ALL}\n"
                         f"  {Fore.LIGHTBLUE_EX + Style.BRIGHT}x{Style.RESET_ALL}      View variable x's value\n"
                         f"  {Fore.LIGHTBLUE_EX + Style.BRIGHT}/m{Style.RESET_ALL}     Peek calculator's memory\n"
                         f"  {Fore.LIGHTBLUE_EX + Style.BRIGHT}/rm{Style.RESET_ALL}    Reset calculator's memory\n"
                         f"  {Fore.LIGHTBLUE_EX + Style.BRIGHT}/exit{Style.RESET_ALL}  anytime!"
                   }

    def __init__(self):
        self.__IDIV = ['//']
        self.__POW = ['**']
        self.__HIGHER_ORDER = ['^']
        self.__MIDDLE_ORDER = ['*', '//', '%', '/']
        self.__LOWER_ORDER = ['+', '-']
        self.__ARITH_OPERATORS = self.__HIGHER_ORDER + self.__MIDDLE_ORDER + self.__LOWER_ORDER
        self.__ALL_OPERATORS = ['='] + self.__ARITH_OPERATORS
        self.__PARENTHESIS = ['(', ')']
        self.__OPERATORS_EXTRAS = self.__PARENTHESIS + self.__ARITH_OPERATORS
        self.__SPACING = '  '
        self.user_input = ''
        self.ultimatum_code = ''
        self.expression = ''
        self.expression_value = 0

    def __memory(self):
        return "  " + Fore.BLUE+Back.LIGHTBLACK_EX+Style.DIM \
               + "".join(["  " + k + " = " + str(v) + "  " for k, v in Calculator.variables.items()]) \
               + Style.RESET_ALL \
               if self.user_input == self.MEMORY and Calculator.variables\
               else f"{self.__SPACING}{self.__ultimatum['me']}"

    def __memory_reset(self):
        if self.user_input == self.RESET_MEMORY:
            Calculator.variables = {}
            print(f"{self.__SPACING}{self.__ultimatum['rm']}")

    def seek_input(self):
        self.user_input = input("input > ").replace(" ", "")
        return self.user_input

    def make_list(self, expression):
        """ Convert arithmetic expression string into a list.
        :param expression: Cleaned Arithmetic expression
        :return: Arithmetic expression as a list
        """
        idiv = ' IDIV '
        expression = expression.replace(self.__IDIV[0], idiv)
        for e in expression:
            if e in self.__ALL_OPERATORS + self.__PARENTHESIS:
                expression = expression.replace(e, ' ' + e + ' ')
        if self.__HIGHER_ORDER[0] in expression:
            expression = expression.replace(self.__HIGHER_ORDER[0], self.__POW[0])
        expression = expression.replace(idiv.strip(), self.__IDIV[0])
        return expression.split()

    def substitute_variables(self):
        """ Substitute variables if any on the right-side of '='
        :return: Substituted expression list
        """
        expression_list = self.user_input
        idx = expression_list.index('=') if '=' in expression_list else -1
        for i, e in enumerate(expression_list[idx + 1:]):
            expression_list[idx + 1 + i] = str(Calculator.variables.get(e, e))
        return expression_list

    def clean_input(self):
        """
        -- is treated as a +
        excess +'s are converted to a single +
        :return: None
        """
        self.user_input = re.sub(r'(--)+', '+', self.user_input)
        self.user_input = re.sub(r'(\+)+', '+', self.user_input)

    def check_command(self):
        if self.user_input.startswith('/'):
            if self.user_input in (Calculator.EXIT, Calculator.HELP):
                self.ultimatum_code = self.user_input
            else:
                self.ultimatum_code = 'uc'
        else:
            self.ultimatum_code = ''

    def check_negative(self, minus):
        return True \
            if len(minus) > 1 and minus[0] == '-' and minus[1:].isnumeric() \
            else False

    def check_float(self, number):
        return True if number.replace('.', '').isnumeric() else False

    def infix_to_postfix(self):
        infix = self.expression
        postfix, stack = [], []

        for e in infix:
            if e.isnumeric() or self.check_negative(e) or self.check_float(e):
                postfix.append(e)
            elif e == '(':
                stack.append(e)
            elif e in self.__ARITH_OPERATORS + self.__POW:
                if not stack:
                    stack.append(e)
                elif e in self.__HIGHER_ORDER + self.__POW:
                    if stack[-1] in self.__HIGHER_ORDER + self.__POW:
                        postfix.append(stack.pop())
                    elif stack[-1] == '(':
                        stack.pop()
                    stack.append(e)
                elif e in self.__MIDDLE_ORDER:
                    if stack[-1] in (self.__POW + self.__HIGHER_ORDER + self.__MIDDLE_ORDER):
                        postfix.append(stack.pop())
                    elif stack[-1] == '(':
                        stack.pop()
                    stack.append(e)
                elif e in self.__LOWER_ORDER:
                    if stack[-1] in (self.__POW + self.__HIGHER_ORDER + self.__MIDDLE_ORDER + self.__LOWER_ORDER):
                        postfix.append(stack.pop())
                    elif stack[-1] == '(':
                        stack.pop()
                    stack.append(e)
                elif e == ')':
                    pop_stack = True
                    while pop_stack:
                        if e == '(':
                            pop_stack = False
                            stack.pop()
                        postfix.append(stack.pop())
        while stack:
            postfix.append(stack.pop())
        return postfix

    def postfix_to_value(self, postfix):
        stack = []
        for p in postfix:
            if p.isnumeric() or self.check_negative(p) or self.check_float(p):
                stack.append(p)
                continue
            r_value, l_value = str(stack.pop()), str(stack.pop())
            lpr = l_value + p + r_value
            try:
                stack.append(eval(lpr))
            except SyntaxError:
                self.ultimatum_code = 'ie'
                return
        if len(stack) == 1:
            value = stack[0]
            self.expression_value = int(value) if int(value) == float(value) else round(value, 2)

    def check_expression(self):
        """ User expression is processed for assignment/calculation
         all while validating for correctness
        :return: None
        """
        # Variable ?
        if self.user_input.isalpha():
            if self.user_input in Calculator.variables:
                print(self.__SPACING + str(Calculator.variables[self.user_input]))
            else:
                self.ultimatum_code = 'uv'
            return

        # Cannot be a variable !
        if self.user_input.isalnum():
            if self.user_input in Calculator.variables:
                print(Calculator.variables[self.user_input])
            else:
                self.ultimatum_code = 'ii'
            return

        # '=' at either end
        if self.user_input[0] == '=' or self.user_input[-1] == '=':
            self.ultimatum_code = 'ia'
            return

        # LONE OPERATORS at either end
        if self.user_input[0] in self.__MIDDLE_ORDER + self.__HIGHER_ORDER \
                or self.user_input[-1] \
                in self.__LOWER_ORDER + self.__MIDDLE_ORDER + self.__HIGHER_ORDER:
            self.ultimatum_code = 'ie'
            return

        # ** and /// CHECK
        if '**' in self.user_input or self.user_input.count('///'):
            self.ultimatum_code = 'ie'
            return

        # CHECK the FIRST PARENTHESIS | PARENTHESIS COUNT
        if (self.user_input.find('(') > self.user_input.find(')')) \
                or (self.user_input.count('(') - self.user_input.count(')')):
            self.ultimatum_code = 'ie'
            return

        self.clean_input()

        expression_operators = {}
        for ui in self.user_input:
            if ui in self.__ALL_OPERATORS:
                if ui in expression_operators:
                    expression_operators[ui] += 1
                else:
                    expression_operators[ui] = 1

        self.user_input = self.make_list(self.user_input)
        self.user_input = self.substitute_variables()

        if expression_operators.get('=', -1) == -1:
            # UNRESOLVED VARIABLES ?
            for ui in self.user_input:
                if ui.isalpha():
                    self.ultimatum_code = 'ie'
                    return
        else:
            idx_l, idx_r, max_lim = 0, 0, -1
            for _ in range(expression_operators['='] - (1 if expression_operators['='] > 1 else 0)):
                for i, ui in enumerate(self.user_input[0:max_lim]):
                    if ui == '=':
                        idx_l = idx_r
                        idx_r = i

                max_lim = idx_r - 1
                val = ''.join(self.user_input[idx_r + 1:])
                # UNRESOLVED VARIABLES after an '=' ?
                for ui in val:
                    if ui.isalpha():
                        self.ultimatum_code = 'ie'
                        break

                if not self.ultimatum_code:
                    # VARIABLE before an '=' ?
                    var = ''.join(self.user_input[(idx_l + 1 if idx_l > 0 else idx_l):idx_r])
                    try:
                        val = eval(val)
                    except SyntaxError:
                        self.ultimatum_code = 'ie'
                        break

                    if var.isalnum() and not var.isalpha():
                        self.ultimatum_code = 'ii'
                        break
                    elif var.isalpha():
                        Calculator.variables[var] = int(val) if int(val) == float(val) else round(val, 2)
                    else:
                        self.ultimatum_code = 'ie'
            return

        self.expression = self.user_input.copy()
        self.evaluate_expression()

    def ultimatum(self):
        self.check_command()
        if not self.ultimatum_code:
            self.check_expression()
        return Calculator.__ultimatum.get(self.ultimatum_code, Calculator.PROCEED)

    def evaluate_expression(self):
        try:
            if not self.ultimatum_code:
                expression_postfix = self.infix_to_postfix()
                self.postfix_to_value(expression_postfix)
                self.custom_display(left=''.join(self.user_input), right=self.expression_value)
        except ZeroDivisionError:
            print(Fore.RED + self.__SPACING + 'Division by Zero!')
        finally:
            self.reset()

    def custom_display(self, left, right, sep='='):
        if right in ['', None]:
            print(f"{self.__SPACING}{left} {sep} {Style.BRIGHT} {self.__ultimatum['ie']} ! See /help\n")
        else:
            print(f"{self.__SPACING}{left} {sep} {Style.BRIGHT}{right}\n")

    def reset(self):
        self.expression = ''
        self.expression_value = ''
        self.ultimatum_code = ''

    def main(self):
        while self.seek_input() != Calculator.EXIT:
            # NO INPUT : do nothing
            if len(self.user_input) == 0:
                continue

            # PURE NUMERIC INPUT : echo
            if self.user_input.replace(".", '').isnumeric():
                print(self.__SPACING + calc.user_input, end='\n\n')
                continue

            if self.user_input.count('=') > 1:
                print(self.__SPACING + self.__ultimatum['ma'], end='\n\n')

            if self.user_input == self.MEMORY:
                print(self.__memory(), end='\n\n')
                continue

            if self.user_input == self.RESET_MEMORY:
                self.__memory_reset()
                continue

            # Seal fate!
            ultimatum_response = self.ultimatum()
            if ultimatum_response != Calculator.PROCEED:
                print(self.__SPACING+ultimatum_response, end='\n\n')
                self.reset()
                continue
        else:
            # Don't forget to say Good byes!
            print(""
                  , f"{Style.BRIGHT}Thank you for trying my SMART CALCULATOR!"
                  , f"{Style.BRIGHT} Psst! Don't forget to spread the word!"
                  , sep="\n")

    @staticmethod
    def about():
        print(''
              , f"{Fore.BLACK + Back.LIGHTBLACK_EX + Style.DIM}"
                f" x = 4   y = x   x + y   z = x + y * (5 + 7)   7 * (5 ^x)   a = b + c   c // 10 ".center(80, " ")
              , f"{Style.BRIGHT}S M A R T    C A L C U L A T O R".center(80, " ")
              , ""
              , "Operators and symbols supported".center(80, " ")

              , f"{Fore.BLUE + Style.BRIGHT}"
                f"       +    -    *    /    //    ^       ( )         ="
                f"{Style.RESET_ALL}          alphabetic".center(80, " ")
              , "  add  sub  mul  div  idiv  pow  parenthesis assignment   variable names".center(80, " ")
              , ""
              , f"{Fore.BLUE + Style.BRIGHT}/help    /exit    /m    /rm".center(80, " ")
              , f"{Fore.BLACK + Back.LIGHTBLACK_EX + Style.DIM}"
                f" century=100   decade=10   years=century/decade   months=12   years=1000/months ".center(80, " ")
              , ""
              , sep="\n")


if __name__ == '__main__':
    init(autoreset=True)
    calc = Calculator()

    Calculator.about()
    if __name__ == '__main__':
        calc.main()
    deinit()
