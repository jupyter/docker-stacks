# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import torch

print(torch.tensor([[1.0, 4.0, 7.0], [4.0, 9.0, 11.0]]))

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
# Create large tensors
size = 10000
torch.randn(size, size, device=device)
