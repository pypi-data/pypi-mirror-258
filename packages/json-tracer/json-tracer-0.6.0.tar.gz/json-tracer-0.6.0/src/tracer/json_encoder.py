# Online Python Tutor
# https://github.com/pgbovine/OnlinePythonTutor/
#
# Copyright (C) Philip J. Guo (philip@pgbovine.net)
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Thanks to John DeNero for making the encoder work on both Python 2 and 3
# (circa 2012-2013)


# Given an arbitrary piece of Python data, encode it in such a manner
# that it can be later encoded into JSON.
#   http://json.org/
#
# We use this function to encode run-time traces of data structures
# to send to the front-end.
#
# Format:
#   Primitives:
#   * None, int, long, float, str, bool - unchanged
#     (json.dumps encodes these fine verbatim, except for inf, -inf, and nan)
#
#   exceptions: float('inf')  -> ['SPECIAL_FLOAT', 'Infinity']
#               float('-inf') -> ['SPECIAL_FLOAT', '-Infinity']
#               float('nan')  -> ['SPECIAL_FLOAT', 'NaN']
#               x == int(x)   -> ['SPECIAL_FLOAT', '%.1f' % x]
#               (this way, 3.0 prints as '3.0' and not as 3, which looks like an int)
#
#   If render_heap_primitives is True, then primitive values are rendered
#   on the heap as ['HEAP_PRIMITIVE', <type name>, <value>]
#
#   (for SPECIAL_FLOAT values, <value> is a list like ['SPECIAL_FLOAT', 'Infinity'])
#
#   added on 2018-06-13:
#   ['IMPORTED_FAUX_PRIMITIVE', <type>, <label>] - renders externally imported objects
#                                                  like they were primitives, to save
#                                                  space and to prevent from having to
#                                                  recurse into of them to see internals
#
#   Compound objects:
#   * list     - ['LIST', elt1, elt2, elt3, ..., eltN]
#   * tuple    - ['TUPLE', elt1, elt2, elt3, ..., eltN]
#   * set      - ['SET', elt1, elt2, elt3, ..., eltN]
#   * dict     - ['DICT', [key1, value1], [key2, value2], ..., [keyN, valueN]]
#   * instance - ['INSTANCE', class name, [attr1, value1], [attr2, value2], ..., [attrN, valueN]]
#   * instance with non-trivial __str__ defined - ['INSTANCE_PPRINT', class name, <__str__ value>, [attr1, value1], [attr2, value2], ..., [attrN, valueN]]
#   * class    - ['CLASS', class name, [list of superclass names], [attr1, value1], [attr2, value2], ..., [attrN, valueN]]
#   * function - ['FUNCTION', function name, parent frame ID (for nested functions),
#                 [*OPTIONAL* list of pairs of default argument names/values] ] <-- final optional element added on 2018-06-13
#   * module   - ['module', module name]
#   * other    - [<type name>, string representation of object]
#   * compound object reference - ['REF', target object's unique_id]
#
# the unique_id is derived from id(), which allows us to capture aliasing


import math
import re
import types
from collections import defaultdict
import inspect

typeRE = re.compile("<type '(.*)'>")
classRE = re.compile("<class '(.*)'>")

# number of significant digits for floats
FLOAT_PRECISION = 4


def is_class(dat):
    """Return whether dat is a class."""
    return isinstance(dat, type)


def is_instance(dat):
    """Return whether dat is an instance of a class."""
    return type(dat) not in PRIMITIVE_TYPES and \
        isinstance(type(dat), type) and \
        not isinstance(dat, type)


def get_name(obj):
    """Return the name of an object."""
    return obj.__name__ if hasattr(obj, '__name__') else get_name(type(obj))


PRIMITIVE_TYPES = (int, float, str, bool, type(None))


def encode_primitive(dat):
    t = type(dat)
    if t is float:
        if math.isinf(dat):
            if dat > 0:
                return ['SPECIAL_FLOAT', 'Infinity']
            else:
                return ['SPECIAL_FLOAT', '-Infinity']
        elif math.isnan(dat):
            return ['SPECIAL_FLOAT', 'NaN']
        else:
            # render floats like 3.0 as '3.0' and not as 3
            if dat == int(dat):
                return ['SPECIAL_FLOAT', '%.1f' % dat]
            else:
                return round(dat, FLOAT_PRECISION)
    else:
        # return all other primitives verbatim
        return dat


# grab a line number like ' <line 2>' or ' <line 2b>'
def create_lambda_line_number(codeobj, line_to_lambda_code):
    try:
        lambda_lineno = codeobj.co_firstlineno
        lineno_str = str(lambda_lineno)
        return ' <line ' + lineno_str + '>'
    except:
        return ''


