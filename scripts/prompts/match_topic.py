import pandas as pd
import sys

def find_matching_lines(file1, file2, predict_all_file, element):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines_file1 = f1.readlines()
        lines_file2 = f2.readlines()
        predict_all_df = pd.read_csv(predict_all_file)

        matches = []
        for line_num, line_file1 in enumerate(lines_file1, start=1):
            for idx, line_file2 in enumerate(lines_file2, start=1):
                if line_file1.strip() == line_file2.strip():
                    if line_num != 1:
                        predicted_row = predict_all_df[predict_all_df['text_index'] == idx - 1]
                        matches.append({'Line_num': line_num - 1, 'all_idx': idx, 'topic': predicted_row['predicted_topic'].values[0]})
                        break
        output_df = pd.DataFrame(matches)
        output_df.to_csv('./' + element + '_output.csv', index=False)
    

def main():
    if len(sys.argv) != 2:
        print("Usage: python match_topic.py <element>")
        print("Usage: <element> is either formula, image, or pseudocode")
        return
    
    element = sys.argv[1]

    test_file = './' + element + 'test.csv'
    all_file = './' + element + '/all.csv'
    predict_all_file = './' + element + '/predict_all.csv'

    find_matching_lines(test_file, all_file, predict_all_file, element)

if __name__ == "__main__":
    main()
