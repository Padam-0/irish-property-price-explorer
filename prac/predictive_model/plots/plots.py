import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def room_transform20(string):
    if string >=20:
        return 20
    else:
        return string

def room_transform5(string):
    if string >=5:
        return 5
    else:
        return string


def bar_plot(df):
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

    bath_df = df[['bed', 'bath']].groupby(['bath']).count().reset_index()
    bed_df = df[['bed', 'bath']].groupby(['bed']).count().reset_index()

    label = [0, 1, 2, 3, 4, 5]
    ax1.bar(bath_df.bath, bath_df.bed, width=0.7, color='b')
    ax1.set_xlabel('Number of bathrooms')
    ax1.set_ylabel('Count')
    ax1.set_title('Number of Bathrooms - 5 Bath Max')
    ax1.set_xticks(np.arange(6) + 0.8 / 2)
    ax1.set_xticklabels(label, rotation=0, minor=False)

    labels = [1, 2, 3, 4, 5]
    ax2.bar(bed_df.bed, bed_df.bath, width=0.7, color='r')
    ax2.set_xlabel('Number of bedrooms')
    ax2.set_ylabel('Count')
    ax2.set_title('Number of Bedrooms - 5 Bed Max')
    ax2.set_xticks(np.arange(5) + 1 + 0.8 / 2)
    ax2.set_xticklabels(labels, rotation=0, minor=False)

    # df['bed'] = df['bed'].apply(lambda x: room_transform2(x))
    # df['bath'] = df['bath'].apply(lambda x: room_transform2(x))

    # df_new = df[['bed', 'bath']].groupby(['bath']).count().reset_index()
    # print(df_new.head())
    #
    # labels = [1,2,3,4,5]
    # ax3.bar(df_new.bath, df_new.bed, width=0.7, color='r')
    # ax3.set_xlabel('Number of bathrooms')
    # ax3.set_ylabel('Count')
    # ax3.set_title('Number of Bathrooms - 5 Bath Max')
    # ax3.set_xticks(np.arange(5) + 1 + 0.8 / 2)
    # ax3.set_xticklabels(labels, rotation=0, minor=False)
    plt.axis('tight')
    plt.show()


def fancy_bar_plot(df):
    bath_df = df[['bed', 'bath']].groupby(['bath']).count().reset_index()
    bed_df = df[['bed', 'bath']].groupby(['bed']).count().reset_index()

    sns.set_style("white")
    plt.rc('font', family='Raleway')
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False)

    # label = [0, 1, 2, 3, 4, 5]
    sns.barplot(bath_df.bath, bath_df.bed, color='#05084e', ax=ax1)
    ax1.set_xlabel('Number of bathrooms', fontsize=16)
    ax1.set_ylabel('Count', fontsize=16)
    ax1.set_title('Bathroom - Room Count', fontsize=18)
    # ax1.set_xticks(np.arange(6))
    # ax1.set_xticklabels(label, rotation=0, minor=False)

    # labels = [1, 2, 3, 4, 5]
    sns.barplot(bed_df.bed, bed_df.bath, color='#b32650', ax=ax2)
    ax2.set_xlabel('Number of bedrooms', fontsize=16)
    ax2.set_ylabel('Count', fontsize=16)
    ax2.set_title('Bedroom  - Room Count', fontsize=18)
    # ax2.set_xticks(np.arange(5))
    # ax2.set_xticklabels(labels, rotation=0, minor=False)

    sns.despine()
    plt.show()


def main():
    # Data Import
    # df = pd.read_csv('model_data_model_split.csv', encoding='latin1', index_col=0)
    df = pd.read_csv('../model_data_final.csv', encoding='latin1', index_col=0)

    # Refactor bed and bath data
    df['bed'] = df['bed'].apply(lambda x: room_transform20(x)).astype(int)
    df['bath'] = df['bath'].apply(lambda x: room_transform20(x)).astype(int)

    # Plots
    # bar_plot(df)
    fancy_bar_plot(df)

if __name__ == '__main__':
    main()