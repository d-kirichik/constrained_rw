import sys
import os

home = os.getenv("HOME")
file_name = 'final_MSFT'
file_path = "data/%s.csv" % file_name
regenerated_size = 10
z_vector_dimensions = [10, 11, 12, 13, 14, 15, 16, 17]
taus = [5, 6, 7, 8, 9, 10]

def gen_job_name(z_vector_dim, tau, regenerated_size):
    return "job-%s-%s:%s:%s" % (file_name, z_vector_dim, tau, regenerated_size)


for z_vector_dim in z_vector_dimensions:

    for tau in taus:
        job_name = gen_job_name(z_vector_dim, tau, regenerated_size)
        job_file = os.path.join('%s/constrained_rw/jobs/' % home,"%s.job" % job_name)
        output_file = os.path.join('%s/constrained_rw/outputs/' % home,"%s.csv" % job_name)

        with open(job_file, 'w+') as fh:
            os.chmod(job_file, 0o755)
            fh.writelines("#!/bin/bash\n")
            fh.writelines("#SBATCH --job-name=%s.job\n" % job_name)
            fh.writelines("#SBATCH --output=%s/constrained_rw/.out/%s.out\n" % (home, job_name))
            fh.writelines("#SBATCH --error=%s/constrained_rw/.out/%s.err\n" % (home, job_name))
            fh.writelines("python $HOME/constrained_rw/constrained_rw.py %s %s %s %s %s\n" % (file_path, z_vector_dim, tau, regenerated_size, output_file))

        #os.system("sbatch %s" % job_file)
