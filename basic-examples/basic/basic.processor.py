# Minimalistic BlenderVR processor file example

import blendervr
import os


# The blendervr.is_virtual_environment() condition is satisfied
# for the running of a daemon and its associated blenderplayer
# (i.e. it concerns BlenderVR logic related to the running of
# the blender game engine, where you'll probably want to add
# your own code :).
if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                # This line tell the master that every item in bge.logic as to be synchronized
                # between the slaves and itself (white listing).
                # Partial synchronization can be used to unload network exchanges and improve
                # real-time rendering performances.
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)


# The blendervr.is_creating_loader() condition is satisfied
# when BlenderVR uses the bpy module to open a .blend scene
# and modify it 'on the fly' before the blender game engine
# is launched, e.g. to add an Always Actuator to run the main
# BlenderVR module or to add the oculus dk2 shader if required.
elif blendervr.is_creating_loader():
    import bpy

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, creator):
            super(Processor, self).__init__(creator)


# The blendervr.is_console() condition is satisfied only on the
# Master node that runs the BlenderVR console (which controls the
# daemons running blenderplayer instances).
elif blendervr.is_console():
    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, console):
            global try_wait_user_name, try_chooser, try_console_arc_balls
            super(Processor, self).__init__(console)

        def useLoader(self):
            return True
