
import math


def dot_product(A, B):
    if len(A) != len(B):
        raise ValueError("Vectors must have the same length")

    return sum(a * b for a, b in zip(A, B))


def magnitude(A):
    return math.sqrt(sum(a ** 2 for a in A))


def cosine_similarity(A, B):
    mag_A = magnitude(A)
    mag_B = magnitude(B)

    if mag_A == 0 or mag_B == 0:
        raise ValueError("Zero vectors cannot be compared")

    return dot_product(A, B) / (mag_A * mag_B)


if __name__ == "__main__":
    vector_A = [2, 4, 1]
    vector_B = [1, 3, 5]

    score = cosine_similarity(vector_A, vector_B)

    print("Vector A:", vector_A)
    print("Vector B:", vector_B)
    print("Cosine Similarity:", round(score, 4))
