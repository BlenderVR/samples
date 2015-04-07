import blendervr

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Matrix
    from math import radians

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self._user = self.blenderVR.getUserByName('user A')
            self._scene = bge.logic.getCurrentScene()
            self._camera = self._scene.active_camera

        def user_position(self, info):
            super(Processor, self).user_position(info)
            try:
                obj = self._scene.objects['Suzanne']
                # obj2 = self._scene.objects['Suzanne.001']

                # rot = Matrix.Rotation(radians(180),4,'Y')
                # trans = Matrix.Translation(Vector(3,0,0))
                # rot2 = Matrix.Rotation(radians(180),4,'Z')
                # obj.worldTransform = self._camera.worldTransform * self._user.getVehiclePosition() * self._user.getPosition()
                # obj.worldTransform = self._user.getVehiclePosition() * self._user.getPosition()

                rot = Matrix.Rotation(radians(-90),4,'X') # * Matrix.Rotation(radians(90),3,'Z')
                obj.worldTransform = rot.inverted() * (self._user.getVehiclePosition() * self._user.getPosition()) * rot
                # obj2.worldOrientation = rot_blender2GLSL * self._user.getPosition().to_3x3()


                # self.logger.debug(obj.worldTransform)
                # self.logger.debug(user.getVehiclePosition())#  * user.getPosition())
            except:
                self.logger.log_traceback(False)

        def space_navigator_analog(self, info):
            raw_data = info['channel']
            data = {'x' : raw_data[0],
                    'y' : raw_data[1],
                    'z' : raw_data[2],
                    'tilt' : raw_data[3],
                    'yaw' : raw_data[4],
                    'roll' : raw_data[5],
                    }

            factor_pos = 0.5
            translation = Matrix.Translation((factor_pos * -data['x'], factor_pos * data['z'],factor_pos * -data['y']))

            # comment the following block to cancel translation relative to oculus' rotation
            userRot_Y = Matrix.Rotation(self._user.getPosition().to_euler().y,4,'Y')
            rel_trans = userRot_Y.inverted() * translation
            loc, rot, scale = rel_trans.decompose()
            translation = Matrix.Translation(loc)

            factor_rot = 0.2
            rotation = Matrix.Rotation(factor_rot * data['roll'], 4, 'Y')

            new_ori = rotation * translation * self._user.getVehiclePosition()
            self._user.setVehiclePosition(new_ori)
            # except:
            #     self.logger.log_traceback(False)

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
