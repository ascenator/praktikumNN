#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
""" bla bla bla"""   #TODO: Write summary about this file!

__author__ = "Daniel Speck, Florian Kock"
__copyright__ = "Copyright 2014, Praktikum Neuronale Netze"
__license__ = "GPLv3"
__version__ = "1.0.0"
__maintainer__ = "Daniel Speck, Florian Kock"
__email__ = "2speck@informatik.uni-hamburg.de, 2kock@informatik.uni-hamburg.de"
__status__ = "Development"

import logging
from NeuralNetwork import NeuralNetwork
import numpy
import os.path
from concol import ConCol

class knnframe:
    def __init__(self, loadConfig, name):
        """
        :param loadConfig:
        :param name:
        :return:
        """

        # Logging
        path = 'log_player_' + str(name) + '.log' # logging file path

        # check if logfile exists

        self.file = open(path, "w+")


        # logging stuff
        #logging.basicConfig(filename=path, level=logging.debug)

        self.name = str(name)
        self.timesteps = 20.0
        self.hitratio = 0.5
        self.fakediff = 0.0
        self.newfakediff()
        self.knn = NeuralNetwork([2,5,1],8)
        self.reward_count = 0
        self.printcount = 10

    def saveconfig(self,filename):
        #no Return
        #self.knn.save(filename) #TODO correct this!
        print('Configuration saved: ' + filename)
        
    def predict(self,xpos,ypos,mypos):
        #return action  (up:      u
                      #  down:    d
                      #  nothing: n

        pred = self.knn.predict([[xpos,ypos]])
        #print( bcolors.FAIL + 'Player ' + self.name + ' predicted: ' + str(pred[0][0]) + ' with sourcedata: ' + str([xpos,ypos]) + bcolors.ENDC)
        #logging.debug('predicting...')
        #logging.debug(self.knn.debug())


        return float(pred[0][0])

        self.fakediff = 0.0 #TODO seems not to work like this... damn!
        diff = mypos - pred[0][0]



        #print( bcolors.HEADER + 'Player ' + self.name + ' diff: ' + str(diff) + bcolors.ENDC)

        if diff > 0.1:
            #print('Player ' + self.name +': up!')
            return 'd'
        elif diff < -0.1:
            #print('Player ' + self.name +': down!')
            return 'u'
        #print('hold position!')
        return 'n'

    def reward_pos(self,err):
        self.rew_diag()
        self.knn.reward(err)
        #self.knn.reward(self.fakediff)
        #print('\a') #Bell
        # Verhaeltnis von Treffern vom Schläger zu Out's: 0..1
        self.hitratio += 1.0/self.timesteps
        if self.hitratio > 1.0:
            self.hitratio = 1.0

        if self.reward_count % self.printcount == 0:
            print( ConCol.OKGREEN + 'Player ' + self.name + ': got positive reward! Hitratio is now: ' + str(self.hitratio) + ConCol.ENDC )
        self.newfakediff()

    def reward_neg(self,err):
        self.rew_diag()
        if self.reward_count % self.printcount == 0:
            print('Player ' + self.name + ': error is: ' + str(err))
        self.knn.reward(err)
        # Verhaeltnis von Treffern vom Schläger zu Out's: 0..1
        self.hitratio -= 1.0/self.timesteps
        if self.hitratio < 0.0:
            self.hitratio = 0.0

        if self.reward_count % self.printcount == 0:
            print( ConCol.OKBLUE + 'Player ' + self.name + ': got negative reward! Hitratio is now: ' + str(self.hitratio) + ConCol.ENDC)
        self.newfakediff()

    def newfakediff(self):
        self.fakediff = numpy.random.normal(0.0,1.0/3.0)*(1.0-self.hitratio)
        # Gauss Normalverteilung von etwa -1 - +1 bei  self.hitratio = 0
        #print('Player ' + self.name + ': fakediff is now: ' + str(self.fakediff))

    def rew_diag(self):
        self.reward_count += 1
        print('Rewards: ', self.reward_count)
        print('Hitratio: ', self.hitratio)
        if self.reward_count == 20:
            #print('20')
            self.file.write('hitratio@20: ' + str(self.hitratio) + '\n')
        elif self.reward_count == 50:
            #print('50')
            self.file.write('hitratio@50: ' + str(self.hitratio)+ '\n')
        elif self.reward_count == 75:
            #print('75')
            self.file.write('hitratio@75: ' + str(self.hitratio)+ '\n')
        elif self.reward_count == 100:
            #print('150')
            self.file.write('hitratio@100: ' + str(self.hitratio)+ '\n')
        elif self.reward_count == 150:
            #print('150')
            self.file.write('hitratio@150: ' + str(self.hitratio)+ '\n')


