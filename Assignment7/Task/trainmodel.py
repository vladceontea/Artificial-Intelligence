
from matplotlib import pyplot as plt

from myModel import *


def train():
    data = torch.load("mydataset.dat")

    input_data = data.narrow(1, 0, 2)
    output_data = data.narrow(1, 2, 1)

    lossFunction = torch.nn.MSELoss()

    # we create the ANN
    ann = Net(n_feature=2, n_hidden=40, n_output=1)

    print(ann)
    # we use an optimizer that implements stochastic gradient descent
    optimizer_batch = torch.optim.SGD(ann.parameters(), lr=0.08)

    # we memorize the losses for some graphics
    loss_list = []

    batch_size = 20
    n_batches = int(len(data) / batch_size)

    for epoch in range(3000):
        for batch in range(n_batches):
            #compute output for batch
            batch_input, batch_output = input_data[batch * batch_size:(batch + 1) * batch_size, ], \
                                        output_data[batch * batch_size:(batch + 1) * batch_size, ]

            #print(batch_input)
            #print(batch_output)

            prediction = ann(batch_input)

            #print(prediction)

            #compute loss for batch
            loss = lossFunction(prediction, batch_output)
            #print(loss)
            loss_list.append(loss.item())

            #set up the gradients for the weights to zero
            optimizer_batch.zero_grad()

            #compute automatically the variation for each weight (and bias) of the network
            loss.backward()

            #compute the new values for the weights
            optimizer_batch.step()

        #print loss for the dataset for each 10th epoch
        if epoch % 100 == 99:
            y_pred = ann(input_data)
            loss = lossFunction(y_pred, output_data)
            print('\repoch: {}\tLoss =  {:.5f}'.format(epoch, loss))

    plt.plot(loss_list)
    plt.savefig("loss.png")
    plt.show()

    return ann


def save_to_file():
    ann = train()
    torch.save(ann.state_dict(), "myNetwork.pt")


save_to_file()
