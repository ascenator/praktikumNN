#!/usr/bin/env python3.4

import numpy as n

n.set_printoptions(precision=10)

def _tanh(x):  
    return n.tanh(x)

def _tanh_deriv(x):  
    return 1.0 - x**2


class NeuralNetwork:
    def __init__(self, layer):  
        """  
        :param layer: A list containing the number of units in each layer.
        Should be at least two values  
        """  
        
        self.W = []
        self.B = []
        for i in range(1, len(layer)):
            self.W.append(n.random.random((layer[i],layer[i - 1]))) #erzeuge layer[i - 1] Gewichte für jedes layer für jedes Neuron
            self.B.append(n.random.random((layer[i]))) #erzeuge 1 Bias für jedes Neuron
            
        #print('W ist: ' + str(self.W))
        #print('B ist: ' + str(self.B))
        
        print('')
        print('============================================================================')
        print('')

    def guess(self, s_in):
        """Feedforward Activation of the MLP.

        Keyword arguments:
        s_in -- input value, should be a list of values, quantity like the input layer!
        """
        
        a = n.atleast_2d(s_in)
        #print('a ist: ' + str(a))
        
        for l in range(0, len(self.W)): #für alle Layer...
            #print('self.W[l] ist ' + str(self.W[l]))
            a = _tanh(n.dot(a, n.transpose(self.W[l])) ) # + self.B[l]) #multipliziere die Arraygewichte...
            # Achtung: a ist ein [[ x y z]] und self.B[l] ist ein [] array! Funktioniert trotzdem!
            #print('a ist: ' + str(a))
            #print('self.B[l] ist: ' + str(self.B[l]))
              
            #print('a ist: ' + str(a))
        return a


    def teach(self, s_in, s_teach, epsilon=0.2, repeats=10000):
        """Learning function for the MLP.
        
        Keyword arguments:
        s_in -- input value, should be a array of arrays of values. Quantity like the input layer! Order!
        s_teach -- result value, should be a array of arrays of values. Quantity like the output layer! Order!
        epsilon -- Factor for learning rate (default 0.2)
        epochs -- number of repeated learning steps (default 1000)
        """
        
        s_teach = n.atleast_2d(s_teach)      # -> faster!
        
        
        
        for k in range(repeats):
            i = n.random.randint(s_in.shape[0])
            a = n.atleast_2d(s_in[i])
            R = n.array([])
            
            Activation = []
            Activation.append(a)
            Output = []
            Output.append(a)
            
            for l in range(0, len(self.W)): #für alle Layer...
                #zum merken der net-Werte
                int_a=n.dot(a, n.transpose(self.W[l]))  # + self.B[l] erstmal ohne bias
                Activation.append(int_a)
                a = _tanh(int_a) 
                Output.append(a)
            
            print('Activations:')
            print(Activation)
            
            #
            #Backpropagation:
            
            delta_lambda = _tanh_deriv(int_a) * (s_teach[i] - a[-1])    #Erzeugt delta_Lamda zum ersten mal: interner Wert von den Ausgabeneuronen ohne 
            
            print('Gewichte vor lernen:')
            print(self.W)
            
            for l in range(len(self.W)-1, -1, -1): #für alle Layer...
                print('+++++++++++++++++++++++++')
                print('Passe Layer an: ' + str(l))
                
                #print('delta_lambda:   ' + str(delta_lambda))
                #print('a:              ' + str(a))
                #print('Activation:     ' + str(Activation[l]))
                #print('Output[l] :     ' + str(Output[l]))
                #print('W(l):           ' + str(self.W[l]))
                #print('tanh_deriv:     ' + str(_tanh_deriv(Activation[l])))
                
                
                #self.W[l] = self.W[l] + epsilon * n.outer(Output[l-1], delta_lambda)
                
                #n.outer(Output[l-1], delta_lambda)
                
                
                #print('n.outer:     ' + str(n.outer(delta_lambda, Output[l])))
                #print('Output:      ' + str(Output[l]))
                #print('delta_lambda:' + str(delta_lambda))
                
                
                print('_tanh_deriv(Output[l]):' + str(_tanh_deriv(Output[l])))
                print('delta_lambda:' + str(n.transpose(delta_lambda)))
                print('self.W[l]:' + str(self.W[l-1]))
                
                
                
                
                print('n.dot:' + str(n.dot(n.transpose(delta_lambda), (self.W[l-1]))))
                
                
                delta_lambda = _tanh_deriv(Output[l]) * n.dot(self.W[l-1],delta_lambda)
                
                print('+++++++++++++++++++++++++')
                
            
            
            
            print('ENDE!!!!')
            print('Output:   ' + str(Output))
            
                
            
            
            
        print('Gewichte nach lernen:')
        print(self.W)



