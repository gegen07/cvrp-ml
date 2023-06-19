from model import CVRPInstance, CVRPSolution, ORToolsParams, solve, CVRPSeries
from distances import calculate_distance_matrix_m
# from classes import CVRPSeries
import os
import numpy as np
import pandas
import geopandas
import h3
from shapely import wkt
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import h3
import warnings

warnings.simplefilter(action='ignore', category=pandas.errors.PerformanceWarning)


import requests
def calculate_distance_matrix_tuple(
    points
):
    if len(points) < 2:
        return 0

    coords_uri = ";".join(
        ["{},{}".format(point[0], point[1]) for point in points]
    )

    response = requests.get(
        f"http://localhost:5000/table/v1/driving/{coords_uri}?annotations=distance",
        timeout=6000,
    )
    # print(coords_uri)
    response.raise_for_status()

    return np.array(response.json()["distances"])

def generate_instance_df(instance, area, distance_matrix, map_dd_cells):
    map_instances = np.array(list(map(lambda x: map_dd_cells[x] if x in map_dd_cells.keys() else np.nan, list(instance.h3_boundary.unique()))))
    map_instances = map_instances[~np.isnan(map_instances)].astype(int)

    distances = []

    for i in map_instances:
        for j in map_instances:
            if i < j:
                distances.append(distance_matrix[i][j])

    distances = np.array(distances)
    distance_stat_list = [np.mean(distances), np.std(distances), np.median(distances), np.max(distances), np.min(distances), np.var(distances)]
    dict_distance = dict(zip(['distance_mean', 'distance_std', 'distance_median', 'distance_max', 'distance_min', 'distance_var'], distance_stat_list))
    df = pandas.DataFrame.from_dict(dict_distance, orient='index').T

    censo_columns=['media_moradores_por_domicilio',
       'media_rendimento_medio_por_morador_com_ou_sem_renda',
       'media_rendimento_medio_por_morador_com_renda',
       'media_rendimento_medio_por_morador_reponsavel_com_ou_sem_Renda',
       'media_rendimento_medio_por_morador_responsavel_com_renda',
       'n_alfabetizados_homens', 'n_alfabetizados_mulheres', 'n_amarelos',
       'n_brancos', 'n_domicilios', 'n_homens', 'n_idade_0_10',
       'n_idade_11_20', 'n_idade_21_30', 'n_idade_31_40', 'n_idade_41_50',
       'n_idade_51_60', 'n_idade_61_70', 'n_idade_71_100', 'n_indigenas',
       'n_moradores', 'n_mulheres', 'n_pardos', 'n_pretos',
       'variancia_moradores_por_domicilio']
    
    stat_censo = area.loc[map_instances, censo_columns].agg({"mean", "std", "median", "max", "min", "var"})
    stats_list = stat_censo.index.tolist()
    columns = stat_censo.columns.tolist()
    for i in range(len(columns)):
        for j in range(len(stats_list)):
            df[f"{columns[i]}_{stats_list[j]}"] = stat_censo.iloc[j, i]

    return df

if __name__ == "__main__":
    # all_gdf = []

    base_dir = "../data/cvrp-instances-1.0/dev/"

    pa_area = pandas.read_csv("/media/gegen07/Expansion/data/pa_interpolated_res_6_interest.csv")

    pa_area.reset_index(drop=True, inplace=True)
    pa_area['geometry'] = pa_area.geometry.apply(wkt.loads)
    pa_area = geopandas.GeoDataFrame(pa_area, geometry="geometry")
    pa_area["centroid"] = pa_area.centroid
    pa_area["h3_boundary"] = pa_area.centroid.apply(lambda x: h3.geo_to_h3(x.y, x.x, 6))

    dd_cells = pa_area.h3_boundary.to_dict()
    map_dd_cells = {v: k for k, v in dd_cells.items()}

    cells_points = [x.coords[0] for x in pa_area.centroid.values]

    distance_matrix = (calculate_distance_matrix_tuple(cells_points)/1000)


    dfs = []
    for i in range(90, 30+90):
        print(i)
        instance = CVRPSeries.from_file(os.path.join(base_dir, f"pa-0/cvrp-0-pa-{i}.json"))
        gdf = instance.to_gdf()


        train_df = generate_instance_df(gdf, pa_area, distance_matrix, map_dd_cells)

        # Get mean distance per vehicle (target metric)
        instance = CVRPInstance.from_file(os.path.join(base_dir, f"pa-0/cvrp-0-pa-{i}.json"))

        solution: CVRPSolution = solve(instance, ORToolsParams())
        total = 0
        if solution is not None:
            print("feasible")
            for v in solution.vehicles:
                matrix = calculate_distance_matrix_m(v.circuit)
                # print(matrix)
                total_distance = 0
                for i in range(len(matrix)-1):
                    total_distance += matrix[i][i+1]
                total += total_distance
                # print(f"Circuit: {v.circuit}\nOccupation: {v.occupation}\nQuantity of deliveries: {len(v.deliveries)}\nTotal Distance:{total_distance}\n")

            train_df["target"] = (total / len(solution.vehicles))
            dfs.append(train_df)
        else:
            print("infeasible")
    train_df = pandas.concat(dfs)
    train_df.to_csv(os.path.join(base_dir, "cvrp-0-pa-test.csv"), index=False)