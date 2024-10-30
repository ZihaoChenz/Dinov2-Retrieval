# Import necessary modules and functions
from utils.data_process import feature_inference
from utils.load_data import load_data
from model import model_process  # Import custom model from model.py file
import torch
import torch.optim as optim
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='parameter')
    parser.add_argument('--CheckFolder', help="input check image folder", required=True, type=str)
    parser.add_argument('--OutputFolder', help="output folder path", required=False, type=str, default="output")
    args = parser.parse_args()
    return args

args = parse_args()
check_folder = args.CheckFolder
output_folder = args.OutputFolder




# Check if CUDA is available and set PyTorch to use GPU or CPU accordingly
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Use the load_data function from tools.training to load our dataset
# This function presumably returns a set of data loaders and the number of classes in the dataset
dataloaders = load_data(check_folder)

# Initialize our classifier model with the number of output classes equal to num_classes

model = model_process() # this will load the small model
# model = model_process(backbone = 'dinov2_b') # to load the base model
# model = model_process(backbone = 'dinov2_l') # to load the large model
# model = model_process(backbone = 'dinov2_g') # to load the largest model


# Move the model to the device (GPU or CPU)
model.to(device)


# Initialize Stochastic Gradient Descent (SGD) as our optimizer
# Set the initial learning rate to 0.001 and momentum to 0.9
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)


# Finally, use the train_model function from tools.training to train our model
# The model, dataloaders, loss function, optimizer, learning rate scheduler, and device are passed as arguments
model = feature_inference(model, dataloaders, optimizer, device, output_folder)
