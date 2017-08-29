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

    probas = [0.2,0.3,0.4,0.5,0.6,0.7,0.9]

    num_cores = multiprocessing.cpu_count()

    print("Starting benchmarking on ",num_cores," cores")

    for proba in probas:

        inputs = range(0,3)

        results = Parallel(n_jobs=num_cores-1)(delayed(runHistoSimulation)(i,proba) for i in inputs)

        scoreL2 = [v[0] for v in results]
        scoreChi2 = [v[1] for v in results]
        Graphs  = [v[2] for v in results]
        distsToSource = [v[3] for v in results]

        print("\nGlobal Score for L2 : ",np.mean(scoreL2))
        print("Global Score for Chi2 : ",np.mean(scoreChi2))
        print("dists : ", distsToSource)

        # Compute proba of detection First one
        probaDetectL2 = []
        probaDetectChi2 = []
        # Compute proba of detection first 5
        probaDetect5L2 = []
        # Compute proba of detection first 10
        probaDetect10L2 =[]

        for score in scoreL2 :
            if score == 0 :
                probaDetectL2.append(1)
            else:
                probaDetectL2.append(0)
            if score <= 4:
                probaDetect5L2.append(1)
            else:
                probaDetect5L2.append(0)
            if score <=9:
                probaDetect10L2.append(1)
            else:
                probaDetect10L2.append(0)

        moyProba = np.mean(probaDetectL2)
        moyProba5 = np.mean(probaDetect5L2)
        moyProba10 = np.mean(probaDetect10L2)


        for score in scoreChi2:
            if score == 0:
                probaDetectChi2.append(1)
            else:
                probaDetectChi2.append(0)

        moyProbaChi2 = np.mean(probaDetectChi2)


        moyDist = np.mean(distsToSource)

        print("All proba L2", probaDetectL2)
        print("Global Proba L2: ",moyProba)
        print("Global Proba Chi2: ",moyProbaChi2)
        print(moyDist)
        with open('results.txt','a') as f:
            f.write("Proba = "+str(proba)+"\nGlobal Score for L2 : " + str(np.mean(scoreL2)) +"\nGlobal Score for Chi2 : "
                    + str(np.mean(scoreChi2))+ "\nProba Detect L2 " + str(moyProba)+ "\nProba Bo5 L2 " + str(moyProba5)
                    + "\nProba Bo10 L2 " + str(moyProba10)+ "\n Mean min dist to real source : " + str(moyDist) +"\n")



    if os.name == 'nt':
        toaster.show_toast("Simulation Over",
                       "P: "+str(proba)+" L2: "+str(np.mean(scoreL2))+" Chi2: "+str(np.mean(scoreChi2)),
                       duration=60)
