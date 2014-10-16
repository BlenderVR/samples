import bge
import os

timer      = 0
frameRates = []

def run():
    global timer, frameRates

    frameRates.append(round(bge.logic.getAverageFrameRate(),2))

    timer += 1
    if timer >= 500:

        file_name = 'results'
        if hasattr(bge.logic, 'blenderVR'):
            if not bge.logic.blenderVR.isMaster():
                return
            if hasattr(bge.logic, 'filename_postfix'):
                file_name += '_' + bge.logic.filename_postfix
            else:
                import random
                file_name += '_' + str(random.randrange(268431360))

        fileName = os.path.join(bge.logic.expandPath('//'), 'records', file_name)
        if hasattr(bge.logic, 'blenderVR'):
            bge.logic.blenderVR.logger.debug('File name:', fileName)
        File = open(fileName, 'w')
        File.write(str(frameRates))
        File.close()

        if hasattr(bge.logic, 'blenderVR'):
            bge.logic.blenderVR.quit('end of bench !')
        else:
            bge.logic.endGame()

