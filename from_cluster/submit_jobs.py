import argparse
import os
import csv, subprocess

def create_dirs(n_dir):
    logpath=os.path.join(n_dir,"job_logs")
    resultpath=os.path.join(n_dir,"results")
    
    if not os.path.isdir(n_dir):
        os.mkdir(n_dir)
    if not os.path.isdir(logpath):
        os.mkdir(logpath)
    if not os.path.isdir(resultpath):
        os.mkdir(resultpath)
    print(resultpath)            

def main():
    parser = argparse.ArgumentParser(
        description="Automatically submit jobs using a csv file")

    parser.add_argument('jobscript',help="job script to use")
    parser.add_argument('parameters',help="csv parameter file to use")
    parser.add_argument('-t','--test',action='store_false',help="test script without submitting jobs")
    args = parser.parse_args()

    with open(args.parameters,mode='r',newline='',encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        created_dirs = []
        for job in reader:
            n_dir = "/scratch/MrLavaLoba/{0}_{1}_{2}_{3}_{4}_{5}/".format(*job)
            if dir not in created_dirs:
                create_dirs(n_dir)
                created_dirs.append(n_dir)
            print(args.jobscript)
            job.append("/scratch/MrLavaLoba/{0}_{1}_{2}_{3}_{4}_{5}/results".format(*job))
            submit_command = (
                "sbatch " +
                "-o /scratch/MrLavaLoba/{0}_{1}_{2}_{3}_{4}_{5}/job_logs/out.txt ".format(*job) +
                "--job-name=mrlavaloba_{0}_{1}_{2}_{3}_{4}_{5} "
                "--ntasks=1 "
                "--time=00:45:00 "
                "--export=xVent={0},yVent={1},length={2},flowrate={3},runtime={4},minnlobes={5},destination={6} ".format(*job) + args.jobscript)
            if not args.test:
                print(submit_command)
            else:
                exit_status = subprocess.call(submit_command,shell=True)
                # Check to make sure the job submitted
                if exit_status is 1:
                    print("Job {0} failed to submit".format(submit_command))

    print("Done submitting jobs")

if __name__ == "__main__":
    main()
