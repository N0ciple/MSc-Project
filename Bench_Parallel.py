from benchmark_histo import *
from joblib import Parallel, delayed
import multiprocessing
import os
import sys


if os.name == 'nt' :
    from win10toast import ToastNotifier


if __name__ == '__main__':
    if os.name == 'nt':
        toaster = ToastNotifier()

    probas = [0.4]

    num_cores = multiprocessing.cpu_count()

    print("Starting benchmarking on ",num_cores," cores")

    for proba in probas:

        inputs = range(0,10)

        results = Parallel(n_jobs=num_cores-1)(delayed(runHistoSimulation)(i,proba) for i in inputs)

        scoreL2 = [v[0] for v in results]
        scoreChi2 = [v[1] for v in results]
        moyProba  = [v[2] for v in results]

        print("\nGlobal Score for L2 : ",np.mean(scoreL2))
        print("Global Score for Chi2 : ",np.mean(scoreChi2))
        print("Global Proba : ",np.mean(moyProba))
        print(moyProba)

        with open('results.txt','a') as f:
            f.write("\nProba = "+str(proba)+"\n\tGlobal Score for L2 : " + str(np.mean(scoreL2)) +"\n\tGlobal Score for Chi2 : " + str(np.mean(scoreChi2)))




    if os.name == 'nt':
        toaster.show_toast("Simulation Over",
                       "P: "+str(proba)+" L2: "+str(np.mean(scoreL2))+" Chi2: "+str(np.mean(scoreChi2)),
                       duration=60)
