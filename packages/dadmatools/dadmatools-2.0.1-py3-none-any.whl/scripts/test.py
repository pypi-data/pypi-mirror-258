import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))



from dadmatools.pipeline import Pipeline

# nlp = Pipeline('lem,pos,ner,dep,cons,spellchecker,kasreh,sent,itf')
nlp = Pipeline('lem,pos,ner,dep')

# text = 'اینو اگه خواستین میتونین تست کنین واسه تبدیل'
text = 'به مدرسه برویم.'
# text = 'غذا گرم رسید کیفیت و پخت گوشت عالی بود'
# text = [['امیری', 'خاطرنشان', 'کرد', ':', 'امسال', 'شرایط', 'بروز', 'طغیان', 'اسهال', 'آبکی', 'و', 'خونی', 'و', 'همچنین', 'وبا', 'و', 'بیماری های', 'عفونی', 'مساعد', 'است', 'که', 'این', 'بیماری ها', 'در', 'فصل', 'تابستان', 'و', 'پاییز', 'بیشتر', 'بروز', 'پیدا', 'می کند', '.']]

doc = nlp(text)
print(doc)
#######################################################################################

# from dadmatools.pipeline import Pipeline
# from tqdm import tqdm

# with open(CURRENT_DIR + '/text.txt') as f:
#     text = f.read()
#     print(len(text))

# # nlp = Pipeline('lem,pos,ner,dep,cons,spellchecker,kasreh,sent,itf')
# nlp = Pipeline('ner')
# # text = 'غذا گرم رسید کیفیت و پخت گوشت عالی بود'

# for i in tqdm(range(1000000)):
#     doc = nlp(text)
    

#######################################################################################

# from dadmatools.datasets import SnappfoodSentiment
# from dadmatools.pipeline.tpipeline import TPipeline
# data = SnappfoodSentiment()

# with open('scripts/sent_train.txt', 'w') as f:
#     for i in data.train:
#         f.write(f'{i["comment"]}\t{i["label"]}\n')
#         # break

# with open('scripts/sent_test.txt', 'w') as f:
#     for index, sample in enumerate(data.test):
#         f.write(f'{sample["comment"]}\t{sample["label"]}\n')
#         # break
#         if index > 9:
#             break

# trainer = TPipeline(
#     training_config={
#       'max_epoch': 10,
#       'embedding': 'xlm-roberta-base',
#       'category': 'customized-sent',  # pipeline category
#       'task': 'sentiment', # task name
#       'save_dir': 'scripts', # directory to save the trained model
#       'train_bio_fpath': 'scripts/sent_train.txt', # training data in BIO format
#       'dev_bio_fpath': 'scripts/sent_test.txt' # training data in BIO format
#     }
# )

# trainer.train()

################################################


# import dadmatools.pipeline.language as language
# from dadmatools.datasets import SnappfoodSentiment
# from tqdm import tqdm

# # as tokenizer is the default tool, it will be loaded even without calling
# pips = 'sent'
# nlp = language.Pipeline(pips)

# data = SnappfoodSentiment()

# result = {
#     'total_count': 0,
#     'total_sad': 0,
#     'total_happy': 0,
#     'tp_sad': 0,
#     'tp_happy': 0,
# }
# for i in tqdm(data.test):
#     result['total_count'] += 1
#     doc = nlp(i['comment'])

#     label = 'SAD' if doc['sentiment']['SAD'] > doc['sentiment']['HAPPY'] else 'HAPPY'


#     if i['label'] == 'SAD':
#         result['total_sad'] += 1
#         if i['label'] == label:
#             result['tp_sad'] += 1

#     elif i['label'] == 'HAPPY':
#         result['total_happy'] += 1
#         if i['label'] == label:
#             result['tp_happy'] += 1

# result['tp_sad'] = result['tp_sad'] / result['total_sad']
# result['tp_happy'] = result['tp_happy'] / result['total_happy']
# print(result)

##############################################################################
# from dadmatools.pipeline import Pipeline

# nlp = Pipeline('')

# text = '8 جا زدم فقط 2 جا پول دادم😂😂😂'

# doc = nlp(text)
# print(doc)

###############################################################################
# import emoji

# def split_emojis(words):
#     emoji_chars = emoji.unicode_codes.get_emoji_unicode_dict('en').values()
#     emoji_list = []
#     text_list = []

#     for word in words:
#         if any(char in emoji_chars for char in word):
#             # Split emojis from the word and add them separately to the emoji list
#             emoji_parts = [char for char in word if char in emoji_chars]
#             emoji_list.extend(emoji_parts)
            
#             # Remove emojis from the original word
#             word = ''.join(char for char in word if char not in emoji_chars)
            
#             if word:  # Add the modified word to the text list if it's not empty
#                 text_list.append(word)
#         else:
#             text_list.append(word)

#     return text_list, emoji_list

# # Example usage:
# input_list = [['8', 'جا', 'زدم', '😂😂فقط', '2', 'جا', 'پول', 'دادم😂😂', '😂']]
# modified_list = [split_emojis(words) for words in input_list]

# print(modified_list)


# import emoji
# emoji_chars = emoji.unicode_codes.get_emoji_unicode_dict('en').values()
# def tokenize_with_emojis(tokens):
#     emoji_tokens = []

#     for token in tokens:
#         if any(char in emoji_chars for char in token):
#             emoji_parts = [char for char in token if char in emoji_chars]
#             emoji_tokens.extend(emoji_parts)
#         else:
#             emoji_tokens.append(token)

#     return emoji_tokens

# # Example usage:
# input_list = [['8', 'جا', 'زدم', '😂😂فقط', '2', 'جا', 'پول', 'دادم😂😂', '😂']]
# modified_list = [tokenize_with_emojis(words) for words in input_list]

# print("Tokenized Text:", modified_list)


###########################################################

