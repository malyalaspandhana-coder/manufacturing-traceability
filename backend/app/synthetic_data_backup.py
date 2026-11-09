import pandas as pd
import random
from pathlib import Path

def generate_data(records=1000):
    data = []

    for i in range(records):
        data.append({
            "product_id": f"P{i+1:04d}",
            "temperature": round(random.uniform(20, 100), 2),
            "pressure": round(random.uniform(1, 10), 2),
            "speed": random.randint(500, 3000),
            "quality": random.choice(["Good", "Defective"])
        })

    df = pd.DataFrame(data)

    output = Path("data/generated")
    output.mkdir(parents=True, exist_ok=True)

    df.to_csv(output / "manufacturing_data.csv", index=False)

    print("Dataset generated successfully!")

if __name__ == "__main__":
    generate_data()