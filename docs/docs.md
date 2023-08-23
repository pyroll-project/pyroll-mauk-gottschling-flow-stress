# The PyRolL Mauk and Gottschling Flow Stress Model Plugin

## Model approach

The flow stress model of Mauk and Gottschling is a flexible empirical flow stress model approach. It features several
terms and
coefficients to model common shapes of flow stress curves in cold and hot forming. The flow stress is here assumed to be
only dependent on strain, strain rate and temperature, thus all other influences are included in the empirical
coefficients.

The model includes several exponential and power terms. The material dependent coefficients are $K$ and the $m_i$. One
has not to use everytime all coefficients, if a term is not needed the corresponding coefficient can be set to zero.

$$ k_\mathrm{f} \left( \varphi, \dot{\varphi}, \vartheta \right) = K\exp\left(m_1 \vartheta\right)
\varphi^{m_3} \dot{\varphi}^{m_2 + m_5 \vartheta} \exp\left(m_4 \varphi\right)  $$

The temperature is commonly used in °C, conversion is done internally, since PyRoll uses temperatures in K. The function
shows results to 0 at $\varphi = 0$ and $\dot{\varphi} = 0$, so commonly small base values are added to the variables (
about 0.01 to 0.1). These influence the model fitting, so one should receive those used in fitting together with the
coefficients.

For model fitting one needs several flow stress curves, determined from compression, torsion or tension tests, at
several temperatures and strain rates. A common thumb rule for hot forming is to take temperatures every $50$ or $100
\mathrm{K}$ in the desired range and strain rates of $0.1$, $1$ and $10 s^{-1}$. The model should not be used across
major structural transitions of the material.

## Usage of the Plugin

Load the plugin with the module name `pyroll_mauk_gottschling_flow_stress`.

### The `RollPassProfile.mauk_gottschling_flow_stress_coefficients` hook

The plugin specifies the `RollPassProfile.mauk_gottschling_flow_stress_coefficients` hook to deliver material
coefficients to
the flow stress function. The hook function must return an instance of the `MaukGottschlingFlowStressCoefficients`
class.

    MaukGottschlingFlowStressCoefficients(
        K, m1, m2, m3, m4, m5,
        baseStrain, baseStrainRate
    )

The constructor takes in addition to the coefficients the base values for strain and strain rate to prevent zero flow
stress.

> The unit of the returned flow stress depends solely on the value of $K$.
> Choose the unit of $K$ in that way, that the function returns flow stress in Pa (SI unit).
> Coefficient sets found in literature often return flow stress in MPa, fix that by multiplying $A$ by `1e6`.

For a few common materials hooks delivering coefficients are implemented. Those implementations ask for a `material`
attribute on the profile, being a string for material identification. The following materials are implemented (
case-insensitive):

- C15
- C55
- 100Cr6

Implement your own hook function to extend this. As with all hooks, to use custom coefficients one could simply give a
keyword argument `freiberg_flow_stress_coefficients` to the initial profile to use a constant coefficient set.

### The `RollPassProfile.flow_stress` hook

The plugin implements a function for the `RollPassProfile.flow_stress` hook, calculating flow stress according to
the [model](model.md). This hook function asks for `mauk_gottschling_flow_stress_coefficients` on the profile. If no
coefficients are available the function returns `None`. It also asks for `strain` and `temperature` on the profile, as
well as for `strain_rate` on the roll pass. If those are not available an error will occur.

## References

- Mauk, P. J., and Gottschling. J. "Hot flow curves of metallic materials." Proceedings 14th
  international forgemasters meeting, IFM. Vol. 3. 2000.