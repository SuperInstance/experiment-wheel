#!/usr/bin/env python3
"""
W1 — THE MATING AT SCALE (Experiment Wheel, Station 2: BENCH, RTX 4050)

Pre-registered (in EXPERIMENT-WHEEL.md before this ran):
  QUESTION: does the mating advantage compound at population scale, or was
            the 3/30 (10%) an artifact of small numbers?
  KILL: if sexual real-rate < 1% at 10,000 pairs with genuine diversity,
        the advantage does NOT compound — file negative, move on.
  METRICS: real-rate (sexual vs asexual) at n=10,000; tolerance sweep
           (the rate-vs-tolerance curve); CPU-vs-GPU wall time.
  PROVENANCE: extends seed-canon/papers/mating_verified.py (station 1,
              2026-08-26: 3/30 sexual vs 0/30 asexual, orbit 15 vs 11).

Two experiments:
  E1: scalar mating at scale (station-1 semantics, 10k pairs)
  E2: the paper's own vector claim at scale — tanh-net cells (n=16),
      cross- vs self-iteration, relevance-vs-steps (10k populations)
"""
import torch
import time
import json

DEV = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
N_PAIRS = 10_000
CROSS_STEPS = 10
DIM = 16
TARGET = 0.5
TOL = 0.05
SEED = 20260826

def bench(fn):
    t0 = time.perf_counter()
    out = fn()
    torch.cuda.synchronize() if DEV.type == 'cuda' else None
    return out, time.perf_counter() - t0

# ── E1: scalar mating at 10k, vectorized ────────────────────────────
def e1(device):
    g = torch.Generator(device='cpu').manual_seed(SEED)
    def rand(n): return torch.rand(n, generator=g).to(device)

    # per-pair phases (genuine diversity)
    pa, pb = rand(N_PAIRS), rand(N_PAIRS)
    xa = 0.2 + (rand(N_PAIRS) - 0.5) * 0.1     # A states near 0.2
    xb = 0.8 + (rand(N_PAIRS) - 0.5) * 0.1     # B states near 0.8

    PI = torch.tensor(torch.acos(torch.tensor(-1.0)).item(), device=device)
    for _ in range(CROSS_STEPS):
        fa = 0.2 + 0.2 * torch.sin(xb * PI * 2 + pa * PI)   # A's fn on B's state
        fb = 0.8 + 0.2 * torch.cos(xa * PI * 2 + pb * PI)   # B's fn on A's state
        xa, xb = fa, fb
    child = 0.5 * (torch.sin(xb * PI * 2 + pa * PI) +
                   torch.cos(xa * PI * 2 + pb * PI))
    real_sexual = (child - TARGET).abs() <= TOL

    # asexual control: self-iterate A then mutate
    xa2 = 0.2 + (rand(N_PAIRS) - 0.5) * 0.1
    for _ in range(CROSS_STEPS):
        xa2 = 0.2 + 0.2 * torch.sin(xa2 * PI * 2 + pa * PI)
    child_asex = xa2 + (rand(N_PAIRS) - 0.5) * 0.1
    real_asexual = (child_asex - TARGET).abs() <= TOL

    # tolerance sweep for the rate curve
    sweeps = {}
    for t in (0.02, 0.05, 0.10, 0.20):
        sweeps[t] = {
            'sexual': float(((child - TARGET).abs() <= t).float().mean()),
            'asexual': float(((child_asex - TARGET).abs() <= t).float().mean()),
        }
    return {
        'n_pairs': N_PAIRS,
        'real_sexual': int(real_sexual.sum()),
        'real_asexual': int(real_asexual.sum()),
        'rate_sexual': float(real_sexual.float().mean()),
        'rate_asexual': float(real_asexual.float().mean()),
        'tolerance_sweep': sweeps,
    }

# ── E2: tanh-net cells (the paper's appendix), population-scale ────
def e2(device, steps=(1, 5, 10, 50)):
    g = torch.Generator(device='cpu').manual_seed(SEED + 1)
    def randn(*shape): return torch.randn(*shape, generator=g).to(device)

    # two populations of cells: A and B (functions = W,b; states = s)
    WA, bA = randn(N_PAIRS, DIM, DIM), randn(N_PAIRS, DIM)
    WB, bB = randn(N_PAIRS, DIM, DIM), randn(N_PAIRS, DIM)
    sA0, sB0 = randn(N_PAIRS, DIM), randn(N_PAIRS, DIM)
    target = torch.full((N_PAIRS, DIM), 0.7, device=device)

    def fa(s): return torch.tanh(torch.bmm(WA, s.unsqueeze(-1)).squeeze(-1) + bA)
    def fb(s): return torch.tanh(torch.bmm(WB, s.unsqueeze(-1)).squeeze(-1) + bB)
    def rel(s): return ((s - target).norm(dim=1) <= 0.1).float().mean()

    out = {}
    # cross-iteration track
    sA, sB = sA0.clone(), sB0.clone()
    # self-iteration track (A alone)
    sSelf = sA0.clone()
    for k in range(1, max(steps) + 1):
        sA, sB = fa(sB), fb(sA)          # cross
        sSelf = fa(sSelf)                 # self
        if k in steps:
            mate_child = 0.5 * (fa(sB) + fb(sA))
            out[k] = {
                'cross_relevance': float(rel(sA)),
                'self_relevance': float(rel(sSelf)),
                'mated_child_relevance': float(rel(mate_child)),
            }
    return out

if __name__ == '__main__':
    print(f'W1 — the mating at scale | device: {DEV}' +
          (f' ({torch.cuda.get_device_name(0)})' if DEV.type == "cuda" else ''))
    results = {'device': str(DEV), 'n_pairs': N_PAIRS}

    r_cpu, t_cpu = bench(lambda: e1(torch.device('cpu')))
    results['e1_cpu'] = r_cpu; results['e1_cpu_seconds'] = round(t_cpu, 3)
    if DEV.type == 'cuda':
        r_gpu, t_gpu = bench(lambda: e1(DEV))
        results['e1_gpu'] = r_gpu; results['e1_gpu_seconds'] = round(t_gpu, 4)

    r2, t2 = bench(lambda: e2(DEV))
    results['e2_tanh_nets'] = r2; results['e2_seconds'] = round(t2, 3)

    print(json.dumps(results, indent=2)[:1800])
    json.dump(results, open('w1-results.json', 'w'), indent=2)
    print('saved w1-results.json')
