'''
The MIT License (MIT)

Copyright (c) 2015 stendarr (github.com/stendarr)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


from collections import Counter
import os.path

#definitions
def printResults():
    print('='*50)
    print('Lines                 : ',lines)
    print('Blanklines            : ',blanklines)
    print('Sentences             : ',sentences)
    print('Words:                : ',words)
    print('Anglicisms            : ',len(anglicisms))
    print('Words until anglicism : ',int(words)/len(anglicisms)-1)
    print('All anglicisms        :\n',Counter(anglicisms))
    print('='*50)
    
def derivatesFromAnglicism(word):
    return any([word.startswith('ge'+a) for a in listOfAnglicisms]) or any([word.startswith(a) for a in listOfAnglicisms])

#welcome message
print('='*68)
print(' Welcome to the ANGLICISM COUNTER by stendarr (see github.com/stendarr) ')
print('='*68)

#start program in loop
while True:
    
    #setting values
    lines, blanklines, sentences, words, setnum = 0,0,0,0,1
    listOfAnglicisms = open('lists/anglicisms.txt').read().split()
    listOfGermanWords = open('lists/frequents.txt').read().split()
    anglicisms = []
    falsepositive = []
    setname = input('Please enter setname: ')
    
    #checking if valid file
    while os.path.isfile(str(setname+str(setnum)+'.txt')) == False:
        setname = input('There is no file called "'+str(setname+str(setnum)+'.txt')+'"\nPlease enter a valid setname: ')
    
    #loop until there are no files of the entered set
    while os.path.isfile(str(setname+str(setnum)+".txt")) == True:

        textf = open(setname+str(setnum)+'.txt')

        #analyze line by line
        for line in textf:
            line = line.lower()
            lines+=1

            if line.startswith('\n'):
                blanklines+=1
            else:
                sentences += line.count('.') + line.count('!') + line.count('?')
                words += len(line.split(None))
                anglicisms.extend([word for word in line.split() if derivatesFromAnglicism(word)])
                anglicisms = [x for x in anglicisms if x not in listOfGermanWords]
                
        setnum+=1

    textf.close()
    printResults()

    #manually remove false positives if there are any
    while falsepositive != 'n':
        falsepositive = input('Please enter a false positive or "n" to continue: ')
        if falsepositive == 'n':
            pass
        else:
            while falsepositive in anglicisms:
                anglicisms.remove(falsepositive)
        printResults()

    #want to output a file? just enter y
    if  input('Enter "y" if you want to create an output file: ') == 'y':
        results = open('results_'+setname+'.txt', 'w')
        
        results.write(
            ('='*50)+
            '\n'+
            setname+'\n'+
            'Lines                 : '+str(lines)+'\n'+
            'Blanklines            : '+str(blanklines)+'\n'+
            'Sentences             : '+str(sentences)+'\n'+
            'Words:                : '+str(words)+'\n'+
            'Anglicisms            : '+str(len(anglicisms))+'\n'+
            'Words until anglicism : '+str(int(words)/len(anglicisms)-1)+'\n'+
            'All anglicisms        :\n'+str(Counter(anglicisms))+'\n'+
            ('='*50)+
            '\n'
            )
        results.close()
    else:
        #let the magic begin again
        pass
    print('='*50)
