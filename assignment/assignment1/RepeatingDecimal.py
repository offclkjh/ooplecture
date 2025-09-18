import math
import re

########################################################
# TODO: MUST REPLACE THIS WITH YOUR STUDENT ID
student_id = "2025150001"  # Replace with your student ID
########################################################

class RepeatingDecimal:
    # TODO: IMPLEMENT THIS CONSTRUCTOR (Place for definition)
    def __init__(self, sign, int_part, non_repeat, repeat):
        """
        Initializes a RepeatingDecimal object.
        The number being represented is of the form: (sign) int_part.non_repeat[repeat part] (Note: the reason we use integers for int_part and non_repeat is to avoid floating point precision issues)
        Make sure that all the member variables are private to avoid accidental modification.
        It may be wise to clean up after setting the variables using the cleanup method (which you also have to implement below)
        :param sign: The sign of the number (1 for positive and 0, -1 for negative)
        :param int_part: The integer part of the number, excluding the sign (nonnegative integer)
        :param non_repeat: The non-repeating digits after the decimal point as a list of digits (if there are no non-repeating digits after the decimal point, should be an empty array, [])
        :param repeat: The repeating digits after the decimal point as a list of digits (if there are no repeating digits after the decimal point, should be an empty array, [])
        """
        # TODO: IMPLEMENT THE BODY OF THE CONSTRUCTOR (Probably < 10 lines of code)
        self.__sign = 1 if sign == 1 else -1
        self.__int_part = int_part
        self.__non_repeat = non_repeat
        self.__repeat = repeat
        self.cleanup()


    @classmethod
    def fromString(cls, s):
        """
        Creates a RepeatingDecimal object from a string representation. (of the format sign int_part.non_repeat[repeat part], no commas included)
        The string should be in the format: sign int_part.non_repeat[repeat part]
        This code should be helpful in debugging your code.
        :param s: The string representation of the RepeatingDecimal
        :return: A RepeatingDecimal object
        """
        pattern = r'^([+-]?)(\d+)(?:\.(\d*?))?(?:\[(\d+)\])?$'
        match = re.fullmatch(pattern, s.strip())

        sign_str, int_part, non_repeat, repeat = match.groups()

        sign = -1 if sign_str == '-' else 1
        int_part = int(int_part)
        non_repeat = [int(d) for d in (non_repeat or "")]
        repeat = [int(d) for d in (repeat or "")]

        return cls(sign, int_part, non_repeat, repeat)


    def cleanup(self):
        """
        Performs any carryover operations leading to >10 or <0 numbers in the digits in non_repeat and repeat needed to ensure the RepeatingDecimal is in a valid state (e.g., [-1] is converted to [8], [10] is converted to [1]).
        Also, ensures that the repeat is minimal (i.e., repeat is not [3,3], but just [3]) and absorbs any repeating digits from non_repeat.
        Ensure that the repeat [0], [9] are handled as well. (e.g., (0).[9] should be converted to just (1)), and remove any trailing zeros from non_repeat if there is no repeat.
        Be especially aware of the case when the integer part becomes negative, since it can lead to a second round update of non_repeat and repeat.
        """
        # TODO: IMPLEMENT THE BODY OF THE CLEANUP METHOD (The solution is about 70-80 lines of code with comments and spacing)
        def forwardcarrier(deminum, carrier):
            """
            internal function for remaining only 0 ~ 9 and carrying exceeding numbers
            """
            demicalset = []
            settotal = 0
            for i, num in enumerate(reversed(deminum)):
                settotal += num * 10 ** i
            settotal += carrier
            if settotal < 0:
                for i in range(len(deminum)):
                    demicalset.insert(0, int(str(10**(len(str(settotal)) - 1) + settotal)[-i - 1]))
                    carrier = int(settotal/10**len(deminum)) - 1
            elif settotal > 0:
                if len(str(settotal)) > len(deminum):
                    for i in range(len(deminum)):
                        demicalset.insert(0, int(str(settotal)[-i - 1]))
                    carrier = int(str(settotal)[:-len(deminum)])
                else:
                    for i in range(len(deminum)):
                        if i < len(str(settotal)):
                            demicalset.insert(0, int(str(settotal)[-i - 1]))
                        else:
                            demicalset.insert(0, 0)
                    carrier = 0
            else:
                return [], carrier

            return demicalset, carrier

        # remain only 0 ~ 9
        demicalsetlist = []
        demicalset = []
        carrier = [0, None]
        if len(self.__repeat) == 1:
            self.__repeat *= 2
        while carrier[0] != carrier[1]:
            carrier[1] = carrier[0]
            demicalset, carrier[0] = forwardcarrier(self.__repeat, carrier[0])
            if not demicalset:
                break
            demicalsetlist.append(demicalset)
        self.__repeat = demicalset
        # reduce unnecessary decimal repeat expression
        for n in range(len(self.__repeat)):
            if not len(self.__repeat) % (n + 1):
                div = [self.__repeat[i:i + n + 1] for i in range(0, len(self.__repeat), n + 1)]
                if all(i == div[0] for i in div):
                    self.__repeat = div[0]
        if self.__repeat == [0]:
            self.__repeat = []
        elif self.__repeat == [9]:
            self.__repeat = []
            carrier += 1
        # remain only 0 ~ 9
        self.__non_repeat, carrier[0] = forwardcarrier(self.__non_repeat, carrier[0])
        # reduce unnecessary decimal expression
        if not self.__repeat:
            for i in range(len(self.__non_repeat) - 1, -1, -1):
                if i == 0:
                    del self.__non_repeat[0]
        # consider absorbing part
        else:
            i = 0
            for i, num in enumerate(reversed(self.__non_repeat)):
                k = i % len(self.__repeat)
                if self.__repeat[-(k + 1)] != num:
                    break
            if i > 0 and len(self.__repeat) != 1:
                self.__non_repeat = self.__non_repeat[:-i]
                for k in range(i % len(self.__repeat)):
                    self.__repeat.append(self.__repeat[0])
                    del self.__repeat[0]
        self.__int_part += carrier[0]
        # correct sign
        if self.__int_part < 0:
            self.__sign *= -1
            if not (self.__repeat or self.__non_repeat):
                self.__int_part = self.__int_part * -1
                return
            self.__int_part = self.__int_part * -1 - 1
            if not self.__repeat:
                self.__non_repeat[-1] = 10 - self.__non_repeat[-1]
                for i in range(len(self.__non_repeat) - 1):
                    self.__non_repeat[i] = 9 - self.__non_repeat[i]
            else:
                for i in range(len(self.__non_repeat)):
                    self.__non_repeat[i] = 9 - self.__non_repeat[i]
            for i in range(len(self.__repeat)):
                self.__repeat[i] = 9 - self.__repeat[i]


    # TODO: IMPLEMENT THE FOLLOWING OPERATION OVERLOADING METHODS

    # TODO: SIGN NEGATION HEADER (i.e., -x unary operator)
    def __neg__(self):
        """
        Returns a new RepeatingDecimal object with the sign negated.
        """
        # TODO: IMPLEMENT THE BODY OF THE SIGN NEGATION METHOD (The solution is about 1 line of code)
        return RepeatingDecimal(self.__sign * -1, self.__int_part, self.__non_repeat, self.__repeat)


    # TODO: ADDITION HEADER (i.e., x + y binary operator)
    def __add__(self, other):
        """
        Adds two RepeatingDecimal objects and returns a new RepeatingDecimal object.
        """
        # TODO: IMPLEMENT THE BODY OF THE ADDITION METHOD (The solution is about 20-25 lines of code with comments and spacing)
        dec1, dec2 = (self, other) if len(self.__non_repeat) > len(other.__non_repeat) else (other, self)
        sign = [1, 1]
        if dec1.__sign == -1:
            sign[0] = -1
        if dec2.__sign == -1:
            sign[1] = -1
        int_part = dec1.__int_part * sign[0] + dec2.__int_part * sign[1]
        non_repeat = [i * sign[0] for i in dec1.__non_repeat]
        p = 0
        for i in range(len(dec2.__non_repeat)):
            non_repeat[i] += dec2.__non_repeat[i] * sign[1]
            p += 1
        while p < len(non_repeat) and dec2.__repeat:
            non_repeat[p] += dec2.__repeat[p % len(dec2.__repeat)] * sign[1]
            p += 1
        repeat = []
        if not dec1.__repeat and not dec2.__repeat:
            pass
        elif not dec1.__repeat:
            for i in range(len(dec2.__repeat)):
                repeat.append(dec2.__repeat[(i + p) % len(dec2.__repeat)] * sign[1])
        elif not dec2.__repeat:
            for i in range(len(dec1.__repeat)):
                repeat.append(dec1.__repeat[i] * sign[0])
        else:
            for i in range(len(dec1.__repeat) * len(dec2.__repeat)):
                repeat.append(dec1.__repeat[i % len(dec1.__repeat)] * sign[0] + dec2.__repeat[(i + p) % len(dec2.__repeat)] * sign[1])

        return RepeatingDecimal(1, int_part, non_repeat, repeat)


    # TODO: SUBTRACTION HEADER (i.e., x - y binary operator)
    def __sub__(self, other):
        """
        Subtracts another RepeatingDecimal object from this one and returns a new RepeatingDecimal object.
        """
        # TODO: IMPLEMENT THE BODY OF THE SUBTRACTION METHOD (The solution is about 1 line of code, but can also take it in another direction with more lines of code)
        return self + (-other)


    # TODO: STRING REPRESENTATION HEADER -- THIS ONE IS OPTIONAL, BUT CAN BE HELPFUL FOR DEBUGGING
    def __str__(self):
        """
        Returns a string representation of the RepeatingDecimal.
        The format is: sign int_part.non_repeat[repeat part]
        If the non_repeat or repeat parts are empty, they are omitted (along with the decimal point if both are empty).
        """
        # TODO: IMPLEMENT THE BODY OF THE STRING REPRESENTATION METHOD (The solution is about 5-10 lines of code)
        return f"{"+" if self.__sign == 1 else "-"}({self.__int_part}).{str(self.__non_repeat)[1:-1].replace(" ", "")}[{str(self.__repeat)[1:-1].replace(" ", "")}]"


    def __mul__(self, other):
        # case: other is integer
        if not other.__repeat and not other.__non_repeat:
            if other.__int_part == 0:
                return 0
            else:
                non_repeat, repeat = [], []
                for i in self.__non_repeat:
                    non_repeat.append(i * other.__int_part)
                for i in self.__repeat:
                    repeat.append(i * other.__int_part)
                return RepeatingDecimal(self.__sign, self.__int_part * other.__int_part, non_repeat, repeat)
        if not self.__repeat and not self.__non_repeat:
            return other * self
        # delete non-repeat part temporarily
        print(self)
        if self.__non_repeat:
            return ((self * RepeatingDecimal(1, 10 ** len(self.__non_repeat), [], [])) * other) / RepeatingDecimal(1, 10 ** len(self.__non_repeat), [], [])
        if other.__non_repeat:
            return (self * (other * RepeatingDecimal(1, 10 ** len(other.__non_repeat), [], []))) / RepeatingDecimal(1, 10 ** len(other.__non_repeat), [], [])

        sum = RepeatingDecimal(1, 0, [], [])
        # int * int
        sum += self.__int_part * other.__int_part
        # int * repeat
        for int_part, repeat in [(self.__int_part, other.__repeat), (other.__int_part, self.__repeat)]:
            if not int_part or not repeat:
                break
            for i in range(len(repeat)):
                repeat[i] *= int
            sum += RepeatingDecimal(1, 0, [], repeat)
        # repeat * repeat
        # ex : 0.[6] * 0.[4] --> 0.[6 * 0.[4]], 0.[24] + 0.0[24] + 0.00[24] + 0.000[24] / is this possible?
        len1, len2 = len(self.__repeat), len(other.__repeat)
        if len1 and len2:
            settotal1 = 0
            for i, num in enumerate(reversed(self.__repeat)):
                settotal1 += num * 10 ** i
            settotal2 = 0
            for i, num in enumerate(reversed(other.__repeat)):
                settotal2 += num * 10 ** i
            repnum = settotal1 * settotal2
            repeat = []
            for i in range(len2):
                repeat.insert(0, repnum % (10 ** (i+1)))
            sum += RepeatingDecimal(1, 0, [], repeat) * (10 ** len1) / ((10 ** len1) - 1)


        sum.__sign *= (self.__sign * other.__sign)
        return sum


    def __truediv__(self, other):
        # a / b --> a * (1 / b), a / 10 ** n --> int part to non-repeat part
        if other.__int_part == 0 and not other.__non_repeat and not other.__repeat:
            raise ZeroDivisionError
        # 1 / b
        repset = [1]
        result = []
        index = 0
        for i in repset:
            rest = 0
            resnum = 0
            j = 1
            while True:
                if other * RepeatingDecimal(1, j, [], []) > i:
                    resnum, rest = j -1, (i - other * RepeatingDecimal(1, j, [], [])) * RepeatingDecimal(1, 10, [], [])
                    break
                j += 1
            result.append(resnum)
            if rest in repset:
                index = repset.index(rest)
                break
            else:
                repset.append(rest)
        return self * RepeatingDecimal(other.__sign, result[0], result[1:index], result[index:])

if __name__ == "__main__":
    # IF YOU WANT TO TEST YOUR CODE, YOU CAN DO SO HERE
    a = RepeatingDecimal(1, 2, [-1], [-3])
    print(a)
    b = RepeatingDecimal(-1, 0, [], [-1, 0])
    print(b)
    c = RepeatingDecimal(1, -2, [9], [9, 10])
    print(c)
    d = RepeatingDecimal(1, 0, [], [1, -10])
    print(d)
    e = RepeatingDecimal(1, 10, [], [])
    print(e)

    print(a * c)
    print(a * b)
    print(a * d)
    pass