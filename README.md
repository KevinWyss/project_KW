# 2019-numeric-hydraulic-1D-discharge-modelling
## Automated stage-discharge-relationships out of DGPS and drone-crosssections in an alpine river
### *Python 2.7, IDE PyCharm 2018.2.5 Community Edition*

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

## Input parameters, measurements and processing
The success of this project was joint with field work/data collection in the Grimsel and Susten area. The following input parameters are necessary to run the script:
  - River crosssections
  - Digital elevation models to set the flow gradient
  - Permanent stage mesurements at the particular cross sections
  - Discharge measurements to kalibrate the roughness coefficient

The river cross sections got measured with DGPS (Differential Global Positioning System). The DGPS cross sections get directly loaded into the python script as text files. To get a more precise (higher point density) cross section, the area of interest got flown by a DJI professional drone. The created photographs got post processed with a structure from motion software (Agisoft PhotoScan) to generate a digital elevation model (DEM). The DEM was used to create the high precision cross section and to calculate the flow gradient. To get those inforamtions out of the DEM, the Software QGIS Desktop (2.18.10) was used. The permanent recording of the water-levels got done by pressure probes. The probe measures the stage every minute and creates an average over ten minutes. The information about the water level is necessary in combination of the manually measured discharge and the resulting stage-discharge relationship. The discharge got measured with the salt dilution method, which means, that a certain abount of salt (dependent on the amount of discharge - 5kg salt for one cubic meter per second discharge) gets added to the river. After enough stirring distance the salt flows through an analyzer of electronic conductivity, which leads through the integration of the salt curve to the discharge.

## One dimensional numeric-hydraulic-modelling
 One dimensional numeric hydraulic modelling depends on the flow formula after Manning Strickler. In this sence the discharge (Q) results out of the multiplication of flow velocity (vm), which is supposed to be the same in the whole cross section, and the flown through area (A).
 
    Q [l/s] = vm [m/s] * A [m^2]
 
 Whereat the flow velocity (vm):
 
    vm [m/s] = kst [] * Rhy^(2/3) [m] * J^(1/2) [m/m]
   
kst  = roughness coefficient after Manning Strickler 

Rhy  = hydraulic radius 

J    = flow gradient 

## Workflow
The whole workflow of this project takes place in the script ***1D_PQ_Beziehung_kwy_5.0.py***. The script is subdivided in differnet steps, marked with a title.

  **1) Four packages get loaded and are used to:**

   Package | Use
   ------------ | -------------
   *numpy* | create arrays to work with
   *pandas* | load profiles and connect seperate lists
   *matplot* | plot figures
   *prettytable* | show results in a table

  **2) Define parameters:**
  
  The user needs to define the four parameters:

   Shortcut | Parameter
   ------------ | -------------
   *pn* | define the profile name
   *fn* | define the file name which should be stored in the same folder as the script
   *h* | define the water-level which should be investigated (cm)
   *kst* | define the roughness value after Manning Strickler
   *J* | define the flow cradient as a fload (m/m)
   
   **3) Beginning of the loop:**
   
   Bevore the loop starts, the script creates five empty lists, which then get filled with the calculated area (A), wet perimeter (P), hydraulic radius (Rhy) and the discharge (Q) for different hights (H), starting at 0.1, 0.11, 0.12... until the users definded water-level (h). 
   
   **3.1) Profile gets loaded
   
   The profile which got defined in step 2) gets loaded into the script. In the same step the geographical elevation gets transformed into metric values
   
   **3.2) Intersections of the profile
   
   With linear interpolation, the intersections get generated at the points, where the water-level (h) crosses the profile line. This step needs a lot of conditions for example: When the point left of (i) is higher than the water level (h) and the next point (i+1) is lower than the water-level (h) there need to be a intersection point. As told there enters linear interpolation into force:
   
    xa = x1 + (ya - y1) * ((x1 - x2) / (y1 - y2))
    
xa  = 
# Results
PDF file "??" in the project folder.
