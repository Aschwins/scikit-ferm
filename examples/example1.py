from skferm.datasets.synthetic import generate_synthetic_growth
import matplotlib.pyplot as plt
import numpy as np

def main():
    # Parameters
    time = np.linspace(0, 24, 100)
    synthetic_data = generate_synthetic_growth(
        time, model="logistic", N0=1e6, Nmax=1e9, r=0.3, noise_std=1e7
    )

    # Plot
    plt.plot(synthetic_data["time"], synthetic_data["population"], label="Synthetic Data")
    plt.xlabel("Time (hours)")
    plt.ylabel("Population (CFU/mL)")
    plt.title("Synthetic Microbial Growth Curve")
    plt.legend()
    plt.savefig("synthetic_growth_curve.png")

if __name__ == "__main__":
    main()