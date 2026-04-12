"""
arithmetic.py - Modulo aritmetico Novae (21 simboli)
Allineato al motore HTML definitivo e al Principia Novae Mathematicae.
"""

from typing import List, Tuple, Dict

# =============================================================================
# 1. Simboli e mappatura
# =============================================================================
SYMBOLS = ['-9','-8','-7','-6','-5','-4','-3','-2','-1','-0','∅','+0','+1','+2','+3','+4','+5','+6','+7','+8','+9']

_SYM_TO_DEC: Dict[str, int] = {}
_DEC_TO_SYM: Dict[int, str] = {}

def _init_maps():
    _SYM_TO_DEC['∅'] = 0
    _DEC_TO_SYM[0] = '∅'
    for d in range(9, -1, -1):
        sym = f"-{d}"
        val = -(d + 1)
        _SYM_TO_DEC[sym] = val
        _DEC_TO_SYM[val] = sym
    for d in range(0, 10):
        sym = f"+{d}"
        val = d + 1
        _SYM_TO_DEC[sym] = val
        _DEC_TO_SYM[val] = sym

_init_maps()

# =============================================================================
# 2. Tabelle di addizione e sottrazione (soglia 10)
# =============================================================================
ADD_TABLE: Dict[Tuple[str, str], Tuple[str, str]] = {}
SUB_TABLE: Dict[Tuple[str, str], Tuple[str, str]] = {}

for a in SYMBOLS:
    for b in SYMBOLS:
        sa = _SYM_TO_DEC[a]
        sb = _SYM_TO_DEC[b]
        # Addizione
        s_add = sa + sb
        if s_add > 10:
            res = _DEC_TO_SYM[s_add - 10]
            carry = '+0'
        elif s_add < -10:
            res = _DEC_TO_SYM[s_add + 10]
            carry = '-0'
        else:
            res = _DEC_TO_SYM[s_add]
            carry = '∅'
        ADD_TABLE[(a, b)] = (res, carry)

        # Sottrazione
        s_sub = sa - sb
        if s_sub > 10:
            res = _DEC_TO_SYM[s_sub - 10]
            borrow = '+0'
        elif s_sub < -10:
            res = _DEC_TO_SYM[s_sub + 10]
            borrow = '-0'
        else:
            res = _DEC_TO_SYM[s_sub]
            borrow = '∅'
        SUB_TABLE[(a, b)] = (res, borrow)

# =============================================================================
# 3. Moltiplicazione di singoli Nit
# =============================================================================
def mul_nits(a: str, b: str) -> Tuple[str, str]:
    """Restituisce (unità, decine) come simboli."""
    prod = _SYM_TO_DEC[a] * _SYM_TO_DEC[b]
    unit_val = prod % 10
    tens_val = prod // 10
    if prod >= 0:
        unit = _DEC_TO_SYM[unit_val]
        tens = _DEC_TO_SYM[tens_val] if tens_val != 0 else '∅'
    else:
        unit = _DEC_TO_SYM[-unit_val] if unit_val != 0 else '∅'
        tens = _DEC_TO_SYM[-tens_val] if tens_val != 0 else '∅'
        if unit != '∅':
            unit = _DEC_TO_SYM[-_SYM_TO_DEC[unit]]
        if tens != '∅':
            tens = _DEC_TO_SYM[-_SYM_TO_DEC[tens]]
    return unit, tens

# =============================================================================
# 4. Classe Nit
# =============================================================================
class Nit:
    __slots__ = ('_symbol',)
    def __init__(self, symbol: str):
        if symbol not in SYMBOLS:
            raise ValueError(f"Simbolo non valido: {symbol}")
        self._symbol = symbol

    @property
    def symbol(self) -> str:
        return self._symbol

    def __repr__(self):
        return f"Nit('{self._symbol}')"

    def __str__(self):
        return self._symbol

    def __eq__(self, other):
        return isinstance(other, Nit) and self._symbol == other._symbol

    def __hash__(self):
        return hash(self._symbol)

    def to_dec(self) -> int:
        return _SYM_TO_DEC[self._symbol]

    def add_with_carry(self, other: 'Nit') -> Tuple['Nit', 'Nit']:
        res, carry = ADD_TABLE[(self._symbol, other._symbol)]
        return Nit(res), Nit(carry)

    def sub_with_borrow(self, other: 'Nit') -> Tuple['Nit', 'Nit']:
        res, borrow = SUB_TABLE[(self._symbol, other._symbol)]
        return Nit(res), Nit(borrow)

# =============================================================================
# 5. Normalizzazione (elimina ∅ interni e finali)
# =============================================================================
def normalize(lst: List[Nit]) -> List[Nit]:
    if not lst:
        return [Nit('∅')]
    res = [n.symbol for n in lst]
    # Rimuovi ∅ finali (zeri non significativi)
    while len(res) > 1 and res[-1] == '∅':
        res.pop()
    if len(res) == 1 and res[0] == '∅':
        return [Nit('∅')]
    # Converti ∅ interni
    changed = True
    while changed:
        changed = False
        for i in range(len(res)):
            if res[i] == '∅' and len(res) > 1:
                sign = None
                for s in res:
                    if s != '∅':
                        sign = s[0]
                        break
                if sign is None:
                    return [Nit('∅')]
                replacement = '+9' if sign == '+' else '-9'
                res[i] = replacement
                carry = -1
                j = i + 1
                while carry != 0:
                    if j >= len(res):
                        res.append(_DEC_TO_SYM[carry])
                        carry = 0
                    else:
                        val = _SYM_TO_DEC[res[j]] + carry
                        res[j] = _DEC_TO_SYM[val]
                        carry = 0
                    j += 1
                changed = True
                break
    return [Nit(s) for s in res]

