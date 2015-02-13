import blendervr

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Vector

    class Processor(blendervr.processor.getProcessor()):
        _is_scaling_up = False
        _is_scaling_down = False

        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

        def run(self):
            """
            Main loop routine, it runs a few times per frame.
            """
            super(Processor, self).run()

            try:
                monkey = bge.logic.getCurrentScene().objects['Monkey']

                if self._is_scaling_up:
                    monkey.localScale *= 1.05

                elif self._is_scaling_down:
                    monkey.localScale /= 1.05

            except Exception as err:
                self.logger.error(err)

        def space_navigator_analog(self, info):
            """
            Callback for a Space Navigator (3D Connexion)
            Defined in the XML config file.

            It is called everytime the analogic handle is used.

            This function moves and rotates the Monkey.
            """
            try:
                #self.logger.info("Analog @ 3d connexion: {0}".format(info))

                raw_data = info['channel']
                data = {'x' : raw_data[0],
                        'y' : raw_data[1],
                        'z' : raw_data[2],
                        'tilt' : raw_data[3],
                        'yaw' : raw_data[4],
                        'roll' : raw_data[5],
                        }

                monkey = bge.logic.getCurrentScene().objects['Monkey']
                monkey.worldPosition[0] += data['x']
                monkey.worldPosition[1] -= data['y']
                monkey.worldPosition[2] -= data['z']

                # use the commented out line below if you want to rotate all the axis of the Monkey
                #rotation = Vector((data['tilt'], -data['yaw'], -data['roll']))
                rotation = Vector((0, 0, -data['roll']))
                factor = 0.2

                monkey.applyRotation(rotation * factor)

            except Exception as err:
                self.logger.error(err)

        def space_navigator_button(self, info):
            """
            Callback for a Space Navigator (3D Connexion)
            Defined in the XML config file.

            It is called everytime a button in the Space
            Navigator is clicked.

            This function scales the Monkey up and down.
            """
            try:
                if info['button'] == 0:
                    if info['state'] == 1:
                        self.logger.info("1st button clicked @ Space Navigator (3D Connexion)")
                        self._is_scaling_down = True
                    else:
                        self.logger.info("1st button released @ Space Navigator (3D Connexion)")
                        self._is_scaling_down = False

                elif info['button'] == 1:
                    if info['state'] == 1:
                        self.logger.info("2nd button clicked @ Space Navigator (3D Connexion)")
                        self._is_scaling_up = True
                    else:
                        self.logger.info("2nd button released @ Space Navigator (3D Connexion)")
                        self._is_scaling_up = False

            except Exception as err:
                self.logger.error(err)


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

