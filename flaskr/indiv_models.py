import torch
from transformers import *
import pandas as pd
# import numpy as np
import os


class PositiveRatioModel:

    def __init__(self):
        # Load a trained model and vocabulary that you have fine-tuned
        # self.initModel()
        print("PRM: ", os.listdir(os.curdir))
        self.output_dir = '/app/model/'
        # self.tokenizer = BertTokenizer.from_pretrained(
        #     "https://indivprojcht116.s3.eu-west-2.amazonaws.com/model")
        # self.model = BertForSequenceClassification.from_pretrained(
        #     "https://indivprojcht116.s3.eu-west-2.amazonaws.com/model")
        self.tokenizer = BertTokenizer.from_pretrained(self.output_dir)
        self.model = BertForSequenceClassification.from_pretrained(
            self.output_dir)
        self.setDevice()

    # def initModel(self):
    #     q = Queue('dl', connection=conn)
    #     # util.downloadDirectoryFroms3("indivprojcht116", "model")
    #     job = q.enqueue(util.downloadDirectoryFroms3,
    #               "indivprojcht116", "model")

    def setDevice(self):
        # If there's a GPU available...
        if torch.cuda.is_available():

            # Tell PyTorch to use the GPU.
            device = torch.device("cuda")

            print('There are %d GPU(s) available.' % torch.cuda.device_count())

            print('We will use the GPU:', torch.cuda.get_device_name(0))

        # If not...
        else:
            print('No GPU available, using the CPU instead.')
            device = torch.device("cpu")
        # Copy the model to the GPU.

        self.model.to(device)

    def predict(self, articles):

        # Load the dataset into a pandas dataframe.
        df = pd.DataFrame(articles)
        print("DF MEMORY USAGE: ", df.memory_usage())

        # Report the number of sentences.
        print('Number of test sentences: {:,}\n'.format(df.shape[0]))

        # Create sentence and label lists
        sentences = df.title.values
        # labels = df.label.values

        # Tokenize all of the sentences and map the tokens to thier word IDs.
        input_ids = []

        # For every sentence...
        for sent in sentences:
            # `encode` will:
            #   (1) Tokenize the sentence.
            #   (2) Prepend the `[CLS]` token to the start.
            #   (3) Append the `[SEP]` token to the end.
            #   (4) Map tokens to their IDs.
            encoded_sent = self.tokenizer.encode(
                sent,                      # Sentence to encode.
                add_special_tokens=True,  # Add '[CLS]' and '[SEP]'
                pad_to_max_length=True,
                max_length=30,
            )

            input_ids.append(encoded_sent)

        # Create attention masks
        attention_masks = []

        # Create a mask of 1s for each token followed by 0s for padding
        for seq in input_ids:
            seq_mask = [float(i > 0) for i in seq]
            attention_masks.append(seq_mask)

        # Convert to tensors.
        prediction_inputs = torch.tensor(input_ids)
        prediction_masks = torch.tensor(attention_masks)
        # prediction_labels = torch.FloatTensor(labels)

        with torch.no_grad():
            # print(input_ids)
            outputs = self.model(prediction_inputs, token_type_ids=None,
                                 attention_mask=prediction_masks)

        logits = outputs[0]

        scores = logits.reshape(-1).tolist()
        return scores
        # # Set the batch size.
        # batch_size = 32

        # # Create the DataLoader.
        # prediction_data = TensorDataset(
        #     prediction_inputs, prediction_masks, prediction_labels)
        # prediction_sampler = SequentialSampler(prediction_data)
        # prediction_dataloader = DataLoader(
        #     prediction_data, sampler=prediction_sampler, batch_size=batch_size)
