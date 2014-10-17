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

blendervr.processor.appendProcessor(os.path.join(blendervr.tools.getModulePath(), 'processors.py'))

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent, head_navigator = True, laser = 'ray')

            if hasattr(self, '_navigator'):
                self._navigator.setPositionFactors(0, 0.25, 1.0)
                self._navigator.setPositionFactors(1, 10.0, 1.0)
                self._navigator.setPositionFactors(2, 0.25, 1.0)

            self._scene = bge.logic.getCurrentScene()
            #self.logger.debug('objets : ', self._scene.objects)

            # Don't move the floor and the edges ...
            self._laser.allowDisallowObjects(True) 
            self._laser.allowDisallowObjects(False, self._scene.objects['Ground'])
            self._laser.allowDisallowObjects(False, self._scene.objects['Edges'].children)

            self._user = self.blenderVR.getUserByName('user A')

            try:
                god = self.blenderVR.getUserByName('god')
                if god is not None:
                    god.setParent(self._scene.objects['Horse'])
                    self._viewpoint.viewpointScale = 0.01
            except:
                pass

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)

                from blendervr.interactor import reset_objects
                self._reset_objects = reset_objects.ResetObjects(self)
                self._reset_objects.save()

                self._sound_objects = {}

        def start(self):
            if self.blenderVR.isMaster():
                try:
                    self._OSC = self.blenderVR.getPlugin('osc')
                    self._OSC.getGlobal().start(True)

                    ambisonic_user = self._OSC.getUser('Ambisonic')
                    A_sound_user   = self._OSC.getUser(self._user)

                    osc_objects = [{'name'  : 'Cube',
                                    'sound' : 'TF_kick.wav',
                                    'mute'  : False},
                                   {'name'  : 'Link.013',
                                    'sound' : 'TF_ride.wav',
                                    'mute'  : False},
                                   {'name'  : 'Link.014',
                                    'sound' : 'TF_snare.wav',
                                    'mute'  : False},
                                   {'name'  : 'Sphere.003',
                                    'sound' : 'TF_piano.wav',
                                    'mute'  : False},
                                   {'name'  : 'Ball',
                                    'sound' : 'TF_saxophone.wav',
                                    'mute'  : False}]

                    for osc_object_def in osc_objects:
                        blender_object = self._scene.objects[osc_object_def['name']]
                        osc_object     = self._OSC.getObject(blender_object)
                        osc_object.sound(osc_object_def['sound'])
                        osc_object.loop(True)

                        self._sound_objects[id(blender_object)] = {'object' : osc_object,
                                                             'volume' : 2,
                                                             'mute'   :  False}

                        self._OSC.getObjectUser(osc_object, ambisonic_user)
                        self._OSC.getObjectUser(osc_object, A_sound_user)

                    self.reset_sound()
                    self.reset_volume()
                except:
                    self.logger.info('No OSC available.')

        def process_hcnav(self, matrix):
            self.logger.debug(matrix)

        def reset(self, users = None):
            super(Processor, self).reset(users)
            self._reset_objects.reset()

        def buttons(self, info):
            if info['button'] == 0:
                if info['state'] == 1:
                    self._laser.toggle()
            if (info['button'] == 1) and (info['state'] == 1):
                obj = self._laser.getHitObject()
                if (obj is not None) and (id(obj) in self._sound_objects):
                    obj = self._sound_objects[id(obj)]
                    obj['mute'] = (obj['mute'] == False)
                    self.send_volume()

        def movements(self, info):
            if info['channel'][1] != 0:
                obj = self._laser.getHitObject()
                if (obj is not None) and (id(obj) in self._sound_objects):
                    obj = self._sound_objects[id(obj)]
                    if info['channel'][1] > 0:
                        obj['volume'] = obj['volume'] - 1
                    else:
                        obj['volume'] = obj['volume'] + 1
                    if obj['volume'] > 100:
                        obj['volume'] = 100
                    if obj['volume'] < 0:
                        obj['volume'] = 0
                    self.send_volume()

        def keyboardAndMouse(self, info):
            try:
                if (info['key'] == ord('p')) and (info['state'] == 1):
                    for id, obj in self._sound_objects.items():
                        obj['mute'] = (obj['mute'] == False)
                    self.send_volume()
                    return
                if (info['key'] == ord('r')) and (info['state'] == 1):
                    self.reset()
                    return
            except KeyError:
                pass 
            super(Processor, self).keyboardAndMouse(info)
           

        def send_volume(self):
            for id, obj in self._sound_objects.items():
                if obj['mute']:
                    obj['object'].volume('%0')
                else:
                    obj['object'].volume('%'+str(obj['volume']))

        def reset_volume(self):
            for id, obj in self._sound_objects.items():
                obj['volume'] = 2
            self.send_volume()

        def reset_sound(self):
            for id, obj in self._sound_objects.items():
                obj['object'].start(False)
            for id, obj in self._sound_objects.items():
                obj['object'].start(True)

else: # not VR screen => Console

    from PyQt4 import QtCore, QtGui, uic
    
    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, console):
            super(Processor, self).__init__(console, ('chess', 'designer', 'chess.ui'), head_navigator=True)

            if hasattr(self, '_navigator'):
                self._navigator.registerWidget(self._ui.HC_Nav)

        def useLoader(self):
            return True
