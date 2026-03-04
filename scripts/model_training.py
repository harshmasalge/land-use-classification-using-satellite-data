import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your prepared data

X_train = np.load("data/processed/X_train.npy", allow_pickle=True)
y_train = np.load("data/processed/y_train.npy", allow_pickle=True)

# Encode labels
le = LabelEncoder()
y_train_enc = le.fit_transform(y_train)

# Save label encoder for evaluation file
joblib.dump(le, "models/label_encoder.pkl")

num_classes = len(le.classes_)

# Dataset class

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

# Transforms

transform = transforms.Compose([
    transforms.Resize((128,128)),
    transforms.ToTensor(),
])

train_dataset = LandUseDataset(X_train, y_train_enc, "data/processed/inside_images", transform)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)


# Model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18(pretrained=True)
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop

epochs = 5

for epoch in range(epochs):
    model.train()
    running_loss = 0

    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss/len(train_loader):.4f}")

# Save model

torch.save(model.state_dict(), "models/resnet18_landuse.pth")
print("Model saved successfully.")