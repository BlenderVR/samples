# Illustration of how to use BlenderVR OSC API

import blendervr
import os

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

        def start(self):
            """
            BlenderVR Callback, called at BlenderVR start.
            """
            self.logger.debug("## Start my Processor")
            if self.BlenderVR.isMaster():
                try:
                    # get access to BlenderVR OSC API
                    self.OSC = self.BlenderVR.getPlugin('osc')


                    try: # check if OSC client is available
                        osc_isAvailable = self.OSC.isAvailable()
                        self.logger.debug('OSC Client is available:', osc_isAvailable)
                    except AttributeError: # i.e. plugin self.OSC not instantiated
                        self.logger.warning('OSC plugin not/badly defined in configuration file -> OSC disabled')

                    else:

                        # Define global OSC parameters
                        self.OSC.getGlobal().start(True) # OSC msg: '/global start 1'
                        self.OSC.getGlobal().mute(False) # OSC msg: '/global mute 0'
                        self.OSC.getGlobal().volume('%40') # OSC msg: '/global volume %40'

                        # Print current blendervr users <-> osc users mapping
                        osc_users_dict = self.OSC.getUsersDict()
                        self.logger.debug('Current OSC mapping (OSC user ... is attached to BlenderVR user ...):')
                        for listener_name in osc_users_dict.keys():
                            osc_user = osc_users_dict[listener_name]
                            bvr_user = osc_user.getUser()
                            if bvr_user: self.logger.debug('-', osc_user.getName(), '<->', bvr_user.getName())
                            else:  self.logger.debug('-', osc_user.getName(), '<->', None)

                        # Define OSC users parameters
                        osc_user = self.OSC.getUser('Binaural 1')
                        osc_user.start(True) # OSC msg: '/user 1 start 1'
                        osc_user.mute(False) # OSC msg: '/user 1 mute 0'
                        osc_user.volume('%80') # OSC msg: '/user 1 volume %80'
                        # or equivalently, see .xml configuration
                        bvr_user = self.BlenderVR.getUserByName('user A')
                        osc_user = self.OSC.getUser(bvr_user)

                        # Define OSC objects parameters
                        scene = bge.logic.getCurrentScene()
                        kx_object = scene.objects['Cube']
                        osc_object = self.OSC.getObject(kx_object)
                        # because of the previous line, the kx_object 4x4 orientation matrix will
                        # 1) be sent to the OSC client
                        # 2) be updated each time the kx_object moved
                        osc_object.sound('HeyPachuco.wav') # OSC msg: '/object 1 sound HeyPachuco.wav'
                        osc_object.loop(True) # OSC msg: '/object 1 loop 1'
                        osc_object.mute(False) # OSC msg: '/object 1 mute 0'
                        osc_object.volume('%45') # OSC msg: '/object 1 volume %45'
                        osc_object.start(True) # OSC msg: '/object 1 start 1'


                        # Route OSC object sound channel to OSC user (for selective listening)
                        osc_objectUser = self.OSC.getObjectUser(osc_object, osc_user)
                        osc_objectUser.mute(False) # OSC msg: '/objectUser 1 0 mute 0'
                        osc_objectUser.volume('%50') # OSC msg: '/objectUser 1 0 volume %50'


                except:
                    # this try/except using self.logger.log_traceback(False) is the best way
                    # to trace back errors happening on console/master/slaves in BlenderVR.
                    # Without it, some errors won't be printed out in either windows (console's nor master's nor slave's).
                    self.logger.log_traceback(False)

        def run (self):
            """
            BlenderVR Callback, called every frame.
            """
            # self.logger.debug('######## RUN')
            return

        def quit(self):
            """
            BlenderVR Callback, called at run stop.
            """
            if self.BlenderVR.isMaster():
                try:
                    ## it seems that reset flag is updated but
                    ## that the associated callback (run) is killed before
                    ## it can actually update anything
                    # self.OSC.getGlobal().reset()

                    # this works :)
                    self.OSC.reset() # sends "/global reset" OSC msg
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
            global try_wait_user_name, try_chooser, try_console_arc_balls
            super(Processor, self).__init__(console)

        def useLoader(self):
            return True
