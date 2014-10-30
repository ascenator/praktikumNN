import numpy as n


def _tanh_deriv(x):  
    return x   #!! Achtung !!


Activation = n.array([[ 0.2 , 0.3 , 0.4 ]]) #[1x3]
OldDelta =   n.array([[ 0.4 , 0.5 ]])       #[1x2]

W =          n.array([[ 1 , 4 ], #[3x2]
                      [ 2 , 5 ],
                      [ 3 , 6 ]]) 

print('SUMME: ' + str((W * OldDelta)))#  OK!
print('SUMME: ' + str((W * OldDelta).sum(axis=1)))#  OK! << ist die Summe!!!
#[[ 0.4  2. ]
# [ 0.8  2.5]
# [ 1.2  3. ]]

#[ 2.4  3.3  4.2]

NewDelta = _tanh_deriv(Activation)  *  (W * OldDelta).sum(axis=1)

#NewDelta:[[ 0.48  0.99  1.68]] YAAAAAA!!!


print('NewDelta:' + str(NewDelta))



delta = n.array([[ 0.7099682949 , 0.565172551 ]])
             
w = n.array([[ 0.7033336583 , 0.4069464066 , 0.8978248964 , 0.7710629217 , 0.7749434992
   ,0.0124129597 , 0.9043779826 , 0.6853623098 , 0.2205394991 , 0.613363292 ],
 [ 0.9272066594 , 0.3947880904 , 0.0826401212 , 0.1785261892 , 0.0155527656,
   0.0862432825 , 0.0130291996 , 0.173364312 ,  0.1512376921 , 0.6139588859]]
)
print(w * n.transpose(delta))
print((w * n.transpose(delta)).sum(axis=1))


print('----------------------------------')

Output = n.array( [[ 0.0001241624 , 0.0007341834 , 0.0013483308 , 0.0103916043 , 0.0079608496,
   0.0014719776 , 0.0002846182 , 0.0026139545 , 0.0012658083 , 0.0003886146]])
W= n.array ( [[ 4.9181574699 , 4.0431062145 , 4.2007191951 , 4.8967675382 , 4.7472052014,
   4.5582000349 , 4.7530092586 , 4.7188183334 , 4.2873299821 , 4.4520313518],
 [ 2.4857620387 , 2.6051843094 , 3.0361427006 , 3.2719862769 , 3.052730672,
   2.5903648539 , 2.8081617499 , 3.028590967  , 3.1254999138 , 3.2298318324]])
delta = n.array ( [[ 39.27093641  ,  24.2338831372]])

print( Output * (W * n.transpose(delta)).sum(axis=0))


print('----------------------------------')


print('W-Test:')
print(n.dot(Output, n.transpose(W)))
