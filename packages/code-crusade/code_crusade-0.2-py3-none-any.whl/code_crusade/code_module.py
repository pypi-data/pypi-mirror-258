def submit(problem_number:int, func:classmethod):
    """
    Submits your answer to Code Crusade to be graded
    problem_number (int): The number of the problem you are submitting
    func (function): The function you are submitting
    """

    if problem_number == 0:
        case_numbers = [1,2,3,4,5,6,7,8,9,10,20,25,30,40,50,60,100,102,340,500,2000]
        case_multipliers = [0, 1, 2, 3, 5, 10]

        for i in case_numbers:
            for j in case_multipliers:
                try:
                    user_answer = func(i, j)
                except:
                    print("RUNTIME ERROR")
                    exit()

                correct = i * j

                if user_answer != correct:
                    print("INCORRECT ANSWER")
                    exit()

        print("CORRECT! 0 Points Earned.")

    else:
        print("Problem Number not Valid (Program was not tested).")