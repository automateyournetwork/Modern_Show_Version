'''
To run the job:

$ pyats run job Modern_Show_Version_job.py --testbed-file ../testbed/3850.yaml

'''

import os

def main(runtime):
    # Find the location of the script in relation to the job file
    testscript = os.path.join(os.path.dirname(__file__), '../job/Modern_Show_Version.py')
    
    # run script
    runtime.tasks.run(testscript=testscript)
