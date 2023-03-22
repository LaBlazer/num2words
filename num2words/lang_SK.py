# -*- coding: utf-8 -*-
# Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.
# Copyright (c) 2013, Savoir-faire Linux inc.  All Rights Reserved.

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA

from __future__ import unicode_literals

from .base import Num2Word_Base
from .utils import get_digits, splitbyx

ZERO = ('nula',)

ONES = {
    1: ('jeden',),
    2: ('dva',),
    3: ('tri',),
    4: ('štyri',),
    5: ('päť',),
    6: ('šesť',),
    7: ('sedem',),
    8: ('osem',),
    9: ('deväť',),
}

TENS = {
    0: ('desať',),
    1: ('jedenásť',),
    2: ('dvanásť',),
    3: ('trinásť',),
    4: ('štrnásť',),
    5: ('pätnásť',),
    6: ('šestnásť',),
    7: ('sedemnásť',),
    8: ('osemnásť',),
    9: ('devätnásť',),
}

TWENTIES = {
    2: ('dvadsať',),
    3: ('tridsať',),
    4: ('štyridsať',),
    5: ('päťesiat',),
    6: ('šesťdesiat',),
    7: ('sedemdesiat',),
    8: ('osemdesiat',),
    9: ('deväťdesiat',),
}

HUNDREDS = {
    1: ('sto',),
    2: ('dvesto',),
    3: ('tristo',),
    4: ('štyristo',),
    5: ('päťsto',),
    6: ('šesťsto',),
    7: ('sedemsto',),
    8: ('osemsto',),
    9: ('deväťsto',),
}

THOUSANDS = {
    1: ('tisíc', 'tisíce', 'tisíc'),  # 10^3
    2: ('milión', 'milióny', 'miliónov'),  # 10^6
    3: ('miliarda', 'miliardy', 'miliárd'),  # 10^9
    4: ('bilión', 'bilióny', 'biliónov'),  # 10^12
    5: ('biliarda', 'biliardy', 'biliárd'),  # 10^15
    6: ('trilión', 'trilióny', 'triliónov'),  # 10^18
    7: ('triliarda', 'triliardy', 'triliárd'),  # 10^21
    8: ('kvadrilin', 'kvadrilióny', 'kvadriliónov'),  # 10^24
    9: ('kvadriliarda', 'kvadriliardy', 'kvadriliárd'),  # 10^27
    10: ('quintillión', 'quintillióny', 'quintilliónov'),  # 10^30
}

POINTWORDS = {
    1: ('celá',),
    2: ('celé',),
    3: ('celých',),
}

class Num2Word_SK(Num2Word_Base):
    CURRENCY_FORMS = {
        'CZK': (
            ('koruna', 'koruny', 'korún'), ('halier', 'haliere', 'halierov')
        ),
        'EUR': (
            ('euro', 'euro', 'euro'), ('cent', 'centy', 'centov')
        ),
    }

    def get_pointword(self, n):
        if n == 0:
            return "celých"
        if n == 1:
            return "celá"
        if n < 5:
            return "celé"
        return "celých"

    def setup(self):
        self.negword = "mínus "

    def to_cardinal(self, number):
        n = str(number).replace(',', '.')
        if '.' in n:
            left, right = n.split('.')
            leading_zero_count = len(right) - len(right.lstrip('0'))
            decimal_part = ((ZERO[0] + ' ') * leading_zero_count +
                            self._int2word(int(right)))
            return u'%s %s %s' % (
                self._int2word(int(left)),
                self.get_pointword(int(left[-1])),
                decimal_part
            )
        else:
            return self._int2word(int(n))

    def pluralize(self, n, forms):
        print(n)
        if n == 1:
            form = 0
        elif 5 > n:
            form = 1
        else:
            form = 2
        return forms[form]

    def to_ordinal(self, number):
        raise NotImplementedError()

    def _int2word(self, n):
        if n == 0:
            return ZERO[0]
        if n < 0:
            return self.negword + self._int2word(-n)

        words = []
        chunks = list(splitbyx(str(n), 3))
        i = len(chunks)
        for x in chunks:
            i -= 1

            if x == 0:
                continue

            n1, n2, n3 = get_digits(x)

            if n3 > 0:
                words.append(HUNDREDS[n3][0])

            if n2 > 1:
                words.append(TWENTIES[n2][0])

            if n2 == 1:
                words.append(TENS[n1][0])
            elif n1 > 0 and not (i > 0 and x == 1):
                words.append(ONES[n1][0])

            if i > 0:
                words.append(self.pluralize(x, THOUSANDS[i]))

        return ' '.join(words)
