# 2019-numeric-hydraulic-1D-discharge-modelling
## Automated stage-discharge-relationships out of DGPS and drone cross sections in an alpine river
### *Python 2.7, IDE PyCharm 2018.2.5 Community Edition*

This project is part of my master thesis about "Discharge measurements in alpine rivers - Opportunities of numeric, hydraulic stage-discharge-relationships". The whole project got developed in partnership with the Institute of Geography, department of hydrology and the hydropower company Kraftwerke Oberhasli AG (KWO).

You will find more insights of the project about *Project overview*, *Investigation area*, *Scientific background* and *Results / interpretation* in the **Report_kwy.pdf**.

Author: Kevin Wyss, 14-104-640, kevin.wyss@students.unibe.ch, University of Bern, Seminar Geodata analysis and modelling 2019

## Goal of the script
The goal of this python script is to create an automated stage-discharge-relationship out of a measured river cross section.

## Investigation Area
The areas of interest involve four rivers in the region of Susten and Grimsel in the Bernese Oberland:
  - Steinwasser
  - Giglibach
  - Wendenwasser
  - Hasliaare

The idea of those four alpine rivers are the different types of morphology. Steinwasser and Wendenwasser are two alpine rivers with medium steepness. Giglibach is an alpine torrent and Hasliaare, as the prime site, is a wide and shallow river, investigated in Innertkirchen.

## Input parameters
The success of this project was jointed with a lot of field work and data collection. The following input parameters are necessary to run the script:
  - River cross sections
  - Digital elevation models to set the flow gradient
  - Permanent stage mesurements at the particular cross sections
  - Discharge measurements to kalibrate the roughness coefficient

The river cross sections were measured with DGPS (Differential Global Positioning System). The DGPS cross sections are directly loaded into the python script as text files. To get a more precise (higher point density) cross section, the area of interest was flown by a DJI professional drone. The created photographs have been post processed with a structure from motion software (Agisoft PhotoScan) to generate a digital elevation model (DEM). The DEM was used to create high precision cross sections and to calculate the flow gradient. To get those information’s out of the DEM, the Software QGIS Desktop (2.18.10) was used. The permanent recording of the water-level has been done by pressure probes by Altecno. The probe measures the stage every minute and creates an average over ten minutes. The information about the water level is necessary in combination with the manually measured discharge and the resulting stage-discharge-relationship. The discharge has been measured with the salt dilution method, which means, that a certain amount of salt (dependent on the amount of discharge - 5kg salt for one cubic meter per second discharge) gets added to the river. After enough stirring distance the salt flows through an analyser of electronic conductivity, which leads through the integration of the salt curve to the discharge.

## One-dimensional numeric-hydraulic-modelling
 One dimensional numeric hydraulic modelling depends on the flow formula after Manning Strickler. In this sence the discharge (Q) results out of the multiplication of flow velocity (vm), which is supposed to be equal in the whole cross section, and the flown through area (A):
 
    Q [l/s] = vm [m/s] * A [m^2]
 
 Whereat the flow velocity (vm) is calculated:
 
    vm [m/s] = kst [] * Rhy^(2/3) [m] * J^(1/2) [m/m]
   
    kst  = roughness coefficient after Manning Strickler 
    Rhy  = hydraulic radius 
    J    = flow gradient 

 The hydraulic radius (Rhy) is calculated out of the two profile-known parameters:
 
    Rhy [m] = A [m^2] / P [m]
    
    P   = wetted perimeter
 
