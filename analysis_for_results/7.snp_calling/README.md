SNP calling was carried out using the Java pipeline: https://github.com/DSGlab/SNPCallingPipeline

Using the configuration file similar to what is included in this directiory (configuration_file.txt).

With the jar file in the current directory do:

java -jar SNPCallingPipeline.jar datachecker configuration_file.txt
java -jar SNPCallingPipeline.jar scinetjobcreator configuration_file.txt
java -jar SNPCallingPipeline.jar gethqsnps configuration_file.txt
java -jar SNPCallingPipeline.jar getintraclonalsnps configuration_file.txt
java -jar SNPCallingPipeline.jar snpchecker configuration_file.txt
java -jar SNPCallingPipeline.jar snpfilter configuration_file.txt
java -jar SNPCallingPipeline.jar createalignment configuration_file.txt

To run the various steps in the pipeline (see run_snpcalling_java.sh)


