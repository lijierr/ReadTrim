raw=/30days/s4506266/projects/7.zhengmin_comommax/1.Filter/0.remove_headN/removeN
ot=/30days/s4506266/projects/7.zhengmin_comommax/1.Filter/readtrim

for i in S28 S29 S57 S58
	do

echo "#!/usr/bin/bash
#PBS -A UQ-EAIT-AWMC -l select=1:ncpus=20:mem=30GB -l walltime=50:60:00

export PATH=/90days/s4506266/softwares/FastQC-v0.11.7/:/90days/s4506266/softwares/FastUniq-1.1/source/:/30days/s4506266/softwares/anaconda3/bin:\$PATH
/90days/s4506266/softwares/anaconda3/bin/readtrim --fq1 $raw/${i}.noN.1.fastq.gz --fq2 $raw/${i}.noN.2.fastq.gz  --adap3 AGATCGGAAGAGCACACGTC --adap5 AGATCGGAAGAGCGTCGTGT --remove_dups --remove_adap --outdir $ot --sample_name $i

echo just do it>readtrim.${i}.sh.sign">readtrim.${i}.sh
done
echo done



