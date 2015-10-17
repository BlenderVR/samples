"""
Test scene for Head Mounted Display (HDM) devices
=================================================

Objective
---------
This scene illustrates how to use BlenderVR API to 'parent' Blender objects (e.g. Cube, Suzanne, etc.)
to BlenderVR objects (e.g. user or vehicle).

Controls
--------
WASDRF:             move BlenderVR Vehicle (user viewpoint is attached to vehicle)
LeftCtrl + WASDRF:  move Blender camera (vehicle is attached to camera)
LeftShift + WASDRF: double navigation speed
Spacebar:           throw object forward (rel. to user / vehicle / camera orientation)

Notes
-----
- Moving vehicle or camera (Ctrl key pressed or not) seems one and the same, until more than one user
interacts with the scene (note: this scene is not implemented for 2 or more users yet). In these scenarios,
one will want to move users' vehicle in the scene for navigation rather than camera, as the camera will
impact both user's point of view while vehicle is user specific. Furthermore, in that scene, camera motion
is not applied relative to user's head (yours) orientation (forward is then a global forward).
"""

import blendervr

if blendervr.is_virtual_environment():
    import bge
    from mathutils import Matrix, Quaternion, Vector
    from math import radians

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self._user = self.BlenderVR.getUserByName('user A')
            self._scene = bge.logic.getCurrentScene()

            self._camera = self._scene.active_camera

            # Blender objects used to visualize/represent BlenderVR objects
            self._kx_vehicle = self._scene.objects['Vehicle']
            self._kx_user = self._scene.objects['User']
            self._kx_userSpot = self._scene.objects['UserSpot']

        def run(self):
            ## Parent kx objects to BlenderVR Vehicle and User

            # to avoid using cam.worldTransform, proved bugy
            mat_cam = self._camera.worldOrientation.to_4x4()
            mat_cam.translation = self._camera.worldPosition

            # get vehicle transform matrix (BEWARE, self._user.getVehiclePosition() doesn't return a transform matrix as
            # defined in Blender but rather its inverse (not vehicle to world but world to vehicle)
            vehicle_transform_matrix = mat_cam * self._user.getVehiclePosition().inverted()

            ## Apply BlenderVR vehicle and user transforms to their Blender counterparts/visual representations.

            # apply pre-rotation on vehicle orientation prior to be aplied to Blender vehicle and user,
            # as each KX GameObject has it's own (subjective) way of 'facing forward'
            mat_rot_from_cam_2_monkey = Matrix.Rotation(radians(-90.0), 4, 'X') * Matrix.Rotation(radians(180.0), 4, 'Z')
            # offset applied only to orientation...
            kx_vehicle_worldTransform = (vehicle_transform_matrix * mat_rot_from_cam_2_monkey).to_3x3().to_4x4()
            # ... so keep original object's translation
            kx_vehicle_worldTransform.translation = vehicle_transform_matrix.translation
            # and apply final transform to 'kx_vehicle object' (Blender vehicle)
            self._kx_vehicle.worldTransform = kx_vehicle_worldTransform

            # Do the exact same for kx_user (mirroring BlenderVR user)
            user_transform_matrix = vehicle_transform_matrix * self._user.getPosition().inverted()
            kx_user_worldTransform = (user_transform_matrix * mat_rot_from_cam_2_monkey).to_3x3().to_4x4()
            kx_user_worldTransform.translation = user_transform_matrix.translation
            self._kx_user.worldTransform = kx_user_worldTransform

        def user_position(self, info):
            """
            useless for now (it does not add anything compared to the default user_position callback)
            """
            super(Processor, self).user_position(info)

        def keyboardAndMouse(self, info):
            """
            Move vehicle with keyboard WASDRF (translation) and mouse (Z rotation)
            """
            sensitivity_translation = 0.02
            relativeTranslation = True # translation relative to hmd orientation
            sensitivity_rotation = 0.002
            keys_mapping = {
            'fwd':   'w',
            'bwd':   's',
            'left':  'a',
            'right': 'd',
            'up':    'r',
            'down':  'f',
            }

            try:
                super(Processor, self).keyboardAndMouse(info)

                # (shift to "run"): remember shift key state (as only one key is stored in "info"
                # for each iteration of the keyboardAndMouse method) to apply it when fwd, bwd, etc.
                # keys are pressed
                if not hasattr(bge.logic, 'shiftKeyPressed'):
                    bge.logic.shiftKeyPressed = False
                    bge.logic.ctrlKeyPressed = False

                # Keyboard Control (Vehicle Translation)
                try:

                    # double speed (run) instruction
                    if (info['key'] == bge.events.LEFTSHIFTKEY):
                        bge.logic.shiftKeyPressed = (info['state'] == 1 or info['state'] == 2)

                    # disable vehicle control: keyboard and mouse will then control Blender camera
                    # (see logic bricks / python scripts embedded in .blend)
                    if (info['key'] == bge.events.LEFTCTRLKEY):
                        bge.logic.ctrlKeyPressed = (info['state'] == 1 or info['state'] == 2)

                    keyPressed = (info['state'] == 1 or info['state'] == 2)
                    if keyPressed:

                        # Translation
                        vec_translation = [0.0,0.0,0.0]

                        if bge.logic.shiftKeyPressed: sensitivity_translation *= 2 # run
                        if (info['key'] == ord(keys_mapping['fwd'])):   vec_translation[1] =  sensitivity_translation
                        if (info['key'] == ord(keys_mapping['bwd'])):   vec_translation[1] = -sensitivity_translation
                        if (info['key'] == ord(keys_mapping['left'])):  vec_translation[0] =  sensitivity_translation
                        if (info['key'] == ord(keys_mapping['right'])): vec_translation[0] = -sensitivity_translation
                        if (info['key'] == ord(keys_mapping['up'])):    vec_translation[2] = -sensitivity_translation
                        if (info['key'] == ord(keys_mapping['down'])):  vec_translation[2] =  sensitivity_translation

                        mat_translation = Matrix.Translation((vec_translation[0], vec_translation[2], vec_translation[1]))

                        # vehicle translation relative to user head orientation
                        if relativeTranslation:
                            userRot_Y = Matrix.Rotation(self._user.getPosition().to_euler().y,4,'Y')
                            rel_trans = userRot_Y.inverted() * mat_translation
                            loc, rot, scale = rel_trans.decompose()
                            mat_translation = Matrix.Translation(loc)

                        if not bge.logic.ctrlKeyPressed:
                            # apply translation
                            new_ori = mat_translation * self._user.getVehiclePosition()
                            self._user.setVehiclePosition(new_ori)

                        # # Debug
                        # if keyPressed:
                        #     self.logger.debug('vehicle \n', self._user.getVehiclePosition())
                        #     self.logger.debug('user', self._user.getPosition())
                        #     obj = self._scene.objects['Monkey']
                        #     self.logger.debug('monkey \n', obj.worldTransform)
                        #     self.logger.debug('---')

                except KeyError:
                    pass

                # Mouse Control (Vehicle Z Orientation (Z becomes Y in openGL coordinates))
                try:
                    # get new mouse position
                    (x,y)= info['mouse position']

                    # reset mouse position at screen's center
                    window_center = (int(bge.render.getWindowWidth()/2), int(bge.render.getWindowHeight()/2))
                    bge.render.setMousePosition(window_center[0],window_center[1])


                    delta = [0.0, 0.0]
                    # init view (delta to 0.0)
                    if not hasattr(bge.logic,'mouseVehicleViewInit'):
                        # avoid first run during processor init (where setMousePosition is not properly applied)
                        if x != 0 and y != 0:
                            bge.logic.mouseVehicleViewInit = True
                    else:
                        # get relative rotation based on small mouse movement
                        delta[0] = x - window_center[0]
                        delta[1] = y - window_center[1]

                    if not bge.logic.ctrlKeyPressed:
                        # apply rotation
                        mat_rotation = Matrix.Rotation(sensitivity_rotation * delta[0], 4, 'Y')
                        # mat_rotation *= Matrix.Rotation(sensitivity_rotation * delta[1], 4, 'X')
                        new_ori = mat_rotation * self._user.getVehiclePosition()
                        self._user.setVehiclePosition(new_ori)

                except KeyError:
                    pass

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