# Note that this might BLOAT MEMORY CONSUMPTION since we're holding on
# to every reference ever created by the program without ever releasing
# anything!
class ObjectEncoder:
    def __init__(self, parent):
        self.parent = parent  # should be a PGLogger object

        # Key: canonicalized small ID
        # Value: encoded (compound) heap object
        self.encoded_heap_objects = {}

        self.render_heap_primitives = parent.render_heap_primitives

        self.id_to_small_IDs = {}
        self.cur_small_ID = 1

        # wow, creating unique identifiers for lambdas is quite annoying,
        # especially if we want to properly differentiate:
        # 1.) multiple lambdas defined on the same line, and
        # 2.) the same lambda code defined multiple times on different lines
        #
        # However, it gets confused when there are multiple identical
        # lambdas on the same line, like:
        # f(lambda x:x*x, lambda y:y*y, lambda x:x*x)

        # (assumes everything is in one file)
        # Key:   line number
        # Value: list of the code objects of lambdas defined
        #        on that line in the order they were defined
        self.line_to_lambda_code = defaultdict(list)

    def get_heap(self):
        return self.encoded_heap_objects

    def reset_heap(self):
        # VERY IMPORTANT to reassign to an empty dict rather than just
        # clearing the existing dict, since get_heap() could have been
        # called earlier to return a reference to a previous heap state
        self.encoded_heap_objects = {}

    def set_function_parent_frame_ID(self, ref_obj, enclosing_frame_id):
        assert ref_obj[0] == 'REF'
        func_obj = self.encoded_heap_objects[ref_obj[1]]
        assert func_obj[0] == 'FUNCTION'
        func_obj[-1] = enclosing_frame_id

    # return either a primitive object or an object reference;
    # and as a side effect, update encoded_heap_objects
    def encode(self, dat, get_parent):
        """Encode a data value DAT using the GET_PARENT function for parent ids."""
        # primitive type
        if not self.render_heap_primitives and type(dat) in PRIMITIVE_TYPES:
            return encode_primitive(dat)
        # compound type - return an object reference and update encoded_heap_objects
        else:
            # IMPORTED_FAUX_PRIMITIVE feature added on 2018-06-13:
            is_externally_defined = False  # is dat defined in external (i.e., non-user) code?
            try:
                # some objects don't return anything for getsourcefile() but DO return
                # something legit for getmodule(). e.g., "from io import StringIO"
                # so TRY getmodule *first* and then fall back on getsourcefile
                # since getmodule seems more robust empirically ...
                gsf = inspect.getmodule(dat).__file__
                if not gsf:
                    gsf = inspect.getsourcefile(dat)

                # a hacky heuristic is that if gsf is an absolute path, then it's likely
                # to be some library function and *not* in user-defined code
                #
                # NB: don't use os.path.isabs() since it doesn't work on some
                # python installations (e.g., on my webserver) and also adds a
                # dependency on the os module. just do a simple check:
                #
                # hacky: do other checks for strings that are indicative of files
                # that load user-written code, like '__main__.py'
                if gsf and gsf[0] == '/' and '__main__.py' not in gsf:
                    is_externally_defined = True
            except (AttributeError, TypeError):
                pass  # fail soft

            my_id = id(dat)

            # if this is an externally-defined object (i.e., from an imported
            # module, don't try to recurse into it since we don't want to see
            # the internals of imported objects; just return an
            # IMPORTED_FAUX_PRIMITIVE object and continue along on our way
            if is_externally_defined:
                dat_type = 'object'
                dat_label = dat.__str__()
                try:
                    dat_type = get_name(type(dat))
                    if dat_label[0] == '<' and dat_label[-1] == '>':
                        dat_label = get_name(dat)
                except:
                    pass
                return ['IMPORTED_FAUX_PRIMITIVE', dat_type, dat_label]  # punt early!

            try:
                my_small_id = self.id_to_small_IDs[my_id]
            except KeyError:
                my_small_id = self.cur_small_ID
                self.id_to_small_IDs[my_id] = self.cur_small_ID
                self.cur_small_ID += 1

            del my_id  # to prevent bugs later in this function

            ret = ['REF', my_small_id]

            # punt early if you've already encoded this object
            if my_small_id in self.encoded_heap_objects:
                return ret

            # major side-effect!
            new_obj = []
            self.encoded_heap_objects[my_small_id] = new_obj

            typ = type(dat)

            if typ == list:
                new_obj.append('LIST')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == tuple:
                new_obj.append('TUPLE')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == set:
                new_obj.append('SET')
                for e in dat:
                    new_obj.append(self.encode(e, get_parent))
            elif typ == dict:
                new_obj.append('DICT')
                for (k, v) in dat.items():
                    # don't display some built-in locals ...
                    if k not in ('__module__', '__return__', '__locals__'):
                        new_obj.append([self.encode(k, get_parent), self.encode(v, get_parent)])
            elif typ in (types.FunctionType, types.MethodType):
                argspec = inspect.getfullargspec(dat)

                printed_args = [e for e in argspec.args]

                default_arg_names_and_vals = []
                if argspec.defaults:
                    num_missing_defaults = len(printed_args) - len(argspec.defaults)
                    assert num_missing_defaults >= 0
                    # tricky tricky tricky how default positional arguments work!
                    for i in range(num_missing_defaults, len(printed_args)):
                        default_arg_names_and_vals.append(
                            (printed_args[i], self.encode(argspec.defaults[i - num_missing_defaults], get_parent)))

                if argspec.varargs:
                    printed_args.append('*' + argspec.varargs)

                # kwonlyargs come before varkw
                if argspec.kwonlyargs:
                    printed_args.extend(argspec.kwonlyargs)
                    if argspec.kwonlydefaults:
                        # iterate in order of appearance in kwonlyargs
                        for varname in argspec.kwonlyargs:
                            if varname in argspec.kwonlydefaults:
                                val = argspec.kwonlydefaults[varname]
                                default_arg_names_and_vals.append((varname, self.encode(val, get_parent)))
                if argspec.varkw:
                    printed_args.append('**' + argspec.varkw)

                func_name = get_name(dat)

                pretty_name = func_name

                # sometimes might fail for, say, <genexpr>, so just ignore
                # failures for now ...
                try:
                    pretty_name += '(' + ', '.join(printed_args) + ')'
                except TypeError:
                    pass

                # put a line number suffix on lambdas to more uniquely identify
                # them, since they don't have names
                if func_name == '<lambda>':
                    cod = dat.__code__
                    lst = self.line_to_lambda_code[cod.co_firstlineno]
                    if cod not in lst:
                        lst.append(cod)
                    pretty_name += create_lambda_line_number(cod,
                                                             self.line_to_lambda_code)

                encoded_val = ['FUNCTION', pretty_name, None]
                if get_parent:
                    enclosing_frame_id = get_parent(dat)
                    encoded_val[2] = enclosing_frame_id
                new_obj.extend(encoded_val)
                # OPTIONAL!!!
                if default_arg_names_and_vals:
                    new_obj.append(default_arg_names_and_vals)  # *append* it as a single list element

            elif typ is types.BuiltinFunctionType:
                pretty_name = get_name(dat) + '(...)'
                new_obj.extend(['FUNCTION', pretty_name, None])
            elif is_class(dat) or is_instance(dat):
                self.encode_class_or_instance(dat, new_obj)
            elif typ is types.ModuleType:
                new_obj.extend(['module', dat.__name__])
            elif typ in PRIMITIVE_TYPES:
                assert self.render_heap_primitives
                new_obj.extend(['HEAP_PRIMITIVE', type(dat).__name__, encode_primitive(dat)])
            else:
                typeStr = str(typ)
                m = typeRE.match(typeStr)

                if not m:
                    m = classRE.match(typeStr)

                assert m, typ

                encoded_dat = str(dat)
                new_obj.extend([m.group(1), encoded_dat])

            return ret

    def encode_class_or_instance(self, dat, new_obj):
        """Encode dat as a class or instance."""
        if is_instance(dat):
            if hasattr(dat, '__class__'):
                # common case ...
                class_name = get_name(dat.__class__)
            else:
                # super special case for something like
                # "from datetime import datetime_CAPI" in Python 3.2,
                # which is some weird 'PyCapsule' type ...
                # http://docs.python.org/release/3.1.5/c-api/capsule.html
                class_name = get_name(type(dat))

            pprint_str = None
            # do you or any of your superclasses have a __str__ field? if so, pretty-print yourself!
            if hasattr(dat, '__str__'):
                try:
                    pprint_str = dat.__str__()

                    # sometimes you'll get 'trivial' pprint_str like: '<__main__.MyObj object at 0x10f465cd0>'
                    # or '<module 'collections' ...'
                    # IGNORE THOSE!!!
                    if pprint_str[0] == '<' and pprint_str[-1] == '>' and (
                            ' at ' in pprint_str or pprint_str.startswith('<module')):
                        pprint_str = None
                except:
                    pass

            # TODO: filter for trivial-looking pprint_str like those produced
            # by object.__str__
            if pprint_str:
                new_obj.extend(['INSTANCE_PPRINT', class_name, pprint_str])
            else:
                new_obj.extend(['INSTANCE', class_name])

            # don't traverse inside modules, or else risk EXPLODING the visualization
            if class_name == 'module':
                return
        else:
            superclass_names = [e.__name__ for e in dat.__bases__ if e is not object]
            new_obj.extend(['CLASS', get_name(dat), superclass_names])

        # traverse inside of its __dict__ to grab attributes
        # (filter out useless-seeming ones, based on anecdotal observation):
        hidden = ('__doc__', '__module__', '__return__', '__dict__',
                  '__locals__', '__weakref__', '__qualname__')
        if hasattr(dat, '__dict__'):
            user_attrs = sorted([e for e in dat.__dict__ if e not in hidden])
        else:
            user_attrs = []

        for attr in user_attrs:
            new_obj.append([self.encode(attr, None), self.encode(dat.__dict__[attr], None)])
