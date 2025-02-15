from MTP_lib import *

def heuristic_algorithm(file_path):
    '''
    1. Write your heuristic algorithm here.
    2. We would call this function in grading_program.py to evaluate your algorithm.
    3. Please do not change the function name and the file name.
    4. Do not import any extra library. We will import libraries from MTP_lib.py.
    5. The parameter is the file path of a data file, whose format is specified in the document.
    6. You need to return your schedule in two lists "machine" and "completion_time".
        (a) machine[j][0] is the machine ID (an integer) of the machine to process the first stage of job j + 1, and
            machine[j][1] is the machine ID (an integer) of the machine to process the second stage of job j + 1.
            Note. If job j + 1 has only one stage, you may store any integer in machine[j][1].
        (b) completion_time[j][0] is the completion time (an integer or a floating-point number) of the first stage of job j + 1, and
            completion_time[j][1] is the completion time (an integer or a floating-point number) of the second stage of job j + 1.
            Note. If job j + 1 has only one stage, you may store any integer or floating-point number in completion_time[j][1].
        Note 1. If you have n jobs, both the two lists are n by 2 (n rows, 2 columns).
        Note 2. In the list "machine", you should record the IDs of machines
                (i.e., to let machine 1 process the first stage of job 1,
                you should have machine[0][0] == 1 rather than machine[0][0] == 0).
    7. The only PY file that you need and are allowed to submit is this algorithm_module.py.
    '''

    # read data and store the information into your self-defined variables
    fp = open(file_path, 'r')
    # for a_row in fp:
    #    print(a_row) # a_row is a list
    # ...

    # start your algorithm here
    machine = []
    completion_time = []
    # ...
    # ////////////////////////////////////////////////////////////////
    instance = pd.read_csv(file_path)
    # import pandas as pd
    # machine = []
    # completion_time = []
    # instance = pd.read_csv('instance04.csv')
    jobs = range(len(instance['Job ID']))
    machine_num = 0
    processing_times = [[],[]]
    processing_times[0] = instance['Stage-1 Processing Time']
    processing_times[1] = instance['Stage-2 Processing Time']
    dues = instance['Due Time']
    stage_machines = [[],[]]
    stage_machines[0] = instance['Stage-1 Machines']
    stage_machines[1] = instance['Stage-2 Machines']
    for i in jobs:
        for j in range(2):
            value = stage_machines[j][i]
            if isinstance(value, float):  # Check if it's a float
                value = str(value)  # Convert float to string
            if value == 'nan':
                stage_machines[j][i] = []
            else:
                inte = [int(num) for num in value.split(",")]
                maxi = max(inte)
                machine_num = max(machine_num, maxi)
                stage_machines[j][i] = inte
    machines = range(machine_num)
    Machines = range(machine_num)

    mac = [[0 for j in range(2)] for i in jobs]
    completion = [[0 for j in range(2)] for i in jobs]
    x = []
    y = []
    not_in_one = []
    importance = [0] * len(machines)
    for i in range(len(jobs)):
        x.append([])
        for k in machines:
            if stage_machines[1][i] != []:
                if k+1 in stage_machines[0][i]:
                    importance[k]+=1
                if k+1 in stage_machines[1][i]:
                    importance[k]+=1
                if k+1 in stage_machines[0][i] and k+1 in stage_machines[1][i]:
                    x[i].append(1)
                else:
                    x[i].append(0)
            else:
                if k+1 in stage_machines[0][i]:
                    x[i].append(1)
                else:
                    x[i].append(0)
        if 1 not in x[i]:
            not_in_one.append(i)
            y.append([])
            for j in range(2):
                y[i].append([])
                for k in machines:
                    if k+1 in stage_machines[j][i]:
                        importance[k]+=1
                        y[i][j].append(k)
        else:
            y.append([])
            for j in range(2):
                y[i].append([])

    left = list()
    c = list()
    for i in jobs:
        left.append(processing_times[0][i] + processing_times[1][i])
        c.append(0)

    time = [0] * len(machines)

    def find(k):
        infeasible = 0
        minn = 10000
        smallest = 0
        for i in jobs:
            if x[i][k] == 1:
                if dues[i] - left[i] < minn :
                    infeasible += 1
                    minn = dues[i] - left[i]
                    smallest = i
        if(infeasible != 0):
            return smallest
        else:
            return 300
        

    min_value = min(importance)
    min_machine = importance.index(min_value)
    THEmachine = min_machine
    deleted = [-1] * len(machines)
    threshold = 1e-10  # 设置一个非常小的阈值
    while True:
        goal = find(THEmachine)
        if goal == 300:
            deleted[THEmachine] = time[THEmachine]
            time[THEmachine] = 10000
            min_value = min(time)
            min_machine = time.index(min_value)
            THEmachine = min_machine
            continue

        time[THEmachine] = time[THEmachine] + left[goal]
        c[goal] = time[THEmachine]
        mac[goal][0] = THEmachine
        mac[goal][1] = THEmachine
        completion[goal][0] = time[THEmachine] - processing_times[1][goal]
        completion[goal][1] = time[THEmachine]

        for k in machines:
            x[goal][k] = 0

        left[goal] = 0
        min_value = min(time)
        min_machine = time.index(min_value)
        THEmachine = min_machine

        if(sum(left)-sum([left[i] for i in not_in_one])) <= 0:
            break
        
        
        
    for k in machines:
        if deleted[k] != -1:
            time[k] = deleted[k]
    for i in not_in_one:
        # stage1

        # /////////////////////////////////////////////////////////////////////////////////
        available_machines = [m for m in y[i][0] if m < len(time)]
        min_value = min([time[m] for m in available_machines])
        min_machine = time.index(min_value)
        if min_machine in available_machines:
            machine1 = min_machine
        else:
            machine1 = available_machines[0] if available_machines else None
        # //////////////////////////////////////////////////////////////////////////////////

        time[machine1] = time[machine1] + processing_times[0][i]
        # stage2
        
        # /////////////////////////////////////////////////////////////////////////////////
        available_machines = [m for m in y[i][1] if m < len(time)]
        min_value = min([time[m] for m in available_machines])
        min_machine = time.index(min_value)
        if min_machine in available_machines:
            machine2 = min_machine
        else:
            machine2 = available_machines[0] if available_machines else None
        # //////////////////////////////////////////////////////////////////////////////////
        if time[machine2] > time[machine1]  + 1:#本來就可以接著執行，且需要1往後來配合
            time[machine2] = time[machine2] + processing_times[1][i]
            time[machine1] = time[machine2] - processing_times[1][i] - 1
        elif time[machine2] > time[machine1] :#本來就可以接著執行，且不需要1往後來配合
            time[machine2] = time[machine2] + processing_times[1][i]
        else:#time2不夠
            time[machine2] = time[machine1] + processing_times[1][i]
        c[i] = time[machine2]
        mac[i][0] = machine1
        mac[i][1] = machine2
        completion[i][0] = time[machine1] 
        completion[i][1] = time[machine2]
        
    tard = 0
    for i in jobs:
        if(c[i]-dues[i] > 0):
            tard += c[i]-dues[i]
                
                
                
                
    Machine = [[0 for j in range(2)] for i in jobs]
    Completion = [[0 for j in range(2)] for i in jobs]
    xx = []
    yy = []
    not_in_one = []
    Machines = range(machine_num)
    importance = [0] * len(Machines)
    for i in range(len(jobs)):
        xx.append([])
        for k in Machines:
            if stage_machines[1][i] != []:
                if k+1 in stage_machines[0][i]:
                    importance[k]+=1
                if k+1 in stage_machines[1][i]:
                    importance[k]+=1
                if k+1 in stage_machines[0][i] and k+1 in stage_machines[1][i]:
                    xx[i].append(1)
                else:
                    xx[i].append(0)
            else:
                if k+1 in stage_machines[0][i]:
                    xx[i].append(1)
                else:
                    xx[i].append(0)
        if 1 not in xx[i]:
            not_in_one.append(i)
            yy.append([])
            for j in range(2):
                yy[i].append([])
                for k in Machines:
                    if k+1 in stage_machines[j][i]:
                        importance[k]+=1
                        yy[i][j].append(k)
        else:
            yy.append([])
            for j in range(2):
                yy[i].append([])
        
        
        
    Left = list()
    cc = list()
    for i in jobs:
        Left.append(processing_times[0][i] + processing_times[1][i])
        cc.append(0)

    # time = [0] * len(machines)

    def Find(k):
        infeasible = 0
        minn = 10000
        smallest = 0
        for i in jobs:
            if xx[i][k] == 1:
                if dues[i] - Left[i] < minn :
                    infeasible += 1
                    minn = dues[i] - Left[i]
                    smallest = i
        if(infeasible != 0):
            return smallest
        else:
            return 300

    Time = []
    for k in Machines:
        Time.append(0)
    min_value = min(importance)
    min_machine = importance.index(min_value)
    THEmachine = min_machine
    for i in not_in_one:
        # stage1

        # /////////////////////////////////////////////////////////////////////////////////
        available_machines = [m for m in yy[i][0] if m < len(Time)]
        min_value = min([Time[m] for m in available_machines])
        min_machine = Time.index(min_value)
        if min_machine in available_machines:
            machine1 = min_machine
        else:
            machine1 = available_machines[0] if available_machines else None
        # //////////////////////////////////////////////////////////////////////////////////

        Time[machine1] = Time[machine1] + processing_times[0][i]
        # stage2
        # /////////////////////////////////////////////////////////////////////////////////
        available_machines = [m for m in yy[i][1] if m < len(Time)]
        min_value = min([Time[m] for m in available_machines])
        min_machine = Time.index(min_value)
        if min_machine in available_machines:
            machine2 = min_machine
        else:
            machine2 = available_machines[0] if available_machines else None
        # //////////////////////////////////////////////////////////////////////////////////
        if Time[machine2] > Time[machine1]  + 1:#本來就可以接著執行，且需要1往後來配合
            Time[machine2] = Time[machine2] + processing_times[1][i]
            Time[machine1] = Time[machine2] - processing_times[1][i] - 1
        elif Time[machine2] > Time[machine1] :#本來就可以接著執行，且不需要1往後來配合
            Time[machine2] = Time[machine2] + processing_times[1][i]
        else:#time2不夠
            Time[machine2] = Time[machine1] + processing_times[1][i]
        cc[i] = Time[machine2]
        Machine[i][0] = machine1
        Machine[i][1] = machine2
        Completion[i][0] = Time[machine1] 
        Completion[i][1] = Time[machine2]
        

    delete_times = 0
    deleted = []
    threshold = 1e-10  # 设置一个非常小的阈值
    while True:
        goal = Find(THEmachine)
        if goal == 300:
            deleted.append(THEmachine)
            delete_times +=1
            del Time[THEmachine]
            for i in jobs:
                del xx[i][THEmachine]
            Machines = range(len(Machines) - 1)
            min_value = min(Time)
            min_machine = Time.index(min_value)
            THEmachine = min_machine
            continue
        Time[THEmachine] = Time[THEmachine] + Left[goal]
        cc[goal] = Time[THEmachine]
        Machine[goal][0] = THEmachine
        Machine[goal][1] = THEmachine
        Completion[goal][0] = Time[THEmachine] - processing_times[1][goal]
        Completion[goal][1] = Time[THEmachine]

        for k in Machines:
            xx[goal][k] = 0

        Left[goal] = 0
        min_value = min(Time)
        min_machine = Time.index(min_value)
        THEmachine = min_machine

        if(sum(Left)-sum([Left[i] for i in not_in_one])) <= 0:
            break

        
        
    tard2 = 0
    for i in jobs:
        if(cc[i]-dues[i] > 0):
            tard2 += cc[i]-dues[i]
            
            
    if tard < tard2:
        # print("arrange one first",tard)
        machine = mac
        completion_time = completion
        # print(machine)
        # print(completion_time)
        
    else:
        # print("arrange two first",tard2)
        machine = Machine
        completion_time = Completion
        # print(machine)
        # print(completion_time)
    # ///////////////////////////////////////////////////////////////

    return machine, completion_time
