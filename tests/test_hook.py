import weakref

import numpy as np

from pyroll.mauk_gottschling_flow_stress.mauk_gottschling_flow_stress import MaukGottschlingFlowStressCoefficients, \
    flow_stress
from pyroll.mauk_gottschling_flow_stress import mauk_gottschling_flow_stress as hook

strain = 1
strain_rate = 1
temperature = 1200
coefficients = MaukGottschlingFlowStressCoefficients(
    k=5050.220 * 1e6,
    m1=-0.003126,
    m2=-0.168624,
    m3=0.359206,
    m4=-0.702119,
    m5=0.000278,
    baseStrain=0.1,
    baseStrainRate=0.1
)


class DummyProfile:
    def __init__(self):
        self.strain = strain
        self.temperature = temperature
        self.material = "C15"
        self.freiberg_flow_stress_coefficients = coefficients


class DummyRollPass:
    def __init__(self):
        self.strain_rate = strain_rate


def test_hook():
    rp = DummyRollPass()
    p = DummyProfile()
    p.unit = rp
    print()

    fs = hook(p)
    print(fs)
    assert np.isfinite(fs)
    assert fs == flow_stress(coefficients, strain, strain_rate, temperature)

    rp.strain_rate = 0
    fs = hook(p)
    print(fs)
    assert np.isfinite(fs)
    assert fs == flow_stress(coefficients, strain, 0, temperature)

    p.strain = 0
    fs = hook(p)
    print(fs)
    assert np.isfinite(fs)
    assert fs == flow_stress(coefficients, 0, 0, temperature)
