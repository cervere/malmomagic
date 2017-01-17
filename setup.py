
import os,sys

dir = os.path.dirname(os.path.realpath(__file__))

print "Adding current dir "+dir+" to PYTHONPATH in your bashrc so that MalmoPlatform.so is accesible to your malmo programs"
os.system("echo 'export PYTHONPATH="+dir+"' >> ~/.bashrc")
print "Done!"
