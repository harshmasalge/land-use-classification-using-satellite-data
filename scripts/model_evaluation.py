import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt

# Load Test Data

X_test = np.load("data/processed/X_test.npy", allow_pickle=True)
y_test = np.load("data/processed/y_test.npy", allow_pickle=True)

le = joblib.load("models/label_encoder.pkl")
y_test_enc = le.transform(y_test)

num_classes = len(le.classes_)

# Dataset

class LandUseDataset(Dataset):
    def __init__(self, image_names, labels, image_dir, transform=None):
        self.image_names = image_names
        self.labels = labels
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.image_names)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.image_names[idx])
        image = Image.open(img_path).convert("RGB")
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label

transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
])

test_dataset = LandUseDataset(X_test, y_test_enc, "data/processed/inside_images", transform)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Load Model


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18(pretrained=False)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load("models/resnet18_landuse.pth"))
model = model.to(device)
model.eval()


# Evaluation

all_preds = []
all_labels = []

with torch.no_grad():
    for images, labels in test_loader:
        images = images.to(device)
        outputs = model(images)
        _, preds = torch.max(outputs, 1)

        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.numpy())

accuracy = accuracy_score(all_labels, all_preds)
f1 = f1_score(all_labels, all_preds, average='weighted')

print("Test Accuracy:", accuracy)
print("Weighted F1 Score:", f1)

# Confusion Matrix

cm = confusion_matrix(all_labels, all_preds)

plt.figure()
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.colorbar(cmap='Greens')

plt.xticks(range(num_classes), le.classes_, rotation=45)
plt.yticks(range(num_classes), le.classes_)

plt.tight_layout()
plt.show()