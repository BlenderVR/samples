import blendervr

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

                from blendervr.interactor.head_controlled_navigation import HCNav

                self._navigator = HCNav(self, method=None, one_per_user=True)
                self._navigator.setDefaultUser(
                                        self.blenderVR.getUserByName('user A'))
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

                if info['key'] == ord('q'):
                    self.blenderVR.quit("pressed 'q' key")

                elif (info['key'] == ord('v')
                        and info['state'] == device.STATE_PRESS):
                    self._viewpoint.activation(not self._viewpoint.isActivated())
                    return

            except (KeyError, SystemExit):
                pass

            except:
                self.logger.log_traceback(False)

            super(Processor, self).keyboardAndMouse(info)

        def user_position(self, info):
            """
            Callback for one of the sensors of a tracker device.
            Defined in the XML config file.

            Callback defined in the XML config file to one of the VRPN tracker sensors
            """

            super(Processor, self).user_position(info)
            for user in info['users']:
                self._navigator.setHeadLocation(user, info)


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

