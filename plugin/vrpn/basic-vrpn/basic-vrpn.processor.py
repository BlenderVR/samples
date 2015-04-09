import blendervr

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Vector

    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self._monkey = bge.logic.getCurrentScene().objects['Monkey']
            self._is_scaling_up = False
            self._is_scaling_down = False

        def space_navigator_analog(self, info):
            """
            Callback for a Space Navigator (3D Connexion)
            Must be defined (name-wise) in the XML configuration file.

            It is called everytime the analogic handle is used.

            This function moves and rotates the Monkey.
            """
            self.logger.info("test")
            try:
                self.logger.info("test2")
                self.logger.info("Analog @ 3d connexion: {0}".format(info))

                raw_data = info['channel']
                data = {'x' : raw_data[0],
                        'y' : raw_data[1],
                        'z' : raw_data[2],
                        'tilt' : raw_data[3],
                        'yaw' : raw_data[4],
                        'roll' : raw_data[5],
                        }

                factor_pos = 0.8
                self._monkey.worldPosition[0] += factor_pos * data['x']
                self._monkey.worldPosition[1] -= factor_pos * data['y']
                self._monkey.worldPosition[2] -= factor_pos * data['z']

                # use the commented out line below if you want to rotate all the axis of the Monkey
                #rotation = Vector((data['tilt'], -data['yaw'], -data['roll']))
                rotation = Vector((0, 0, -data['roll']))
                factor_rot = 0.4

                self._monkey.applyRotation(rotation * factor_rot)

            except Exception as err:
                self.logger.log_traceback(err)


        def space_navigator_button(self, info):
            """
            Callback for a Space Navigator (3D Connexion)
            Must be defined (name-wise) in the XML configuration file.

            It is called everytime a button in the Space
            Navigator is clicked.

            This function changes Monkey's color and make it invisible.
            """
            self.logger.debug('Space Navigator Button Main')
            try:
                if info['button'] == 0:
                    if info['state'] == 1:
                        self.logger.info("1st button clicked @ Space Navigator (3D Connexion)")
                        self._monkey.visible = False
                    else:
                        self.logger.info("1st button released @ Space Navigator (3D Connexion)")
                        self._monkey.visible = True

                elif info['button'] == 1:
                    if info['state'] == 1:
                        self.logger.info("2nd button clicked @ Space Navigator (3D Connexion)")
                        self._monkey.color = (1,0,0,1)
                    else:
                        self.logger.info("2nd button released @ Space Navigator (3D Connexion)")
                        self._monkey.color = (0,1,0,1)

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

