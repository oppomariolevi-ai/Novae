from novabene import Nit, nit_add, nit_mul, nit_compare, nit_from_string, nit_to_string, SYMBOLS, _SYM_TO_DEC, _dec_to_nit
import random
from typing import List

class IcosahedronNeuron:
    def __init__(self, weights: List[Nit] = None, bias: List[Nit] = None):
        if weights is None:
            self.weights = [Nit(random.choice(SYMBOLS)) for _ in range(13)]
        else:
            self.weights = weights[:]
        self.bias = bias if bias is not None else [Nit('∅')]

    def forward(self, inputs: List[Nit]) -> List[Nit]:
        """Somma pesata con prodotti e accumulo multi‑cifra."""
        total = self.bias[:]
        for w, x in zip(self.weights, inputs):
            prod = [w * x]               # prodotto a singola cifra (lista)
            total = nit_add(total, prod)
        return total

    def update_hebbian(self, inputs: List[Nit], target: List[Nit], eta: Nit):
        """
        Aggiornamento ibrido: calcola l'errore in decimale (solo qui) per passi proporzionali.
        I pesi restano Nit e vengono aggiornati con aritmetica Novabene.
        """
        output = self.forward(inputs)
        if nit_compare(output, target) == 0:
            return

        # Conversione temporanea in decimale per calcolare l'errore
        def to_dec(num: List[Nit]) -> int:
            val = 0
            mul = 1
            for n in num:
                val += _SYM_TO_DEC[n.symbol] * mul
                mul *= 10
            return val

        out_dec = to_dec(output)
        target_dec = to_dec(target)
        error = target_dec - out_dec
        eta_dec = _SYM_TO_DEC[eta.symbol]

        for i in range(13):
            inp_dec = _SYM_TO_DEC[inputs[i].symbol]
            delta_dec = int(round(eta_dec * error * inp_dec))
            old_w_dec = _SYM_TO_DEC[self.weights[i].symbol]
            new_w_dec = old_w_dec + delta_dec
            new_w_dec = max(-10, min(10, new_w_dec))
            self.weights[i] = Nit(_dec_to_nit(new_w_dec))

        # Aggiorna bias (assumiamo bias piccolo, a una cifra)
        old_bias_dec = to_dec(self.bias)
        delta_bias_dec = int(round(eta_dec * error))
        new_bias_dec = old_bias_dec + delta_bias_dec
        # Riconverti in multi‑cifra Novabene
        self.bias = []
        n = abs(new_bias_dec)
        while n > 0:
            r = n % 10
            self.bias.append(Nit(_dec_to_nit(r if r > 0 else 0)))
            n //= 10
        if new_bias_dec < 0:
            self.bias = [Nit(_dec_to_nit(new_bias_dec))]
        if not self.bias:
            self.bias = [Nit('∅')]

    def __repr__(self):
        w_str = ", ".join(str(w) for w in self.weights[:3]) + "..."
        b_str = nit_to_string(self.bias)
        return f"IcosahedronNeuron(weights=[{w_str}], bias={b_str})"


if __name__ == "__main__":
    neuron = IcosahedronNeuron()
    print("Neurone iniziale:", neuron)

    inputs = [Nit('+0') for _ in range(13)]
    output = neuron.forward(inputs)
    print(f"Input: 13 x '+0' -> Output: {nit_to_string(output)}")

    target = nit_from_string("+02")   # 13 in decimale
    eta = Nit('+0')                   # learning rate = +0 (1)
    print(f"\nAddestramento per target = +02, eta = +0")
    for epoch in range(1, 101):
        neuron.update_hebbian(inputs, target, eta)
        if epoch % 20 == 0:
            out_str = nit_to_string(neuron.forward(inputs))
            print(f"Epoch {epoch:3d}: output = {out_str}")
        if nit_compare(neuron.forward(inputs), target) == 0:
            print(f"Convergenza raggiunta all'epoca {epoch}!")
            break
    else:
        print("Non convergente entro 100 epoche.")
