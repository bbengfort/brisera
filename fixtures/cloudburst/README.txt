Sample data for CloudBurst
==========================

CloudBurst has several parameters to control the sensitivity of the
alignment algorithm. Here it finds the unambiguous best alignment for 
100,000 reads allowing up to 3 mismatches when mapping to the corresponding
S. suis genome. 


== Sample input data

s_suis.fa: Streptococcus suis reference genome sequence
100k.fa:   100,000 36bp Illumina reads available from 
           http://www.sanger.ac.uk/Projects/S_suis/

== Format the input data
$ java -jar ConvertFastaForCloud.jar s_suis.fa s_suis.br
$ java -jar ConvertFastaForCloud.jar 100k.fa 100k.br

s_suis.br: reference genome in CloudBurst binary format
100k.br:   Reads in CloudBurst binary format


== Sample Run

# Copy the data files into the cloud
$ hadoop fs -mkdir /data/cloudburst
$ hadoop fs -put s_suis.br /data/cloudburst
$ hadoop fs -put 100k.br /data/cloudburst


# Run CloudBurst: Takes about ~3 minutes on 24-cores
$ hadoop jar CloudBurst.jar /data/cloudburst/s_suis.br \
  /data/cloudburst/100k.br /data/results \
  36 36 3 0 1 240 48 24 24 128 16 >& cloudburst.err


# Copy the raw results to the local filesystem
$ hadoop fs -get /data/results/ results


# Convert the raw results to a text file, sorting to ensure a consistent order
$ java -jar PrintAlignments.jar results | sort -nk4 > 100k.3.txt


# You can then compare your results to 100k.3.txt.gold
$ diff 100k.3.txt 100k.3.txt.gold
(should report no differences)
