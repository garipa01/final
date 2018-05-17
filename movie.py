class Movie:
    def __init__(self):
        self.movie = ""
        self.length = 0

    def __str__(self):
        return self.movie

    def add(self,char):
        self.movie += char
        self.length += 1
        return self.movie
    
    def get(self):
        return self.movie

    def reset(self):
        self.movie = ""
        self.length = 0
        return self.movie
    
    def __len__(self):
        return self.length
    
    def remove(self):
        self.movie = self.movie[:-1]
        self.length -= 1
        return self.movie