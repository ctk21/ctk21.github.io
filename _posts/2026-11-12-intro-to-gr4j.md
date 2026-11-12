---
layout: post
title: What are the GR4J and GR6J hydrology models
date: 2026-11-12
description: What are the GR4J and GR6J hydrology models along with an example of their operational usage.
tags:
  - hydrology
  - rainfall–runoff modelling
---

_I wanted to understand the GR4J and GR6J rainfall runoff models. A good way to build an understanding is to try and explain it to somebody else! This post draws from a collection of published work by others, all mistakes are my own._


[Hydrology](https://en.wikipedia.org/wiki/Hydrology) is the study of the movement, distribution and storage of water in the environment. Hydrology models can help answer questions such as:
 - how likely is it to have too much water coming through this river (i.e. flooding)?
 - how likely is it to have too little water coming through this river (i.e. drought)?
 - which rivers and catchments are able to deal with more extreme weather (i.e. are there policy interventions that can help avoid extreme high or low events)?

## Why do we need rainfall-runoff models?

Take a river catchment receiving rainfall. If we know how much rain fell, how do we relate that to the amount of water which reaches the river and when?

The relationship isn't trivial:
 - Some rainfall evaporates or is transpired by vegetation.
 - Some enters the soil and remains stored there.
 - Some reaches the river rapidly, while some might discharge weeks later.

Rainfall-runoff models try to relate the aggregate behaviour of these processes.

The modelling approach taken by [GR4J](https://doi.org/10.1016/S0022-1694(03)00225-7) is to represent an entire catchment using a small number of interconnected mathematical reservoirs. This is called a _lumped conceptual model_ and it avoids explicitly simulating all the physical processes at each spatial location that make up an entire catchment.

## The GR4J model architecture

The GR4J model has several components:
 - *A production store.* This represents the catchment's ability to retain water. Incoming rainfall increases the store, while evaporation and percolation reduce its water content.
 - *Percolation and effective rainfall.* Some stored water drains from the production store. This combines with rainfall that bypasses storage to produce the water available for routing.
 - *Two unit hydrographs.* These distribute the water over time, accounting for the delay between rainfall and river response. GR4J sends 90% of effective rainfall down one route and 10% down another.
 - *A routing store.* This introduces additional delay and nonlinear storage behaviour before water reaches the river.
 - *Groundwater exchange.* GR4J can add or remove water through an exchange term, allowing it to represent catchments where groundwater moves across the modelled catchment boundary.

We can visualise how these components are linked together in the model as shown:

{% include image.html
   src="/assets/images/2026-11-12-gr4j-gr6j-models/GR4J_Model_Figure.png"
   alt="GR4J model architecture"
   caption="GR4J model architecture."
   width="800"
%}

When using a GR4J model, it has a daily time series of inputs:
 - daily precipitation **P**
 - potential evapotranspiration **E**

It is then iterated daily to produce the main output:
 - daily river discharge **Q**

Internally there is a time series of model states:
 - water content in the production store **S**
 - water content in the routing store **R**

## The GR4J parameters

The GR4J model has 4 parameters:
 - **x1** production store capacity
 - **x2** groundwater exchange coefficient
 - **x3** routing store reference capacity
 - **x4** unit hydrograph time base

As these parameters are varied, the model represents different responses from the meteorological inputs to the daily river discharge.

There is a [tutorial here](https://reflector.vtti.ad.vt.edu/cran/web/packages/airGRteaching/vignettes/v00_teaching_hydrology.html) that allows you to build an intuition of how the model responds to these parameters which makes use of the [airGR R package](https://hydrogr.github.io/airGR/).


## Calibrating the GR4J parameters

One common way to calibrate the parameters _for a given catchment_ is:
 - take a time series for say ten years of observed daily rainfall, potential evapotranspiration and river discharge
 - perform an optimisation to find the parameters **x1, ..., x4** that maximise the [Nash-Sutcliffe Efficiency](https://en.wikipedia.org/wiki/Nash%E2%80%93Sutcliffe_model_efficiency_coefficient)

Notice this calibration procedure gives you parameters only for a catchment where you have historical time series data. There are techniques for estimating model parameters for ungauged catchments, often called regionalisation, but these introduce another modelling problem. There is also the question of how to initialise the model's internal state variables; typically, the model is run through a warm-up period before calibration or evaluation.

The [airGR (R)](https://hydrogr.github.io/airGR/) is one way to calibrate the parameters of a GR4J model. Other packages also exist, for example: [hydromodel (python)](https://github.com/OuyangWenyu/hydromodel) and [GRsuite (python)](https://github.com/Najim33/GRsuite).

## The GR6J parameter additions

[GR6J](https://doi.org/10.1016/j.jhydrol.2011.09.034) extends GR4J, adding:
 - *More flexible groundwater exchange.* This allows the model to better represent catchments that gain or lose water depending on hydrological conditions.
 - *Adding an exponential routing reservoir.* This is designed to improve the representation of low flows.

The two parameters added affecting these additions:
 - **x5** Groundwater exchange threshold. Modifies the existing groundwater exchange mechanism to allow the direction of water transfer to change as the routing store fills or empties.
 - **x6** Exponential reservoir coefficient. Introduces a third conceptual reservoir, operating in parallel with the original routing reservoir.

## Example usage of GR4J / GR6J models

The [UK Hydrological Outlook](https://hydoutuk.net/) produces probabilistic forecasts of river flows across the UK, from one to twelve months ahead. These use GR6J models calibrated to individual catchments, driven by historical climate sequences or meteorological forecasts. Interestingly, the service used GR4J until September 2023 before switching to GR6J, partly reflecting the latter's improved representation of low flows. The methodology page also discusses the relatively modest changes in forecast skill resulting from this switch.

The models are also used for longer-term water resource planning. For example, [Anglian Water's 2024 Water Resources Management Plan](https://www.anglianwater.co.uk/siteassets/household/corporate/wrmp24/wrmp24-supply-forecast.pdf) uses calibrated GR6J rainfall–runoff models to simulate river flows under different climate and drought scenarios. These simulations contribute to assessing the reliability of future water supplies and the need for additional water resource infrastructure.

## Conclusion

What I find interesting about GR4J and GR6J is how much behaviour can be represented using a handful of parameters and relatively simple mathematical structures. They provide useful baseline models against which to evaluate more complex approaches, while raising interesting questions about how well model parameters and internal states can be inferred from observational data.

## References

- [GR4J paper](https://doi.org/10.1016/S0022-1694%2803%2900225-7)
- [GR6J paper](https://doi.org/10.1016/j.jhydrol.2011.09.034)
- The GR4J architecture diagram here evolved from figure 3 of [this paper](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.759534/full), which is consistent with Fig 1. of the GR4J paper.
- [airGR R package](https://hydrogr.github.io/airGR/)
- [UK Hydrological Outlook](https://hydoutuk.net/)
