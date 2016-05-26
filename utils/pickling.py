def pickle_data(data, filename):
    """
    Pickle data

    input
    -----
    data : any data construct. the data
        to be pickled.
    filename : string. name of file to 
        output with full path name.
    """
    import cPickle as pickle
    pkl_file = open(filename, 'wb')
    pickle.dump(data, pkl_file)
    pkl_file.close()

def read_pickled_data(filename):
    """
    Read the pickled data

    input
    -----
    filename : string. name of file that 
        contains pickled data

    output
    ------
    the unpickled data
    """
    import cPickle as pickle
    pkl_file = open(filename, 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()
    return data
