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

if blendervr.is_virtual_environment():

    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent)
            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

            self.blenderVR.pause('Waiting setting result file postfix')

        def receivedFromConsole(self, command, argument):
            if command == 'filename postfix':
                self.logger.info('filename postfix:', argument)
                self.blenderVR.pause()
                bge.logic.filename_postfix = argument
                return
            super(Processor, self).receivedFromConsole(command, argument)

elif blendervr.is_console():

    import os
    from blendervr.tools.gui.qt import QtGui

    class Common(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Common, self).__init__(parent)

            self._window = QtGui.QDialog()
            self._ui = blendervr.tools.gui.load(os.path.join(blendervr.tools.getModulePath(), 'designer', 'scene.ui'), self._window)

            self._ui.set_result_filename_postfix.clicked.connect(self.cb_set_result_filename_postfix)

        def start(self):
            self._window.show()
            self._ui.user_name.setEnabled(True)
            super(Common, self).start()

        def stop(self):
            self._window.hide()
            super(Common, self).stop()

        def quit(self):
            self._window.close()
            super(Common, self).quit()


        def cb_set_result_filename_postfix(self):
            user_name = self._ui.user_name.text()
            if user_name:
                self.sendToVirtualEnvironment('filename postfix', user_name)
                self._ui.user_name.setEnabled(False)

        def useLoader(self):
            return True
