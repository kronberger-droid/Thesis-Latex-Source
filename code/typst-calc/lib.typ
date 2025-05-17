#import calc: abs, pow, round, sqrt

// define scientific constants
#let PI = 3.141592653589793

// universal gas constant in J/(mol K)
#let UNIV_GAS_CONST = 8.314

// bolzmann constant in J/K
#let K_BOLZMANN = 1.380649e-23

// avogadro constant in 1
#let AVOGADRO_CONST = 6.02214076e23

// constructor for sutherland specific constants
#let sutherland_consts(temp_ref, mu_ref, sutherland_const) = (
  temp_ref: temp_ref,
  mu_ref: mu_ref,
  sutherland_temp: sutherland_const,
)

// constructor for all gas specific constants
#let gas(name, heat_ratio, molar_mass, temp_ref, mu_ref, sutherland_const) = (
  name: name,
  heat_ratio: heat_ratio,
  molar_mass: molar_mass,
  specific_gas_const: UNIV_GAS_CONST / molar_mass,
  sutherland_consts: sutherland_consts(temp_ref, mu_ref, sutherland_const),
)

// circle area helper function
#let area_circle(diameter) = {
  PI * pow(diameter / 2, 2)
}

// helper function calculating isentropic mass flow
#let massflow(
  heat_ratio,
  mach_number,
  area,
  total_temp,
  total_pressure,
  gas,
) = {
  (
    area
      * total_pressure
      * sqrt(heat_ratio / (gas.specific_gas_const * total_temp))
      * mach_number
      * pow(
        1 + pow(mach_number, 2) * (heat_ratio - 1) / 2,
        -(heat_ratio + 1) / (2 * (heat_ratio - 1)),
      )
  )
}

#assert(
  round(
    massflow(1.47, 0.1455, 1.2566e-9, 300, 1.5e5, gas(
      "Nitrogen",
      1.47,
      28.01e-3,
      276,
      1.716e-5,
      111,
    ))
      * 1e7,
    digits: 1,
  )
    == 1.1,
  message: "Isentropic massflow formula failed to yield accurate values!",
)

// helper function to calculate dynamic viscosity using sutherlands formula
#let sutherland(T, sutherland_consts) = {
  (
    sutherland_consts.mu_ref
      * pow(T / sutherland_consts.temp_ref, 3 / 2)
      * (sutherland_consts.temp_ref + sutherland_consts.sutherland_temp)
      / (T + sutherland_consts.sutherland_temp)
  )
}

#assert(
  round(
    sutherland(
      300,
      gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111).sutherland_consts,
    )
      * 1e5,
    digits: 2,
  )
    == 1.83,
  message: "Sutherlands formula failed to yield accurate values!",
)

// helper function calculating knudsen number
#let knudsen_number(temp, pressure, char_length, gas) = {
  (
    (sutherland(temp, gas.sutherland_consts) * gas.specific_gas_const)
      / (pressure * char_length)
      * sqrt((PI * gas.molar_mass * temp) / (2 * K_BOLZMANN * AVOGADRO_CONST))
  )
}

#assert(
  round(
    knudsen_number(300, 1.5e5, 40e-6, gas(
      "Nitrogen",
      1.47,
      28.01e-3,
      276,
      1.716e-5,
      111,
    )),
    digits: 4,
  )
    == 0.0011,
)

// helper function calculating reynolds number
#let reynolds_number(temp, pressure, char_length, mach_number, gas) = {
  (
    (mach_number / knudsen_number(temp, pressure, char_length, gas))
      * sqrt((gas.heat_ratio * PI) / 2)
  )
}

// #assert(
//   round(
//     reynolds_number(300 * 0.8097, 1.5e5 * 0.5168, 20e-6, 1, gas(
//       "Nitrogen",
//       1.47,
//       28.01e-3,
//       276,
//       1.716e-5,
//       111,
//     )),
//     digits: 1,
//   )
//     == 195.7,
// )

// helper function calculating the isentropic relation T/T0
#let temp_to_total(mach_number, gas) = {
  pow(1 + pow(mach_number, 2) * (gas.heat_ratio - 1) / 2, -1)
}

#assert(
  round(
    temp_to_total(1, gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111)),
    digits: 2,
  )
    == 0.81,
)

// helper function calculating the isentropic relation p/p0
#let pressure_to_total(mach_number, gas) = {
  pow(
    1 + pow(mach_number, 2) * (gas.heat_ratio - 1) / 2,
    -gas.heat_ratio / (gas.heat_ratio - 1),
  )
}

#assert(
  round(
    pressure_to_total(1, gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111)),
    digits: 2,
  )
    == 0.52,
)

// helper function calculating the isentropic relation p/p0
#let density_to_total(mach_number, gas) = {
  pow(
    1 + pow(mach_number, 2) * (gas.heat_ratio - 1) / 2,
    -1 / (gas.heat_ratio - 1),
  )
}

#assert(
  round(
    density_to_total(1, gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111)),
    digits: 2,
  )
    == 0.64,
)

// helper function calculating terminal velocity
#let terminal_velocity(total_temp, gas) = {
  sqrt(
    2
      * gas.specific_gas_const
      * total_temp
      * gas.heat_ratio
      / (gas.heat_ratio - 1),
  )
}

