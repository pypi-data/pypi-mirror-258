"""
Macros extend Markdown by a [MYMACRO::arg1::arg2] syntax.
Some macros are just that: A fixed manner to convert their arguments into a string.
Some use state that gets baked into their expander function via a closure.
Some use state that is maintained here in an arbitrarily-named namespace, 
so that several macros can share state.
Macros can get notified when the next part starts being processed, 
so they can reset part-specific state. 
"""

import dataclasses
import re
import typing as tg

import markdown

import base as b

@dataclasses.dataclass
class Macrocall:
    """Represent where and how a macro was called, allow producing errors/warnings for it."""
    md: markdown.Markdown
    filename: str
    partname: str
    macrocall_text: str
    macroname: str
    arg1: b.OStr
    arg2: b.OStr

    def error(self, msg: str):
        b.error(f"'{self.filename}': {self.macrocall_text}\n  {msg}")

    def warning(self, msg: str):
        b.warning(f"'{self.filename}': {self.macrocall_text}\n  {msg}")


Macroexpander = tg.Callable[[Macrocall], str]
Partswitcher = tg.Callable[[str, str], None]  # macroname, newpartname
Macrodef = tg.Tuple[int, Macroexpander, Partswitcher]  # num_args, expander, switcher

macrodefs: dict[str, Macrodef] = dict()  # macroname -> macrodef
macrostate: dict[str, tg.Any] = dict()  # namespace -> state_object

macro_regexp = r"\[([A-Z][A-Z0-9_]+)(?:::(.+?))?(?:::(.+?))?\](?=[^(]|$)"  
# bracketed all-caps: [ALL2_CAPS] with zero to two arguments: [NAME::arg] or [NAME::arg1::arg2]
# suppress matches on normal links: [TEXT](url)


def expand_macros(sourcefile: str, partname: str, markup: str) -> str:
    """Apply matching macrodefs, report errors for non-matching macro calls."""
    def my_expand_macro(mm: re.Match) -> str:
        return expand_macro(sourcefile, partname, mm)
    return re.sub(macro_regexp, my_expand_macro, markup)


def expand_macro(sourcefile: str, partname: str, mm: re.Match) -> str:
    """Apply matching macrodef or report error."""
    global macrodefs
    import sdrl.markdown
    call, macroname, arg1, arg2 = mm.group(), mm.group(1), mm.group(2), mm.group(3)
    macrocall = Macrocall(md=sdrl.markdown.md, filename=sourcefile, partname=partname,
                          macrocall_text=call,
                          macroname=macroname, arg1=arg1, arg2=arg2)
    my_numargs = (arg1 is not None) + (arg2 is not None)
    # ----- check name:
    if macroname not in macrodefs:
        macrocall.error(f"Macro '{macroname}' is not defined")
        return call  # unexpanded version helps the user most
    numargs, expander, switcher = macrodefs[macroname]
    # ----- check args:
    if my_numargs != numargs:
        macrocall.error("Macro '%s' called with %d args, expects %d" %
                        (macroname, my_numargs, numargs))
        return call  # unexpanded version helps the user most
    # ----- expand:
    b.debug(f"expanding {macrocall.macrocall_text}")
    return expander(macrocall)


def get_state(namespace: str) -> tg.Any:
    return macrostate[namespace]  # must exist


def set_state(namespace: str, obj: tg.Any):
    global macrostate
    macrostate[namespace] = obj


def switch_part(newpartname: str):
    for macroname, macrodef in macrodefs.items():
        nargs, expander, switcher = macrodef
        switcher(macroname, newpartname)


def register_macro(name: str, numargs: int, expander: Macroexpander, 
                   switcher: Partswitcher = lambda mn,pn: None, redefine=False):
    global macrodefs
    if redefine:
        assert name in macrodefs
    else:
        assert name not in macrodefs
    assert 0 <= numargs <= 2
    assert name == name.upper()  # macronames must be all uppercase
    macrodefs[name] = (numargs, expander, switcher)


def _testmode_reset():
    global macrodefs, macrostate
    macrodefs = dict()
    macrostate = dict()