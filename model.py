import torch
import torch.nn as nn
from torch.hub import load
import torchvision.models as models


dino_backbones = {
    'dinov2_s':{
        'name':'dinov2_vits14',
        'embedding_size':384,
        'patch_size':14
    },
    'dinov2_b':{
        'name':'dinov2_vitb14',
        'embedding_size':768,
        'patch_size':14
    },
    'dinov2_l':{
        'name':'dinov2_vitl14',
        'embedding_size':1024,
        'patch_size':14
    },
    'dinov2_g':{
        'name':'dinov2_vitg14',
        'embedding_size':1536,
        'patch_size':14
    },
}





class model_process(nn.Module):
    def __init__(self, backbone='dinov2_s'):
        super(model_process, self).__init__()
        # self.heads = {
        #     'linear':linear_head
        # }
        self.backbones = dino_backbones
        self.backbone = load('facebookresearch/dinov2', self.backbones[backbone]['name'])
        self.backbone.eval()
        # self.head = self.heads[head](self.backbones[backbone]['embedding_size'],num_classes)

    def forward(self, x):
        with torch.no_grad():
            x = self.backbone(x)
        return x


