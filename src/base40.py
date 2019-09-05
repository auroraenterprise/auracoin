# Auracoin
# 
# Copyright (C) Aurora Enterprise. All Rights Reserved.
# 
# https://aur.xyz
# Licensed by the Auracoin Open-Source Licence, which can be found at LICENCE.md.

class BaseError(Exception):
    pass

class Base40:
    def __init__(self):
        self.digits = "01234568abcdefghjkmnprtuvwxyABDEHJLMNRTY"
        self.base = len(self.digits)

        assert self.base == 40
    
    def encode(self, number):
        final = ""
        division = 0
        modulo = 0

        if number < self.base:
            return self.digits[number]
        else:
            while (number >= self.base):
                division = number // self.base
                modulo = number - (self.base * division)

                final = self.digits[modulo] + final

                number = division
            
            if number > 0:
                final = self.digits[division] + final
            
            return final
    
    def decode(self, value):
        final = 0

        for digit in value:
            final *= self.base

            if digit not in self.digits:
                raise BaseError("digit \"" + digit + "\" invalid in value")
            
            representation = self.digits.index(digit)
            final += representation
        
        return final