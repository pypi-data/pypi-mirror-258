# coding: UTF-8
########################################################################
# Copyright (C) 2016-2024 Mark J. Blair, NF6X
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

"""IEC 60063:2015 standard component values."""

import warnings
import bisect
from decimal import Decimal
from .engformatter import EngFormatter


class Eseries(Decimal):
    """Find nearest standard value in a series.

    The typical use for inheritors of this class is to find the
    nearest standard value in one of the IEC 60063:2015 preferred
    number series:
    https://en.wikipedia.org/wiki/E_series_of_preferred_numbers

    This class is immutable."""

    # Default to [1,2,5] series as commonly used for test equipment
    # range settings. Override this in inherited classes, such as
    # for standard IEC 60063:2015 series E3...E192.
    # This must be a sorted, immutable iterable with values bounded
    # by [1..10). All entries must be Decimal() instances.
    _series = (
        Decimal('1'),
        Decimal('2'),
        Decimal('5')
    )

    # Digits of precision appropriate for this series. Override this
    # in inherited classes.
    _precision = 1

    # Tolerance appropriate for this series. Override this in inherited
    # classes.
    _tolerance = Decimal('0.5')

    def __new__(cls, value, unit='Ω'):
        """Create and return a new standard value approximation."""
        if issubclass(value.__class__, Eseries):
            # Passed value is an Eseries inheritor, so re-approximate
            # the original exact value. For example, find the 1%
            # tolerance approximation of a resistor that was previously
            # approximated with a 5% resistor.
            x = value.exact()
        else:
            x = Decimal(value)
        if x <= 0:
            raise ValueError('Value must be > 0')

        # Normalize value as coefficient in range [1,10) and exponent
        e = x.logb()
        c = x.scaleb(-1*e)


        # Find nearest coefficient in series, assuming series is sorted
        # and each element is in range [1,10). Start by building a
        # a temporary copy of the series with top of lower decade and
        # bottom of higher decade added.
        s = (cls._series[-1].scaleb(-1),) \
            + cls._series \
            + (cls._series[0].scaleb(1),)
        # Bisect the list such that c >= s[i-1] and i>0
        i = bisect.bisect(s,c)
        # is c closer to s[i-1] or s[i]? Choose s[i-1] in a tie.
        # In either case, adjust to point to a coefficient in the
        # normal series.
        if c-s[i-1] <= s[i]-c:
            i = i-2
        else:
            i = i-1
        # If index is still past the end of the normal series, then
        # bump up to the next decade.
        if i == len(cls._series):
            i = 0
            e = e + 1

        # Create and initialize the new class instance
        n = super().__new__(cls, cls._series[i].scaleb(e), None)
        n._orig = value
        n._exact = x
        n._exponent = e
        n._index = i
        n._unit = unit
        return n

    def __str__(self):
        fmt = '{:' + str(self._precision) + 'i}' + self._unit
        return EngFormatter().format(fmt, self)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._orig})"

    def next_plus(self):
        """Return the next greater value in this series.

        This overrides the Decimal().next_plus() method to use
        values from this series."""

        if self._index == (len(self._series) - 1):
            newidx = 0
            newexp = self._exponent + 1
        else:
            newidx = self._index + 1
            newexp = self._exponent
        return self.__class__(self._series[newidx].scaleb(newexp), self._unit)

    def next(self):
        """Deprecated: Use next_plus() instead."""
        warnings.warn(__doc__, DeprecationWarning)
        return self.next_plus()

    def next_minus(self):
        """Return the previous smaller value in this series.

        This overrides the Decimal().next_minus() method to use
        values from this series."""

        if self._index == 0:
            newidx = len(self._series) - 1
            newexp = self._exponent - 1
        else:
            newidx = self._index - 1
            newexp = self._exponent
        return self.__class__(self._series[newidx].scaleb(newexp), self._unit)

    def prev(self):
        """Deprecated: Use next_minus() instead."""
        warnings.warn(__doc__, DeprecationWarning)
        return self.next_minus()

    def next_toward(self, other):
        """Return the next series value approaching the passed value.

        This overrides the Decimal().next_toward() method to use
        values from this series."""

        if other > self:
            return self.next_plus()
        if other < self:
            return self.next_minus()
        return self

    def orig(self):
        """Return original value passed when instance was initialized

        Original value can be of any type accepted by Decimal(),
        so this may return an int, float, tuple, str, Decimal, etc."""

        return self._orig

    def exact(self):
        """Return exact value used to initialize this approximation.

        Return value is a Decimal()."""

        return self._exact

    def error(self):
        """Return ratio (approximation-exact)/exact.

        This is the signed approximation error of this standard value
        vs. the original value being approximated."""

        return (self - self._exact)/self._exact

    def tolerance(self):
        """Return component tolerance appropriate for this series.

        For example, the E96 series is typically used for +/-1% component
        tolerances, so E96.tolerance() would return 0.01."""

        return self._tolerance

    def precision(self):
        """Return number of digits of precision appropriate for this series.

        Return value is an int."""

        return self._precision

    def series(self):
        """Return the list of decade coefficients for this series."""

        return self._series

    def index(self):
        """Return the index in the decade coefficient list for this value."""

        return self._index


