# Import necessary modules
import torch
import os
import numpy as np
from tqdm import tqdm
from utils.txt_operation import save_txt



# Define a function to train the model
def feature_inference(model, dataloaders, optimizer, device, output_folder):

    for phase in ['check', 'ref']:
        if phase == 'check':
            save_path = os.path.join(output_folder, 'check')
        else:
            save_path = os.path.join(output_folder, 'ref')

        # Use tqdm for progress bar
        pbar = tqdm(total=len(dataloaders[phase]), desc=f'Processing {phase}')
        # Iterate over mini-batches
        for inputs, labels, filename in dataloaders[phase]:
            # Move input and label tensors to the default device (GPU or CPU)
            inputs = inputs.to(device)
            # labels = labels.to(device)

            # Clear the gradients of all optimized variables
            optimizer.zero_grad()

            # Forward pass: compute predicted outputs by passing inputs to the model
            # with torch.set_grad_enabled(False):
            with torch.no_grad():  # Only calculate gradients in training phase

                # get the dinov2 result
                outputs = model(inputs)
                # save the output data as txt file
                save_txt(os.path.join(save_path, os.path.splitext(filename[0])[0]), outputs, output_folder, process='inference')
            # update pbar
            pbar.update(1)
        pbar.close()
    print(f"Result Data already save into {output_folder}")
    print("Finish Progress")
