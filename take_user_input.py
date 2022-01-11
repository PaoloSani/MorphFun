def take_user_input():

    user_input = input('Type a number between 1 and 4\n')
    isInRange = False
    
    while isInRange==False:
    
        while not(user_input.strip().isdigit()):
            print("The input was not a number between 1 and 4.\nTry Again\n")
            user_input = input('Type a number between 1 and 4\n')
    
        
        if (1<=int(user_input)<=4):
            user_input = int(user_input) -1
            isInRange=True
        else:
            print("The input was not a number between 1 and 4.\nTry Again\n")
            user_input = input('Type a number between 1 and 4\n')

    return user_input



