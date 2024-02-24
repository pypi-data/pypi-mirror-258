# ------------------------------------------------------------------------------
#  es7s/commons
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import pytermor as pt
from pytermor import PTT, FT

from .common import Regex

URL_REGEX = Regex(
    R"""
 (https?)(:/)
 ([-/a-zA-Z0-9_%.]+)
 ([-/a-zA-Z0-9_%])
""",
    verbose=True,
)

_chars_to_codes = lambda *s: {*map(ord, s)}

UCS_CYRILLIC = _chars_to_codes(
    *pt.char_range("а", "я"),
    *pt.char_range("А", "Я"),
    *("ё", "Ё"),
)

# fmt: off
UCS_CONTROL_CHARS = pt.CONTROL_CHARS + [
    0x85,   0x061C, 0x200E, 0x200F,
    0x2028, 0x2029, 0x202A, 0x202B,
    0x202C, 0x202D, 0x202E, 0x2066,
    0x2067, 0x2068, 0x2069,
]
# fmt: on


class NamedGroupsRefilter(pt.AbstractNamedGroupsRefilter):
    def __init__(self, pattern: PTT[str], group_st_map: dict[str, FT], renderer: pt.IRenderer):
        super().__init__(pattern, group_st_map)
        self._renderer = renderer

    def _render(self, v: pt.RT, st: pt.FT) -> str:
        return self._renderer.render(v, st)


class RegexValRefilter(NamedGroupsRefilter):
    def __init__(self, pattern: pt.filter.PTT[str], val_st: pt.FT, renderer: pt.IRenderer):
        super().__init__(pattern, {"val": val_st}, renderer)


class Transmap(dict[int, str]):
    def __init__(self, inp: str, out: str):
        if (li := len(inp)) != (lo := len(out)):
            raise ValueError(f"Strings should have equal length ({li} != {lo})")
        self._inp_set = set(inp)

        super().__init__(str.maketrans({k: v for (k, v) in zip(inp, out)}))

    def translate(self, s: str, *, strict: bool = False) -> str:
        if strict and (miss := set(s) - self._inp_set):
            raise ValueError(
                f"String contains characters without mapping: "
                + f"{' '.join([*miss][:5])}"
                + (f" (+{len(miss)} more)" if len(miss) > 5 else "")
            )
        return s.translate(self)


SUBSCRIPT_TRANS = Transmap(
    # missing: "bcdfgqwyz" and all capitals
    "0123456789+-=()aehijklmnoprstuvx",
    "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ",
)


SUPERSCRIPT_TRANS = Transmap(
    # missing: "SXYZ"
    "0123456789+-=()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVW",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ𐞥ʳˢᵗᵘᵛʷˣʸᶻᴬᴮꟲᴰᴱfᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾꟴᴿᵀᵁⱽᵂ",
)


def to_subscript(s: str, *, strict: bool = False) -> str:
    return SUBSCRIPT_TRANS.translate(s.lower(), strict=strict)


def to_superscript(s: str, *, strict: bool = False) -> str:
    return SUPERSCRIPT_TRANS.translate(s, strict=strict)


def re_unescape(s: str) -> str:
    return s.replace("\\", "")


#
# def wrap_sgr(
#     rendered: str | list[str],
#     width: int,
#     indent_first: int = 0,
#     indent_subseq: int = 0,
# ) -> str:
#     # modified to handle ⏺ lists offsets
#
#     sgrs: list[str] = []
#
#     def push(m: t.Match):
#         sgrs.append(m.group())
#         return pt.text._PRIVATE_REPLACER
#
#     if isinstance(rendered, str):  # input can be just one paragraph
#         rendered = [rendered]
#
#     inp = "\n\n".join(rendered).split("\n\n")
#     result = ""
#     for raw_line in inp:
#         # had an inspiration and wrote it; no idea how does it work exactly, it just does
#         replaced_line = re.sub(r"(\s?\S?)((\x1b\[([0-9;]*)m)+)", push, raw_line)
#         if replaced_line.lstrip().startswith("⏺"):
#             cur_indent_first = indent_first
#             cur_indent_subseq = indent_subseq + 2
#         else:
#             cur_indent_first = indent_first
#             cur_indent_subseq = indent_subseq
#         wrapped_line = f"\n".join(
#             textwrap.wrap(
#                 replaced_line,
#                 width=width,
#                 initial_indent=(cur_indent_first * " "),
#                 subsequent_indent=(cur_indent_subseq * " "),
#             )
#         )
#         final_line = re.sub(pt.text._PRIVATE_REPLACER, lambda _: sgrs.pop(0), wrapped_line)
#         result += final_line + "\n"
#     return result
