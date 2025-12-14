import time
import numpy as np
import matplotlib.pyplot as plt

from solvers import NaiveSolver, MinimumDominatingSetSolver
from graph_generators import GraphGenerator


class TestSmallGraphs:
    def __init__(self, max_n=6):
        self.max_n = max_n
        self.results = {}

    def run(self):
        for n in range(2, self.max_n + 1):
            self._test_for_n(n)

        self._plot_results()

    def _test_for_n(self, n):
        graphs = GraphGenerator.generate_all_graphs_fixed_n(n)

        times_naive = []
        times_our_nocache = []
        times_our_cache = []
        for graph in graphs:
            start = time.perf_counter()
            NaiveSolver(graph).solve()
            times_naive.append(time.perf_counter() - start)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=False).solve()
            times_our_nocache.append(time.perf_counter() - start)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=True).solve()
            times_our_cache.append(time.perf_counter() - start)

        self.results[n] = {
            'our_nocache_time': np.mean(times_our_nocache),
            'our_cache_time': np.mean(times_our_cache),
            'cache_speedup': np.mean(times_our_nocache) / np.mean(times_our_cache)
        }

        if times_naive:
            self.results[n]['naive_time'] = np.mean(times_naive)
            self.results[n]['speedup_vs_naive'] = np.mean(times_naive) / np.mean(times_our_cache)

    def _plot_results(self):
        n_values = sorted(self.results.keys())

        plt.figure(figsize=(10, 5))

        our_nocache_times = [self.results[n]['our_nocache_time'] for n in n_values]
        our_cache_times = [self.results[n]['our_cache_time'] for n in n_values]

        plt.plot(n_values, our_nocache_times, 'bo-', label='Наш без кэша')
        plt.plot(n_values, our_cache_times, 'go-', label='Наш с кэшем')

        naive_n_values = [n for n in n_values if 'naive_time' in self.results[n]]
        if naive_n_values:
            naive_times = [self.results[n]['naive_time'] for n in naive_n_values]
            plt.plot(naive_n_values, naive_times, 'ro-', label='Наивный')

        plt.xlabel('Количество вершин (n)')
        plt.ylabel('Время (секунды)')
        plt.title('Тест 1: Время выполнения')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')

        plt.savefig('test1_time.png', dpi=100, bbox_inches='tight')

        plt.figure(figsize=(8, 4))

        cache_speedups = [self.results[n]['cache_speedup'] for n in n_values]
        plt.bar([str(n) for n in n_values], cache_speedups)

        plt.xlabel('Количество вершин (n)')
        plt.ylabel('Ускорение (раз)')
        plt.title('Ускорение от кэширования')
        plt.grid(True, axis='y')

        plt.savefig('test1_speedup.png', dpi=100, bbox_inches='tight')

        plt.show()


def main():
    tester = TestSmallGraphs(max_n=9)
    tester.run()


if __name__ == "__main__":
    main()