import os

def ReadQuestion(questionType, timer):
    """
    Returns the full information for the question.
    """
    if (type(questionType) != str) and (type(timer) != int):
        return "[Issue: Please check script logs and send the log to Steven#0097 on Discord]"

    if ' ' in questionType: #Checks for spaces to convert to '_'
        questionType = questionType.replace(' ', '_')

    if os.path.exists('Services/Scripts/Poll/Questions/{}.txt'.format(questionType)):
        f = open("Services/Scripts/Poll/Questions/{}.txt".format(questionType), "r")
        lines = f.readlines()
        f.close()

        if len(lines) == 2:
            question = lines[0]
            options = lines[1].split(", ")

            newQuestion = [question, options, timer]

            return newQuestion
        else:
            return "[Warning - Data missing from text file] Check the full question is on line 1 and the options are on line 2."
    else:
        return "[Warning - Question does not exist] Check your question information file name matches the question provided."