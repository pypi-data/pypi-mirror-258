"""Utilities."""
from decimal import Decimal
import os.path
import re


filename_regexp = re.compile(
    r"""
    (?P<prefix>[^\.]+)\.             # Prefix
    (
        (?P<decimal>-?\d*(\.\d+)?)?  # Optional Decimal
        (?P<remainder>.*)\.          # Remainder
    )?                               # This portion is optional
    (?P<ext>\w*)                     # Extension
""",
    re.VERBOSE,
)


def filename_sort_key(filename):
    """Return the sort key for filename.


    Examples
    --------
    >>> filename_sort_key("pre.3.npy")
    ['pre', Decimal('3'), '', 'npy']
    >>> filename_sort_key("pre.3a.npy")
    ['pre', Decimal('3'), 'a', 'npy']
    >>> filename_sort_key("pre.3.a.npy")
    ['pre', Decimal('3'), '.a', 'npy']
    """
    match = filename_regexp.match(os.path.basename(filename))
    if not match:
        raise ValueError(
            f"Invalid filename {filename}. "
            + "Must have form  <prefix>.[<decimal>]<str>.<ext>."
        )

    prefix, decimal, remainder, ext = map(
        match.group, ["prefix", "decimal", "remainder", "ext"]
    )
    if not decimal:
        decimal = "-inf"  # Make sure that empty decimals sort first
    decimal = Decimal(decimal)

    # This is the Human sorting algorithm from
    # https://nedbatchelder.com/blog/200712/human_sorting.html
    if remainder:
        remainder = [
            int(c) if c.isdigit() else c for c in re.split("([0-9]+)", remainder)
        ]
    else:
        remainder = [""]

    return [prefix, decimal] + remainder + [ext]


def sort_filenames(filenames):
    """Sort filenames in a natural order.

    We assume that the filenames have the following form::

        <prefix>.<ext>                   # Always comes first
        <prefix>.[<decimal>]<str>.<ext>

    Filenames without a decimal will sort before those with a decimal.

    This splits the strings into a sequence of digits and letters, then interprets the
    digits as integers for the purpose of comparison.

    Examples
    --------
    >>> files = ["pre.wdat", "pre.a.ext", "pre.-1.3.wdat", "pre.-1.2.wdat",
    ...          "pre.0.wdat", "pre.1.wdat", "pre.002.wdat",
    ...          "pre.3.wdat", "pre.3.0014.wdat", "pre.3.013.wdat", "pre.3.0131.wdat",
    ...          "pre.4.wdat", "pre.9.wdat", "pre.10.wdat", "pre.11.wdat",
    ...          "pre.99.wdat", "pre.100.wdat", "pre.3.a.npy"]
    >>> print("\\n".join(sort_filenames(files)))
    pre.wdat
    pre.-1.3.wdat
    pre.-1.2.wdat
    pre.0.wdat
    pre.1.wdat
    pre.002.wdat
    pre.3.wdat
    pre.3.a.npy
    pre.3.0014.wdat
    pre.3.013.wdat
    pre.3.0131.wdat
    pre.4.wdat
    pre.9.wdat
    pre.10.wdat
    pre.11.wdat
    pre.99.wdat
    pre.100.wdat

    References
    ----------
    * https://blog.codinghorror.com/sorting-for-humans-natural-sort-order/
    * https://nedbatchelder.com/blog/200712/human_sorting.html
    """
    dirs = set(map(os.path.dirname, filenames))
    if not len(dirs) == 1:
        raise ValueError(
            f"Files must all be in the same directory: got {len(dirs)}: {dirs}"
        )

    return sorted(filenames, key=filename_sort_key)
