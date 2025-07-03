import numpy as np
import matplotlib.pyplot as plt
import hashlib

def get_seed_from_string(input_str):
    hash_digest = hashlib.sha256(input_str.encode()).hexdigest()
    seed = int(hash_digest[:8], 16)
    return seed

def julia_set(width, height, zoom, move_x, move_y, cX, cY, max_iter):
    x = np.linspace(-1.5, 1.5, width) / zoom + move_x
    y = np.linspace(-1.5, 1.5, height) / zoom + move_y
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    C = complex(cX, cY)
    div_time = np.zeros(Z.shape, dtype=int)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C
        mask_new = np.abs(Z) < 1000
        div_time[mask & ~mask_new] = i
        mask = mask & mask_new
    div_time[div_time == 0] = max_iter
    return div_time

def get_character_palette(name):
    name = name.lower()
    if 'sukuna' in name:
        return {'r_base': (0.9, 0.1), 'g_base': (0.1, 0.05), 'b_base': (0.1, 0.05)}  # Red
    elif 'gojo' in name:
        return {'r_base': (0.4, 0.1), 'g_base': (0.2, 0.1), 'b_base': (0.8, 0.1)}  # Blue/purple
    elif 'mahoraga' in name:
        return {'r_base': (0.9, 0.05), 'g_base': (0.9, 0.05), 'b_base': (0.9, 0.05)}  # White/glow
    elif 'megumi' in name:
        return {'r_base': (0.1, 0.05), 'g_base': (0.3, 0.05), 'b_base': (0.4, 0.1)}  # Shadowy blue
    elif 'yuta' in name:
        return {'r_base': (0.5, 0.05), 'g_base': (0.5, 0.05), 'b_base': (0.9, 0.05)}  # Calm blue glow
    elif 'toji' in name:
        return {'r_base': (0.1, 0.1), 'g_base': (0.9, 0.1), 'b_base': (0.1, 0.1)}  # Cursed green
    else:
        # Fallback: random palette
        np.random.seed(get_seed_from_string(name))
        return {
            'r_base': (np.random.rand(), np.random.rand() * 0.2),
            'g_base': (np.random.rand(), np.random.rand() * 0.2),
            'b_base': (np.random.rand(), np.random.rand() * 0.2),
        }

def cursed_colors(iter_array, max_iter, palette):
    norm = iter_array / max_iter

    r_mean, r_var = palette['r_base']
    g_mean, g_var = palette['g_base']
    b_mean, b_var = palette['b_base']

    r = np.clip(r_mean + r_var * np.sin(10 * norm * np.pi * 5), 0, 1)
    g = np.clip(g_mean + g_var * np.cos(15 * norm * np.pi * 4), 0, 1)
    b = np.clip(b_mean + b_var * np.sin(20 * norm * np.pi * 3), 0, 1)

    pulse = (np.sin(50 * norm * np.pi)) ** 12
    r = np.clip(r + pulse * 0.7, 0, 1)
    g = np.clip(g + pulse * 0.4, 0, 1)
    b = np.clip(b + pulse * 0.15, 0, 1)

    return np.dstack((r, g, b))

def main():
    input_str = input("Enter your Jujutsu Kaisen inspired input (name or number): ")
    seed = get_seed_from_string(input_str)
    np.random.seed(seed)

    palette = get_character_palette(input_str)

    width, height = 800, 800
    zoom = 1.2 + np.random.rand() * 0.5
    move_x, move_y = np.random.uniform(-0.5, 0.5, 2)
    cX, cY = np.random.uniform(-0.8, 0.8, 2)
    max_iter = 300

    iter_array = julia_set(width, height, zoom, move_x, move_y, cX, cY, max_iter)
    img = cursed_colors(iter_array, max_iter, palette)

    plt.figure(figsize=(8,8))
    plt.imshow(img, extent=(-1.5, 1.5, -1.5, 1.5))
    plt.axis('off')
    plt.title(f'Cursed Energy Fractal: "{input_str}"', fontsize=16, color='white', pad=20)
    plt.gca().set_facecolor('black')
    plt.show()

if __name__ == "__main__":
    main()