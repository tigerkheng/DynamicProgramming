import numpy as np

def solver_hengrui(x, s):
    '''
    solver_hengrui() uses optimal_process(0, n-1) to find the
    optimal solution. optimal_process(i, j) will find the optimal 
    capability of data from time 0 to n-1 (inclusive), given a 
    reboot time at i-1 and j+1. Since the period is between two
    reboots, the time cost will not be affected no matter how other
    days are managed. Also, it will check every days between i and j
    to find whether reboot on that day makes a better solution. In 
    the code, when it checks the day k, it will add the op(i,k-1) 
    and op(k+1,j) to calculate the cost if it reboot at k.
    '''
    # length
    n = int(x.__len__())
    # the matrix to save the results, -1 means not computed
    mat = np.zeros([n, n]) - 1
    # the matrix to trace back the reboot time
    trace = np.zeros([n, n], dtype = np.int) - 1

    # no reboot case, from i to j inclusive
    def basic_process(i, j):
        res = 0
        for k in range(j-i+1):
            # check the minimum between capability and data volume
            res = res + min(x[i+k], s[k])
        return res
    
    # optimal reboot case, from i to j inclusive
    def optimal_process(i, j):
        # basic case: only one day
        if i > j:
            return 0
        # check if the result has been computed
        if mat[i, j] >= 0:
            return mat[i, j]
        # no reboot case, compared with reboots at day k
        res = basic_process(i, j)
        for k in range(i+1, j):
            tmp = optimal_process(i, k-1) + optimal_process(k+1, j)
            if tmp > res:
                res = tmp
                trace[i, j] = int(k)
        # save the result
        mat[i, j] = res
        return mat[i, j]
    
    # find reboot days, the recursion is similar to how we compute them
    def find_reboot(i, j):
        reboot = trace[i, j]
        if reboot < 0:
            return []
        return find_reboot(i, reboot-1)+[reboot]+find_reboot(reboot+1, j)

    # find the amount of data processed on each day
    def get_data_processed(reboot_days):
        # the parameter reboot_days is a list containing the days where we want to reboot
        # data_processed is a list that will hold the amount of data processed on each day
        data_processed = []
        # x and s start on day 1 (index 0)
        x_index = 0
        s_index = 0
        # reboot_index is used to keep track of when the next reboot day is
        reboot_index = 0
        while len(data_processed) < len(x):
            # if there are no more reboot days, then we don't have to worry about it
            if reboot_index >= len(reboot_days):
                # the minimum between x and s is the amount of data that will get processed
                data_processed.append(min(x[x_index], s[s_index]))
                x_index = x_index + 1
                s_index = s_index + 1
            else:
                # if we reboot, no data is processed and s starts over from the beginning but x still increments
                if reboot_days[reboot_index] == x_index:
                    data_processed.append(0)
                    reboot_index = reboot_index + 1
                    x_index = x_index + 1
                    s_index = 0
                else:
                    data_processed.append(min(x[x_index], s[s_index]))
                    x_index = x_index + 1
                    s_index = s_index + 1

        return data_processed

    res = optimal_process(0, n-1)
    reboot = find_reboot(0, n-1)
    data_processed = get_data_processed(reboot)
    # Print total data processed
    print(int(res))
    # Print data processed on each day
    for i in data_processed:
        print(int(i), end=" ")
        

if __name__ == "__main__":
    # basic example
    # x = [10, 1, 7, 7]
    # s = [8, 4, 2, 1]
    # the other test, current
    x = [20, 80, 20, 60, 20, 60, 80, 10, 40, 10]
    s = [100, 90, 50, 45, 40, 35, 20, 15, 10, 5]
    solver_hengrui(x, s)
