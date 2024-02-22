import json
import logging
import time

from audio.Audio import Audio
from data.Datasend import Datasend
from data.Dataverify import Dataverify
from display.Display import Display
from timemeasure.Timeconsumption import Timeconsumption
from energy.Energyconsumption import Energyconsumption


class main:

    def __init__(self):

        logging.basicConfig(encoding='utf-8', level=logging.INFO)
        logging.info("main init")
        self.__config = json.load(open('config.json'))
        self.__datasend = Datasend(str(self.__config['Data']['WebURL']))
        self.__dataverify = Dataverify(str(self.__config['Data']['PRENURL']), str(self.__config['Data']['PRENTEAM']))
        self.__display = Display()
        self.__display.clearDisplay()
        self.__timemeasure = Timeconsumption()
        self.__audio = Audio(str(self.__config['Machineconfig']['Audiofile']))
        self.__energy = Energyconsumption(str(self.__config['Data']['SHELLYURL']), str(self.__config['Data']['SHELLYDEVID']), str(self.__config['Data']['SHELLYAUTHKEY']))

    def initialization(self):
        logging.info("main initialization")
        self.__display.drawInitialDisplay()
        self.__display.updateDisplay(10, 30, 'Initialisierung')

        # Check Web Connection
        if (str(self.__config['Machineconfig']['WebConnection'])) == True:
            logging.info('WebConnection True')
            if self.__dataverify.checkavailability():
                self.__display.updateDisplay(10, 30, 'Conn. PREN-Server OK')
            else:
                self.__display.updateDisplay(10, 30, 'Conn. PREN-Server NOK')
                exit()
        else:
            logging.info('WebConnection False')
            self.__display.updateDisplay(10, 30, 'No internet connection')

        # Check Shelly Connection
        if (str(self.__config['Machineconfig']['ShellyConnection'])) == True:
            logging.info('ShellyConnection True')
            if self.__energy.checkavailability():
                self.__display.updateDisplay(10, 30, 'Conn. Shelly OK')
            else:
                self.__display.updateDisplay(10, 30, 'Conn. Shelly NOK')
                exit()
        else:
            logging.info('ShellyConnection False')
            self.__display.updateDisplay(10, 30, 'No Shelly connection')

    def start(self):
        logging.info("main start")
        self.__display.updateDisplay(10, 30, 'Programm läuft')
        self.__timemeasure.setstarttime()
        if (str(self.__config['Machineconfig']['ShellyConnection'])) == True:
            self.__energy.setinitialpower()

    def end(self):
        self.__timemeasure.setendtime()
        if (str(self.__config['Machineconfig']['ShellyConnection'])) == True:
            self.__energy.setendpower()
        logging.info("main end")

        # self.__display.updateDisplay(10, 10, 'PREN TEAM 33')
        self.__display.updateDisplay(10, 30, 'Programm beendet')
        # self.__display.updateDisplay(10, 80, 'Beanspruchte Zeit')
        self.__display.updateDisplay(10, 100, str(self.__timemeasure.getelapsedtime()) + ' Sekunden')
        # self.__display.updateDisplay(10, 150, 'Stromverbrauch')
        if (str(self.__config['Machineconfig']['ShellyConnection'])) == True:
            self.__display.updateDisplay(10, 170, self.__energy.getconsumtpion() + ' Wh')
        else:
            self.__display.updateDisplay(10, 170, 'No Shelly connection')
        self.__audio.playaudio()

        time.sleep(int(self.__config['Machineconfig']['DisplaySleepTimeSeconds']))

        if (str(self.__config['Machineconfig']['DrawQR'])) == True:
            self.__display.drawPicture(self.__config['Machineconfig']['DrawQRFile'])

        time.sleep(int(self.__config['Machineconfig']['DisplaySleepTimeSeconds']))

        if (str(self.__config['Machineconfig']['SendData'])) and (str(self.__config['Machineconfig']['WebConnection'])):
            self.__datasend.send(self.__timemeasure.getelapsedtime(), 0.5)

        self.__display.clearDisplay()
        self.__display.shutdownDisplay()


if __name__ == "__main__":
    try:
        mn = main()
        mn.initialization()
        mn.start()
        time.sleep(5)
        mn.end()
    except KeyboardInterrupt:
        logging.warning("ctrl + c:")
