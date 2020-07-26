# ramp_analyzer
A tool to analyze and modify ramp file

## Install:
```
pip install git+https://github.com/RedisLabsModules/ramp_analyzer
```

## Usage:
```        
ramp-Analizer > help

Documented commands (type help <topic>):
========================================
close  dumpdeps  dumpfiles  dumpjson  exit  help  open  rewritedeps  save
ramp-Analizer > help open

        Open a ramp file to work on

ramp-Analizer > help close

        Close the current open file
        
ramp-Analizer > help dumpdeps

        Dump the dependencies and supported-dependencies section in the ramp file
        
ramp-Analizer > help dumpfiles

        Dump all the files in the ramp.zip
        
ramp-Analizer > help dumpjson

        Dump the entire module.json file
        
ramp-Analizer > help exit

        exit the application. Shorthand: x q Ctrl-D.
        
ramp-Analizer > help rewritedeps

        Rewrite the dependencies section of the ramp.
        
ramp-Analizer > help save

        Save the ramp file to disc
        
```

Notice that its also possible to start the ramp-analyzer with a given ramp file:
```
> ramp-analyzer /path/to/module.zip
```