class E3(Eseries):
    """IEC 60063:2015 standard ±40% tolerance component values."""
    _tolerance = Decimal('0.4')
    _precision = 2
    _series = (
        Decimal('1.0'),
        Decimal('2.2'),
        Decimal('4.7')
    )


class E6(Eseries):
    """IEC 60063:2015 standard ±20% tolerance component values."""
    _tolerance = Decimal('0.2')
    _precision = 2
    _series = (
        Decimal('1.0'),
        Decimal('1.5'),
        Decimal('2.2'),
        Decimal('3.3'),
        Decimal('4.7'),
        Decimal('6.8')
    )


class E12(Eseries):
    """IEC 60063:2015 standard ±10% tolerance component values."""
    _tolerance = Decimal('0.1')
    _precision = 2
    _series = (
        Decimal('1.0'),
        Decimal('1.2'),
        Decimal('1.5'),
        Decimal('1.8'),
        Decimal('2.2'),
        Decimal('2.7'),
        Decimal('3.3'),
        Decimal('3.9'),
        Decimal('4.7'),
        Decimal('5.6'),
        Decimal('6.8'),
        Decimal('8.2')
    )


class E24(Eseries):
    """IEC 60063:2015 standard ±5% tolerance component values."""
    _tolerance = Decimal('0.05')
    _precision = 2
    _series = (
        Decimal('1.0'),
        Decimal('1.1'),
        Decimal('1.2'),
        Decimal('1.3'),
        Decimal('1.5'),
        Decimal('1.6'),
        Decimal('1.8'),
        Decimal('2.0'),
        Decimal('2.2'),
        Decimal('2.4'),
        Decimal('2.7'),
        Decimal('3.0'),
        Decimal('3.3'),
        Decimal('3.6'),
        Decimal('3.9'),
        Decimal('4.3'),
        Decimal('4.7'),
        Decimal('5.1'),
        Decimal('5.6'),
        Decimal('6.2'),
        Decimal('6.8'),
        Decimal('7.5'),
        Decimal('8.2'),
        Decimal('9.1')
    )


class E48(Eseries):
    """IEC 60063:2015 standard ±2% tolerance component values."""
    _tolerance = Decimal('0.02')
    _precision = 3
    _series = (
        Decimal('1.00'),
        Decimal('1.05'),
        Decimal('1.10'),
        Decimal('1.15'),
        Decimal('1.21'),
        Decimal('1.27'),
        Decimal('1.33'),
        Decimal('1.40'),
        Decimal('1.47'),
        Decimal('1.54'),
        Decimal('1.62'),
        Decimal('1.69'),
        Decimal('1.78'),
        Decimal('1.87'),
        Decimal('1.96'),
        Decimal('2.05'),
        Decimal('2.15'),
        Decimal('2.26'),
        Decimal('2.37'),
        Decimal('2.49'),
        Decimal('2.61'),
        Decimal('2.74'),
        Decimal('2.87'),
        Decimal('3.01'),
        Decimal('3.16'),
        Decimal('3.32'),
        Decimal('3.48'),
        Decimal('3.65'),
        Decimal('3.83'),
        Decimal('4.02'),
        Decimal('4.22'),
        Decimal('4.42'),
        Decimal('4.64'),
        Decimal('4.87'),
        Decimal('5.11'),
        Decimal('5.36'),
        Decimal('5.62'),
        Decimal('5.90'),
        Decimal('6.19'),
        Decimal('6.49'),
        Decimal('6.81'),
        Decimal('7.15'),
        Decimal('7.50'),
        Decimal('7.87'),
        Decimal('8.25'),
        Decimal('8.66'),
        Decimal('9.09'),
        Decimal('9.53')
    )


