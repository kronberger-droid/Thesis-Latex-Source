#import calc: abs, pow, round, sqrt
#import "lib.typ": *
#import "@preview/lilaq:0.2.0" as lq

// contructing nitrogen gas datatype
#let nitrogen = gas("Nitrogen", 1.47, 28.01e-3, 276, 1.716e-5, 111)

// characteristic length of the inlet nozzle inlet
// corresponds to diameter in m
#let length_inlet_in = 40e-6

// crosssectional area of the inlet nozzle inlet
// in m^2
#let area_inlet_in = area_circle(length_inlet_in)

// characteristic length of the inlet nozzle inlet
// corresponds to diameter in m
#let length_inlet_out = 20e-6

// crosssectional area of the inlet nozzle outlet
// in m^2
#let are_inlet_out = area_circle(length_inlet_out)

// characteristic length of the reactor volume
// corresponds to twice the height in m
#let length_reactor = 40e-6

// crosssectional area of the middle of the reactor
// in m^2
#let area_reactor = 0.5e-3 * length_reactor / 2

// characteristic length of the outlet nozzle inlet
// corresponds to diameter in m
#let length_outlet_in = length_inlet_out // in m

// crosssectional area of the outlet nozzle inlet
// in m^2
#let area_outlet_in = area_circle(length_outlet_in)

// characteristic length of the outlet nozzle outlet
// corresponds to diameter in m
#let length_outlet_out = length_inlet_in // in m

// crosssectional area of the outlet nozzle outlet
// in m^2
#let area_outlet_out = area_circle(length_outlet_out)

// total temperature in the reservoir
// in K
#let total_temp_min = 300
#let total_temp_max = 600

// total pressure in the reservoir
// in Pa
#let total_pressure = 1.5e5

// Plotting the knudsen and reynolds number over the mach range of (0, 3.5)
#let mach_range = lq.linspace(1e-1, 3.5)

#let gas = nitrogen

= Summary for #gas.name

#v(1cm)

#grid(
  columns: (1fr, 1fr),
  align: center,
  column-gutter: 20pt,
  lq.diagram(
    width: 7cm,
    height: 6cm,
    title: [Reynolds number over M],
    xlabel: [Mach number - M],
    xlim: (0, 3.6),
    xaxis: (mirror: false),
    ylim: (10, 2000),
    yscale: "log",
    lq.plot(mark: none, mach_range, mach_range.map(point => {
      let total_temp = total_temp_min
      let char_length = length_inlet_in
      let temp = temp_to_total(point, nitrogen) * total_temp
      let pressure = pressure_to_total(point, gas) * total_pressure
      reynolds_number(temp, pressure, char_length, point, gas)
    })),
    lq.plot(mark: none, mach_range, mach_range.map(point => {
      let total_temp = total_temp_min
      let char_length = length_inlet_out
      let temp = temp_to_total(point, nitrogen) * total_temp
      let pressure = pressure_to_total(point, gas) * total_pressure
      reynolds_number(temp, pressure, char_length, point, gas)
    })),
    lq.plot(mark: none, mach_range, mach_range.map(point => {
      let total_temp = total_temp_max
      let char_length = length_inlet_in
      let temp = temp_to_total(point, nitrogen) * total_temp
      let pressure = pressure_to_total(point, gas) * total_pressure
      reynolds_number(temp, pressure, char_length, point, gas)
    })),
    lq.plot(mark: none, mach_range, mach_range.map(point => {
      let total_temp = total_temp_max
      let char_length = length_inlet_out
      let temp = temp_to_total(point, nitrogen) * total_temp
      let pressure = pressure_to_total(point, gas) * total_pressure
      reynolds_number(temp, pressure, char_length, point, gas)
    })),
    lq.line((0, 2000), (3.6, 2000), stroke: maroon + 3pt),
  ),
  lq.diagram(
    width: 7cm,
    height: 6cm,
    title: [Knudsen number over M],
    xlabel: [Mach number - M],
    xlim: (0, 3.6),
    xaxis: (mirror: false),
    yaxis: (ticks: none, mirror: none),
    lq.yaxis(
      position: right,
      scale: "log",
      lim: (0.001, 0.1),
      mirror: true,
      lq.plot(mark: none, mach_range, mach_range.map(point => {
        let total_temp = total_temp_min
        let char_length = length_inlet_in
        let temp = temp_to_total(point, nitrogen) * total_temp
        let pressure = pressure_to_total(point, gas) * total_pressure
        knudsen_number(temp, pressure, char_length, gas)
      })),
      lq.plot(mark: none, mach_range, mach_range.map(point => {
        let total_temp = total_temp_min
        let char_length = length_inlet_out
        let temp = temp_to_total(point, nitrogen) * total_temp
        let pressure = pressure_to_total(point, gas) * total_pressure
        knudsen_number(temp, pressure, char_length, gas)
      })),
      lq.plot(mark: none, mach_range, mach_range.map(point => {
        let total_temp = total_temp_max
        let char_length = length_inlet_in
        let temp = temp_to_total(point, nitrogen) * total_temp
        let pressure = pressure_to_total(point, gas) * total_pressure
        knudsen_number(temp, pressure, char_length, gas)
      })),
      lq.plot(mark: none, mach_range, mach_range.map(point => {
        let total_temp = total_temp_max
        let char_length = length_inlet_out
        let temp = temp_to_total(point, nitrogen) * total_temp
        let pressure = pressure_to_total(point, gas) * total_pressure
        knudsen_number(temp, pressure, char_length, gas)
      })),
      lq.line((0.0, 0.1), (3.6, 0.1), stroke: maroon + 3pt),
    ),
  ),
)

== Massflow for disconnected reserviors without leak
#let mach_number_no_leak = disconnected_mach_isen(gas)
#let massflow_no_leak = massflow(
  gas.heat_ratio,
  mach_number_no_leak,
  are_inlet_out,
  total_temp_min,
  total_pressure,
  gas,
)
$
  dot(m) = #massflow_no_leak
$
