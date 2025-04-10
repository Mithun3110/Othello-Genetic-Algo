import random

class Genes:
    def __init__(self, edges_w, corners_w, centres_w, diagonals_w, stability_w, coin_diff_w):
        self.edges_w = edges_w
        self.corners_w = corners_w
        self.centres_w = centres_w
        self.diagonals_w = diagonals_w
        self.stability_w = stability_w
        self.coin_diff_w = coin_diff_w

    def create_random(self):
        self.edges_w = random.uniform(-1.0, 1.0)
        self.corners_w = random.uniform(-1.0, 1.0)
        self.centres_w = random.uniform(-1.0, 1.0)
        self.diagonals_w = random.uniform(-1.0, 1.0)
        self.stability_w = random.uniform(-1.0, 1.0)
        self.coin_diff_w = random.uniform(-1.0, 1.0)

    