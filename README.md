# malmomagic
Getting started with Malmo


Okay.. here is the plan!

Assuming you have already installed Malmo, every python program you want to run needs this module 'MalmoPlatform.so' to be able to open Malmo.

So this file is available in the current folder. Run the following for the programs to be able to access it.
 
```
$ python setup.py ; source ~/.bashrc 
Adding current dir ./malmomagic to PYTHONPATH in your bashrc
so that MalmoPlatform.so is accessible to your malmo programs
Done!
```

For every tiny program/situation/scenario our agent is in, lets have a folder 

`./<<some sensible experiment NAME>>/NAME.py`

and make sure you give some description about what the agent is trying to do in that scenario