class E96(Eseries):
    """IEC 60063:2015 standard ±1% tolerance component values."""
    _tolerance = Decimal('0.01')
    _precision = 3
    _series = (
        Decimal('1.00'),
        Decimal('1.02'),
        Decimal('1.05'),
        Decimal('1.07'),
        Decimal('1.10'),
        Decimal('1.13'),
        Decimal('1.15'),
        Decimal('1.18'),
        Decimal('1.21'),
        Decimal('1.24'),
        Decimal('1.27'),
        Decimal('1.30'),
        Decimal('1.33'),
        Decimal('1.37'),
        Decimal('1.40'),
        Decimal('1.43'),
        Decimal('1.47'),
        Decimal('1.50'),
        Decimal('1.54'),
        Decimal('1.58'),
        Decimal('1.62'),
        Decimal('1.65'),
        Decimal('1.69'),
        Decimal('1.74'),
        Decimal('1.78'),
        Decimal('1.82'),
        Decimal('1.87'),
        Decimal('1.91'),
        Decimal('1.96'),
        Decimal('2.00'),
        Decimal('2.05'),
        Decimal('2.10'),
        Decimal('2.15'),
        Decimal('2.21'),
        Decimal('2.26'),
        Decimal('2.32'),
        Decimal('2.37'),
        Decimal('2.43'),
        Decimal('2.49'),
        Decimal('2.55'),
        Decimal('2.61'),
        Decimal('2.67'),
        Decimal('2.74'),
        Decimal('2.80'),
        Decimal('2.87'),
        Decimal('2.94'),
        Decimal('3.01'),
        Decimal('3.09'),
        Decimal('3.16'),
        Decimal('3.24'),
        Decimal('3.32'),
        Decimal('3.40'),
        Decimal('3.48'),
        Decimal('3.57'),
        Decimal('3.65'),
        Decimal('3.74'),
        Decimal('3.83'),
        Decimal('3.92'),
        Decimal('4.02'),
        Decimal('4.12'),
        Decimal('4.22'),
        Decimal('4.32'),
        Decimal('4.42'),
        Decimal('4.53'),
        Decimal('4.64'),
        Decimal('4.75'),
        Decimal('4.87'),
        Decimal('4.99'),
        Decimal('5.11'),
        Decimal('5.23'),
        Decimal('5.36'),
        Decimal('5.49'),
        Decimal('5.62'),
        Decimal('5.76'),
        Decimal('5.90'),
        Decimal('6.04'),
        Decimal('6.19'),
        Decimal('6.34'),
        Decimal('6.49'),
        Decimal('6.65'),
        Decimal('6.81'),
        Decimal('6.98'),
        Decimal('7.15'),
        Decimal('7.32'),
        Decimal('7.50'),
        Decimal('7.68'),
        Decimal('7.87'),
        Decimal('8.06'),
        Decimal('8.25'),
        Decimal('8.45'),
        Decimal('8.66'),
        Decimal('8.87'),
        Decimal('9.09'),
        Decimal('9.31'),
        Decimal('9.53'),
        Decimal('9.76')
    )


