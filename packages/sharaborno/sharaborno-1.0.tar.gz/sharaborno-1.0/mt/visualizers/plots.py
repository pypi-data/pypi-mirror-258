import os.path

import matplotlib.pyplot as plt
import mt

import matplotlib.pyplot as plt


def save_loss_plot(history):
    # Plotting
    plt.plot(history.history['loss'], label='Training Loss', color='blue', linestyle='-')
    plt.plot(history.history['val_loss'], label='Validation Loss', color='orange', linestyle='--')
    plt.ylim([0, max(max(history.history['loss']), max(history.history['val_loss']))])
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Cross Entropy per Token', fontsize=12)
    plt.title('Training and Validation Loss', fontsize=14)
    plt.legend()
    plt.grid(True)

    # Save plot
    plot_path = os.path.join(mt.utils.const.configs["report_dir"], "figures", "loss_plot.jpg")
    plt.savefig(plot_path)
    plt.close()  # Close the plot to prevent overlapping when plotting multiple figures


def save_accuracy_plot(history):
    # Plotting
    plt.plot(history.history['masked_acc'], label='Training Accuracy', color='green', linestyle='-')
    plt.plot(history.history['val_masked_acc'], label='Validation Accuracy', color='red', linestyle='--')
    plt.ylim([0, max(max(history.history['masked_acc']), max(history.history['val_masked_acc']))])
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.title('Training and Validation Accuracy', fontsize=14)
    plt.legend()
    plt.grid(True)

    # Save plot
    plot_path = os.path.join(mt.utils.const.configs["report_dir"], "figures", "accuracy_plot.jpg")
    plt.savefig(plot_path)
    plt.close()  # Close the plot to prevent overlapping when plotting multiple figures
