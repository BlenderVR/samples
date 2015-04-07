import blendervr

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

        def user_position(self, info):
            """
            Callback defined in the XML config file to one of the Oculus DK2

            This function is optional but it's useful for debugging or non-standard
            usage of the Oculus DK2 devices.

            An analog function defined in the main Processor already takes care of
            updating the position (and orientation) of the users, and it's used
            as a callback when no processor_method is specified in the XML config file
            """
            # self.logger.debug('RIGHT', info['users'][0].getName(), len(info['users']))
            super(Processor, self).user_position(info)


elif blendervr.is_creating_loader():
    import bpy

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, creator):
            super(Processor, self).__init__(creator)


elif blendervr.is_console():
    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, console):
            super(Processor, self).__init__(console)

        def useLoader(self):
            return True