class E192(Eseries):
    """IEC 60063:2015 standard ±0.5% tolerance component values."""
    _tolerance = Decimal('0.005')
    _precision = 3
    _series = (
        Decimal('1.00'),
        Decimal('1.01'),
        Decimal('1.02'),
        Decimal('1.04'),
        Decimal('1.05'),
        Decimal('1.06'),
        Decimal('1.07'),
        Decimal('1.09'),
        Decimal('1.10'),
        Decimal('1.11'),
        Decimal('1.13'),
        Decimal('1.14'),
        Decimal('1.15'),
        Decimal('1.17'),
        Decimal('1.18'),
        Decimal('1.20'),
        Decimal('1.21'),
        Decimal('1.23'),
        Decimal('1.24'),
        Decimal('1.26'),
        Decimal('1.27'),
        Decimal('1.29'),
        Decimal('1.30'),
        Decimal('1.32'),
        Decimal('1.33'),
        Decimal('1.35'),
        Decimal('1.37'),
        Decimal('1.38'),
        Decimal('1.40'),
        Decimal('1.42'),
        Decimal('1.43'),
        Decimal('1.45'),
        Decimal('1.47'),
        Decimal('1.49'),
        Decimal('1.50'),
        Decimal('1.52'),
        Decimal('1.54'),
        Decimal('1.56'),
        Decimal('1.58'),
        Decimal('1.60'),
        Decimal('1.62'),
        Decimal('1.64'),
        Decimal('1.65'),
        Decimal('1.67'),
        Decimal('1.69'),
        Decimal('1.72'),
        Decimal('1.74'),
        Decimal('1.76'),
        Decimal('1.78'),
        Decimal('1.80'),
        Decimal('1.82'),
        Decimal('1.84'),
        Decimal('1.87'),
        Decimal('1.89'),
        Decimal('1.91'),
        Decimal('1.93'),
        Decimal('1.96'),
        Decimal('1.98'),
        Decimal('2.00'),
        Decimal('2.03'),
        Decimal('2.05'),
        Decimal('2.08'),
        Decimal('2.10'),
        Decimal('2.13'),
        Decimal('2.15'),
        Decimal('2.18'),
        Decimal('2.21'),
        Decimal('2.23'),
        Decimal('2.26'),
        Decimal('2.29'),
        Decimal('2.32'),
        Decimal('2.34'),
        Decimal('2.37'),
        Decimal('2.40'),
        Decimal('2.43'),
        Decimal('2.46'),
        Decimal('2.49'),
        Decimal('2.52'),
        Decimal('2.55'),
        Decimal('2.58'),
        Decimal('2.61'),
        Decimal('2.64'),
        Decimal('2.67'),
        Decimal('2.71'),
        Decimal('2.74'),
        Decimal('2.77'),
        Decimal('2.80'),
        Decimal('2.84'),
        Decimal('2.87'),
        Decimal('2.91'),
        Decimal('2.94'),
        Decimal('2.98'),
        Decimal('3.01'),
        Decimal('3.05'),
        Decimal('3.09'),
        Decimal('3.12'),
        Decimal('3.16'),
        Decimal('3.20'),
        Decimal('3.24'),
        Decimal('3.28'),
        Decimal('3.32'),
        Decimal('3.36'),
        Decimal('3.40'),
        Decimal('3.44'),
        Decimal('3.48'),
        Decimal('3.52'),
        Decimal('3.57'),
        Decimal('3.61'),
        Decimal('3.65'),
        Decimal('3.70'),
        Decimal('3.74'),
        Decimal('3.79'),
        Decimal('3.83'),
        Decimal('3.88'),
        Decimal('3.92'),
        Decimal('3.97'),
        Decimal('4.02'),
        Decimal('4.07'),
        Decimal('4.12'),
        Decimal('4.17'),
        Decimal('4.22'),
        Decimal('4.27'),
        Decimal('4.32'),
        Decimal('4.37'),
        Decimal('4.42'),
        Decimal('4.48'),
        Decimal('4.53'),
        Decimal('4.59'),
        Decimal('4.64'),
        Decimal('4.70'),
        Decimal('4.75'),
        Decimal('4.81'),
        Decimal('4.87'),
        Decimal('4.93'),
        Decimal('4.99'),
        Decimal('5.05'),
        Decimal('5.11'),
        Decimal('5.17'),
        Decimal('5.23'),
        Decimal('5.30'),
        Decimal('5.36'),
        Decimal('5.42'),
        Decimal('5.49'),
        Decimal('5.56'),
        Decimal('5.62'),
        Decimal('5.69'),
        Decimal('5.76'),
        Decimal('5.83'),
        Decimal('5.90'),
        Decimal('5.97'),
        Decimal('6.04'),
        Decimal('6.12'),
        Decimal('6.19'),
        Decimal('6.26'),
        Decimal('6.34'),
        Decimal('6.42'),
        Decimal('6.49'),
        Decimal('6.57'),
        Decimal('6.65'),
        Decimal('6.73'),
        Decimal('6.81'),
        Decimal('6.90'),
        Decimal('6.98'),
        Decimal('7.06'),
        Decimal('7.15'),
        Decimal('7.23'),
        Decimal('7.32'),
        Decimal('7.41'),
        Decimal('7.50'),
        Decimal('7.59'),
        Decimal('7.68'),
        Decimal('7.77'),
        Decimal('7.87'),
        Decimal('7.96'),
        Decimal('8.06'),
        Decimal('8.16'),
        Decimal('8.25'),
        Decimal('8.35'),
        Decimal('8.45'),
        Decimal('8.56'),
        Decimal('8.66'),
        Decimal('8.76'),
        Decimal('8.87'),
        Decimal('8.98'),
        Decimal('9.09'),
        Decimal('9.20'),
        Decimal('9.31'),
        Decimal('9.42'),
        Decimal('9.53'),
        Decimal('9.65'),
        Decimal('9.76'),
        Decimal('9.88')
    )


