import numpy as np

class Dataset:
    def __init__(self, length=10, d=3, batch_size=1):
        self.input_data = np.random.random((length, d))
        self.batch_size = batch_size

    def __iter__(self):
        _buffer = []
        while True:
            for x in self.input_data:
                _buffer.append(x)
                if len(_buffer) >= self.batch_size:
                    yield np.stack(_buffer)
                    del _buffer[:]

    def __len__(self):
        return self.input_data.shape[0]

