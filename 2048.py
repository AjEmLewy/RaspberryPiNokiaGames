import timeit

#pola = ['' for x in range(16)]
#pola[1]=2
#pola[2]=2
pola=[2,2,4,4,2,4,8,16,16,2,2,8,2,2,2,2]

def mr(pola):
    apola=[pola[0:4],pola[4:8],pola[8:12],pola[12:16]]
    for pole in apola: print(pole)
    for pole in apola:
        #3 pole
        if pole[2]!='':
            if pole[3] == '':
                pole[3]=pole[2]
                pole[2]=''
            else:
                if pole[3]==pole[2]:
                    pole[3]*=2
                    pole[2]=''
        #2 pole
        if pole[1]!='':
            if (pole[2]=='' and pole[3]==''):
                pole[3]=pole[1]
                pole[1]=''
            elif(pole[3]!='' and pole[2] == ''):
                if pole[3]==pole[1]:
                    pole[3]*=2
                else:
                    pole[2]=pole[1]
                pole[1]=''
            elif(pole[2]!=''):
                if pole[2]==pole[1]:
                    pole[2]*=2
                    pole[1]=''
            
        #1 pole
        if pole[0]!='':
            if(pole[3]=='' and pole[2] =='' and pole[1]==''):
               pole[3] = pole[0]
               pole[0] = ''
            elif (pole[3] != '' and pole[2] == '' and pole[1] == ''):
               if pole[3] == pole[0]:
                   pole[3]*=2
               else:
                   pole[2]=pole[0]
               pole[0]=''
            elif (pole[2] != '' and pole[1]==''):
                if pole[2] == pole[0]:
                    pole[2]*=pole[0]
                else:
                    pole[1]=pole[0]
                pole[0]=''
            elif (pole[1]!= ''):
                if( pole[1]==pole[0]):
                    pole[1]*=2
                    pole[0]=''
                
            


    return apola[0]+apola[1]+apola[2]+apola[3]
