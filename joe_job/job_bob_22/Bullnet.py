import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)

class Bullnet(nn.Module):

    def __init__(self, embedding_sizes, input_size):
        super(Bullnet, self).__init__()
        self.embedding_sizes = embedding_sizes
        self.input_size = input_size
        self.n_embeddings = len(embedding_sizes)
        self.n_non_cat = input_size - self.n_embeddings
        # define network layers
        self.embedding_layers = [nn.Embedding(cat_size, emb_size)
                                 for (cat_size, emb_size) in self.embedding_sizes]
        self.linear1 = nn.Linear(input_size, 1028)
        self.linear2 = nn.Linear(1028, 1)

    def forward(self, cat_input, non_cat_input):
        embeddings = []
        for i in range(self.n_embeddings):
            embed = self.embedding_layers[i](cat_input[:,i])
            embeddings.append(embed.type('torch.FloatTensor'))
        inputs_ls = embeddings + [non_cat_input]
        inpts = torch.cat(inputs_ls, dim=1)
        out1 = F.relu(self.linear1(inpts))
        out2 = self.linear2(out1)
        return out2.view(-1)
