from optimizer.ml_optimizer import run_pipeline

if __name__ == "__main__":

    test_input = {
        "traffic": 2500,
        "cpu": 12,
        "memory": 32
    }

    result = run_pipeline(**test_input)

    print("\n===== OPTIMIZATION RESULT =====\n")

    print("INPUT CONFIG:")
    print(result["input"])

    print("\nBEFORE OPTIMIZATION:")
    print(result["before"])

    print("\nAFTER OPTIMIZATION:")
    print(result["after"])

    print("\nIMPACT:")
    print(result["impact"])