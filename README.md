# malmomagic
Getting started with Malmo


Okay.. here is the plan!

Assuming you have already installed Malmo, every python program you want to run needs the module 'MalmoPlatform.so' to be able to open Malmo.
Copy it to the current directory, to be able to run programs from this project folder.
Alternatively, you can always copy the program to ~/MalmoPlatform/Python_Examples/ and run it from there.

Run the following to take care of the things mentioned above.
 
```
$ cp ~/MalmoPlatform/Python_Examples/MalmoPython.so . ; python setup.py ; source ~/.bashrc 
Adding current dir ./malmomagic to PYTHONPATH in your bashrc
so that MalmoPlatform.so is accessible to your malmo programs
Done!
```

For every tiny program/situation/scenario our agent is in, lets have a folder 

`./<<some sensible experiment NAME>>/NAME.py`

and make sure you give some description about what the agent is trying to do in that scenario