# =============================================================================
# 6. Operazioni multi‑cifra
# =============================================================================
def nit_add(a: List[Nit], b: List[Nit]) -> List[Nit]:
    max_len = max(len(a), len(b))
    res = []
    carry = Nit('∅')
    for i in range(max_len):
        ai = a[i] if i < len(a) else Nit('∅')
        bi = b[i] if i < len(b) else Nit('∅')
        s1, c1 = ai.add_with_carry(bi)
        s2, c2 = s1.add_with_carry(carry)
        c12, _ = c1.add_with_carry(c2)
        res.append(s2)
        carry = c12
    if carry.symbol != '∅':
        res.append(carry)
    return normalize(res)

def nit_sub(a: List[Nit], b: List[Nit]) -> List[Nit]:
    max_len = max(len(a), len(b))
    res = []
    borrow = Nit('∅')
    for i in range(max_len):
        ai = a[i] if i < len(a) else Nit('∅')
        bi = b[i] if i < len(b) else Nit('∅')
        s1, b1 = ai.sub_with_borrow(bi)
        s2, b2 = s1.sub_with_borrow(borrow)
        b12, _ = b1.add_with_carry(b2)
        res.append(s2)
        borrow = b12
    return normalize(res)

def nit_mul(a: List[Nit], b: List[Nit]) -> List[Nit]:
    # Casi speciali per zero e uno
    dec_a = sum(n.to_dec() * (10**i) for i, n in enumerate(a))
    dec_b = sum(n.to_dec() * (10**i) for i, n in enumerate(b))
    if dec_a == 0 or dec_b == 0:
        return [Nit('∅')]
    if dec_a == 1:
        return normalize(b)
    if dec_b == 1:
        return normalize(a)
    # Moltiplicazione lunga
    result = [Nit('∅')]
    for i, ai in enumerate(a):
        row = [Nit('∅')] * i
        carry = Nit('∅')
        for bj in b:
            unit_sym, tens_sym = mul_nits(ai.symbol, bj.symbol)
            unit = Nit(unit_sym)
            tens = Nit(tens_sym)
            s1, c1 = unit.add_with_carry(carry)
            row.append(s1)
            carry, _ = tens.add_with_carry(c1)
        if carry.symbol != '∅':
            row.append(carry)
        result = nit_add(result, row)
    return normalize(result)

def nit_div(a: List[Nit], b: List[Nit]) -> Tuple[List[Nit], List[Nit]]:
    dec_a = sum(n.to_dec() * (10**i) for i, n in enumerate(a))
    dec_b = sum(n.to_dec() * (10**i) for i, n in enumerate(b))
    if dec_b == 0:
        raise ZeroDivisionError("Divisione per zero")
    q = dec_a // dec_b
    r = dec_a % dec_b
    # Converti quoziente e resto in liste little‑endian
    def from_dec(n: int) -> List[Nit]:
        if n == 0:
            return [Nit('∅')]
        sign = '+' if n > 0 else '-'
        n_abs = abs(n)
        digits = []
        while n_abs > 0:
            r = n_abs % 10
            if r == 0:
                digits.append(Nit('+9' if sign == '+' else '-9'))
                n_abs = (n_abs - 10) // 10
            else:
                digits.append(Nit(sign + str(r-1)))
                n_abs = (n_abs - r) // 10
        return digits
    return from_dec(q), from_dec(r)

# =============================================================================
# 7. Conversioni stringa <-> lista
# =============================================================================
def nit_from_string(s: str) -> List[Nit]:
    s = s.strip()
    if s in ('', '∅'):
        return [Nit('∅')]
    if s == '0':
        return [Nit('+0')]
    syms = []
    i = 0
    sign = None
    while i < len(s):
        ch = s[i]
        if ch in '+-':
            sign = ch
            i += 1
        elif ch == '∅':
            syms.append('∅')
            sign = None
            i += 1
        elif ch.isdigit():
            syms.append((sign if sign else '+') + ch)
            i += 1
        else:
            raise ValueError(f"Carattere non valido: {ch}")
    return [Nit(sym) for sym in reversed(syms)]

def nit_to_string(lst: List[Nit]) -> str:
    if not lst:
        return '∅'
    norm = normalize(lst)
    if len(norm) == 1 and norm[0].symbol == '∅':
        return '∅'
    sign = None
    for n in norm:
        if n.symbol != '∅':
            sign = n.symbol[0]
            break
    if sign is None:
        return '∅'
    rev = [n.symbol for n in reversed(norm)]
    out = '-' if sign == '-' else ''
    for sym in rev:
        if sym == '∅':
            out += '0'
        else:
            out += sym[1]
    return out

# =============================================================================
# 8. Test interni
# =============================================================================
if __name__ == "__main__":
    # Test addizione
    a = nit_from_string("5")
    b = nit_from_string("7")
    s = nit_add(a, b)
    print(f"5 + 7 = {nit_to_string(s)}")  # 03

    # Test moltiplicazione
    m = nit_mul(nit_from_string("0"), nit_from_string("9"))
    print(f"0 × 9 = {nit_to_string(m)}")  # 9

    # Test divisione
    q, r = nit_div(nit_from_string("8"), nit_from_string("2"))
    print(f"8 ÷ 2 = {nit_to_string(q)} resto {nit_to_string(r)}")  # 2 resto ∅
