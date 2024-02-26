# coding: UTF-8
########################################################################
# Copyright (C) 2022-2024 Mark J. Blair, NF6X
#
# This file is part of nf6x_eetools.
#
# nf6x_eetools is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# nf6x_eetools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with eetools.  If not, see <http://www.gnu.org/licenses/>.
########################################################################

"""Twist drill size tables"""

from decimal import Decimal

fractional_drill_table = {
    "1/64in":  Decimal(1/64),
    "1/32in":  Decimal(1/32),
    "3/64in":  Decimal(3/64),
    "1/16in":  Decimal(1/16),
    "5/64in":  Decimal(5/64),
    "3/32in":  Decimal(3/32),
    "7/64in":  Decimal(7/64),
    "1/8in":   Decimal(1/8),
    "9/64in":  Decimal(9/64),
    "5/32in":  Decimal(5/32),
    "11/64in": Decimal(11/64),
    "3/16in":  Decimal(3/16),
    "13/64in": Decimal(13/64),
    "7/32in":  Decimal(7/32),
    "15/64in": Decimal(15/64),
    "1/4in":   Decimal(1/4),
    "17/64in": Decimal(17/64),
    "9/32in":  Decimal(9/32),
    "19/64in": Decimal(19/64),
    "5/16in":  Decimal(5/16),
    "21/64in": Decimal(21/64),
    "11/32in": Decimal(11/32),
    "23/64in": Decimal(23/64),
    "3/8in":   Decimal(3/8),
    "25/64in": Decimal(25/64),
    "13/32in": Decimal(13/32),
    "27/64in": Decimal(27/64),
    "7/16in":  Decimal(7/16),
    "29/64in": Decimal(29/64),
    "15/32in": Decimal(15/32),
    "31/64in": Decimal(31/64),
    "1/2in":   Decimal(1/2),
    "33/64in": Decimal(33/64),
    "17/32in": Decimal(17/32),
    "35/64in": Decimal(35/64),
    "9/16in":  Decimal(9/16),
    "37/64in": Decimal(37/64),
    "19/32in": Decimal(19/32),
    "39/64in": Decimal(39/64),
    "5/8in":   Decimal(5/8),
    "41/64in": Decimal(41/64),
    "21/32in": Decimal(21/32),
    "43/64in": Decimal(43/64),
    "11/16in": Decimal(11/16),
    "45/64in": Decimal(45/64),
    "23/32in": Decimal(23/32),
    "47/64in": Decimal(47/64),
    "3/4in":   Decimal(3/4),
    "49/64in": Decimal(49/64),
    "25/32in": Decimal(25/32),
    "51/64in": Decimal(51/64),
    "13/16in": Decimal(13/16),
    "53/64in": Decimal(53/64),
    "27/32in": Decimal(27/32),
    "55/64in": Decimal(55/64),
    "7/8in":   Decimal(7/8),
    "57/64in": Decimal(57/64),
    "29/32in": Decimal(29/32),
    "59/64in": Decimal(59/64),
    "15/16in": Decimal(15/16),
    "61/64in": Decimal(61/64),
    "31/32in": Decimal(31/32),
    "63/64in": Decimal(63/64),
    "1in":     Decimal('1.000')
}

