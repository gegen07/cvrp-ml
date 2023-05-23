from model import CVRPInstance, CVRPSolution, ORToolsParams, solve
import os

base_dir = "../data/cvrp-instances-1.0/train/"

if __name__ == "__main__":
    instance = CVRPInstance.from_file(os.path.join(base_dir, "df-0/cvrp-0-df-0.json"))
    solution: CVRPSolution = solve(instance, ORToolsParams())
    for v in solution.vehicles:
        print(f"Circuit: {v.circuit}\nOccupation: {v.occupation}\nQuantity of deliveries: {len(v.deliveries)}\n")