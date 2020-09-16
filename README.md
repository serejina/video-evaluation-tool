# Table of contents
1. [Intro](#intro)
2. [Project structure](#structure)
3. [How to run](#run)
## Intro <a name="intro"></a>
This is trivial set of scripts which process input videos and create report about their quality based on using metrics (PSNR for now).
It assume that user provide list of pairs with two video files which are needed to be compared.
## Project structure <a name="structure"></a>
```
video_coding_evaluation tool (VCETool) - project folder structure
│   README.md  
│   requirements.txt
│   main.py
|
└─── config  
│    │   input_config_1.json  
│   
└───source
|   │   config.py
|   │   exceptions.py
|   |   metrics.py
|   |   psnr.py
|   |   report.py
|   └───templates
|       |   base_template.html
|
└───test  
```

#### requirements.txt
The file with names of python packages required to run the project  

#### main.py
The python module with the main function  

####config
The folder with configuration files. Information about videos to evaluate is in configuration files.  
The configuration file at least shall contain the following information:  
```
{
  "videos": [
    {
      "reference_video": "./test_1.mkv",
      "compressed_video": "./test1.mp4",
    }
  ]
}
```

###source
The folder with all project modules  
```config.py``` - module with class to represent the configuration file   
```exceptions.py``` - module with the project exceptions  
```metrics.py``` - module with class of validation metrics.  
Currently, min/max/median PSNR, and ratio of PSNR filtered by specified criteria to all PSNR (i.e. Ratio of PSNR being below a certain configurable threshold)  
```psnr.py``` - module with functions to calculate PSNR for each video frames  
```report.py``` - module with functions to create html-report with metrics for each processed videos  
###test
The folder with unit tests (currently empty)

## How to run <a name="run"></a>
1. Open ./config/ folder create or update .json file with videos to check
2. Go to main.py module, check the name of the configuration file and the report file name
3. Run main function
4. Check the report file