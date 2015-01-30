## Copyright (C) LIMSI-CNRS (2014)
##
## contributor(s) : Jorge Gascon, Damien Touraine, David Poirier-Quinot,
## Laurent Pointal, Julian Adenauer,
##
## This software is a computer program whose purpose is to distribute
## blender to render on Virtual Reality device systems.
##
## This software is governed by the CeCILL  license under French law and
## abiding by the rules of distribution of free software.  You can  use,
## modify and/ or redistribute the software under the terms of the CeCILL
## license as circulated by CEA, CNRS and INRIA at the following URL
## "http://www.cecill.info".
##
## As a counterpart to the access to the source code and  rights to copy,
## modify and redistribute granted by the license, users are provided only
## with a limited warranty  and the software's author,  the holder of the
## economic rights,  and the successive licensors  have only  limited
## liability.
##
## In this respect, the user's attention is drawn to the risks associated
## with loading,  using,  modifying and/or developing or reproducing the
## software by the user in light of its specific status of free software,
## that may mean  that it is complicated to manipulate,  and  that  also
## therefore means  that it is reserved for developers  and  experienced
## professionals having in-depth computer knowledge. Users are therefore
## encouraged to load and test the software's suitability as regards their
## requirements in conditions enabling the security of their systems and/or
## data to be ensured and,  more generally, to use and operate it in the
## same conditions as regards security.
##
## The fact that you are presently reading this means that you have had
## knowledge of the CeCILL license and that you accept its terms.
##

import blendervr
import os

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
            super(Processor, self).__init__(parent, head_navigator = True, use_viewpoint = try_viewpoint)

            random.seed()

            if try_use_stream_between_master_and_slave:
                self.blenderVR.addObjectToSynchronize(self, 'main processor')

            if hasattr(self, '_navigator'):
                self._navigator.setPositionFactors(1, 20.0, 1.0)

            self._user = self.blenderVR.getUserByName('user A')

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            if try_wait_user_name:
                self.blenderVR.pause('Waiting for the user name')

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
# Worth reimplementing the feature "sphere visible" to new blenderVR?

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
                self.blenderVR.quit("because user asked !")

        def receivedFromConsole(self, command, argument):
            global try_wait_user_name
            if command == 'user name':
                if try_wait_user_name:
                    self.logger.debug('user name: ', argument)
                    self.blenderVR.pause()
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
