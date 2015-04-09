import blendervr
import os

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)


elif blendervr.is_creating_loader():
    import bpy

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, creator):
            super(Processor, self).__init__(creator)


elif blendervr.is_console():
    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, console):
            global try_wait_user_name, try_chooser, try_console_arc_balls
            super(Processor, self).__init__(console)

        def useLoader(self):
            return True
