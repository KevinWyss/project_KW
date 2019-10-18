# 2019-numeric-hydraulic-1D-discharge-modelling
## Automated stage-discharge-relationships out of DGPS and drone-crosssections in an alpine river
### Python 2.7, IDE PyCharm 2018.2.5 Community Edition

This project is part of my master thesis about "Discharge measurements in alpine rivers - Opportunities of numeric hydraulic stage-discharge-relationships". The whole project got developped in the partnership of the Institute of Geography, department of hydrology and the hydro power company Kraftwerke Oberhasli AG (KWO).

If you want a more detailed insight of the project, you will find a PDF ("") in my project folder.

Author: Kevin Wyss, 14-104-640, University of Berne, Seminar Geodata analysis and modelling 2019

## Goal of the script
The goal of this python script is to create an automated stage-discharge-relationship out of a measured river crosssection.

## Investigation Area
My area of intrest concerning four rivers in the region of Susten and Grimsel. They were:
  - Steinwasser
  - Giglibach
  - Wendenwasser
  - Hasliaare

The idea of those four alpine rivers where the different types of morphology. Steinwasser and Wendenwasser are two alpine rivers with medium steepness. Giglibach is an apline torrent and Hasliaare as the prime site is a wide and shallow river, investigated in Innertkirchen.

## Data / Input parameters
The success of this project was joint with field work/data collection in the Grimsel and Susten area. The following input parameters are necessary to run the script:
  - River crosssections
  - Digital elevation models to set the flow gradient
  - Permanent stage mesurements at the particular cross sections
  - Discharge measurements to kalibrate the roughness coefficient

## Method
 measured with DGPS (Differential Global Positioning System) or Drone photogrammetry

Stage measured every minute, then the mean over 10min
The stage gets measured with a pressure probe.

Flow formula after Manning Strickler
