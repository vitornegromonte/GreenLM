# Transformer FLOPs Equation: C ≈ 6ND
# Extended version: τT = 6ND

def compute_flops(N, D, G):
    """
    Compute FLOPs using the equation C ≈ 6ND.
    :param N: Number of tokens
    :param D: Model dimension
    :param gpus: Proportional learning coef. (6 or 8)
    :return: Compute (C) in FLOPs
    """
    return G * N * D

def compute_throughput_time(N, D, G, T=None, tau=None):
    """
    Verify or compute throughput and training time relationship with C.
    :param N: Number of tokens
    :param D: Model dimension
    :param T: Training time (optional)
    :param tau: Cluster throughput (optional)
    :return: A dictionary with computed values
    """
    C = compute_flops(N, D, G)
    
    if T and tau:
        # Verify the relationship
        valid = abs(tau * T - C) < 1e-6  # Allow small tolerance for float comparisons
        return {
            "C (FLOPs)": C,
            "Valid Relationship": valid
        }
    elif T:
        # Calculate throughput τ
        tau = C / T
        return {
            "C (FLOPs)": C,
            "Throughput (τ)": tau
        }
    elif tau:
        # Calculate training time T
        T = C / tau
        return {
            "C (FLOPs)": C,
            # convert to hours
            "Training Time (T) - in hours": T / 3600
            
        }
    else:
        raise ValueError("At least one of T (training time) or τ (throughput) must be provided.")

# Example Usage
if __name__ == "__main__":
    N = float(input("Enter the model size (N): "))
    D = float(input("Enter the dataset size - in tokens (D): "))
    G = int(input("Enter the coefficient for single GPU or more (6 or 8): "))
    choice = input("Do you want to enter training time (T) or throughput (τ)? (T/t): ").strip().lower()
    
    if choice == "T":
        T = float(input("Enter training time (T) in seconds: "))
        result = compute_throughput_time(N, D, G, T=T)
    elif choice == "t":
        tau = float(input("Enter throughput (τ) in FLOPs/s: "))
        result = compute_throughput_time(N, D, G, tau=tau)
    else:
        print("Invalid choice. Exiting...")
        exit()
    
    print("\nResults:")
    for key, value in result.items():
        print(f"{key}: {value}")