#!/usr/bin/env python3

class Polynomial:
    """Creates a Polynomial class object.
    
    Usage:

    Examples of supported initializations:

        pol1 = Polynomial([1,-3,0,2])
        pol2 = Polynomial(1,-3,0,2)
        pol3 = Polynomial(x0=1,x3=2,x1=-3)
    You can use print() function and/or '+', '**' and '==' operators:
        
        print(pol2)
        2x^3 - 3x + 1

        print(Polynomial(1,-3,0,2) + Polynomial(0, 2, 1))
        2x^3 + x^2 - x + 1

        print(Polynomial(-1, 1) ** 2)
        x^2 - 2x  + 1
    Also you can use '.derivative()' or '.at_value()':

        print(pol1.derivative())
        6x^2 - 3
        print(pol1.at_value(2))
        11
        print(pol1.at_value(2,3))
        35
    """

    def __init__(self, *values, **kwargs):
        """
        Examples of supported initializations:

        pol1 = Polynomial([1,-3,0,2])
        pol2 = Polynomial(1,-3,0,2)
        pol3 = Polynomial(x0=1,x3=2,x1=-3)
        """
        # Create list where values will be stored
        self.vals = []
        # Load values into list
        if not kwargs:
            ## For list
            if type(values[0]) == list:
                self.vals = values[0].copy()
            ## For tuple
            else:
                for value in values:
                    self.vals.append(value)
        else:
            ## For dict
            sorted_values = sorted(kwargs.items(), key=lambda num: int(num[0][1:])) # Sort by number after 'x' in the key
            i=j=0
            while i <= int(sorted_values[::-1][0][0][1:]): # i <= max value in xN
                if str(i) == sorted_values[j][0][1:]:
                    self.vals.append(sorted_values[j][1]) # Append value
                    j+=1
                else:
                    self.vals.append(0) # Append 0 when there is a missing key
                i+=1
        # Delete residue 0s
        for i in range(len(self.vals)):
            if self.vals[::-1][0] == 0 and len(self.vals) > 1:
                del self.vals[-1]

    def __eq__(self, other):
        "Returns True if vectors are equal, otherwise False."
        
        return self.vals == other.vals

    def __add__(self, other):
        "Returns a new Polynomial from sum of 'self' and 'other'."
        
        # Append 0s to polynomials for them to be equal length 
        added = []
        if len(self.vals) > len(other.vals): # If the multiplied polynomial is longer
            toAppend = len(self.vals) - len(other.vals)
            for i in range(toAppend):
                other.vals.append(0)
        elif len(self.vals) < len(other.vals): # If the second polynomial is longer
            toAppend = len(other.vals) - len(self.vals)
            for i in range(toAppend):
                self.vals.append(0)

        # Add corresponding values
        if len(self.vals) == len(other.vals):
            for i in range(len(self.vals)):
                added.append(self.vals[i] + other.vals[i])

        # Return new polynomial with sum of values in added
        return Polynomial(added)
    
    def multi(self, other):
        "Used in recursive multiplying of '__pow__' (**)."

        # Get values which are being multiplied to a list
        multiplied = list(self)
        # Create another list where results will me assigned
        result = [0] * (len(multiplied) + len(other)-1)
        # Multiply loop
        for i in range(len(multiplied)):
            for j in range(len(other)):
                result[i+j] += multiplied[i] * other[j]
        # Return a new list of multiplied values
        return result

    def __pow__(self, power):
        "Returns a new Polynomial from 'self' to power of 'other'."

        # Copy original list of values
        result = self.vals.copy()
        # Call 'multi' function "power-1" times
        for _ in range(power-1):
            result = Polynomial.multi(result, self.vals)
        # Return raised Polynomial
        return Polynomial(result)

    def derivative(self):
        "Returns a new Polynomial which is derivative of previous Polynomial."

        # Just derivate it
        if len(self.vals) == 1:
            return Polynomial(0)
        else:
            return Polynomial([i * item for i, item in enumerate(self.vals)][1:])

    def at_value(self, val1, val2=None):
        "Returns a value for 'x'."

        if not val2: # If only one value is passed
            xValue2 = str(self).replace('^','**').replace('x', '*('+str(val1)+')')
            xValue1 = "0"
        else: # Else both
            xValue2 = str(self).replace('^','**').replace('x', '*('+str(val2)+')')
            xValue1 = str(self).replace('^','**').replace('x', '*('+str(val1)+')')
        try: # Evaluate strings as expressions
            result2 = eval(xValue2)
            result1 = eval(xValue1)
        except:
            pass
        # Return result
        return result2-result1

    def __str__(self):
        "Retruns a polynomial in a basic form."

        # If all values are 0 then return 0.
        if all(item == 0 for item in self.vals):
            return str(0)

        # Make list of string representations of vals
        poly = [str(val) for val in self.vals]
        # Add 'x' to strings except the multiplied one
        poly = [str(val)+'x' if i > 0 else str(val) for i,val in enumerate(poly)]
        # Add '^n' to strings except multiplied two
        poly = [val+'^'+str(i) if i > 1 else val for i,val in enumerate(poly)][::-1]

        # Append correct values to new list - all but 0 values
        result = []
        for i,item in enumerate(poly):
            if item[0] == '-':
                if item[1] != '0':
                    result.append(item)
            elif item[0] != '0':
                result.append(item)

        # Return correct form of polynomial
        return str(' + '.join(result).replace('-1x','-x').replace('1x','x').replace('-','- ').replace('+ -', '-'))

