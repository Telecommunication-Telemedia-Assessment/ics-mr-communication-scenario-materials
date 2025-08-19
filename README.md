# ICS-MR: Communication Scenario Materials

This repository contains materials for the scenarios described in the ICS-MR (Interactive Conversation Scenarios for Assessment of Mixed Reality Communication) dataset.
Corresponding Unity-based implementations can be found in a [separate repository](https://github.com/Telecommunication-Telemedia-Assessment/ics-mr-communication-scenario-materials).

## Materials

The material dataset is organized by scenario. Materials for each scenario are summarized below.

### SCENARIO 1: Floor Plan Negotiation

Provided materials:
* Various apartment floor plan images with different characteristics. 

**Number of Rooms:** There are different sets of floor plans, with 4 and 5 assignable rooms respectively. All image files include the string `4room` or `5room` to signify the number of assignable rooms.

**Environment:** There are also different sets of floor plans with the apartment's surrounding environment shown. Image files with the environment shown include the string `_env` in their name.

**File Type:** All images are included as vector graphics (`.svg`) in directory `FloorPlanSVG` for convenient editing and as rasterized images (`.png`) in directory `FloorPlanImages` for use as textures in Unity.  

### SCENARIO 2: Spot the Difference

Provided materials:
* Lists of shapes to be shown to each participant
* An image for each listed shape
* A python script to generate images from the shape lists, in case the shape lists are changed

**Shape Lists:** One list of shapes is intended to be used for each trial. Each list contains the type of shape and the color of the shape to be shown to each participant (assuming that there are 2 participants). While most of the shapes pairs will be matching, three shape pairs will not (i.e. their color and/or shape will differ). Four shape lists are provided (plus a shorter one for the training round). Shape lists may be edited. However, introducing additional shapes or colors requires the Unity implementation and python script to be updated to support those colors/shapes.

**Shape Images:** For application of this scenario outside of Unity, `.svg` image collections corresponding to the shape lists are provided in directory `ShapeSVGs`. 

**Image Creation Script:** If shape images are required for shape lists that have been updated, the python script included in directory `SVGGenerator` can be executed to create new collections of shape images.

### SCENARIO 3: Survival Game

Provided materials:
* Text descriptions of 5 survival scenarios
* A list of items for each survival scenario
* An image corresponding to each survival item (incl. corresponding image attribution)
* Task sheets with scenario descriptions and item lists that can be printed for use in a real-world use of the scenario
* A python script to generate task sheets for different numbers of participants or for edited item lists

**Scenario Descriptions:** A set of `.txt` files in the `Scenario` directory of desciptions to be shown before (and/or during) each trial to set the scene for each scenario.

**Item Lists:** A set of `.csv` files stored in the `SurvivalItemData` directory, with short and long names for each item, and an ID used to link to an image.

**Item Images:** A set of `.png` images stored in the `SurvivalItemImages` directory, with one image per item. Corresponding image attributions are stored in [Image Attribution](S3_SurvivalGame/image_attributions.md).

**Task Sheets:** The task sheets can be found as latex (`.tex`) and PDF files in the `SurvivalItemSheets` directory.

**Task Sheet Generator:** New task sheets for different participant group sizes or new item lists can be generated using the `generate_item_sheets_merged.py` script in the `SurvivalItemSheetGenerator` directory.


## License

This dataset is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) license.

See the [LICENSE](LICENSE.txt) and [Image Attribution](S3_SurvivalGame/image_attributions.md) files for details.