#assert(
  round(
    terminal_velocity(300, gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111)),
    digits: 1,
  )
    == 746.3,
)

#let solve_mach_newton(
  target_area_ratio,
  gas,
  supersonic: false,
  tolerance: 1e-6,
  max_iterations: 1000,
) = {
  // initial Mach‐number guess
  let mach = if supersonic { 2.0 } else { 0.001 }
  let heat_ratio = gas.heat_ratio

  // exponent in the area–Mach relation
  let exponent = (heat_ratio + 1.0) / (2.0 * (heat_ratio - 1.0))

  // area–Mach function A/A*
  let area_ratio(m) = {
    let quadratic_term = 1.0 + 0.5 * (heat_ratio - 1.0) * m * m
    let normalization = pow((heat_ratio + 1.0) / 2.0, -exponent)
    pow(quadratic_term, exponent) * normalization / m
  }

  // derivative d(A/A*)/dM
  let area_ratio_derivative(m) = {
    let quadratic_term = 1.0 + 0.5 * (heat_ratio - 1.0) * m * m
    let normalization = pow((heat_ratio + 1.0) / 2.0, -exponent)
    let d_quadratic = (heat_ratio - 1.0) * m
    let d_power_term = (
      exponent * pow(quadratic_term, exponent - 1.0) * d_quadratic
    )
    let d_reciprocal = -1.0 / (m * m)

    (
      normalization
        * (d_power_term / m + pow(quadratic_term, exponent) * d_reciprocal)
    )
  }

  // Newton–Raphson iteration
  for iteration in range(0, max_iterations) {
    let residual = area_ratio(mach) - target_area_ratio
    let slope = area_ratio_derivative(mach)
    let update = residual / slope

    mach = mach - update
    if abs(update) < tolerance {
      return mach
    }
  }

  // fallback if no convergence
  mach
}

#assert(
  round(
    solve_mach_newton(
      318,
      gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111),
      supersonic: false,
    ),
    digits: 4,
  )
    == 0.0018,
)

#assert(
  round(
    solve_mach_newton(
      318,
      gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111),
      supersonic: true,
    ),
    digits: 4,
  )
    == 10.5430,
)

// helper function calculating disconnected reservoirs inlet mach number for isentropic case
#let disconnected_mach_isen(gas) = {
  let heat_ratio = gas.heat_ratio
  pow(1 + (heat_ratio - 1) / 2, -(heat_ratio + 1) / (2 * (heat_ratio - 1)))
}

#assert(
  round(
    disconnected_mach_isen(gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111)),
    digits: 3,
  )
    == 0.574,
)

// helper function calculating disconnected reservoirs inlet mach number for isothermal case
#let disconnected_mach_iso(gas) = {
  let heat_ratio = gas.heat_ratio
  sqrt(
    -1 / (heat_ratio - 1)
      + sqrt(
        1 / pow(heat_ratio - 1, 2)
          + 2
            / (heat_ratio - 1)
            * pow(2 / (heat_ratio + 1), (heat_ratio + 1) / (heat_ratio - 1)),
      ),
  )
}

#assert(
  round(
    disconnected_mach_iso(gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111)),
    digits: 3,
  )
    == 0.555,
)

// helper function calculating max massflow through the leak until inlet goes sonic
// for isentropic connection between back conditions and reactor conditions
#let leak_massflow_isen(area, total_temp, total_pressure, gas) = {
  let heat_ratio = gas.heat_ratio
  let specific_gas_const = gas.specific_gas_const
  let reactor_temp = temp_to_total(1, gas) * total_temp
  let reactor_pressure = pressure_to_total(1, gas) * total_pressure

  (
    area
      * reactor_pressure
      * sqrt(heat_ratio / (specific_gas_const * reactor_temp))
      * (
        1
          - pow(
            1 + (heat_ratio - 1) / 2,
            -(heat_ratio + 1) / (2 * (heat_ratio - 1)),
          )
      )
  )
}

#assert(
  round(
    leak_massflow_isen(100 * PI * 10e-12, 300, 1.5e5, gas(
      "Nitrogen",
      1.47,
      28.01e-3,
      276,
      1.716e-5,
      111,
    ))
      * 1e7,
    digits: 3,
  )
    == 4.681,
)

// helper function calculating max massflow through the leak until inlet goes sonic
// for isentropic connection between back conditions and reactor conditions
#let leak_massflow_isen(area, temp, total_pressure, gas) = {
  let heat_ratio = gas.heat_ratio
  let specific_gas_const = gas.specific_gas_const
  let reactor_pressure = pressure_to_total(1, gas) * total_pressure

  (
    area
      * reactor_pressure
      * sqrt(heat_ratio / (specific_gas_const * temp))
      * (
        pow(
          1 + (heat_ratio - 1) / 2,
          -(heat_ratio + 1) / (2 * (heat_ratio - 1)),
        )
      )
      * (pow(1 + (heat_ratio - 1) / 2, heat_ratio / (heat_ratio - 1)) - 1)
  )
}

#assert(
  round(
    leak_massflow_isen(100 * PI * 10e-12, 300, 1.5e5, gas(
      "Nitrogen",
      1.47,
      28.01e-3,
      276,
      1.716e-5,
      111,
    ))
      * 1e7,
    digits: 3,
  )
    == 5.313,
)