number_drill_table = {
    'no104': Decimal('0.0031'),
    'no103': Decimal('0.0035'),
    'no102': Decimal('0.0039'),
    'no101': Decimal('0.0043'),
    'no100': Decimal('0.0047'),
    'no99':  Decimal('0.0051'),
    'no98':  Decimal('0.0055'),
    'no97':  Decimal('0.0059'),
    'no96':  Decimal('0.0063'),
    'no95':  Decimal('0.0067'),
    'no94':  Decimal('0.0071'),
    'no93':  Decimal('0.0075'),
    'no92':  Decimal('0.0079'),
    'no91':  Decimal('0.0083'),
    'no90':  Decimal('0.0087'),
    'no89':  Decimal('0.0091'),
    'no88':  Decimal('0.0095'),
    'no87':  Decimal('0.010'),
    'no86':  Decimal('0.0105'),
    'no85':  Decimal('0.011'),
    'no84':  Decimal('0.0115'),
    'no83':  Decimal('0.012'),
    'no82':  Decimal('0.0125'),
    'no81':  Decimal('0.013'),
    'no80':  Decimal('0.0135'),
    'no79':  Decimal('0.0145'),
    'no78':  Decimal('0.016'),
    'no77':  Decimal('0.018'),
    'no76':  Decimal('0.020'),
    'no75':  Decimal('0.021'),
    'no74':  Decimal('0.0225'),
    'no73':  Decimal('0.024'),
    'no72':  Decimal('0.025'),
    'no71':  Decimal('0.026'),
    'no70':  Decimal('0.028'),
    'no69':  Decimal('0.0292'),
    'no68':  Decimal('0.031'),
    'no67':  Decimal('0.032'),
    'no66':  Decimal('0.033'),
    'no65':  Decimal('0.035'),
    'no64':  Decimal('0.036'),
    'no63':  Decimal('0.037'),
    'no62':  Decimal('0.038'),
    'no61':  Decimal('0.039'),
    'no60':  Decimal('0.040'),
    'no59':  Decimal('0.041'),
    'no58':  Decimal('0.042'),
    'no57':  Decimal('0.043'),
    'no56':  Decimal('0.0465'),
    'no55':  Decimal('0.052'),
    'no54':  Decimal('0.055'),
    'no53':  Decimal('0.0595'),
    'no52':  Decimal('0.0635'),
    'no51':  Decimal('0.067'),
    'no50':  Decimal('0.070'),
    'no49':  Decimal('0.073'),
    'no48':  Decimal('0.076'),
    'no47':  Decimal('0.0785'),
    'no46':  Decimal('0.081'),
    'no45':  Decimal('0.082'),
    'no44':  Decimal('0.086'),
    'no43':  Decimal('0.089'),
    'no42':  Decimal('0.0935'),
    'no41':  Decimal('0.096'),
    'no40':  Decimal('0.098'),
    'no39':  Decimal('0.0995'),
    'no38':  Decimal('0.1015'),
    'no37':  Decimal('0.104'),
    'no36':  Decimal('0.1065'),
    'no35':  Decimal('0.110'),
    'no34':  Decimal('0.111'),
    'no33':  Decimal('0.113'),
    'no32':  Decimal('0.116'),
    'no31':  Decimal('0.120'),
    'no30':  Decimal('0.1285'),
    'no29':  Decimal('0.136'),
    'no28':  Decimal('0.1405'),
    'no27':  Decimal('0.144'),
    'no26':  Decimal('0.147'),
    'no25':  Decimal('0.1495'),
    'no24':  Decimal('0.152'),
    'no23':  Decimal('0.154'),
    'no22':  Decimal('0.157'),
    'no21':  Decimal('0.159'),
    'no20':  Decimal('0.161'),
    'no19':  Decimal('0.166'),
    'no18':  Decimal('0.1695'),
    'no17':  Decimal('0.173'),
    'no16':  Decimal('0.177'),
    'no15':  Decimal('0.180'),
    'no14':  Decimal('0.182'),
    'no13':  Decimal('0.185'),
    'no12':  Decimal('0.189'),
    'no11':  Decimal('0.191'),
    'no10':  Decimal('0.1935'),
    'no9':   Decimal('0.196'),
    'no8':   Decimal('0.199'),
    'no7':   Decimal('0.201'),
    'no6':   Decimal('0.204'),
    'no5':   Decimal('0.2055'),
    'no4':   Decimal('0.209'),
    'no3':   Decimal('0.213'),
    'no2':   Decimal('0.221'),
    'no1':   Decimal('0.228')
}

letter_drill_table = {
    'A': Decimal('0.234'),
    'B': Decimal('0.238'),
    'C': Decimal('0.242'),
    'D': Decimal('0.246'),
    'E': Decimal('0.250'),
    'F': Decimal('0.257'),
    'G': Decimal('0.261'),
    'H': Decimal('0.266'),
    'I': Decimal('0.272'),
    'J': Decimal('0.277'),
    'K': Decimal('0.281'),
    'L': Decimal('0.290'),
    'M': Decimal('0.295'),
    'N': Decimal('0.302'),
    'O': Decimal('0.316'),
    'P': Decimal('0.323'),
    'Q': Decimal('0.332'),
    'R': Decimal('0.339'),
    'S': Decimal('0.348'),
    'T': Decimal('0.358'),
    'U': Decimal('0.368'),
    'V': Decimal('0.377'),
    'W': Decimal('0.386'),
    'X': Decimal('0.397'),
    'Y': Decimal('0.404'),
    'Z': Decimal('0.413'),
}

drill_table = {
    **fractional_drill_table,
    **number_drill_table,
    **letter_drill_table
}


def drill(diameter, margin=0, showdiam=True, table=drill_table):
    """Return string representing nearest American drill size

    For a given diameter, return a string representing the nearest
    American twist drill size. Arguments:

    diameter
    margin    If 0, return nearest size;
              if > 0, return equal or larger size;
              if < 0, return equal or smaller size
    showdiam  If True, include actual diameter in returned string
    table     Drill table to use [drill_table]"""

    d = Decimal(diameter)
    if margin > 0:
        s = min({k: table[k] for k in table if table[k] >= d},
                key=lambda x: table[x]-d)
    elif margin < 0:
        s = min({k: table[k] for k in table if table[k] <= d},
                key=lambda x: d-table[x])
    else:
        s = min(table, key=lambda x: abs(table[x]-d))

    if showdiam:
        s = s + f" ({table[s]:g} in)"

    return s
