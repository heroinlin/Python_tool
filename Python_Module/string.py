"""A collection of string operations (most are no longer used).

Warning: most of the code you see here isn't normally used nowadays.
Beginning with Python 1.6, many of these functions are implemented as
methods on the standard string object. They used to be implemented by
a built-in module called strop, but strop is now obsolete itself.

Public module variables:

whitespace -- a string containing all characters considered whitespace
lowercase -- a string containing all characters considered lowercase letters
uppercase -- a string containing all characters considered uppercase letters
letters -- a string containing all characters considered letters
digits -- a string containing all characters considered decimal digits
hexdigits -- a string containing all characters considered hexadecimal digits
octdigits -- a string containing all characters considered octal digits
punctuation -- a string containing all characters considered punctuation
printable -- a string containing all characters considered printable

"""

# Some strings for ctype-style character classification
whitespace = ' \t\n\r\v\f'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = lowercase + uppercase
ascii_lowercase = lowercase
ascii_uppercase = uppercase
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = """!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + letters + punctuation + whitespace

# Case conversion helpers
# Use str to convert Unicode literal in case of -U
l = map(chr, xrange(256))
_idmap = str('').join(l)
del l

# Functions which aren't available as string methods.

# Capitalize the words in a string, e.g. " aBc  dEf " -> "Abc Def".
def capwords(s, sep=None):
    """capwords(s [,sep]) -> string
    用split拆分参数转换为单词，利用capitalize使单词首字母大写，并且用join连接这些单词。
    如果可选的第二个参数sep是缺省或无，以单个空格代替一串空白字符串，
    开头和结尾的空格被删除，否则以sep为分隔符来分割和连接单词.
    如string.capwords("   nice   to   meet  you     "),输出为：Nice To Meet You
    如string.capwords(" niceto  meet  you ","e"),输出为： niceTo  meeT  you
    Split the argument into words using split, capitalize each
    word using capitalize, and join the capitalized words using
    join.  If the optional second argument sep is absent or None,
    runs of whitespace characters are replaced by a single space
    and leading and trailing whitespace are removed, otherwise
    sep is used to split and join the words.

    """
    return (sep or ' ').join(x.capitalize() for x in s.split(sep))


# Construct a translation string
_idmapL = None
def maketrans(fromstr, tostr):
    """maketrans(frm, to) -> string
    返回一个转换表适用于string.translate使用（字符串长256字节）。字符串frm和to必须具有相同的长度
    Return a translation table (a string of 256 bytes long)
    suitable for use in string.translate.  The strings frm and to
    must be of the same length.

    """
    if len(fromstr) != len(tostr):
        raise ValueError, "maketrans arguments must have same length"
    global _idmapL
    if not _idmapL:
        _idmapL = list(_idmap)
    L = _idmapL[:]
    fromstr = map(ord, fromstr)
    for i in range(len(fromstr)):
        L[fromstr[i]] = tostr[i]
    return ''.join(L)



####################################################################
import re as _re

class _multimap:
    """Helper class for combining multiple mappings.

    Used by .{safe_,}substitute() to combine the mapping and keyword
    arguments.
    """
    def __init__(self, primary, secondary):
        self._primary = primary
        self._secondary = secondary

    def __getitem__(self, key):
        try:
            return self._primary[key]
        except KeyError:
            return self._secondary[key]


class _TemplateMetaclass(type):
    pattern = r"""
    %(delim)s(?:
      (?P<escaped>%(delim)s) |   # Escape sequence of two delimiters
      (?P<named>%(id)s)      |   # delimiter and a Python identifier
      {(?P<braced>%(id)s)}   |   # delimiter and a braced identifier
      (?P<invalid>)              # Other ill-formed delimiter exprs
    )
    """

    def __init__(cls, name, bases, dct):
        super(_TemplateMetaclass, cls).__init__(name, bases, dct)
        if 'pattern' in dct:
            pattern = cls.pattern
        else:
            pattern = _TemplateMetaclass.pattern % {
                'delim' : _re.escape(cls.delimiter),
                'id'    : cls.idpattern,
                }
        cls.pattern = _re.compile(pattern, _re.IGNORECASE | _re.VERBOSE)


class Template:
    """A string class for supporting $-substitutions."""
    __metaclass__ = _TemplateMetaclass

    delimiter = '$'
    idpattern = r'[_a-z][_a-z0-9]*'

    def __init__(self, template):
        self.template = template

    # Search for $$, $identifier, ${identifier}, and any bare $'s

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' %
                         (lineno, colno))

    def substitute(*args, **kws):
        if not args:
            raise TypeError("descriptor 'substitute' of 'Template' object "
                            "needs an argument")
        self, args = args[0], args[1:]  # allow the "self" keyword be passed
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]
        # Helper function for .sub()
        def convert(mo):
            # Check the most common path first.
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                val = mapping[named]
                # We use this idiom instead of str() because the latter will
                # fail if val is a Unicode containing non-ASCII characters.
                return '%s' % (val,)
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)

    def safe_substitute(*args, **kws):
        if not args:
            raise TypeError("descriptor 'safe_substitute' of 'Template' object "
                            "needs an argument")
        self, args = args[0], args[1:]  # allow the "self" keyword be passed
        if len(args) > 1:
            raise TypeError('Too many positional arguments')
        if not args:
            mapping = kws
        elif kws:
            mapping = _multimap(kws, args[0])
        else:
            mapping = args[0]
        # Helper function for .sub()
        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                try:
                    # We use this idiom instead of str() because the latter
                    # will fail if val is a Unicode containing non-ASCII
                    return '%s' % (mapping[named],)
                except KeyError:
                    return mo.group()
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                return mo.group()
            raise ValueError('Unrecognized named group in pattern',
                             self.pattern)
        return self.pattern.sub(convert, self.template)



####################################################################
# NOTE: Everything below here is deprecated.  Use string methods instead.
# This stuff will go away in Python 3.0.

# Backward compatible names for exceptions
index_error = ValueError
atoi_error = ValueError
atof_error = ValueError
atol_error = ValueError

# convert UPPER CASE letters to lower case
def lower(s):
    """lower(s) -> string
    返回字符串s转换为小写的副本。
    Return a copy of the string s converted to lowercase.

    """
    return s.lower()

# Convert lower case letters to UPPER CASE
def upper(s):
    """upper(s) -> string
    返回字符串s转换为大写的副本。
    Return a copy of the string s converted to uppercase.

    """
    return s.upper()

# Swap lower case letters and UPPER CASE
def swapcase(s):
    """swapcase(s) -> string
    返回的字符串s的副本,大写字符转换为小写，反之亦然。
    Return a copy of the string s with upper case characters
    converted to lowercase and vice versa.

    """
    return s.swapcase()

# Strip leading and trailing tabs and spaces
def strip(s, chars=None):
    """strip(s [,chars]) -> string
    返回字符串s的副本，开头和结尾的空格去掉。
    如果chars给出，删除s开头和结尾的chars字符串，如string.strip("as1asdgas","as"),输出为：1asdg
    Return a copy of the string s with leading and trailing
    whitespace removed.
    If chars is given and not None, remove characters in chars instead.
    If chars is unicode, S will be converted to unicode before stripping.

    """
    return s.strip(chars)

# Strip leading tabs and spaces
def lstrip(s, chars=None):
    """lstrip(s [,chars]) -> string
    返回的字符串s的副本,开头空格删除。
    如果字符给出，而不是None，删除s开头的chars字符串。如string.lstrip("as1asdgas","as"),输出为：1asdgas
    Return a copy of the string s with leading whitespace removed.
    If chars is given and not None, remove characters in chars instead.

    """
    return s.lstrip(chars)

# Strip trailing tabs and spaces
def rstrip(s, chars=None):
    """rstrip(s [,chars]) -> string
    返回的字符串s的副本,结尾空格删除。
    如果字符给出，而不是None，删除s结尾的chars字符串。如string.rstrip("as1asdgas","as"),输出为：as1asdg
    Return a copy of the string s with trailing whitespace removed.
    If chars is given and not None, remove characters in chars instead.

    """
    return s.rstrip(chars)


# Split a string into a list of space/tab-separated words
def split(s, sep=None, maxsplit=-1):
    """split(s [,sep [,maxsplit]]) -> list of strings
    返回字符串s中单词的列表，用sep作为字符串的分隔符。如果maxsplit给出，分割在不超过第
    maxsplit个分隔符的位置（结果至多为maxsplit+ 1个单词）。如果sep未指定或为None，以空白字符串作为分隔符。
    如string.split("a  ds sd"),输出为['a','ds','sd']
    string.split("a  ds sd",maxsplit=1),输出为['a','ds sd']
    Return a list of the words in the string s, using sep as the
    delimiter string.  If maxsplit is given, splits at no more than
    maxsplit places (resulting in at most maxsplit+1 words).  If sep
    is not specified or is None, any whitespace string is a separator.

    (split and splitfields are synonymous)

    """
    return s.split(sep, maxsplit)
splitfields = split

# Split a string into a list of space/tab-separated words
def rsplit(s, sep=None, maxsplit=-1):
    """rsplit(s [,sep [,maxsplit]]) -> list of strings
    返回字符串s中单词的列表，用sep作为字符串的分隔符,分割符从字符串s尾部开始算起。如果maxsplit给出，分割在不超过第
    maxsplit个分隔符的位置（结果至多为maxsplit+ 1个单词）。如果sep未指定或为None，以空白字符串作为分隔符。
    如string.rsplit("a  ds sd"),输出为['a','ds','sd']
    string.rsplit("a  ds sd",maxsplit=1),输出为['a ds','sd']
    Return a list of the words in the string s, using sep as the
    delimiter string, starting at the end of the string and working
    to the front.  If maxsplit is given, at most maxsplit splits are
    done. If sep is not specified or is None, any whitespace string
    is a separator.
    """
    return s.rsplit(sep, maxsplit)

# Join fields with optional separator
def join(words, sep = ' '):
    """join(list [,sep]) -> string
    返回列表中的单词所组成字符串，以sep相串联。默认的分隔符是一个空格。
    如string.join(["nice","to", "meet","you"])，输出为：nice to meet you
    Return a string composed of the words in list, with
    intervening occurrences of sep.  The default separator is a
    single space.

    (joinfields and join are synonymous)

    """
    return sep.join(words)
joinfields = join

# Find substring, raise exception if not found
def index(s, *args):
    """index(s, sub [,start [,end]]) -> int
    类似find，但是没有找到子串时引发ValueError错误。返回子串出现的首位置，否则报错。
    如string.index("a sd fg a","a"),输出为：0
    如string.index("a sd fg a fg","sdsdfg"[4:5]),输出为:5
    Like find but raises ValueError when the substring is not found.

    """
    return s.index(*args)

# Find last substring, raise exception if not found
def rindex(s, *args):
    """rindex(s, sub [,start [,end]]) -> int
    类似rfind，但是没有找到子串时引发ValueError错误。返回子串出现的最后位置，否则报错。
    如string.rindex("a sd fg a","a"),输出为：8
    如string.rindex("a sd fg a fg","sdsdfg"[4:5]),输出为:10
    Like rfind but raises ValueError when the substring is not found.

    """
    return s.rindex(*args)

# Count non-overlapping occurrences of substring
def count(s, *args):
    """count(s, sub[, start[,end]]) -> int
    返回字符串s[start:end]中的子串sub出现的次数.可选参数start和end都解释为片符号。
    如string.count("a sd fg a","a"),输出为2
    如string.count("a sd fg a fg","sdsdfg"[2:3]),输出为:1
    Return the number of occurrences of substring sub in string
    s[start:end].  Optional arguments start and end are
    interpreted as in slice notation.

    """
    return s.count(*args)

# Find substring, return -1 if not found
def find(s, *args):
    """find(s, sub [,start [,end]]) -> int
    返回子串出现的首位置，子串包含在s[start,end]中(即子串sub长度不超过s).可选参数start和end都解释为片符号。不存在是返回-1
    如string.find("a sd fg a","a"),输出为：0
    如string.find("a sd fg a fg","sdsdfg"[4:5]),输出为:5
    Return the lowest index in s where substring sub is found,
    such that sub is contained within s[start,end].  Optional
    arguments start and end are interpreted as in slice notation.

    Return -1 on failure.

    """
    return s.find(*args)

# Find last substring, return -1 if not found
def rfind(s, *args):
    """rfind(s, sub [,start [,end]]) -> int
    返回子串出现的最后位置，子串包含在s[start,end]中(即子串sub长度不超过s).可选参数start和end都解释为片符号。不存在是返回-1
    如string.rfind("a sd fg a","a"),输出为：8
    如string.rfind("a sd fg a fg","sdsdfg"[4:5]),输出为:10
    Return the highest index in s where substring sub is found,
    such that sub is contained within s[start,end].  Optional
    arguments start and end are interpreted as in slice notation.

    Return -1 on failure.

    """
    return s.rfind(*args)

# for a bit of speed
_float = float
_int = int
_long = long

# Convert string to float
def atof(s):
    """atof(s) -> float

    Return the floating point number represented by the string s.

    """
    return _float(s)


# Convert string to integer
def atoi(s , base=10):
    """atoi(s [,base]) -> int

    Return the integer represented by the string s in the given
    base, which defaults to 10.  The string s must consist of one
    or more digits, possibly preceded by a sign.  If base is 0, it
    is chosen from the leading characters of s, 0 for octal, 0x or
    0X for hexadecimal.  If base is 16, a preceding 0x or 0X is
    accepted.

    """
    return _int(s, base)


# Convert string to long integer
def atol(s, base=10):
    """atol(s [,base]) -> long

    Return the long integer represented by the string s in the
    given base, which defaults to 10.  The string s must consist
    of one or more digits, possibly preceded by a sign.  If base
    is 0, it is chosen from the leading characters of s, 0 for
    octal, 0x or 0X for hexadecimal.  If base is 16, a preceding
    0x or 0X is accepted.  A trailing L or l is not accepted,
    unless base is 0.

    """
    return _long(s, base)


# Left-justify a string
def ljust(s, width, *args):
    """ljust(s, width[, fillchar]) -> string
    返回s的左对齐的版本，在该场指定宽度，可以根据需要用空格填充。该字符串不会被截断。如果指定了fillchar,以此代替空格。
    如string.ljust(" adf", 8,"s"),输出为： adfssss
    如string.ljust(" adfsfsfsfa", 3,"s"),(体现出不被截断)输出为 adfsfsfsfa
    Return a left-justified version of s, in a field of the
    specified width, padded with spaces as needed.  The string is
    never truncated.  If specified the fillchar is used instead of spaces.

    """
    return s.ljust(width, *args)

# Right-justify a string
def rjust(s, width, *args):
    """rjust(s, width[, fillchar]) -> string
    返回s的右对齐的版本，在该场指定宽度，可以根据需要用空格填充。该字符串不会被截断。如果指定了fillchar,以此代替空格。
    如string.rjust(" adf", 8,"s"),输出为：ssss adf
    如string.rjust(" adfsfsfsfa", 3,"s"),(体现出不被截断)输出为 adfsfsfsfa
    Return a right-justified version of s, in a field of the
    specified width, padded with spaces as needed.  The string is
    never truncated.  If specified the fillchar is used instead of spaces.

    """
    return s.rjust(width, *args)

# Center a string
def center(s, width, *args):
    """center(s, width[, fillchar]) -> string
    返回s的中心对齐的版本，在该场指定宽度，可以根据需要用空格填充。该字符串不会被截断。如果指定了fillchar,以此代替空格。
    如string.center(" adf", 9,"s"),输出为：sss adfss
    如string.center(" adfsfsfsfa", 3,"s"),(体现出不被截断)输出为 adfsfsfsfa
    Return a center version of s, in a field of the specified
    width. padded with spaces as needed.  The string is never
    truncated.  If specified the fillchar is used instead of spaces.

    """
    return s.center(width, *args)

# Zero-fill a number, e.g., (12, 3) --> '012' and (-3, 3) --> '-03'
# Decadent feature: the argument may be a string or a number
# (Use of this is deprecated; it should be a string as with ljust c.s.)
def zfill(x, width):
    """zfill(x, width) -> string
    在字符串x左边，填充0达到指定的宽度。该字符串x不会被截断。
    如string.zfill(" adf", 9),输出为：00000 adf
    Pad a numeric string x with zeros on the left, to fill a field
    of the specified width.  The string x is never truncated.

    """
    if not isinstance(x, basestring):
        x = repr(x)
    return x.zfill(width)

# Expand tabs in a string.
# Doesn't take non-printing chars into account, but does understand \n.
def expandtabs(s, tabsize=8):
    """expandtabs(s [,tabsize]) -> string
    返回字符串s的副本，所有的制表符(tab)由适当数量的空格替代，取决于当前列和制表符大小（默认为8）
    Return a copy of the string s with all tab characters replaced
    by the appropriate number of spaces, depending on the current
    column, and the tabsize (default 8).

    """
    return s.expandtabs(tabsize)

# Character translation through look-up table.
def translate(s, table, deletions=""):
    """translate(s,table [,deletions]) -> string
    返回字符串s的副本，可选参数deletions出现的所有字符被删除，剩下的字符通过给定的转换表来映射，
    转换表必须是长度为256的字符串.deletions不允许Unicode字符串
    如t=string.maketrans('abc','ABC'),string.translate("abc123",t,'12'),输出为：ABC3
    Return a copy of the string s, where all characters occurring
    in the optional argument deletions are removed, and the
    remaining characters have been mapped through the given
    translation table, which must be a string of length 256.  The
    deletions argument is not allowed for Unicode strings.

    """
    if deletions or table is None:
        return s.translate(table, deletions)
    else:
        # Add s[:0] so that if s is Unicode and table is an 8-bit string,
        # table is converted to Unicode.  This means that table *cannot*
        # be a dictionary -- for that feature, use u.translate() directly.
        return s.translate(table + s[:0])

# Capitalize a string, e.g. "aBc  dEf" -> "Abc  def".
def capitalize(s):
    """capitalize(s) -> string
    返回字符串s的副本，只有首字符大写
    Return a copy of the string s with only its first character
    capitalized.

    """
    return s.capitalize()

# Substring replacement (global)
def replace(s, old, new, maxreplace=-1):
    """replace (str, old, new[, maxreplace]) -> string
    返回字符串str的副本，以子串new代替所有出现的子串old。如果可选参数maxreplace给出，只有第一个maxreplace出现的地方被替换
    如string.replace("old ffa old fsda old", "old", "new",2),输出为：new ffa new fsda old
    Return a copy of string str with all occurrences of substring
    old replaced by new. If the optional argument maxreplace is
    given, only the first maxreplace occurrences are replaced.

    """
    return s.replace(old, new, maxreplace)


# Try importing optional built-in module "strop" -- if it exists,
# it redefines some string operations that are 100-1000 times faster.
# It also defines values for whitespace, lowercase and uppercase
# that match <ctype.h>'s definitions.

try:
    from strop import maketrans, lowercase, uppercase, whitespace
    letters = lowercase + uppercase
except ImportError:
    pass                                          # Use the original versions

########################################################################
# the Formatter class
# see PEP 3101 for details and purpose of this class

# The hard parts are reused from the C implementation.  They're exposed as "_"
# prefixed methods of str and unicode.

# The overall parser is implemented in str._formatter_parser.
# The field name parser is implemented in str._formatter_field_name_split

class Formatter(object):
    def format(*args, **kwargs):
        if not args:
            raise TypeError("descriptor 'format' of 'Formatter' object "
                            "needs an argument")
        self, args = args[0], args[1:]  # allow the "self" keyword be passed
        try:
            format_string, args = args[0], args[1:] # allow the "format_string" keyword be passed
        except IndexError:
            if 'format_string' in kwargs:
                format_string = kwargs.pop('format_string')
            else:
                raise TypeError("format() missing 1 required positional "
                                "argument: 'format_string'")
        return self.vformat(format_string, args, kwargs)

    def vformat(self, format_string, args, kwargs):
        used_args = set()
        result = self._vformat(format_string, args, kwargs, used_args, 2)
        self.check_unused_args(used_args, args, kwargs)
        return result

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in \
                self.parse(format_string):

            # output the literal text
            if literal_text:
                result.append(literal_text)

            # if there's a field, output it
            if field_name is not None:
                # this is some markup, find the object and do
                #  the formatting

                # given the field_name, find the object it references
                #  and the argument it came from
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)

                # do any conversion on the resulting object
                obj = self.convert_field(obj, conversion)

                # expand the format spec, if needed
                format_spec = self._vformat(format_spec, args, kwargs,
                                            used_args, recursion_depth-1)

                # format the object and append to the result
                result.append(self.format_field(obj, format_spec))

        return ''.join(result)


    def get_value(self, key, args, kwargs):
        if isinstance(key, (int, long)):
            return args[key]
        else:
            return kwargs[key]


    def check_unused_args(self, used_args, args, kwargs):
        pass


    def format_field(self, value, format_spec):
        return format(value, format_spec)


    def convert_field(self, value, conversion):
        # do any conversion on the resulting object
        if conversion is None:
            return value
        elif conversion == 's':
            return str(value)
        elif conversion == 'r':
            return repr(value)
        raise ValueError("Unknown conversion specifier {0!s}".format(conversion))


    # returns an iterable that contains tuples of the form:
    # (literal_text, field_name, format_spec, conversion)
    # literal_text can be zero length
    # field_name can be None, in which case there's no
    #  object to format and output
    # if field_name is not None, it is looked up, formatted
    #  with format_spec and conversion and then used
    def parse(self, format_string):
        return format_string._formatter_parser()


    # given a field_name, find the object it references.
    #  field_name:   the field being looked up, e.g. "0.name"
    #                 or "lookup[3]"
    #  used_args:    a set of which args have been used
    #  args, kwargs: as passed in to vformat
    def get_field(self, field_name, args, kwargs):
        first, rest = field_name._formatter_field_name_split()

        obj = self.get_value(first, args, kwargs)

        # loop through the rest of the field_name, doing
        #  getattr or getitem as needed
        for is_attr, i in rest:
            if is_attr:
                obj = getattr(obj, i)
            else:
                obj = obj[i]

        return obj, first
