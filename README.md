# ICS-MR: Communication Scenario Materials

This repository contains task materials for the scenarios contained in the ICS-MR (Interactive Conversation Scenarios for Assessment of Mixed Reality Communication) dataset.

## Materials

The task materials are organized by scenario, and are summarized below:

### TASK 1: Floor Plan Negotiation

The task materials for the floor plan negotiation scenario consist of various apartment floor plan images with different characteristics. 

**Number of Rooms:** There are different sets of floor plans, with 4 and 5 assignable rooms respectively. All image files include the string `4room` or `5 room` to signify the number of assignable rooms.

**Environment:** There are also different sets of floor plans with the apartment's surrounding environment shown. Image files with the environment shown include the string `_env` in their name.

**File Type:** All images are included as vector graphics (.svg) in directory `FloorPlanSVG` and as rasterized images (.png) in directory `FloorPlanImages` for use in Unity.  

### TASK 2: Spot the Difference

The task materials for the 'spot the difference' task encompass: 
* lists of shapes to be shown to each participant
* an image for each listed shape
* a python script to generate images from the shape lists, in case the shape lists are changed

**Shape Lists:** One list of shapes is intended to be used for each trial. Each list contains the type of shape and the color of the shape to be shown to each participant (assuming that there are 2 participants). While most of the shapes pairs will be matching, three shape pairs will not (i.e. their color and/or shape will differ). Four shape lists are provided (plus a shorter one for the training round). Shape lists may be edited. However, introducing additional shapes or colors requires the Unity implementation and python script to be updated to support those colors/shapes.

**Shape Images:** For application of this task outside of Unity, SVG image collections corresponding to the shape lists are provided in directory `ShapeSVGs`. 

**Image Creation Script:** If shape images are required for shape lists that have been updated, the python script included in directory `SVGGenerator` can be executed to create new collections of shape images.

### TASK 3: Survival Game

The task materials for the survival game consist of:
* Text descriptions of 5 survival scenarios
* A list of items for each survival scenario
* An image corresponding to each survival item

**Scenario Descriptions:** to be shown before (and/or during) each trial to set the scene for each scenario.

**Item Lists:** A set of .csv files stored in the `SurvivalItemData` directory, with short and long names for each item, and an ID used to link to an image.

**Item Images:** A set of .png images stored in the `SurvivalItemImages` directory, with one image per item.
