
from myModel import *

#save_db()

ann = Net(2, 40, 1)
ann.load_state_dict(torch.load("myNetwork.pt"))
ann.eval()


for name, param in ann.named_parameters():
    if param.requires_grad:
        print(name, param.data)

while True:
    command = input("New set of data?Y/N ")
    if command == "N":
        break
    if command == "Y":
        x = float(input("x = "))
        y = float(input("y = "))
        data = torch.tensor([x, y])
        print(ann(data).item())
        print(torch.sin(data[0] + data[1]/torch.pi))
    else:
        print("Not a valid answer")
