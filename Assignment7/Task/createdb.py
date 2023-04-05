import torch


def create_db():
    #create 1000 pairs of 2 numbers in the interval [-10, 10]
    input_data = 20*torch.rand(1000, 2)-10

    # compute f(x1,x2) = sin(x1 + x2/pi) for each point
    output_data = []

    for data in input_data:
        output_data.append(torch.sin(data[0] + data[1]/torch.pi))

    output_data = torch.tensor(output_data)

    return torch.column_stack((input_data, output_data))


def save_db():
    data = create_db()
    torch.save(data, "mydataset.dat")
