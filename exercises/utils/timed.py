from timeit import default_timer as timer

class timed:
    def __init__(self, label="Elapsed"):
        self.label = label

    def __enter__(self):
        self.start = timer()
        return self

    def __exit__(self, exc_type, exc, tb):
        end = timer()
        print(f"{self.label}: {end - self.start:.6f} seconds")