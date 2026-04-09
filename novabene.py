"""
novabene.py - Modulo per l'aritmetica Novabene (21 simboli)
Basato sulle regole definite in NovDec.html.
Include addizione, sottrazione e moltiplicazione esatta.
"""

from typing import List, Tuple, Dict

# =============================================================================
# 1. Definizione dei simboli e mappatura iniziale (solo per costruzione tabelle)
# =============================================================================
SYMBOLS = ['∅'] + [f"-{d}" for d in range(9, -1, -1)] + [f"+{d}" for d in range(0, 10)]

# Mappa simbolo -> valore decimale (usata solo per inizializzazione)
_SYM_TO_DEC: Dict[str, int] = {}
_SYM_TO_DEC['∅'] = 0
for d in range(9, -1, -1):
    _SYM_TO_DEC[f"-{d}"] = -(d + 1)
for d in range(0, 10):
    _SYM_TO_DEC[f"+{d}"] = d + 1

def _dec_to_nit(val: int) -> str:
    """Converte un intero in [-10,10] nel simbolo corrispondente."""
    if val == 0:
        return '∅'
    elif val > 0:
        return f"+{val-1}"
    else:
        return f"-{abs(val)-1}"

# =============================================================================
# 2. Tabelle di addizione e sottrazione (risultato, riporto/borrow)
# =============================================================================
ADD_TABLE: Dict[Tuple[str, str], Tuple[str, str]] = {}
SUB_TABLE: Dict[Tuple[str, str], Tuple[str, str]] = {}

for a in SYMBOLS:
    for b in SYMBOLS:
        s_add = _SYM_TO_DEC[a] + _SYM_TO_DEC[b]
        if -10 <= s_add <= 10:
            res_add, carry = _dec_to_nit(s_add), '∅'
        elif s_add > 10:
            res_add, carry = _dec_to_nit(s_add - 11), '+0'
        else:
            res_add, carry = _dec_to_nit(s_add + 11), '-0'
        ADD_TABLE[(a, b)] = (res_add, carry)

        s_sub = _SYM_TO_DEC[a] - _SYM_TO_DEC[b]
        if -10 <= s_sub <= 10:
            res_sub, borrow = _dec_to_nit(s_sub), '∅'
        elif s_sub > 10:
            res_sub, borrow = _dec_to_nit(s_sub - 11), '+0'
        else:
            res_sub, borrow = _dec_to_nit(s_sub + 11), '-0'
        SUB_TABLE[(a, b)] = (res_sub, borrow)

# =============================================================================
# 3. Tabella di moltiplicazione completa (unità, decine)
# =============================================================================
MUL_TABLE_FULL: Dict[Tuple[str, str], Tuple[str, str]] = {}
for a in SYMBOLS:
    for b in SYMBOLS:
        prod = _SYM_TO_DEC[a] * _SYM_TO_DEC[b]
        units = prod % 10
        tens = prod // 10
        # Gestione segno: il prodotto ha il segno di a*b
        if prod >= 0:
            unit_sym = _dec_to_nit(units)
            tens_sym = _dec_to_nit(tens) if tens > 0 else '∅'
        else:
            # prodotto negativo: units e tens negativi
            unit_sym = _dec_to_nit(-units) if units != 0 else '∅'
            tens_sym = _dec_to_nit(-tens) if tens != 0 else '∅'
            # riportiamo il segno negativo sull'unità
            if unit_sym != '∅':
                unit_sym = _dec_to_nit(-_SYM_TO_DEC[unit_sym])
            if tens_sym != '∅':
                tens_sym = _dec_to_nit(-_SYM_TO_DEC[tens_sym])
        MUL_TABLE_FULL[(a, b)] = (unit_sym, tens_sym)

# =============================================================================
# 4. Classe Nit (cifra Novabene)
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
        if not isinstance(other, Nit):
            return NotImplemented
        return self._symbol == other._symbol

    def __hash__(self):
        return hash(self._symbol)

    def __add__(self, other: 'Nit') -> 'Nit':
        return Nit(ADD_TABLE[(self._symbol, other._symbol)][0])

    def add_with_carry(self, other: 'Nit') -> Tuple['Nit', 'Nit']:
        res, carry = ADD_TABLE[(self._symbol, other._symbol)]
        return Nit(res), Nit(carry)

    def __sub__(self, other: 'Nit') -> 'Nit':
        return Nit(SUB_TABLE[(self._symbol, other._symbol)][0])

    def sub_with_borrow(self, other: 'Nit') -> Tuple['Nit', 'Nit']:
        res, borrow = SUB_TABLE[(self._symbol, other._symbol)]
        return Nit(res), Nit(borrow)

    def __mul__(self, other: 'Nit') -> Tuple['Nit', 'Nit']:
        """Restituisce (unità, decine) del prodotto."""
        u, t = MUL_TABLE_FULL[(self._symbol, other._symbol)]
        return Nit(u), Nit(t)

