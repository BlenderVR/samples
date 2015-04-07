import blendervr
import copy

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Vector

    class Processor(blendervr.processor.getProcessor()):

        for obj in bge.logic.getCurrentScene().objects:
            if 'rocks_rock_02' in obj.name:
                obj['is_scaling_up'] = False
                obj['is_scaling_down'] = False
                obj['worldPosition'] = copy.copy(obj.worldPosition)

        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self._scene = bge.logic.getCurrentScene()
            self._userA = self.blenderVR.getUserByName('user A')
            self._userB = self.blenderVR.getUserByName('user B')
            self._sound_objects = {}

        def start(self):

            if self.blenderVR.isMaster():
                try:

                    self._OSC = self.blenderVR.getPlugin('osc')

                    # Define global parameters
                    self._OSC.getGlobal().start(True)
                    self._OSC.getGlobal().volume('%20')

                    # get OSC users
                    # ambisonic_user = self._OSC.getUser('Ambisonic')
                    A_sound_user = self._OSC.getUser(self._userA)
                    B_sound_user = self._OSC.getUser(self._userB)

                    osc_objects = [{'name'  : 'rocks_rock_02',
                                    'sound' : 'HeyPachuco.wav',
                                    'mute'  : False},
                                   {'name'  : 'rocks_rock_02.001',
                                    'sound' : 'Randy_Newman_Monsters_Inc.wav',
                                    'mute'  : False}]

                    # get and instantiate OSC objects
                    for osc_object_def in osc_objects:
                        blender_object = self._scene.objects[osc_object_def['name']]
                        osc_object     = self._OSC.getObject(blender_object)
                        osc_object.sound(osc_object_def['sound'])
                        # self.logger.debug('11111', osc_object_def['sound'])
                        osc_object.mute(osc_object_def['mute'])
                        osc_object.loop(True)
                        osc_object.start(True)

                        self._sound_objects[id(blender_object)] = {'object' : osc_object,
                                                             'volume' : 20,
                                                             'mute'   :  False}

                        #self._OSC.getObjectUser(osc_object, ambisonic_user)

                    self._OSC.getObjectUser(self._OSC.getObject(self._scene.objects[osc_objects[0]['name']]), A_sound_user)
                    self._OSC.getObjectUser(self._OSC.getObject(self._scene.objects[osc_objects[1]['name']]), B_sound_user)

                    self.logger.debug("### OSC Initialized")

                except AttributeError:
                    self.logger.warning('OSC plugin not/badly defined in configuration file -> OSC disabled.')
                except:
                    self.logger.log_traceback(False)

        # def run (self):
        #     self.logger.debug('######## RUN')

        def user_position_right(self, info):
            # self.logger.debug('RIGHT', info['users'][0].getName(), len(info['users']))
            super(Processor, self).user_position(info)

        def user_position_left(self, info):
            # self.logger.debug('LEFT', info['users'][0].getName(), len(info['users']))
            super(Processor, self).user_position(info)

        def run(self):
            super(Processor, self).run()

            try:
                obj = bge.logic.getCurrentScene().objects['rocks_rock_02']
                self.scaleObj(obj)

                obj1 = bge.logic.getCurrentScene().objects['rocks_rock_02.001']
                self.scaleObj(obj1)

            except Exception as err:
                self.logger.error(err)

        def scaleObj(self, obj):
            if obj['is_scaling_up']:
                obj.localScale *= 1.05

            elif obj['is_scaling_down']:
                obj.localScale /= 1.05


        def space_navigator_analog_left(self, info):
            obj = bge.logic.getCurrentScene().objects['rocks_rock_02']
            self.space_navigator_analog(info, obj)


        def space_navigator_analog_right(self, info):
            obj = bge.logic.getCurrentScene().objects['rocks_rock_02.001']
            self.space_navigator_analog(info, obj)
            # obj = bge.logic.getCurrentScene().objects['rocks_rock_02']
            # self.space_navigator_analog(info, obj)

        def space_navigator_analog(self, info, obj):
            """
            Callback for a Space Navigator (3D Connexion)
            Defined in the XML config file.

            It is called everytime the analogic handle is used.

            This function moves and rotates the Rocks.
            """
            try:
                # self.logger.info("Analog @ 3d connexion: {0}".format(info))

                raw_data = info['channel']
                data = {'x' : raw_data[0],
                        'y' : raw_data[1],
                        'z' : raw_data[2],
                        'tilt' : raw_data[3],
                        'yaw' : raw_data[4],
                        'roll' : raw_data[5],
                        }

                rocks_rock_02 = obj
                factor_pos = 0.2
                rocks_rock_02.worldPosition[0] += factor_pos * data['x']
                rocks_rock_02.worldPosition[1] -= factor_pos * data['y']
                rocks_rock_02.worldPosition[2] -= factor_pos * data['z']

                # use the commented out line below if you want to rotate all the axis of the rocks_rock_02
                #rotation = Vector((data['tilt'], -data['yaw'], -data['roll']))
                rotation = Vector((0, 0, -data['roll']))
                factor_rot = 0.4

                rocks_rock_02.applyRotation(rotation * factor_rot)

            except Exception as err:
                self.logger.error(err)


        def space_navigator_button_left(self, info):
            return
            self.logger.debug('Space Navigator Button Left')
            self.space_navigator_button(info)

        def space_navigator_button_right(self, info):
            # self.logger.debug('Space Navigator Button Right!!!')
            obj = bge.logic.getCurrentScene().objects['rocks_rock_02.001']
            self.space_navigator_button(info, obj)

        def space_navigator_button(self, info, obj):
            """
            Callback for a Space Navigator (3D Connexion)
            Defined in the XML config file.

            It is called everytime a button in the Space
            Navigator is clicked.

            This function scales the rocks_rock_02 up and down.
            """
            self.logger.debug('Space Navigator Button Main')
            try:
                if info['button'] == 0:
                    if info['state'] == 1:
                        self.logger.info("1st button clicked @ Space Navigator (3D Connexion)")
                        obj['is_scaling_down'] = True
                    else:
                        self.logger.info("1st button released @ Space Navigator (3D Connexion)")
                        obj['is_scaling_down'] = False

                elif info['button'] == 1:
                    if info['state'] == 1:
                        self.logger.info("2nd button clicked @ Space Navigator (3D Connexion)")
                        obj['is_scaling_up'] = True
                    else:
                        self.logger.info("2nd button released @ Space Navigator (3D Connexion)")
                        obj['is_scaling_up'] = False

            except Exception as err:
                self.logger.error(err)

        def keyboardAndMouse(self, info):
            # super(Common, self).keyboardAndMouse(info)
            try:
                if info['key'] == 32: # reset rocks_rock_02's position if spacebar pressed
                    self.logger.debug('Reset rocks_rock_02s position')

                    for obj in bge.logic.getCurrentScene().objects:
                        if 'rocks_rock_02' in obj.name:
                            obj.worldPosition = obj['worldPosition']
                            self.logger.debug(obj.worldPosition, obj['worldPosition'])

                else:
                    self.logger.debug('###', info['key'])

            except (KeyError, SystemExit):
                pass
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

