import blendervr
import os

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
            super(Processor, self).run()

            try:
                monkey = bge.logic.getCurrentScene().objects['Monkey']

                if self._is_scaling_up:
                    monkey.localScale *= 1.05

                elif self._is_scaling_down:
                    monkey.localScale /= 1.05

            except Exception as err:
                self.logger.error(err)

        def spaceNavAnalog(self, info):
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

                #rotation = Vector((data['tilt'], -data['yaw'], -data['roll']))
                rotation = Vector((0, 0, -data['roll']))
                factor = 0.2

                monkey.applyRotation(rotation * factor)

            except Exception as err:
                self.logger.error(err)

        def spaceNavButton(self, info):
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
            global try_wait_user_name, try_chooser, try_console_arc_balls
            super(Processor, self).__init__(console)

        def useLoader(self):
            return True

