import sys

options = {
    'sequence' : 's',
    'groups' : 'g',
    'file' : 'f',
    'decrypt' : 'd' 
}

def getValue(item):
    if(item[0]=='a'):
        return lambda values : values[len(values)-item[2]]
    try:
        output = int(item)
        return output
    except ValueError:
        pass
    
def buildOperation(sequenceArray):
    operator = sequenceArray[1]
    value1 = getValue(sequenceArray[0])
    value2 = getValue(sequenceArray[2])

    if(operator=='+'):
        return lambda values : value1 + value2
    elif(operator=='-'):
        return lambda values : value1 - value2
    elif(operator=='*'):
        return lambda values : value1 * value2
    elif(operator=="/"):
        return lambda values : value1 / value2
    elif(operator=="%"):
        return lambda values : value1 % value2

def buildInitalConditions(sequenceArray):
    initialConditions = []

    for value in sequenceArray:
        initialConditions.append(int(value))

    return initialConditions

def buildSequence(sequenceText):
   
    operations = []
    initialConditions = []

    sequenceArray = sequenceText.split(" ")

    i=1
    
    if(sequenceArray[0]=='-'):
        value = getValue(sequenceArray[1])
        operations.append(lambda values : -1*value)

    while i<len(sequenceArray):
        if(sequenceArray[i]==','):
            initialConditions = buildInitalConditions(sequenceArray[i+1:len(sequenceArray)])
            break
        operation = buildOperation(sequenceArray[i-1:i+1])
        if(operation):
            operations.append(operation)
        i+=2

    def nextItem(values):
        if len(values) < len(initialConditions):
            return initialConditions[len(values)-1]
        sum = 0
        for i in range(0, len(operations)):
            sum += operations[i](values)
        return sum

    return nextItem

def encrypt(text, sequence, groupSequence):
   
    sequenceValues = []
    groupSequenceValues = []
    index = 0
    output = ""

    while(index<len(text)):
        group = groupSequence(groupSequenceValues) 
        shift = sequence(sequenceValues)
        sequenceValues.append(shift)

        for i in range(0,group):
            output += chr((ord(text[index])+shift)%128)
            index+=1
            if(index>=len(text)):
                break
    print(output)

def encryptFile(text, sequence, groupSequence):
    file = open(text)
    encrypt(file.read(), sequence, groupSequence)
    file.close()

def decrypt(text, sequence, groupSequence):
    newSequence = lambda values : -1*sequence(values)
    encrypt(text, sequence, groupSequence)

def decryptFile(file, sequence, groupSequence):
    newSequence = lambda values : -1*sequence(values)
    encryptFile(file, newSequence, groupSequence)

def parseOption(opt, value, sequence, groupSequence):
            if(opt[1]==options['sequence']):
                sequence = buildSequence(value)
            elif(opt[1]==options['groups']):
                groupSequence = buildSequence(value)
            elif(opt[1]==options['file']):
                encryptFile(value, sequence, groupSequence)
            elif(opt[1]==options['decrypt']):
                if(len(opt)<2):
                    decrypt(value, sequence, groupSequence)
                elif(opt[2]==options['file']):
                    decryptFile(value, sequence, groupSequence)

def main():
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        sequence = lambda last : 1 
        groupSequence = lambda last : 1
        if(arg[0]=='-'):
            i+=1
            parseOption(arg, sys.argv[i], sequence, groupSequence)
        else:
            encrypt(arg, sequence, groupSequence)
        i+=1
main()

