import torch
import numpy as np
from glob import glob
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as tfm
from collections import defaultdict
import matplotlib.pyplot as plt



import myparser

default_transform = tfm.Compose([
    tfm.ToTensor(),
    tfm.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])




class TrainDataset(Dataset):
    def __init__(
        self,
        dataset_folder,
        img_per_place=4,
        min_img_per_place=4,
        transform=default_transform,
    ):
        super().__init__()
        self.dataset_folder = dataset_folder
        self.images_paths = sorted(glob(f"{dataset_folder}/**/*.jpg", recursive=True))
        if len(self.images_paths) == 0:
            raise FileNotFoundError(f"There are no images under {dataset_folder} , you should change this path")
        self.dict_place_paths = defaultdict(list)
        for image_path in self.images_paths:
            place_id = image_path.split("@")[-2]
            self.dict_place_paths[place_id].append(image_path)

        assert img_per_place <= min_img_per_place, \
            f"img_per_place should be less than {min_img_per_place}"
        self.img_per_place = img_per_place
        self.transform = transform

        # keep only places depicted by at least min_img_per_place images
        for place_id in list(self.dict_place_paths.keys()):
            all_paths_from_place_id = self.dict_place_paths[place_id]
            if len(all_paths_from_place_id) < min_img_per_place:
                del self.dict_place_paths[place_id]
        self.places_ids = sorted(list(self.dict_place_paths.keys()))
        self.total_num_images = sum([len(paths) for paths in self.dict_place_paths.values()])

    

    def __getitem__(self, index):
        
        args = myparser.parse_arguments()
         
        place_id = self.places_ids[index]
        
        all_paths_from_place_id = self.dict_place_paths[place_id]
        
        chosen_paths = np.random.choice(all_paths_from_place_id, self.img_per_place)
        
        images = [Image.open(path).convert('RGB') for path in chosen_paths]

        
        if args.self_supervised_learning:
            
            image = Image.open(chosen_paths[0]).convert('RGB')  #code line to highlight the self-sup. approach
            img = self.transform(image)
            
            #i = tfm.functional.to_pil_image(img[0], mode=None)
            #j = torchvision.transforms.functional.to_pil_image(img[1], mode=None)
            #i.show(); #j.show()
            img1 = np.array(img)
            plt.imshow(img1)
            plt.show()
            return torch.stack((img[0], img[1])), torch.tensor(index).repeat(2)   #number of final augmented images
        
        if args.soft_supervised_learning:
            #images= Image.open((chosen_paths[0], chosen_paths[1])).convert('RGB')
            image = [self.transform(img) for img in images]
            return torch.stack(image), torch.tensor(index).repeat(2)
        else:
            images = [Image.open(path).convert('RGB') for path in chosen_paths]
            images = [self.transform(img) for img in images]
            return torch.stack(images), torch.tensor(index).repeat(self.img_per_place)

    def __len__(self):
        """Denotes the total number of places (not images)"""
        return len(self.places_ids)
