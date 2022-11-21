import emoji
import pandas as pd
from tqdm import tqdm

tqdm.pandas()


def read_corpus(file_path):
    data = []
    with open(file_path, 'r') as file:
        current_str = ''
        for line in tqdm(file):
            if line == '\n':
                data.append(current_str)
                current_str = ''
            else:
                line = line.replace('\n', ' ')
                current_str += line
    return data


def main(file_name):
    data = read_corpus(file_name)
    df = pd.DataFrame(data=data, columns=['text'])
    df['n_emoji'] = df.progress_apply(
        lambda row: emoji.emoji_count(row['text']),
        axis=1
    )
    df['has_emoji'] = df.progress_apply(
        lambda row: row['n_emoji'] != 0,
        axis=1
    )
    print(df['has_emoji'].value_counts())
    print(df['has_emoji'].value_counts() / df.shape[0])
    total_words = len(data)
    total_emojis = df['n_emoji'].sum()
    print(total_emojis, total_words, total_emojis / total_words)


if __name__ == '__main__':
    main('full.txt')
