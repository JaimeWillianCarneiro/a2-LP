import numpy as np

def angle_between_vectors(u, v):
    # Calcula o produto escalar
    dot_product = np.dot(u, v)
    # Calcula as normas dos vetores
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    # Calcula o cosseno do ângulo
    cos_theta = dot_product / (norm_u * norm_v)
    # # Garante que o valor esteja no intervalo [-1, 1] para evitar erros numéricos
    # cos_theta = np.clip(cos_theta, -1.0, 1.0)
    # # Calcula o ângulo em radianos
    # theta = np.arccos(cos_theta)
    return cos_theta

# Exemplo de uso
v = np.array([1, 0])
u = np.array([0, 1])

angulo = angle_between_vectors(u, v)
print(f"Ângulo em radianos: {angulo}")
print(f"Ângulo em graus: {np.degrees(angulo)}")