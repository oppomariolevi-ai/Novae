import torch
import torch.nn as nn
from novabene.arithmetic import Nit, ADD_TABLE, MUL_TABLE_FULL, _SYM_TO_DEC, _DEC_TO_SYM

class QuantizedNovaeLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        # Pesi reali per training (STE)
        self.weight_fp = nn.Parameter(torch.randn(out_features, in_features))
        if bias:
            self.bias_fp = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter('bias_fp', None)
        # Inizializza i pesi quantizzati
        self.register_buffer('weight_q', torch.zeros(out_features, in_features, dtype=torch.int8))
        self.register_buffer('bias_q', torch.zeros(out_features, dtype=torch.int8) if bias else None)

    def _quantize(self, x):
        """Mappa float in [-10,10] e arrotonda."""
        return torch.clamp(torch.round(x), -10, 10).to(torch.int8)

    def forward(self, x):
        # Quantizza pesi e bias
        w_q = self._quantize(self.weight_fp)
        b_q = self._quantize(self.bias_fp) if self.bias_fp is not None else None
        # Salva per debug
        self.weight_q = w_q
        if b_q is not None:
            self.bias_q = b_q

        # Converti input in interi (simula quantizzazione attivazioni)
        x_int = torch.clamp(torch.round(x * 10), -10, 10).to(torch.int8)

        # Matmul emulata con lookup Novae (semplificata: usiamo int per velocità)
        # In una vera ALU useremmo le tabelle, ma qui sfruttiamo il fatto che i valori sono in [-10,10]
        # e moltiplicazione/aggiunta sono lineari. Per correttezza, simuliamo passo passo.
        out = torch.zeros(x.size(0), self.out_features, device=x.device, dtype=torch.int32)
        for i in range(self.out_features):
            for j in range(self.in_features):
                prod = w_q[i, j].item() * x_int[:, j]
                out[:, i] += prod
        if b_q is not None:
            out += b_q.unsqueeze(0)

        # Riporta in float e scala
        out = out.float() / 10.0

        # Straight‑Through Estimator: gradiente passa come se fosse lineare
        return out + (self.weight_fp @ x.T).T - out.detach()
