# Following the //samples/basic/basic.processor.py, this processor file illustrates some
# usage of the general BlenderVR API.

import blendervr
import os

# This line 'imports' the processor.py in //blender-vr/samples/, used in the superconstructor
# of herein defined Processor class. You're invited to adapt said processor.py to your own needs
# to factorize BlenderVR scenes. A processor method that you want to use in several of your scene
# can be defined in //blender-vr/samples/processor.py to be called at will in your
# blenderSceneName.processor.py scripts.
blendervr.processor.appendProcessor(os.path.join(blendervr.tools.getRootPath(), 'samples', 'processors.py'))

try_wait_user_name = False
try_chooser = True
try_console_arc_balls = False
try_landmarks = True
try_viewpoint = True
try_use_stream_between_master_and_slave = False

if blendervr.is_virtual_environment():
    import bge
    import math
    import copy
    import random
    from blendervr.player import device

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            # see //blender-vr/samples/processor.py to understand these arguments
            super(Processor, self).__init__(parent, head_navigator = True, use_viewpoint = try_viewpoint)

            random.seed()

            if try_use_stream_between_master_and_slave:
                self.BlenderVR.addObjectToSynchronize(self, 'main processor')

            if hasattr(self, '_navigator'):
                self._navigator.setPositionFactors(1, 20.0, 1.0)

            self._user = self.BlenderVR.getUserByName('user A')

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            if try_wait_user_name:
                self.BlenderVR.pause('Waiting for the user name')

            if try_chooser:
                from blendervr.interactor.object_chooser import Chooser
                self._chooser = Chooser(self)
                self.registerInteractor(self._chooser)

            if try_console_arc_balls:
                from blendervr.interactor.arc_ball import console
                self._console_arc_ball = console.Console(self)
                self.registerInteractor(self._console_arc_ball)
                self._console_arc_ball.selectObject(self._user)

            if try_landmarks:
                from blendervr.interactor import landmarks
                self._landmarks = landmarks.LandMarks(self)
                self.registerInteractor(self._landmarks)

# Commented this section as the pre_render method no longer exists in the
# blender API, replaced by pre_draw only.
# Worth reimplementing the feature "sphere visible" to new BlenderVR?

            # self._scene = bge.logic.getCurrentScene()
            # self._scene.pre_render.append(self._pre_render)
            # self._scene.pre_draw.append(self._pre_draw)
            # self._render_count = 0

        # def _pre_render(self):
        #     self._render_count = 0
        #     self._test()

        # def _pre_draw(self):
        #     self._render_count = 1
        #     self._test()

        # def _test(self):
        #     if self._render_count == 2 :
        #         self._scene.objects['Sphere.Y'].visible = False
        #     else:
        #         self._scene.objects['Sphere.Y'].visible = True

        def buttons(self, info):
            try:
                if (info['button'] == 0) and (info['state'] == 1):
                    self._navigator.update(self._navigator.CALIBRATE, self._user)
                if (info['button'] == 1) and (info['state'] == 1):
                    self._navigator.update(self._navigator.TOGGLE, self._user)
            except:
                pass
            if (info['button'] == 2) and (info['state'] == 1):
                self.reset(info['users'])
            if (info['button'] == 3) and (info['state'] == 1):
                self.BlenderVR.quit("because user asked !")

        def receivedFromConsole(self, command, argument):
            global try_wait_user_name
            if command == 'user name':
                if try_wait_user_name:
                    self.logger.debug('user name: ', argument)
                    self.BlenderVR.pause()
                    self.sendToConsole('reply user name')
            else:
                super(Processor, self).receivedFromConsole(command, argument)

        def getSynchronizerBuffer(self):
            buffer = blendervr.player.buffer.Buffer()
            value = random.randrange(268431360)
            self.logger.debug('Sending', value, 'to the slaves')
            buffer.integer(value)
            return buffer

        def processSynchronizerBuffer(self, buffer):
            value = buffer.integer()
            self.logger.debug('Receiving ', value, ' from the master')

        def keyboardAndMouse(self, info):
            try:
                if info['key'] == ord('s') and info['state'] == device.STATE_PRESS:
                    value = random.randrange(268431360)
                    self.logger.debug('Sending', value, 'to the slaves')
                    self.sendToSlaves('random value', value)
            except (KeyError, SystemExit):
                pass
            except:
                self.logger.log_traceback(False)
            super(Processor, self).keyboardAndMouse(info)

        def receivedFromMaster(self, command, argument):
            if command == 'random value':
                self.logger.debug('Receiving ', argument, ' from the master')
                return
            super(Processor, self).receivedFromMaster(command, argument)

elif blendervr.is_creating_loader():

    import bpy

    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, creator):
            super(Processor, self).__init__(creator)

elif blendervr.is_console():

    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, console):
            global try_wait_user_name, try_chooser, try_console_arc_balls
            ui_path = os.path.join(blendervr.tools.getModulePath(), 'designer', 'simple.ui')
            super(Processor, self).__init__(console, ui_path, head_navigator = True)

            if hasattr(self, '_navigator'):
                self._navigator.registerWidget(self._ui.HC_nav)

            if try_wait_user_name:
                self._ui.set_user_name.clicked.connect(self.cb_set_user_name)

            if try_chooser:
                from blendervr.interactor.object_chooser import Chooser
                self._chooser = Chooser(self)
                self.registerInteractor(self._chooser)

            if try_console_arc_balls:
                from blendervr.interactor.arc_ball import console
                self._console_arc_ball = console.Console(self)
                self.registerInteractor(self._console_arc_ball)
                self._console_arc_ball.registerWidget(self._ui.ArcBall)

            if try_landmarks:
                from blendervr.interactor import landmarks
                self._landmarks = landmarks.LandMarks(self)
                self.registerInteractor(self._landmarks)
                self._landmarks.registerWidget(self._ui.ArcBall)

        def start(self):
            self._ui.user_name.setEnabled(True)
            super(Processor, self).start()

        def quit(self):
            self._window.close()
            super(Processor, self).quit()

        def cb_set_user_name(self):
            user_name = self._ui.user_name.text()
            if user_name:
                self.sendToVirtualEnvironment('user name', user_name)
                self._ui.user_name.setEnabled(False)

        def receivedFromVirtualEnvironment(self, command, argument):
            if command == 'reply user name':
                self.getConsole().logger.debug('Received a reply for user name set !')
                return
            super(Processor, self).receivedFromVirtualEnvironment(command, argument)

        def useLoader(self):
            return True
