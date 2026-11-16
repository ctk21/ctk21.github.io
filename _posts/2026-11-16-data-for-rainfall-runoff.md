---
layout: post
title: What data do rainfall–runoff models need?
date: 2026-11-16
description: What data do rainfall–runoff models need?
tags:
  - hydrology
  - rainfall–runoff modelling
  - ai
---

A rainfall-runoff model predicts river discharge rate from meteorological conditions and catchment properties. In previous posts, I've looked at some [lumped conceptual models]({% post_url 2026-11-12-intro-to-gr4j %}) such as GR4J and some [net-based data-driven models]({% post_url 2026-11-13-intro-to-net-rainfall-runoff %}) such as that used in [Google Flood Hub](https://sites.research.google/floods). A useful model can be used to build operational systems that alert when the flow rates are expected to be too high (e.g. floods) or too low (e.g. droughts).

In this post, we ask what data these models need and where we can find it.

## The building blocks of rainfall–runoff data

Source data used to train and run rainfall–runoff models can be grouped into the following categories.

| Data category | What it contains | Examples of sources |
|---|---|---|
| **1. Streamflow observations** | River discharge observations and gauging station data | [National River Flow Archive (UK)](https://nrfa.ceh.ac.uk/data/about-data), [Global Runoff Data Centre (GRDC)](https://grdc.bafg.de/data/data_portal/) |
| **2. Catchment geography** | Catchment boundaries and river networks. | [National River Flow Archive (UK)](https://nrfa.ceh.ac.uk/data/about-data),  [HydroBASINS](https://www.hydrosheds.org/products/hydrobasins) |
| **3. Static catchment attributes** | Catchment area, elevation, slope, drainage density, river network characteristics, soil texture and depth, geology, bedrock permeability, groundwater characteristics, land cover, vegetation, long-term climate indices (e.g. aridity and mean precipitation), and human influences (e.g. urbanisation, dams and reservoirs). | [HydroATLAS](https://www.hydrosheds.org/hydroatlas), [SoilGrids](https://isric.org/explore/soilgrids), [ESA WorldCover](https://esa-worldcover.org/en/data-access) |
| **4. Historical meteorological data** | Observed or retrospectively estimated precipitation, temperature, evaporation, radiation, humidity, and other meteorological variables. Includes rain-gauge observations, gridded products, satellite estimates, and reanalysis data. | [ERA5-Land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land), [CEH-GEAR](https://doi.org/10.5285/dbf13dd5-90cd-457a-a986-f2f9dd97e93c), [NASA IMERG](https://gpm.nasa.gov/data/imerg), [NOAA CPC](https://www.cpc.ncep.noaa.gov/) |
| **5. Meteorological forecasts** | Predicted precipitation, temperature, and other atmospheric variables at future lead times. May include deterministic forecasts, ensembles, and archived forecasts (hindcasts). | [ECMWF IFS](https://www.ecmwf.int/en/forecasts/datasets/open-data), [WeatherNext](https://github.com/google-deepmind/weathernext), [NOAA GFS](https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast) |
| **6. Additional dynamic observations** | Time-varying hydrological and land-surface conditions, including soil moisture, groundwater levels and storage, snow cover and snow water equivalent, vegetation condition (e.g. NDVI and leaf area index), surface water extent, lake and reservoir levels and storage, and human-controlled flows (e.g. reservoir releases). | [NASA SMAP Soil Moisture](https://smap.jpl.nasa.gov/), [Copernicus Land Monitoring Service](https://land.copernicus.eu/en/dataset-catalog), [GRACE/GRACE-FO Groundwater Storage](https://cds.climate.copernicus.eu/datasets/satellite-groundwater-storage), [NSIDC Snow Data](https://nsidc.org/data/explore-data), [Hydroweb Lake Water Levels](https://catalogue.theia.data-terra.org/meta/HYDROWEB_LAKES_OPE) |

Not all models require every category, and the requirements differ between historical simulation and operational forecasting. The exact inputs depend on the model: conceptual models may use a small set of meteorological inputs, while net-models can also use static catchment attributes. All models use streamflow observations to support calibration, training and evaluation.

## Aggregated data for hydrological modelling

While these individual data sources are useful, combining them across catchments and jurisdictions requires aggregation, quality control and standardisation. There are aggregated datasets for hydrological modelling in which streamflow data, static catchment attributes and meteorological information have already been cleaned, standardised and joined. Two examples of this are:
- **[Caravan](https://github.com/kratzert/Caravan) ([Kratzert et al., 2023](https://www.nature.com/articles/s41597-023-01975-w))**: Caravan combines standardised CAMELS (Catchment Attributes and Meteorology for Large-sample Studies) datasets to make global studies easier. It includes meteorological forcing data, streamflow data, and static catchment attributes (e.g., geophysical, sociological, climatological) for 6,830 catchments in the original release, with subsequent extensions adding further catchments. It has been extended by Caravan MultiMet ([Shalev et al., 2024](https://arxiv.org/abs/2411.09459)) to include several nowcast products (CPC, IMERG v07 Early, CHIRPS), as well as three different forecast products (ECMWF IFS HRES, GraphCast, CHIRPS-GEFS) with multiple bands and 10-day (IFS, GraphCast) or 16-day (CHIRPS-GEFS) lead times.
- **[CAMELS-GB v2](https://catalogue.ceh.ac.uk/documents/9a46d428-958f-4ac1-86eb-94eee70c0955) ([Coxon et al., 2026](https://essd.copernicus.org/articles/18/4345/2026/essd-18-4345-2026.html))**: This presents a standard dataset of daily and hourly streamflow for 671 catchments across Great Britain joined with meteorological and static catchment information. The dataset includes some reservoir and groundwater sites.

Google has also published code supporting its global flood forecasting models including how to source the dataset they used:
- **[Data for "Global prediction of extreme floods in ungauged watersheds"](https://doi.org/10.5281/zenodo.10397664) ([Nearing et al., 2024](https://www.nature.com/articles/s41586-024-07145-1))**: This model was trained using daily streamflow observations from 5,680 gauges, catchment boundaries derived from HydroBASINS, static catchment attributes from HydroATLAS, historical meteorological data from ERA5-Land, NOAA CPC and IMERG, and weather forecasts from ECMWF IFS HRES. The [published data on Zenodo](https://doi.org/10.5281/zenodo.10397664) includes Google model reforecasts, GloFAS reanalyses, trained model artefacts, evaluation metrics and supporting metadata. These are primarily model outputs rather than the original observations and meteorological inputs used for training. See the paper authors' [reproduction code](https://github.com/google-research-datasets/global_streamflow_model_paper) for notes on training data preparation because some inputs (e.g. GRDC) must be obtained separately due to redistribution restrictions.

- **[Google Global Flood Forecasting v2](https://github.com/google-research/flood-forecasting) ([Cohen et al., 2026 _preprint_](https://egusphere.copernicus.org/preprints/2026/egusphere-2026-2283/))**: Rather than providing a completely independent catchment dataset, the [Google Hydrology repository](https://github.com/google-research/flood-forecasting) builds on Caravan for streamflow observations and static catchment attributes, and Caravan MultiMet for historical meteorological inputs and weather forecasts, including ECMWF IFS HRES and GraphCast products. The repository includes model architectures, training and evaluation pipelines, example configurations, and tools for delineating new catchments and extracting HydroATLAS attributes. The paper also links to a [Zenodo model data release](https://doi.org/10.5281/zenodo.19676842).


## Conclusions

A wide range of publicly available datasets support rainfall–runoff modelling, with datasets such as CAMELS-GB and Caravan making it much easier to train models across many catchments. However, the source observations are fragmented across different providers, resolutions and licenses. Open data-processing pipelines allowing datasets to be extended or reproduced may be just as valuable as the source datasets themselves.
