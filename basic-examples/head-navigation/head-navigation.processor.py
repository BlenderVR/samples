import blendervr

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.BlenderVR.isMaster():
                self.BlenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

                from blendervr.interactor.head_controlled_navigation import HCNav

                self._navigator = HCNav(self, method=None, one_per_user=True)
                self._user = self.BlenderVR.getUserByName('user A')
                self._navigator.setDefaultUser(self._user)
                self.registerInteractor(self._navigator)
                self._navigator.setPositionFactors(1, 20.0, 1.0)

                from blendervr.interactor.viewpoint import ViewPoint

                self._viewpoint = ViewPoint(self)
                self._viewpoint.viewpointScale = 0.2
                self.registerInteractor(self._viewpoint)

        def keyboardAndMouse(self, info):
            """
            Function called by the processor during running-time everytime a key
            is pressed or a mouse event is triggered.
            """
            try:
                from blendervr.player import device

                if info['state'] == device.STATE_PRESS:
                    if info['key'] == ord('q'):
                        self.BlenderVR.quit("pressed 'q' key")

                    elif info['key'] == ord('v'):
                        self._viewpoint.activation(not self._viewpoint.isActivated())

                    # Head Navigation Setup
                    elif info['key'] == ord('1'):
                        self.logger.info("Calibrating Navigation")
                        self._navigator.update(self._navigator.CALIBRATE, self._user)

                    elif info['key'] == ord('2'):
                        self.logger.info("Start Navigation")
                        self._navigator.update(self._navigator.TOGGLE, self._user)

                    elif info['key'] == ord('3'):
                        self.logger.info("Reset Navigation")
                        self.reset()

                    elif info['key'] == ord('4'):
                        self.logger.info("Quitting")
                        self.BlenderVR.quit("Because user asked!")

            except (KeyError, SystemExit):
                pass

            except Exception as err:
                self.logger.log_traceback(err)

            super(Processor, self).keyboardAndMouse(info)

        def reset(self):
            """
            Reset all the user position and orientations.
            A new calibration will be required.
            """
            if not hasattr(self, '_navigator'):
                return

            self._navigator.update(self._navigator.RESET, self._user)
            self._user.resetVehiclePosition()

        def user_position(self, info):
            """
            Callback for one of the sensors of a tracker device.
            Defined in the XML config file.

            Callback defined in the XML config file to one of the VRPN tracker sensors
            """
            super(Processor, self).user_position(info)

            try:
                for user in info['users']:
                    if user == self._user:
                        self._navigator.setHeadLocation(user, info)

            except Exception as err:
                self.logger.log_traceback(err)



elif blendervr.is_creating_loader():
    import bpy

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, creator):
            super(Processor, self).__init__(creator)


elif blendervr.is_console():
    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, console):
            super(Processor, self).__init__(console)

            from blendervr.interactor.head_controlled_navigation import HCNav
            self._navigator = HCNav(self)
            self.registerInteractor(self._navigator)

        def useLoader(self):
            return True
