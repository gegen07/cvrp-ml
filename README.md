# Problem
Try to approximate the total time traveled by each vehicle in Capacitated Vehicle Routing Problem with Machine Learning using classic models. It can be used Reinforcement Learning as a baseline 

## Project
- Engineer features like (mean, standard deviation, variance) of the graph distances. Besides that assigning how many districts (mean, standard deviation) a vehicle should drive to complete the tour.
- The project will use the data from [loggibud-challenge](https://github.com/loggi/loggibud). There are 90 feasible instances of cvrp for each district in Distrito Federal, Rio de Janeiro and Pará for training the ML models. Besides this train set, there are also a test set with 30 instances for the same districts explored in train set.

### First Steps
- Create the distance matrix
- Engineer the data with distance traveled using Mixed Integer Linear Programming (MILP). With the tour for each vehicle allocated, calculate the time travel by using some API like Valhalla. (If the API does not have the feature of route time I will try to approximate the distance and simplify the problem).

### Set Up Environment

- Download the `.pbf` file in [geofabrik.de](geofabrik.de)
- Convert the `.osrm` file with osrm docker. This conversion extracts a graph with the hole street/highway networks of Brasil
    - In this step, it was processed 75.358.579 vertexes and 78.914.994 arcs
```docker
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/car.lua /data/brazil-latest.osm.pbf
```
- Do the graph spatial partitioning
```docker
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/brazil-latest.osrm
```
- Customize the graph, assigning weights to the partition cells
```docker
docker run -t -v $(pwd):/data osrm/osrm-backend:latest osrm-customize /data/brazil-latest.osrm
```
- Deploy OSRM server using MLD (Multi-Level Dijkstra) algorithm
```docker
docker run -t -i -p 5000:5000 -v $(pwd):/data -d osrm/osrm-backend:latest osrm-routed — algorithm mld /data/india-latest.osrm
```

### Running Server
```
docker run --rm -t -id \
	--name osrm \
	-p 5000:5000 \
	-v "${PWD}:/data" \
	osrm/osrm-backend osrm-routed --algorithm mld /data/brazil-latest.osrm --max-table-size 10000
```
