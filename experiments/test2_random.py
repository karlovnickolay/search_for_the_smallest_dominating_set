import time
import numpy as np
import matplotlib.pyplot as plt

from solvers import NaiveSolver, MinimumDominatingSetSolver
from graph_generators import GraphGenerator


class TestRandomGraphs:
    def __init__(self):
        self.results = {}

    def run(self):
        test_cases = [
            (10, 0.2, 20),
            (10, 0.5, 20),
            (10, 0.8, 20),
            (15, 0.2, 20),
            (15, 0.5, 20),
            (15, 0.8, 20),
            (20, 0.2, 20),
            (20, 0.5, 20),
            (20, 0.8, 20),
            (25, 0.2, 20),
            (25, 0.5, 20),
            (25, 0.8, 20),
            (30, 0.2, 20),
            (30, 0.5, 20),
            (30, 0.8, 20),
            (35, 0.2, 20),
            (35, 0.5, 20),
            (35, 0.8, 20),
            (40, 0.2, 20),
            (40, 0.5, 20),
            (40, 0.8, 20),
            (45, 0.2, 5),
            (45, 0.5, 5),
            (45, 0.8, 5),
            (50, 0.2, 1),
            (50, 0.5, 1),
            (50, 0.8, 1)
        ]

        for n, p, count in test_cases:
            print('n:', n, 'p:', p, 'count:', count)
            self._test_for_n_p(n, p, count)

        self._plot_results()

    def _test_for_n_p(self, n, p, count):
        times_naive = []
        times_nocache = []
        times_cache = []

        for _ in range(count):
            graph = GraphGenerator._generate_random_gnp(None, n, p)

            if n < 25:
                start = time.perf_counter()
                NaiveSolver(graph).solve()
                times_naive.append(time.perf_counter() - start)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=False).solve()
            times_nocache.append(time.perf_counter() - start)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=True).solve()
            times_cache.append(time.perf_counter() - start)

        key = f"n{n}_p{p}"
        self.results[key] = {
            'n': n,
            'p': p,
            'our_nocache_time': np.mean(times_nocache),
            'our_cache_time': np.mean(times_cache),
            'cache_speedup': np.mean(times_nocache) / np.mean(times_cache)
        }

        if times_naive:
            self.results[key]['naive_time'] = np.mean(times_naive)
            self.results[key]['speedup_vs_naive'] = np.mean(times_naive) / np.mean(times_cache)

    def _plot_results(self):
        plt.figure(figsize=(10, 5))

        n_values = []
        naive_times = []
        nocache_times = []
        cache_times = []

        for key in self.results:
            if self.results[key]['p'] == 0.5:
                n_values.append(self.results[key]['n'])
                nocache_times.append(self.results[key]['our_nocache_time'])
                cache_times.append(self.results[key]['our_cache_time'])
                if 'naive_time' in self.results[key]:
                    naive_times.append(self.results[key]['naive_time'])
                else:
                    naive_times.append(None)

        sorted_indices = np.argsort(n_values)
        n_values = [n_values[i] for i in sorted_indices]
        nocache_times = [nocache_times[i] for i in sorted_indices]
        cache_times = [cache_times[i] for i in sorted_indices]
        naive_times = [naive_times[i] for i in sorted_indices]

        plt.plot(n_values, nocache_times, 'bo-', label='Без кэша')
        plt.plot(n_values, cache_times, 'go-', label='С кэшем')

        valid_naive = [(n, t) for n, t in zip(n_values, naive_times) if t is not None]
        if valid_naive:
            naive_n = [x[0] for x in valid_naive]
            naive_t = [x[1] for x in valid_naive]
            plt.plot(naive_n, naive_t, 'ro-', label='Наивный')

        plt.xlabel('Количество вершин (n), p=0.5')
        plt.ylabel('Время (секунды)')
        plt.title('ТЕСТ 2: Время выполнения')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')
        plt.savefig('test2_time_vs_n.png', dpi=100, bbox_inches='tight')

        plt.figure(figsize=(10, 5))

        p_values = []
        naive_times_p = []
        nocache_times_p = []
        cache_times_p = []

        for key in self.results:
            if self.results[key]['n'] == 20:
                p_values.append(self.results[key]['p'])
                nocache_times_p.append(self.results[key]['our_nocache_time'])
                cache_times_p.append(self.results[key]['our_cache_time'])
                if 'naive_time' in self.results[key]:
                    naive_times_p.append(self.results[key]['naive_time'])
                else:
                    naive_times_p.append(None)

        sorted_indices = np.argsort(p_values)
        p_values = [p_values[i] for i in sorted_indices]
        nocache_times_p = [nocache_times_p[i] for i in sorted_indices]
        cache_times_p = [cache_times_p[i] for i in sorted_indices]
        naive_times_p = [naive_times_p[i] for i in sorted_indices]

        plt.plot(p_values, nocache_times_p, 'bo-', label='Без кэша')
        plt.plot(p_values, cache_times_p, 'go-', label='С кэшем')

        valid_naive_p = [(p, t) for p, t in zip(p_values, naive_times_p) if t is not None]
        if valid_naive_p:
            naive_p = [x[0] for x in valid_naive_p]
            naive_t = [x[1] for x in valid_naive_p]
            plt.plot(naive_p, naive_t, 'ro-', label='Наивный')

        plt.xlabel('Плотность графа (p), n=20')
        plt.ylabel('Время (секунды)')
        plt.title('ТЕСТ 2: Время выполнения')
        plt.legend()
        plt.grid(True)
        plt.yscale('log')
        plt.savefig('test2_time_vs_p.png', dpi=100, bbox_inches='tight')

        plt.figure(figsize=(8, 5))

        n_for_speedup = []
        cache_speedups = []

        for key in self.results:
            n = self.results[key]['n']
            if n not in n_for_speedup:
                n_for_speedup.append(n)
                speedups = []
                for k, v in self.results.items():
                    if v['n'] == n:
                        speedups.append(v['cache_speedup'])
                cache_speedups.append(np.mean(speedups))

        sorted_idx = np.argsort(n_for_speedup)
        n_for_speedup = [n_for_speedup[i] for i in sorted_idx]
        cache_speedups = [cache_speedups[i] for i in sorted_idx]

        plt.bar([str(n) for n in n_for_speedup], cache_speedups)
        plt.xlabel('Количество вершин (n)')
        plt.ylabel('Ускорение (раз)')
        plt.title('Ускорение от кэширования для случайных графов')
        plt.grid(True, axis='y')
        plt.savefig('test2_speedup.png', dpi=100, bbox_inches='tight')

        plt.show()


def main():
    TestRandomGraphs().run()


if __name__ == "__main__":
    main()