import matplotlib.pyplot as plt

def plot_acc(history, experiment):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig('./plots/model_acc_{}.png'.format(experiment))
    plt.close()

def plot_loss(history, experiment):
    plt.figure(0)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig('./plots/model_loss_{}.png'.format(experiment))
    plt.close()