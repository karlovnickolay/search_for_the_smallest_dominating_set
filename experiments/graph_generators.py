import networkx as nx
import requests
from typing import List
import random
import gzip
import io


class GraphGenerator:
    @staticmethod
    def nx_to_adj_list(nx_graph: nx.Graph) -> List[List[int]]:
        n = nx_graph.number_of_nodes()
        adj_list = [[] for _ in range(n)]
        for u, v in nx_graph.edges():
            adj_list[u].append(v)
            adj_list[v].append(u)
        return adj_list

    @staticmethod
    def download_all_graphs_n(n: int) -> List[List[int]]:
        url = f"https://users.cecs.anu.edu.au/~bdm/data/graph{n}.g6"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.content
            all_graphs = []

            for line in data.split(b'\n'):
                line = line.strip()
                if not line:
                    continue

                try:
                    G = nx.from_graph6_bytes(line)
                    all_graphs.append(GraphGenerator.nx_to_adj_list(G))
                except Exception as e:
                    print(f"Ошибка обработки: {e}")
                    continue

            return all_graphs

        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return []

    @staticmethod
    def generate_all_graphs_fixed_n(n: int) -> List[List[int]]:
        return GraphGenerator.download_all_graphs_n(n)

    @staticmethod
    def _generate_random_gnp(self, n, p):
        graph = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < p:
                    graph[i].append(j)
                    graph[j].append(i)
        return graph

    @staticmethod
    def generate_hypercube(d):
        n = 1 << d
        graph = [[] for _ in range(n)]
        for i in range(n):
            for bit in range(d):
                neighbor = i ^ (1 << bit)
                if neighbor > i:
                    graph[i].append(neighbor)
                    graph[neighbor].append(i)
        return graph

    @staticmethod
    def generate_grid(m, n):
        graph = [[] for _ in range(m * n)]
        for i in range(m):
            for j in range(n):
                node = i * n + j
                if j < n - 1:
                    neighbor = i * n + (j + 1)
                    graph[node].append(neighbor)
                    graph[neighbor].append(node)
                if i < m - 1:
                    neighbor = (i + 1) * n + j
                    graph[node].append(neighbor)
                    graph[neighbor].append(node)
        return graph

    @staticmethod
    def generate_crown(n):
        graph = [[] for _ in range(2 * n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    graph[i].append(n + j)
                    graph[n + j].append(i)
        return graph

    @staticmethod
    def load_road_network_simple() -> List[List[int]]:
        url = "https://www.diag.uniroma1.it/challenge9/data/rome/rome99.gr"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        content = response.text
        lines = content.strip().split('\n')

        nodes = 0
        for line in lines:
            if line.startswith('p sp'):
                parts = line.split()
                nodes = int(parts[2])
                break

        if nodes > 200:
            nodes = 200

        graph = [[] for _ in range(nodes)]
        edge_count = 0

        for line in lines:
            if line.startswith('a '):
                parts = line.split()
                u = int(parts[1]) - 1
                v = int(parts[2]) - 1
                if u < nodes and v < nodes:
                    graph[u].append(v)
                    graph[v].append(u)
                    edge_count += 1
                    if edge_count > nodes * 3:
                        break

        return graph

    @staticmethod
    def load_social_network_simple() -> List[List[int]]:
        url = "https://snap.stanford.edu/data/facebook_combined.txt.gz"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
            content = f.read().decode('utf-8')

        edges = []
        for line in content.strip().split('\n'):
            if line.startswith('#') or not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 2:
                u, v = int(parts[0]), int(parts[1])
                edges.append((u, v))

        max_node = 1000
        graph = [[] for _ in range(max_node)]

        for u, v in edges:
            if u < max_node and v < max_node:
                if v not in graph[u]:
                    graph[u].append(v)
                if u not in graph[v]:
                    graph[v].append(u)

        return graph
