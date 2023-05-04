class Utils:
    def checkIfHasPositive(message):
        if 'true' in str(message).lower():
            return True
        elif 'false' in str(message).lower():
            return False
        elif 'false' in str(message).lower() and 'true' in str(message).lower():
            return 'NEUTRAL'
        else:
            return 'NEUTRAL'
