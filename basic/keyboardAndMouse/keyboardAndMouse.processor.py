import blendervr

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Matrix, Quaternion
    from math import radians

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self._textKeyboad = bge.logic.getCurrentScene().objects['TextKey']
            self._textMouse = bge.logic.getCurrentScene().objects['TextMouse']

        def keyboardAndMouse(self, info):
            """
            Handle keyboard and mouse inputs (executed on Master only).
            This method may seem redundant with blender internal logic,
            yet it enables interaction with BlenderVR objects
            (User, Vehicle, etc.) through mouse and keyboard.
            For non BlenderVR interactions (e.g. move kx_object), you may
            continue to use blender based mouse and keyboard actuators.
            """

            super(Processor, self).keyboardAndMouse(info)

            try:
                # keyboard input in info
                if 'key' in info.keys():
                    self._textKeyboad['Text'] = "key: {0}, state: {1}".format(info['key'], info['state'])

                    if info['key'] == ord('q'):
                        self.BlenderVR.quit("pressed 'q' key")

                # mouse input in info
                if 'mouse position' in info.keys():
                    self._textMouse['Text'] = "mouse position: {0}".format(info['mouse position'])

                # # uncomment the following line to print keyboard
                # # and mouse related information in console window
                # self.logger.debug(info)

            except:
                self.logger.log_traceback(False)

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
