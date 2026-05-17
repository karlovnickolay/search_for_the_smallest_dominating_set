import time
import matplotlib.pyplot as plt
from solvers import MinimumDominatingSetSolver
from graph_generators import GraphGenerator


class TestSpecialGraphs:
    def __init__(self):
        self.results = {}

    def run(self):
        self._test_hypercubes()

        self._test_grids()

        self._test_crowns()

        self._plot_results()

    def _test_hypercubes(self):
        times_nocache = []
        times_cache = []
        sizes = []

        for d in range(2, 6):
            print('hypercube', d)
            n = 1 << d
            graph = GraphGenerator.generate_hypercube(d)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=False).solve()
            times_nocache.append(time.perf_counter() - start)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=True).solve()
            times_cache.append(time.perf_counter() - start)

            sizes.append(n)

        self.results['hypercubes'] = {
            'sizes': sizes,
            'nocache': times_nocache,
            'cache': times_cache,
            'speedup': [t1 / t2 for t1, t2 in zip(times_nocache, times_cache)]
        }

    def _test_grids(self):
        times_nocache = []
        times_cache = []
        sizes = []

        for k in range(2, 7):
            print('grid', k)
            n = k * k
            graph = GraphGenerator.generate_grid(k, k)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=False).solve()
            times_nocache.append(time.perf_counter() - start)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=True).solve()
            times_cache.append(time.perf_counter() - start)

            sizes.append(n)

        self.results['grids'] = {
            'sizes': sizes,
            'nocache': times_nocache,
            'cache': times_cache,
            'speedup': [t1 / t2 for t1, t2 in zip(times_nocache, times_cache)]
        }

    def _test_crowns(self):
        times_nocache = []
        times_cache = []
        sizes = []

        for n in range(5, 16, 5):
            print('crown', n)
            graph = GraphGenerator.generate_crown(n)
            vertices = 2 * n

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=False).solve()
            times_nocache.append(time.perf_counter() - start)

            start = time.perf_counter()
            MinimumDominatingSetSolver(graph, cache=True).solve()
            times_cache.append(time.perf_counter() - start)

            sizes.append(vertices)

        self.results['crowns'] = {
            'sizes': sizes,
            'nocache': times_nocache,
            'cache': times_cache,
            'speedup': [t1 / t2 for t1, t2 in zip(times_nocache, times_cache)]
        }

    def _plot_results(self):
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        ax = axes[0]
        data = self.results['hypercubes']
        ax.plot(data['sizes'], data['nocache'], 'bo-', label='Без кэша')
        ax.plot(data['sizes'], data['cache'], 'go-', label='С кэшем')
        ax.set_xlabel('Вершин')
        ax.set_ylabel('Время (с)')
        ax.set_title('Гиперкубы Q_d')
        ax.set_yscale('log')
        ax.grid(True)
        ax.legend()

        ax = axes[1]
        data = self.results['grids']
        ax.plot(data['sizes'], data['nocache'], 'bo-', label='Без кэша')
        ax.plot(data['sizes'], data['cache'], 'go-', label='С кэшем')
        ax.set_xlabel('Вершин')
        ax.set_ylabel('Время (с)')
        ax.set_title('Квадратные решетки')
        ax.set_yscale('log')
        ax.grid(True)
        ax.legend()

        ax = axes[2]
        data = self.results['crowns']
        ax.plot(data['sizes'], data['nocache'], 'bo-', label='Без кэша')
        ax.plot(data['sizes'], data['cache'], 'go-', label='С кэшем')
        ax.set_xlabel('Вершин')
        ax.set_ylabel('Время (с)')
        ax.set_title('Коронные графы')
        ax.set_yscale('log')
        ax.grid(True)
        ax.legend()

        plt.tight_layout()
        plt.savefig('test3_time.png', dpi=150, bbox_inches='tight')

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 3, 1)
        data = self.results['hypercubes']
        plt.bar(range(len(data['sizes'])), data['speedup'])
        plt.xticks(range(len(data['sizes'])), data['sizes'])
        plt.xlabel('Размер гиперкуба')
        plt.ylabel('Ускорение')
        plt.title('Ускорение для гиперкубов')
        plt.grid(True, axis='y')

        plt.subplot(1, 3, 2)
        data = self.results['grids']
        plt.bar(range(len(data['sizes'])), data['speedup'])
        plt.xticks(range(len(data['sizes'])), data['sizes'])
        plt.xlabel('Размер решетки')
        plt.ylabel('Ускорение')
        plt.title('Ускорение для решеток')
        plt.grid(True, axis='y')

        plt.subplot(1, 3, 3)
        data = self.results['crowns']
        plt.bar(range(len(data['sizes'])), data['speedup'])
        plt.xticks(range(len(data['sizes'])), data['sizes'])
        plt.xlabel('Размер короны')
        plt.ylabel('Ускорение')
        plt.title('Ускорение для корон')
        plt.grid(True, axis='y')

        plt.tight_layout()
        plt.savefig('test3_speedup.png', dpi=150, bbox_inches='tight')

        plt.show()


def main():
    TestSpecialGraphs().run()


if __name__ == "__main__":
    main()