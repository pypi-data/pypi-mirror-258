import logging
import os
import re
from dataclasses import field
from difflib import unified_diff
from typing import Sequence, Union

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from mobility import draw_graph
from oemof.solph import EnergySystem, helpers, processing
from oemof.solph._plumbing import sequence as solph_sequence
from oemof.solph.buses import Bus
from oemof.solph.components import Converter, GenericStorage, Sink
from oemof.solph.flows import Flow

from oemof import solph
from oemof.tabular._facade import Facade, dataclass_facade
from oemof.tabular.constraint_facades import GenericIntegralLimit
from oemof.tabular.facades import (
    BackpressureTurbine,
    Commodity,
    Conversion,
    Dispatchable,
    Excess,
    ExtractionTurbine,
    Link,
    Load,
    Reservoir,
    Shortage,
    Storage,
    Volatile,
)
from oemof.tabular.facades.experimental.battery_electric_vehicle import Bev
from oemof.tabular.postprocessing import calculations

date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")

energysystem = solph.EnergySystem(
    groupings=solph.GROUPINGS,
    timeindex=date_time_index,
    infer_last_interval=True,
)

el_bus = solph.Bus("el-bus")
el_bus.type = "bus"
energysystem.add(el_bus)

second_bus = solph.Bus("second-bus")
second_bus.type = "bus"
energysystem.add(second_bus)


source = solph.components.Source(
    label="source",
    outputs={
        el_bus: solph.Flow(nominal_value=300, fix=[1, 0, 0], variable_costs=10)
    },
)
source.type = "source"
energysystem.add(source)

stor = GenericStorage(
    label="storage",
    inputs={
        el_bus: solph.Flow(
            nominal_value=300,
        )
    },
    outputs={
        second_bus: solph.Flow(
            nominal_value=100,
        )
    },
    nominal_storage_capacity=300,
    balanced=False,
    initial_storage_level=0,
)
stor.type = "storage"
energysystem.add(stor)

sink = solph.components.Sink(
    label="sink",
    inputs={
        second_bus: solph.Flow(
            nominal_value=100, fix=[1, 1, 1], variable_costs=10
        )
    },
)
sink.type = "sink"
energysystem.add(sink)

draw_graph(energysystem)

model = solph.Model(
    energysystem,
    timeindex=energysystem.timeindex,
)

# select solver 'gurobi', 'cplex', 'glpk' etc
model.solve("cbc", solve_kwargs={"tee": True})

energysystem.params = solph.processing.parameter_as_dict(
    energysystem, exclude_attrs=["subnodes"]
)
energysystem.results = model.results()
postprocessed_results = calculations.run_postprocessing(energysystem)
print(postprocessed_results)

energysystem.new_results = {}
for r in energysystem.results:
    if r[1] is not None:
        energysystem.new_results[
            f"{r[0].label}: {r[1].label}"
        ] = energysystem.results[r]

fig, ax = plt.subplots(figsize=(10, 8))
energysystem.new_results["el-bus: storage"]["sequences"].plot(
    ax=ax, label="el-bus: storage"
)
energysystem.new_results["storage: second-bus"]["sequences"].plot(
    ax=ax, label="storage: second-bus"
)
ax.legend(title="Legend", bbox_to_anchor=(0.7, 1), loc="upper left")
ax.set_title("Storage")
plt.tight_layout()
fig.show()
