from tqdm import tqdm
import torch
import torch.nn as nn
from torch.autograd import no_grad
import numpy as np


def full_vt(epoch, model, data, prefix, writer=None):
    print(prefix + ' start...')
    model.eval()

    with no_grad():
        precision, recall, ndcg_score, hk, hk_recall = model.full_accuracy(data, topk=20)
        print('---------------------------------{0}-th Precition:{1:.4f} Recall:{2:.4f} NDCG:{3:.4f} '
              'HK@20:{4:.4f} HK_Recall@20:{5:.4f} ---------------------------------'.format(
                epoch, precision, recall, ndcg_score, hk, hk_recall))
        if writer is not None:
            writer.add_scalar(prefix + '_Precition', precision, epoch)
            writer.add_scalar(prefix + '_Recall', recall, epoch)
            writer.add_scalar(prefix + '_NDCG', ndcg_score, epoch)
            writer.add_scalar(prefix + '_Hk', hk, epoch)
            writer.add_scalar(prefix + '_Hk_Recall', hk_recall, epoch)

            writer.add_histogram(prefix + '_visual_distribution', model.v_rep, epoch)
            writer.add_histogram(prefix + '_acoustic_distribution', model.a_rep, epoch)
            writer.add_histogram(prefix + '_textual_distribution', model.t_rep, epoch)

            writer.add_histogram(prefix + '_user_visual_distribution', model.user_preferences[:, :44], epoch)
            writer.add_histogram(prefix + '_user_acoustic_distribution', model.user_preferences[:, 44:-44], epoch)
            writer.add_histogram(prefix + '_user_textual_distribution', model.user_preferences[:, -44:], epoch)

            writer.add_embedding(model.v_rep)
            # writer.add_embedding(model.a_rep)
            # writer.add_embedding(model.t_rep)

            # writer.add_embedding(model.user_preferences[:,:44])
            # writer.add_embedding(model.user_preferences[:, 44:-44])
            # writer.add_embedding(model.user_preferences[:, -44:])
        return precision, recall, ndcg_score, hk, hk_recall