def ratio(v1, v2, maxsteps=1):
    """Find a pair of standard component values approximating a ratio.

    I typically use this for tasks such as finding standard resistor
    values to use in a resistor divider setting the output voltage of a
    regulator.

    Given two values v1 and v2, ratio() finds two nearby standard
    component values which most closely match the ratio of the ideal
    values. If the passed values are derived from Eseries, then the
    chosen value will be in the same series, within +/- maxsteps of the
    nearest standard value. If either passed value is not derived from
    Eseries, then E96 (±1%) values will be used.

    maxsteps must be an integer >= 1.

    Returns tuple of (w1, w2, error) where w1 and w2 are the new
    approximate values, and error is defined as:

                    (w1.approx() / w2.approx())
    error = 1.0  -  ---------------------------
                     (v1.exact() / v2.exact())"""

    if issubclass(v1.__class__, Eseries):
        av1 = v1
    else:
        av1 = E96(v1)

    if issubclass(v2.__class__, Eseries):
        av2 = v2
    else:
        av2 = E96(v2)

    if (not isinstance(maxsteps, int)) or (maxsteps < 1):
        raise ValueError('maxsteps must be an integer >= 1')

    # The target ratio we want to approximate
    target = av1.exact() / av2.exact()

    # Create lists of component value candidates
    clist1 = [None]*((2*maxsteps) + 1)
    clist1[maxsteps] = av1
    clist2 = [None]*((2*maxsteps) + 1)
    clist2[maxsteps] = av2
    for n in range(maxsteps-1, -1, -1):
        clist1[n] = clist1[n+1].next_minus()
        clist2[n] = clist2[n+1].next_minus()
    for n in range(maxsteps+1, (2*maxsteps)+1):
        clist1[n] = clist1[n-1].next_plus()
        clist2[n] = clist2[n-1].next_plus()

    # Evaluate each pair of component value candidates, and pick
    # the pair with minimum error. Give preference to the initial
    # approximations.
    w1 = av1
    w2 = av2
    minerr = Decimal(1.0) - ((av1/av2)/target)
    for c1 in clist1:
        for c2 in clist2:
            err = Decimal(1.0) - ((c1/c2)/target)
            #print(f'c1 = {str(c1)} c2 = {str(c2)} err = {err:+.3%}')
            if abs(err) < abs(minerr):
                w1 = c1
                w2 = c2
                minerr = err

    # Return results
    return (w1, w2, Decimal(minerr))


def match_ratio(v1, v2, maxsteps=1):
    """Deprecated: Use ratio() instead."""
    warnings.warn(__doc__, DeprecationWarning)
    return ratio(v1, v2, maxsteps)


def divider(v_in, v_out, r_total=E96(10000), maxsteps=1):
    """Design a resistor divider using standard values.

    For the passed input voltage v_in and output voltage v_out,
    divider() designs a resistor divider using standard component values
    to produce v_out from v_in. The top and bottom resistors will add up
    to approximately r_total, and will be in the same series as r_total.
    If r_total is not an Eseries subclass, then E96 (±1%) values will be
    used. maxsteps determines how many standard value steps the top and
    bottom resistors may deviate from their initial approximations.
    Increasing maxsteps tends to reduce the v_out error and increase the
    deviation from r_total.

    Returns a tuple of (r_top, r_bot, error), with error defined by:

    error = (v_out_actual - v_out)/v_out"""

    if v_out >= v_in:
        raise ValueError('Output voltage must less than input voltage')

    if issubclass(r_total.__class__, Eseries):
        r_tot = r_total
    else:
        r_tot = E96(r_total)

    r_bot_exact = Decimal(v_out) * r_tot / Decimal(v_in)
    r_top_exact = r_tot - r_bot_exact
    (r_top, r_bot) = ratio(r_tot.__class__(r_top_exact),
                           r_tot.__class__(r_bot_exact),
                           maxsteps)[0:2]
    v_out_actual = Decimal(v_in) * r_bot / (r_bot + r_top)
    err = (v_out_actual - Decimal(v_out))/Decimal(v_out)
    return (r_top, r_bot, err)
