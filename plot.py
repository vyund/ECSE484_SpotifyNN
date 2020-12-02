import matplotlib.pyplot as plt
import seaborn as sns

def plot_acc(history, num_classes, experiment):
    plt.plot(history.history['accuracy'], color='darkgreen')
    plt.plot(history.history['val_accuracy'], color='salmon')
    plt.title('{}-{} model accuracy'.format(num_classes, experiment))
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig('./plots/model_acc_{}{}s.png'.format(num_classes, experiment))
    plt.close()

def plot_loss(history, num_classes, experiment):
    plt.plot(history.history['loss'], color='darkgreen')
    plt.plot(history.history['val_loss'], color='salmon')
    plt.title('{}-{} model loss'.format(num_classes, experiment))
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.savefig('./plots/model_loss_{}{}s.png'.format(num_classes, experiment))
    plt.close()

def plot_cm(confusion_matrix, classes, num_classes, experiment):
    plt.figure(figsize=(8,6))
    sns.heatmap(confusion_matrix, xticklabels=classes, yticklabels=classes, annot=True, cmap='BuGn')
    plt.title('{}-{} model confusion matrix'.format(num_classes, experiment))
    plt.xlabel('Pred')
    plt.ylabel('True')
    plt.savefig('./plots/model_cm_{}{}s.png'.format(num_classes, experiment))
    plt.close()