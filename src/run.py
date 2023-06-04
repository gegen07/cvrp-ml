from model import CVRPInstance, CVRPSolution, ORToolsParams, solve, CVRPSeries
# from classes import CVRPSeries
import os
import pandas as pd

base_dir = "../data/cvrp-instances-1.0/train/"

if __name__ == "__main__":
    all_gdf = []
    for i in range(1):
        instance = CVRPSeries.from_file(os.path.join(base_dir, f"rj-0/cvrp-0-rj-{i}.json"))
        gdf = instance.to_gdf()
        all_gdf.append(gdf)

    df = pd.concat(all_gdf)
    df.to_csv(os.path.join(base_dir, "cvrp-0-rj-0.csv"), index=False)


    # solution: CVRPSolution = solve(instance, ORToolsParams())
    # for v in solution.vehicles:
    #     print(f"Circuit: {v.circuit}\nOccupation: {v.occupation}\nQuantity of deliveries: {len(v.deliveries)}\n")