## Workflow
The whole workflow of this project takes place in the script ***1DPQBeziehung_kwy.py***. The script is subdivided in differnet steps, each marked with a title. As user, you can go to step 2) and define the parameters, then run the script.

  **1) Load four packages:**

   Package | Use
   ------------ | -------------
   *numpy* | create arrays to work with
   *pandas* | load profiles and connect seperate lists
   *matplot* | plot figures
   *prettytable* | show results as a table

  **2) Define parameters:**
  
  The user needs to define the five parameters:

   Shortcut | Parameter
   ------------ | -------------
   *pn* | define the profile name
   *fn* | define the file name of the river cross section (qp) which should be stored in the same folder as the script (text file)
   *h* | define the water-level which should be investigated (cm)
   *kst* | define the roughness value after Manning Strickler 
   *J* | define the flow gradient as a float (m/m)
   
   **3) Beginning of the loop:**
   
   Before the loop starts, the script creates five empty lists, which are then filled with the calculated area (A), wet perimeter (P), hydraulic radius (Rhy) and the discharge (Q) for different hights (H). *H* is starting at 0.1, 0.11, 0.12, [...] until the users definded water-level (h). The loop is used to do all the calculations below (3.2 - 3.7) for all the different hights (H), to get a stage-discharge-relationship in the end.
   
   3.1) Profile gets loaded
   
   The profile which was defined in step 2) gets loaded into the script. In the same step the geographical altitude gets transformed into meter-hights. This happens by the subtraction of all altitudes with the minimum altitude of the list. After this step, every point in the profile list has an x- and y-coordinate. The x-coordinate stays for the measured distance of the cross section (starting at 0 m) and the y-coordinate stays for the hight.
   
   
   3.2) Intersections of the profile
   
   With linear interpolation, the intersections are generated at the points, where the water-level (h) crosses the profile line. This step needs a lot of conditions, for example: When the point left (i-1) of (i) is higher than the water level (h) and the next point (i+1) is lower than the water-level (h) there needs to be an intersection point. As described above there enters linear interpolation into force:
   
    xa = x1 + (ya - y1) * ((x1 - x2) / (y1 - y2))
    
    xa  = wanted x-coordinate where the water-level crosses the profile line
    ya  = hight of the water-level (h)

As shown in the example above, there are 20 other conditions which need to be checked, to get all intersections of the profile with the water-level.


   3.3) Preconditione for the following parameter calculations
   
   In this step the new x- and y-coordinates (with the intersection points) were set into a new list, which then gets adapted to the water-level (h). The points higher than h get set on the water-level, which results in a thinned profile.
   
   
   3.4) Calculation of the area (A) with integration
   
   The area (A) to be calculated is the area between the water-level (h) and the profile curve. This calculation happens for the area between each profile point like this:
   
    A [m^2] = 0.5 * (x2 - x1) * (WD1 + WD2)
      
    x2  = x-coordinate of the point i+1
    x1  = x-coordinate of the point i
    WD1 = water depth of point i (= the water-level (h) minus y-coordinate of point i)  
    WD2 = water depth of point i+1 (= the water-level (h) minus y-coordinate of point i+1)  
      
To get the whole area between water-level and profile, all these sub-areas get summed up.


   3.5) Calculation of the wetted perimeter (P)
   
   The wetted perimeter (P) gets calculated with vector geometry. As a first step to get the distance between all profile-points, the script calculates the direction vector (AB) between each point:
    
    AB = (x2, y2) - (x1, y1)
      
    x2, y2  = x- and y-coordinate of the point i+1
    x1, y1  = x- and y-coordinate of the point i
  
 This results in a new list, CD, with all direction vectors of the profile. To get the actual distance between the points, the script needs to calculate the absolute value (|CD|) of the direction vectors:
 
    |CD| = square root(C^2 + D^2)
    
 In a following while-loop, the point distances get sorted out, which are effectively wetted and which are not. The script from now on processes only the wetted distances and summes those up to get the wetted perimeter (P).
   
   
   3.6) Calculation of the hydraulic radius (Rhy)
   
   The hydrualic radius is being calculated out of the division of the area (A) and the wetted perimeter (P):
   
    Rhy [m] = A [m^2] / P [m]
     
     
   3.7) Calculation of the discharge (Q) and ending of the loop
   
   The discharge is being calculated as in the chapter ***One dimensional numeric-hydraulic-modelling*** described above:
   
    Q [m^s/s] = kst * Rhy^(2/3) [m] * J^(1/2) * A [m^2]
   
   **4) PrettyTable**
   
   After the loop comes to an end and all the calculation (h, A, P, Rhy and Q) is done, the package *PrettyTable* illustrates the entire results in a table for a good overview.
   
   **5) Plotting the profil**
   
   The first plot illustrates the cross section with the thinned profile. This plot shows all profile points and the effectively used profile points for the calculations above. This is not only an illustration, it also functions as a monitoring tool, to check if the script generated the intersection points at the right place.
   
   **6) Plotting the stage-discharge-relationship**
   
   As the last step, the script plotts the resulting stage-discharge-relationship for the entered cross section. This relationship is based on the calculations 3.2 - 3.7 for all different hights (H).
   
# Results and interpretation
To get a more precise insight of the resulting output of the script, see the PDF "Report_kwy.pdf" in the project folder.
