---
layout: post
title: Intro to net based rainfall-runoff models
date: 2026-11-13
description: Intro to net based rainfall-runoff models.
tags:
  - hydrology
  - rainfall–runoff modelling
  - ai
---

_I wanted to understand net rainfall runoff models. Here I attempt a survey of some of them. This post draws from a collection of published work by others, all mistakes are my own._

In a previous [post]({% post_url 2026-11-12-intro-to-gr4j %}) we looked at GR4J as a low parameter 'lumped conceptual model' for rainfall-runoff. Here we will look at using neural networks for rainfall-runoff modelling.

## Why use nets for rainfall-runoff models?

Rainfall-runoff models use meteorological data to predict river flow over time. They must account for evaporation dynamics, catchment moisture and delays as water moves through the catchment.

Net based rainfall-runoff models handle the relationship and dynamics by using a trained neural network (often with recurrent state as an LSTM).

By using a net we can hope to:
 - learn how catchment characteristics and weather patterns shape river flow
 - create models that can work across catchments
 - make more accurate linkages between rainfall and river flows.

## What we will look at here

In this post we will focus on the thread of work that built up to Google's FloodHub:
 - **[Kratzert et al. (2019)](https://arxiv.org/abs/1907.08456)**: demonstrates an LSTM trained across 531 US catchments can outperform a traditional hydrological model calibrated separately for individual basins.
 - **[Nearing et al. (2024)](https://doi.org/10.1038/s41586-024-07145-1)**: investigates whether a model trained on data from 5680 gauges worldwide can deliver reliable forecasts of extreme river flooding in ungauged catchments. That is: can it generalise, used with weather forecasts can it predict extremes and how does it compare to [Copernicus GloFAS v4](https://global-flood.emergency.copernicus.eu/).
 - **[Google Global Flood Forecasting Model Version 2](https://egusphere.copernicus.org/preprints/2026/egusphere-2026-2283/)**: documents the model behind Google FloodHub (as at time of writing). Incorporates GraphCast weather forecasts, uses [ME-LSTM](https://doi.org/10.5194/hess-29-6221-2025) architecture and enlarged training data.


There are other net rainfall-runoff models out there, for example (but not exhaustively):
 - **[Feng et al. (2022)](https://doi.org/10.1029/2022WR032404)**: combines a neural network with the [HBV hydrologic model](https://en.wikipedia.org/wiki/HBV_hydrology_model) which provides some parameter explainability
 - **[Li et al. (2024)](https://doi.org/10.1038/s41598-024-62127-7)**: combines LSTM and attention mechanism for rainfall-runoff models.
 - **[Hoedt et al. (2021)](https://proceedings.mlr.press/v139/hoedt21a.html)**: introduces mass conserving LSTM for use in physically constrained systems with hydrology as a use case.


## From individual catchments to regional models

[Kratzert et al. (2019)](https://arxiv.org/abs/1907.08456) describe how a single regional model using an LSTM could be trained across many catchments displaying better performance than earlier regional multi-basin models. It even outperformed traditional hydrological models calibrated individually for each catchment. They also introduce an Entity-Aware LSTM variant that learns representations of catchment similarities.

The architecture, inputs and outputs are:
{% include image.html
   src="/assets/images/2026-11-13-intro-to-net-rainfall-runoff/Kratzert_Rainfall_Runoff_Model_Architecture.png"
   alt="Kratzert et al. (2019) LSTM with catchment variables"
   caption="Kratzert et al. (2019) LSTM with catchment variables."
   width="700"
%}

The dataset used had daily observations from 531 US catchments in the CAMELS dataset, with training covering 1999–2008 and evaluation covering 1989–1999. Observed river discharge was the prediction target.

This dataset included:
 - **Meteorological inputs (5):** daily precipitation, minimum and maximum air temperature, shortwave solar radiation and vapour pressure.
 - **Static catchment attributes (27)**: includes climate characteristics (mean precipitation, aridity and seasonality), vegetation and land cover, soil characteristics (porosity, hydraulic conductivity, depth and texture), geological permeability and topographical characteristics (such as elevation and slope).

A single LSTM was trained jointly across all catchments using 270-day input sequences. MSE and basin-normalised squared-error (NSE*) losses were examined, with the latter preventing larger or wetter catchments from dominating training.

This experiment evaluates generalisation across time within the training catchments, whereas later work explicitly evaluates spatial generalisation to catchments whose discharge records were withheld from training.

## Predicting extreme events in ungauged catchments and usage for flood forecasts

**[Nearing et al. (2024)](https://doi.org/10.1038/s41586-024-07145-1)**
builds on regional LSTM rainfall–runoff models, extending the approach to global-scale river flow forecasting in ungauged catchments, with particular emphasis on extreme flood events. This work aims to produce a model that can transfer to unseen catchments. It also evaluates the model when used with forecast data to predict extreme events.

The architecture for the LSTM network in this model (_reproduced from [Extended Data Figure 4](https://www.nature.com/articles/s41586-024-07145-1/figures/10)_) is:
{% include image.html
   src="/assets/images/2026-11-13-intro-to-net-rainfall-runoff/nature_global_prediction_of_extreme_floods_in_ungaged_watersheds.png"
   alt="Nearing et al. (2024) LSTM-encoder + LSTM-decoder architecture"
   caption="Nearing et al. (2024) LSTM-encoder + LSTM-decoder architecture."
   width="700"
%}

Unlike the earlier LSTM rainfall–runoff models, which simulate discharge from historical meteorological observations, the encoder–decoder architecture separates the estimation of historical catchment state from the prediction of future discharge. The encoder processes 365 days of historical meteorology, transferring its learned hidden and cell states to a decoder that uses forecast meteorology to predict discharge up to seven days ahead.

The study dataset comprised daily streamflow observations from 5,680 catchments globally, representing approximately 152,000 catchment-years of records. Historical reanalysis covers 1984–2021 and forecast-based evaluation covers 2014–2021, with differing availability across sources and locations.

This dataset included:
 - **Historical meteorological inputs:** daily precipitation, air temperature, shortwave and longwave radiation, snowfall and surface pressure, primarily from [ECMWF ERA5-Land](https://www.ecmwf.int/en/era5-land) reanalysis, supplemented with precipitation estimates from [NOAA CPC](https://www.cpc.ncep.noaa.gov/products/Precip_Monitoring/gl_obs.shtml) and [NASA IMERG](https://gpm.nasa.gov/data/imerg).
 - **Forecast meteorological inputs:** precipitation, temperature, radiation, snowfall and surface pressure from [ECMWF IFS HRES](https://www.ecmwf.int/en/forecasts/datasets/ifs-medium-range-control-forecast-formerly-hres-and-analysis-data-15-days-set-i) weather forecasts, used to predict river discharge up to 7 days ahead.
 - **Static catchment attributes:** geological, geophysical and anthropogenic characteristics from [HydroATLAS](https://www.hydrosheds.org/hydroatlas), including climate (precipitation, temperature and snow fraction), topography (elevation and drainage area), soils, land cover and human influences (such as nighttime lights).

The model predicts the parameters of an asymmetric Laplacian probability distribution for daily catchment-area-normalised river discharge, rather than a single flow value. Observed daily discharge is the training target, with the predicted distributions used to estimate river flow and identify exceedances of flood return-period thresholds.

A shared encoder–decoder LSTM architecture was trained jointly across 5,680 catchments using 365 days of historical meteorological inputs and up to 7 days of weather forecasts. Training used V100 GPUs and took of order 10h with validation.

Cross-validation was used to show that useful predictions of extreme river flows can be given at previously unseen locations. Against Copernicus GloFAS v4, the AI model achieved significantly better flood-event F1 scores and more reliable 1-, 2-, and 5-year event scores than GloFAS's zero-day forecasts.

## Google Flood Forecasting v2: architecture and improvements

[Cohen et al. (2026)](https://egusphere.copernicus.org/preprints/2026/egusphere-2026-2283/) describe v2 of Google's global flood forecasting model, which introduces a Mean Embedding LSTM architecture (see [Gauch et al 2025](https://doi.org/10.5194/hess-29-6221-2025)), incorporates additional meteorological forecast products and expands the training dataset. The updated system improves forecast reliability and extends useful prediction lead times, through better handling of missing inputs and discontinuities between historical and forecast meteorology.

> The ME-LSTM then employs two LSTM layers arranged in a stack that run over the full time sequence (hindcast + forecast), eliminating the handoff discontinuity. The first layer processes a sequence of aggregated embeddings derived from hindcast data and runs over the full sequence, i.e., hindcast (spinup) + forecast sequence length. The second LSTM layer predicts
streamflow. It receives two inputs at every time step: the aggregated forecast embeddings and the hidden state output from the first LSTM layer.

My interpretation _(85% confidence)_ is that we can visualise this as:
{% include image.html
   src="/assets/images/2026-11-13-intro-to-net-rainfall-runoff/egusphere_google_flood_v2_architecture.png"
   alt="Conceptual interpretation of the ME-LSTM architecture for the Google global flood forecasting model v2"
   caption="Conceptual interpretation of the ME-LSTM architecturefor the Google global flood forecasting model v2. Embedding details and some connections are omitted for clarity."
   width="700"
%}

Multiple sources of data that might not overlap can be consumed in the v2 model; which adds more geographic locations, data sources and time history. Training uses daily streamflow observations from Caravan, GRDC and BANDAS, alongside meteorological inputs from ECMWF HRES, GraphCast, CPC and IMERG, covering 1980–2024. To exploit historical data where forecast archives are unavailable, feature unioning substitutes ERA5-Land reanalysis for missing HRES/GraphCast inputs, while the ME-LSTM's masked embeddings allow meteorological products with incomplete or non-overlapping coverage to contribute to training.

The supervision target is observed daily mean streamflow at the catchment outlet for the last 7 forecast days. The outputs are probabilistic predictions
trained with a Continuous Mixture of Asymmetric Laplacians (CMAL) likelihood loss rather than directly minimising squared error.

Across 1,223 test basins, v2 improves streamflow prediction accuracy over v1 and the GloFAS/GEOGLOWS benchmarks, matching or exceeding v1 nowcast NSE at lead times of up to six days in gauged basins and one day in ungauged basins.

## Conclusion

Neural rainfall-runoff models can generalise to ungauged catchments. Combined with weather forecasts, they can predict distributions of future river flow and provide advance warning of extreme floods in live operational systems such as [Google FloodHub](https://sites.research.google/floods/).

## References

- [Google FloodHub](https://sites.research.google/floods/)
- [Copernicus GloFAS](https://global-flood.emergency.copernicus.eu/)
- [Global prediction of extreme floods in ungauged watersheds, Nature, Apr 2024, Nearing et al.](https://doi.org/10.1038/s41586-024-07145-1)
- [LSTM-ME paper](https://doi.org/10.5194/hess-29-6221-2025)
- [Google Global Flood Forecasting Model Version 2 paper](https://egusphere.copernicus.org/preprints/2026/egusphere-2026-2283/)
- [Google Research Blog post on open sourcing hydrology framework](https://research.google/blog/the-next-chapter-in-flood-resilience-open-sourcing-googles-hydrology-framework/)
- [Google Flood Forecasting code](https://github.com/google-research/flood-forecasting)
- [Google Flood Forecasting resources](https://sites.research.google/gr/floodforecasting/resources/)
- [Caravan dataset](https://github.com/kratzert/Caravan)
- [HydroATLAS](https://www.hydrosheds.org/hydroatlas)
