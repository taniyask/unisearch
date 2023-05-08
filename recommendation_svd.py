import pandas as pd
import numpy as np
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import MinMaxScaler

results = []

def model(gre_verbal, gre_quant, ielts_score, undergrad_gpa):
    # Read in the data from the csv file
    data = pd.read_csv("univ.csv")

    # # Define the user inputs
    # gre_verbal = float(input("Enter your GRE verbal score (0-170): "))
    # gre_quant = float(input("Enter your GRE quant score (0-170): "))
    # ielts_score = float(input("Enter your IELTS score (0-9): "))
    # college_tier = int(input("Enter the tier of your undergraduate college (1-4): "))
    # undergrad_gpa = float(input("Enter your undergraduate GPA (0-4): "))
    # work_exp = int(input("Enter the number of years of work experience in related field: "))

    # Define the user inputs
    # gre_verbal = 165
    # gre_quant = 125
    # ielts_score = 7
    # college_tier = 1
    # undergrad_gpa = 4
    # work_exp = 0

    # Normalize the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data.iloc[:, 4:8])

    # Apply SVD to the scaled data
    svd = TruncatedSVD(n_components=2, random_state=42)
    svd_data = svd.fit_transform(scaled_data)

    # Define the user input vector
    user_vector = np.array([gre_verbal, gre_quant, ielts_score, undergrad_gpa]).reshape(1, -1)
    scaled_user_vector = scaler.transform(user_vector)

    # Apply SVD to the user input vector
    user_svd = svd.transform(scaled_user_vector)

    # Calculate the predicted scores using SVD
    scores = np.dot(user_svd, svd_data.T)
    data['predicted_score'] = scores[0]

    # Recommend the top 3 universities based on predicted scores
    recommendations = data.sort_values(by='predicted_score', ascending=False).head(3)
    results = []
    
    for index, row in recommendations.iterrows():
        results.append([row['UNI_NAME'], row['Location'], row['Link'], "static/img/"+str(row['QS_Ranking'])+".png"])
        print(row['UNI_NAME'], row['Location'], row['Link'], row['QS_Ranking'])
    return results