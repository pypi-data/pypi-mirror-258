from openai import OpenAI

import json
from tqdm import tqdm
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def get_list_of_unique_labels(train_bio_fpath, spliter=None, label_convertor=None):
    labels = set()
    with open(train_bio_fpath) as f:
        for line in f:
            if line == '\n':
                continue

            if spliter:
                line_list = line.split(spliter)
            else:
                line_list = line.split()
            label = line_list[-1].replace('\n', '')
            if label_convertor:
                label = label_convertor(label)
            labels.add(label)

    return list(labels)


def get_dataset(train_bio_fpath, spliter=None, label_convertor=None):
    data = {'tokens': list(), 'tags': list()}
    with open(train_bio_fpath) as f:
        tokens = list()
        tags = list()
        for line in f:
            if line == '\n':
                data['tokens'].append(tokens)
                data['tags'].append(tags)
                tokens = list()
                tags = list()
                continue

            if spliter:
                line_list = line.split(spliter)
            else:
                line_list = line.split()
            label = line_list[-1].replace('\n', '')
            if label_convertor:
                label = label_convertor(label)
            token = line_list[0]

            tags.append(label)
            tokens.append(token)

    return data


def get_chatgpt_ner(client, tokens, unique_labels):
    text = ' \n'.join(tokens)
    content = f"""
    Get the NER the following text in persian in the format of 
    token label.
    the lables should be: {' '.join(unique_labels)}
    text is \n'{text}' 
    """
    responce = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": content}],
    )

    return responce.choices[0].message.content


def remove_prefix(tags):
    return [tag[2:] if tag != 'O' else tag for tag in tags]


def calculate_results(data, unique_labels, save_dir, print_wrong_samples=False, is_remove_prefix=False):
    if is_remove_prefix:
        unique_labels = list(set(remove_prefix(unique_labels)))
    import os, sys
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(CURRENT_DIR))
    from dadmatools.pipeline import Pipeline

    nlp = Pipeline('ner')

    actual_tags = list()
    predicted_tags = list()
    total_iterations = len(data['tags'])
    for tags, tokens in tqdm(zip(data['tags'], data['tokens']), total=total_iterations, disable=print_wrong_samples):
        doc = nlp([tokens])
        pred_tags = [t['ner'] for s in  doc['sentences'] for t in s['tokens']]
        pred_tokens = [t['text'] for s in  doc['sentences'] for t in s['tokens']]
        if is_remove_prefix:
            tags = remove_prefix(tags)
            pred_tags = remove_prefix(pred_tags)
        actual_tags += tags
        predicted_tags += pred_tags

        if print_wrong_samples:
            if pred_tags != tags:
                print([tokens[i] if pred_tags[i] == 'O' and tags[i] == 'O' else f'{tokens[i]} <A:{tags[i]}, P:{pred_tags[i]}>' for i in range(len(tokens))])

    conf_matrix = confusion_matrix(actual_tags, predicted_tags, labels=unique_labels)

    params_name = f'is_remove_prefix={is_remove_prefix}'
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', xticklabels=unique_labels, yticklabels=unique_labels)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')
    plt.savefig(f'{save_dir}/confusion_matrix_{params_name}.png')

    # Calculate precision, recall, and F1-score for each class
    result = {key: list() for key in ['Label', 'Precision', 'Recall', 'F1-Score']}
    for i, tag in enumerate(unique_labels):
        true_positive = conf_matrix[i, i]
        false_positive = np.sum(conf_matrix[:, i]) - true_positive
        false_negative = np.sum(conf_matrix[i, :]) - true_positive

        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        result['Label'].append(tag)
        result['Precision'].append(precision)
        result['Recall'].append(recall)
        result['F1-Score'].append(f1_score)

    overall_precision = np.sum(np.diag(conf_matrix)) / np.sum(conf_matrix)
    overall_recall = np.sum(np.diag(conf_matrix)) / np.sum(conf_matrix, axis=1).sum()
    overall_f1_score = 2 * overall_precision * overall_recall / (overall_precision + overall_recall) if (overall_precision + overall_recall) > 0 else 0

    result['Label'].append('Overall')
    result['Precision'].append(overall_precision)
    result['Recall'].append(overall_recall)
    result['F1-Score'].append(overall_f1_score)

    results_df = pd.DataFrame(result)
    results_df.to_csv(f'{save_dir}/results_{params_name}.csv')
    print(results_df)


def test_current_ner_with_peyma(print_wrong_samples=False, is_remove_prefix=False):
    def peyma_label_convertor(label):
        label_mapper = {
            'I_ORG': 'I-org',
            'B_ORG': 'B-org',
            'I_LOC': 'I-loc',
            'B_LOC': 'B-loc',
            'I_PER': 'I-pers',
            'B_PER': 'B-pers',
        }
        return label_mapper.get(label, 'O')
    
    path = 'scripts/peyma/test.txt'
    data = get_dataset(path, spliter='|', label_convertor=peyma_label_convertor)
    unique_labels = get_list_of_unique_labels(path, spliter='|', label_convertor=peyma_label_convertor)

    calculate_results(data, unique_labels, save_dir='scripts/peyma', print_wrong_samples=print_wrong_samples, is_remove_prefix=is_remove_prefix)

def test_current_ner(print_wrong_samples=False, is_remove_prefix=False):
    path = 'scripts/arman/test.txt'
    data = get_dataset(path)
    unique_labels = get_list_of_unique_labels(path)

    calculate_results(data, unique_labels, save_dir='scripts/arman', print_wrong_samples=print_wrong_samples, is_remove_prefix=is_remove_prefix)


def test_persian_ner(print_wrong_samples=False, is_remove_prefix=False):
    def persian_ner_label_convertor(label):
        label_mapper = {
            'I_ORG': 'I-org',
            'B_ORG': 'B-org',
            'I_LOC': 'I-loc',
            'B_LOC': 'B-loc',
            'I_PER': 'I-pers',
            'B_PER': 'B-pers',
        }
        return label_mapper.get(label, 'O')
    
    path = 'scripts/Persian-NER/Persian-NER-part1.txt'
    data = get_dataset(path, label_convertor=persian_ner_label_convertor)[:100]
    unique_labels = get_list_of_unique_labels(path, label_convertor=persian_ner_label_convertor)

    calculate_results(data, unique_labels, save_dir='scripts/Persian-NER', print_wrong_samples=print_wrong_samples, is_remove_prefix=is_remove_prefix)



def main():
    API_KEY = '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'
  
    client = OpenAI(api_key=API_KEY)
    data = get_dataset('scripts/arman/test.txt')
    unique_labels = get_list_of_unique_labels('scripts/arman/test.txt')

    results = list()
    for tags, tokens in tqdm(zip(data['tags'], data['tokens'])):
        r = get_chatgpt_ner(client, tokens, unique_labels)
        result = {
            'tokens': tokens,
            'tags': tags,
            'chatgpt_responce': r
        }
        results.append(result)

        with open('scripts/arman/test.json', "w", encoding='utf-8') as file:
            json.dump(results, file, indent=4, ensure_ascii=False)
    

if __name__ == '__main__':
    # main()
    # test_current_ner()
    test_current_ner_with_peyma(print_wrong_samples=True, is_remove_prefix=True)
    # test_current_ner_with_peyma(is_remove_prefix=True)
    # test_current_ner(is_remove_prefix=True)
    # test_persian_ner(is_remove_prefix=True)