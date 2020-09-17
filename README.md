# Unet Sarcoma segmentation on MRI images
This repository provides a script and recipe to train UNet Medical to segment sarcoma tumors on MRI after the processing of these images.

# Model overview
The UNet model is a convolutional neural network for MRI image segmentation. This repository contains a UNet implementation as described in the original paper [UNet: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597), for more details please check the following [GitHub](https://github.com/NVIDIA/DeepLearningExamples/tree/master/TensorFlow/Segmentation/UNet_Medical).


# Start Guide

 1.  Clone Repository 
 
 2.  Container Docker :

The process of training and inference is done in the **Nvidia DGX Altran** server where the container of Unet is already created (unet_tf).The container contains all the components optimized for usage on NVIDIA hardware.
In case the container file does not exist, the repisotory contain a dockerfile that creates the container. 
The following command will use the `Dockerfile` to create a Docker image named `unet_tf`, downloading all the required components automatically.

    
    docker build -t unet_tf .

3.  Data File:
      - If the Unet is for inference, update just the test-volume.tif image.
      - If the Unet is for training, update all images.


4.  Model File:
     - If the Unet is for inference, the model file should not be updated.
     - If the Unet is for training, create a new model file.


5.  Start a session in the container for inference/training:
     To start a session in the Altran Server, a file launch_docker should be created. This reposotary contain a launch_docker file. It must contain the following comands

```
#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --mem=50g
set -x
export NV_GPU=$SLURM_JOB_GPUS
#INSTANCIER UN CONTAINER DOCKER COMME DANS EXEMPLE CI DESSOUS
nvidia-docker run --rm --name $DNAME -v /raid/IRMA/zelmouaffek/UNet_Medical/:/raid/IRMA/zelmouaffek/UNet_Medical -v /raid/IRMA/zelmouaffek/UNet_Medical/Data_Osteos:/data -v /raid/IRMA/zelmouaffek/UNet_Medical/Model_Lipo:/results -w /raid/IRMA/zelmouaffek/UNet_Medical unet_tf:latest /raid/IRMA/zelmouaffek/UNet_Medical/command.sh
```
The first five lines remains unchanged due to the configuration of the Altran Server. The last line is the line to run the container docker, it should always start with `nvidia-docker run --rm --name $DNAME -v`. It is followed by the path of the working directory, which is always in `/raid` directory. The : that follows specify the container path that we want to mount our working directory into. The right side is our local directory and the left side is the countainer one. Here it's ` /raid/IRMA/zelmouaffek/UNet_Medical/:/raid/IRMA/zelmouaffek/UNet_Medical -v`

The next step is to specify where we placed our data, it is done in the same way `/raid/IRMA/zelmouaffek/UNet_Medical/Data_Osteos:/data -v`. Our data, which is found in the directory Data_Osteos locally, will be found on the container in the data directory.

Then we specify where we placed our model directory,the command is  `
/raid/IRMA/zelmouaffek/UNet_Medical/Model_Lipo:/results
 -w`. Our model is found in the directory Model_Lipo locally, and in results on the container.

After specifying the data and model paths we should specify the path of the countainer `unet tf`, by adding the following command `
/raid/IRMA/zelmouaffek/UNet_Medical unet_tf:latest`.

Lastly we specify the path to the command file that containes the specidied option for training or inference :`
/raid/IRMA/zelmouaffek/UNet_Medical/command.sh`


6.Command File 
In this file we precise how to run the model (Inference or Training ).
	

 - **Inference** : Here we should make sure that the model path in the launch_docker file is referring to either of the ones contained in this repostory.  We ran the following command
```
 #!/bin/bash
 horovodrun -np 1 python main.py --data_dir /data --model_dir /results --exec_mode predict  
 ```
 

 - **Training** : Here we should make sure that the model path in the launch_docker file is a new directory, where the checkpoints and weights are gonna be stores.  We ran the following command
```
#!/bin/bash
horovodrun -np 1 python main.py --data_dir /data --model_dir /results  --exec_mode train    --max_steps 40000 
horovodrun -np 1 python main.py --data_dir /data --model_dir /results  --exec_mode predict
```
6. Run the model 
In order to run the model we navigate with the Linux commands to be placed in the directory containg the launch_docker. The we execute the launch_docker with this command :

```
rm slurm-*.out ; export DNAME=container_projet_ziad ; sbatch --export=ALL launch_docker.sh
```
To check if the model is runing we run on the command line `squeue` , it will show the users in the waiting queue. Also if we want to see the execution of the model in real time we use `tail -f slurm-*.out`.

The results are shown in the model directory, where the wrights of the neurones and checkpoints are stored. It contains also a directory pred where a tif images is stored correspanding to the prediction of the model.
# Sarcoma_segmentation