# =============================================================================
# 5. Operazioni multi‑cifra (little‑endian: indice 0 = cifra meno significativa)
# =============================================================================
def nit_add(a: List[Nit], b: List[Nit]) -> List[Nit]:
    max_len = max(len(a), len(b))
    result = []
    carry = Nit('∅')
    for i in range(max_len):
        ai = a[i] if i < len(a) else Nit('∅')
        bi = b[i] if i < len(b) else Nit('∅')
        s1, c1 = ai.add_with_carry(bi)
        s2, c2 = s1.add_with_carry(carry)
        total_carry, _ = c1.add_with_carry(c2)
        result.append(s2)
        carry = total_carry
    if carry.symbol != '∅':
        result.append(carry)
    return result

def nit_sub(a: List[Nit], b: List[Nit]) -> List[Nit]:
    max_len = max(len(a), len(b))
    result = []
    borrow = Nit('∅')
    for i in range(max_len):
        ai = a[i] if i < len(a) else Nit('∅')
        bi = b[i] if i < len(b) else Nit('∅')
        temp, b1 = ai.sub_with_borrow(bi)
        res, b2 = temp.sub_with_borrow(borrow)
        total_borrow, _ = b1.add_with_carry(b2)
        result.append(res)
        borrow = total_borrow
    while result and result[-1].symbol == '∅':
        result.pop()
    if not result:
        result.append(Nit('∅'))
    return result

def nit_mul(a: List[Nit], b: List[Nit]) -> List[Nit]:
    """Moltiplicazione lunga corretta."""
    result = [Nit('∅')]
    for i, ai in enumerate(a):
        carry = Nit('∅')
        row = [Nit('∅')] * i
        for bj in b:
            unit, tens = ai * bj      # qui usiamo il nuovo __mul__ che restituisce due cifre
            s1, c1 = unit.add_with_carry(carry)
            row.append(s1)
            # Il carry per la prossima colonna è tens + c1
            carry, _ = tens.add_with_carry(c1)
        if carry.symbol != '∅':
            row.append(carry)
        result = nit_add(result, row)
    # Rimuovi zeri finali superflui (ma non l'ultimo)
    while len(result) > 1 and result[-1].symbol == '∅':
        result.pop()
    return result

def nit_compare(a: List[Nit], b: List[Nit]) -> int:
    max_len = max(len(a), len(b))
    a_pad = a + [Nit('∅')] * (max_len - len(a))
    b_pad = b + [Nit('∅')] * (max_len - len(b))
    for i in range(max_len-1, -1, -1):
        idx_a = SYMBOLS.index(a_pad[i].symbol)
        idx_b = SYMBOLS.index(b_pad[i].symbol)
        if idx_a < idx_b:
            return -1
        elif idx_a > idx_b:
            return 1
    return 0

def nit_from_string(s: str) -> List[Nit]:
    symbols = []
    i = 0
    while i < len(s):
        if s[i] in '+-':
            symbols.append(s[i:i+2])
            i += 2
        elif s[i] == '∅':
            symbols.append('∅')
            i += 1
        elif s[i].isdigit():
            symbols.append('+' + s[i])
            i += 1
        else:
            raise ValueError(f"Formato non valido: {s}")
    return [Nit(sym) for sym in reversed(symbols)]

def nit_to_string(num: List[Nit]) -> str:
    if not num:
        return '∅'
    # Unisci cifre consecutive con lo stesso segno (es. +0+2 -> +02)
    result = []
    current_sign = None
    for n in reversed(num):
        sym = n.symbol
        if sym == '∅':
            result.append('∅')
            current_sign = None
        else:
            sign = sym[0]
            digit = sym[1]
            if sign == current_sign:
                result.append(digit)
            else:
                result.append(sym)
                current_sign = sign
    return ''.join(result)

# =============================================================================
# 6. Test
# =============================================================================
if __name__ == "__main__":
    print("Test addizione:")
    a = Nit('+3'); b = Nit('+8')
    res, carry = a.add_with_carry(b)
    print(f"{a} + {b} = {res} con riporto {carry}")

    x = nit_from_string("+5")   # 6
    y = nit_from_string("+7")   # 8
    z = nit_add(x, y)
    print(f"+5 + +7 = {nit_to_string(z)}")

    print("\nTest sottrazione:")
    u = nit_from_string("+3"); v = nit_from_string("+1")
    w = nit_sub(u, v)
    print(f"+3 - +1 = {nit_to_string(w)}")

    print("\nTest moltiplicazione:")
    m = nit_mul(x, y)
    print(f"+5 * +7 = {nit_to_string(m)}")   # dovrebbe dare +43 (48)
