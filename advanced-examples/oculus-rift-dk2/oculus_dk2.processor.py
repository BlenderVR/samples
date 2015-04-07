import blendervr

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Quaternion, Matrix, Vector, Euler
    from math import radians

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self._scene = bge.logic.getCurrentScene()

        def user_position_right(self, info):
            super(Processor, self).user_position(info)
            try:
                obj = self._scene.objects['Suzanne']
                cam = self._scene.active_camera
                user = self.blenderVR.getUserByName('user A')
                rot = Matrix.Rotation(radians(180),4,'Y')
                trans = Matrix.Translation(Vector(3,0,0))
                rot2 = Matrix.Rotation(radians(180),4,'Z')
                obj.worldTransform = cam.worldTransform * user.getVehiclePosition() * user.getPosition()
                # self.logger.debug(obj.worldTransform)
                # self.logger.debug(user.getVehiclePosition())#  * user.getPosition())
            except:
                self.logger.log_traceback(False)

        def user_position_left(self, info):
            super(Processor, self).user_position(info)

        def space_navigator_analog_right(self, info):
            user = self.blenderVR.getUserByName('user B')
            self.space_navigator_analog(info, user)
            # try: self.space_navigator_analog(info, user)
            # except: self.logger.log_traceback(False)

        def space_navigator_analog_left(self, info):
            user = self.blenderVR.getUserByName('user A')
            self.space_navigator_analog(info, user)


        def space_navigator_analog(self, info, user):
            """
            Callback for a Space Navigator (3D Connexion)
            Defined in the XML config file.

            It is called everytime the analogic handle is used.

            This function moves and rotates the Monkey.
            """

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
            userRot_Y = Matrix.Rotation(user.getPosition().to_euler().y,4,'Y')
            rel_trans = userRot_Y.inverted() * translation
            loc, rot, scale = rel_trans.decompose()
            translation = Matrix.Translation(loc)

            factor_rot = 0.2
            rotation = Matrix.Rotation(factor_rot * data['roll'], 4, 'Y')

            new_ori = rotation * translation * user.getVehiclePosition()
            user.setVehiclePosition(new_ori)

        def keyboardAndMouse(self, info):
            try:
                if info['key'] == ord('s') and info['state'] == device.STATE_PRESS:
                    self.logger.debug('###',info['key'])
                else:
                    self.logger.debug('',info['key'])
            except (KeyError, SystemExit):
                pass
            except:
                self.logger.log_traceback(False)
            super(Processor, self).keyboardAndMouse(info)

        def start(self):

            if self.blenderVR.isMaster():
                try:

                    self._OSC = self.blenderVR.getPlugin('osc')

                    # Define global parameters
                    self._OSC.getGlobal().start(True)
                    self._OSC.getGlobal().volume('%20')

                    # get OSC users

                    A_sound_user = self._OSC.getUser(self.blenderVR.getUserByName('user A'))
                    B_sound_user = self._OSC.getUser(self.blenderVR.getUserByName('user B'))
                    A_sound_user.volume('%50')
                    B_sound_user.volume('%50')

                    self._sound_objects = {}

                    osc_objects = [{'name'  : 'Plane.003',
                                    'sound' : 'TF_kick.wav',
                                    'mute'  : False},
                                   {'name'  : 'Plane.005',
                                    'sound' : 'TF_ride.wav',
                                    'mute'  : False},
                                   {'name'  : 'Plane.006',
                                    'sound' : 'TF_snare.wav',
                                    'mute'  : False},
                                   {'name'  : 'Plane.007',
                                    'sound' : 'TF_piano.wav',
                                    'mute'  : False},
                                   {'name'  : 'Plane.008',
                                    'sound' : 'TF_saxophone.wav',
                                    'mute'  : False}]

                    # get and instantiate OSC objects
                    for osc_object_def in osc_objects:
                        blender_object = bge.logic.getCurrentScene().objects[osc_object_def['name']]
                        osc_object     = self._OSC.getObject(blender_object)
                        osc_object.sound(osc_object_def['sound'])
                        # self.logger.debug('11111', osc_object_def['sound'])
                        osc_object.mute(osc_object_def['mute'])
                        osc_object.loop(True)
                        osc_object.start(True)
                        osc_object.mute(osc_object_def['mute'])

                        self._sound_objects[id(blender_object)] = {'object' : osc_object,
                                                             'volume' : 20,
                                                             'mute'   :  False}

                        userObject1 = self._OSC.getObjectUser(osc_object, A_sound_user)
                        userObject1.mute(False)
                        userObject2 = self._OSC.getObjectUser(osc_object, B_sound_user)
                        userObject2.mute(False)

                    self.logger.debug("### OSC Initialized")

                # except AttributeError:
                #     self.logger.warning('OSC plugin not/badly defined in configuration file -> OSC disabled.')
                except:
                    self.logger.log_traceback(False)

        def quit(self):
            """
            blenderVR Callback, called at run stop.
            """
            if self.blenderVR.isMaster():
                try:
                    self._OSC.reset() # sends "/global reset" OSC msg
                    self.logger.debug("## Quit my Processor")
                except:
                    self.logger.log_traceback(False)

        # def run(self):
        #     user = self.blenderVR.getUserByName('user B')
        #     self.logger.debug(user.getVehiclePosition().inverted() * user.getPosition())

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
