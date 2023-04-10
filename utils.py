import pickle

def write_pickle_file(data, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)

def read_pickle_file(file_path):
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data

if __name__ == "__main__":
    # Sample data to pickle
    sample_data = {'key': 'value'}

    # Path to the pickle file
    pickle_file_path = 'sample.pickle'

    # Write the data to the pickle file
    write_pickle_file(sample_data, pickle_file_path)

    # Read the data from the pickle file
    loaded_data = read_pickle_file(pickle_file_path)
    print(loaded_data)   # Output: {'key': 'value'}