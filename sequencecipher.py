import sys

options = {
    'sequence' : 's',
    'groups' : 'g',
    'file' : 'f',
    'decrypt' : 'd' 
}

def getValue(item):
    if(item[0]=='a'):
        return lambda values : values[len(values)-int(item[4])]
    try:
        output = int(item)
        return lambda values : output
    except ValueError:
        pass
    
def buildOperation(sequenceArray):
    operator = sequenceArray[1]
    value1 = getValue(sequenceArray[0])
    value2 = getValue(sequenceArray[2])

    if(operator=='+'):
        return lambda values : value1(values) + value2(values)
    elif(operator=='-'):
        return lambda values : value1(values) - value2(values)
    elif(operator=='*'):
        return lambda values : value1(values) * value2(values)
    elif(operator=="/"):
        return lambda values : value1(values) / value2(values)
    elif(operator=="%"):
        return lambda values : value1(values) % value2(values)

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
        operations.append(lambda values : -1*value(values))

    while i<len(sequenceArray):
        if(sequenceArray[i]==','):
            initialConditions = buildInitalConditions(sequenceArray[i+1:len(sequenceArray)])
            break
        operation = buildOperation(sequenceArray[i-1:i+2])
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

def encrypt(text, sequence, groupSequence, characterEvaluator):
  
    if(characterEvaluator == None):
        characterEvaluator = lambda character, shift : chr((ord(character)-32+shift)%95+32)

    sequenceValues = []
    groupSequenceValues = []
    index = 0
    output = ""

    while(index<len(text)):
        group = groupSequence(groupSequenceValues) 
        shift = sequence(sequenceValues)
        sequenceValues.append(abs(shift))
        for i in range(0,group):
            output += characterEvaluator(text[index],shift)
            index+=1
            if(index>=len(text)):
                break
    print(output)

def encryptFile(text, sequence, groupSequence):
    file = open(text)
    string = file.read()
    encrypt(string[0:len(string)-1], sequence, groupSequence, None)
    file.close()

def decrypt(text, sequence, groupSequence):
    evaluator = lambda character,shift : chr((ord(character)-32-shift)%95+32)
    encrypt(text, sequence, groupSequence, evaluator)

def decryptFile(text, sequence, groupSequence):
    file = open(text)
    string = file.read()
    decrypt(string[0:len(string)-1], sequence, groupSequence)
    file.close()

def main():
    sequence = lambda last : 1 
    groupSequence = lambda last : 1
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if(arg[0]=='-'):
            i+=1
            value = sys.argv[i]
            if(arg[1]==options['sequence']):
                sequence = buildSequence(value)
            elif(arg[1]==options['groups']):
                groupSequence = buildSequence(value)
            elif(arg[1]==options['file']):
                encryptFile(value, sequence, groupSequence)
            elif(arg[1]==options['decrypt']):
                if(len(arg)<3):
                    decrypt(value, sequence, groupSequence)
                elif(arg[2]==options['file']):
                    decryptFile(value, sequence, groupSequence)
        else:
            encrypt(arg, sequence, groupSequence, None)
        i+=1
main()

