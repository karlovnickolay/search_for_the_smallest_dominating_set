import time
import numpy as np
import matplotlib.pyplot as plt
from solvers import MinimumDominatingSetSolver
from graph_generators import GraphGenerator


class TestPracticalGraphs:
    def __init__(self):
        self.results = {}

    def run(self):
        test_cases = [
            ('Дороги', GraphGenerator.load_road_network_simple,
             "Заправки/камеры"),
            ('Соцсеть', GraphGenerator.load_social_network_simple,
             "Лидеры"),
        ]

        for name, loader, application in test_cases:
            self._test_graph(name, loader, application)

        self._plot_results()

    def _test_graph(self, name: str, loader, application: str):
        print(f"Тест: {name}")
        print(f"Применение: {application}")

        graph = loader()
        n = len(graph)
        edges = sum(len(adj) for adj in graph) // 2

        print(f"  Вершин: {n}, Ребер: {edges}")

        runs = 5
        times_nocache = []
        times_cache = []

        for _ in range(runs):
            start = time.perf_counter()
            solver = MinimumDominatingSetSolver(graph, cache=False)
            solver.solve()
            times_nocache.append(time.perf_counter() - start)

            start = time.perf_counter()
            solver = MinimumDominatingSetSolver(graph, cache=True)
            result_cache = solver.solve()
            times_cache.append(time.perf_counter() - start)

        time_nocache = np.mean(times_nocache)
        time_cache = np.mean(times_cache)
        speedup = time_nocache / time_cache

        self.results[name] = {
            'application': application,
            'vertices': n,
            'edges': edges,
            'avg_degree': 2 * edges / n if n > 0 else 0,
            'dominating_size': len(result_cache),
            'coverage_ratio': len(result_cache) / n,
            'time_nocache': time_nocache,
            'time_cache': time_cache,
            'speedup': speedup,
            'std_nocache': np.std(times_nocache),
            'std_cache': np.std(times_cache),
        }

        print(f"  Размер доминирующего множества: {len(result_cache)}")
        print(f"  Покрытие: {len(result_cache) / n * 100:.1f}% вершин")
        print(f"  Время без кэша: {time_nocache:.3f} +- {np.std(times_nocache):.3f}с")
        print(f"  Время с кэшем: {time_cache:.3f} +- {np.std(times_cache):.3f}с")
        print(f"  Ускорение: {speedup:.1f}x")
        print()

    def _plot_results(self):
        self._create_main_plots()

        self._create_compact_table()

        plt.show()

    def _create_main_plots(self):
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        names = list(self.results.keys())

        ax = axes[0]
        times_nocache = [self.results[n]['time_nocache'] for n in names]
        times_cache = [self.results[n]['time_cache'] for n in names]

        x = np.arange(len(names))
        width = 0.35

        ax.bar(x - width / 2, times_nocache, width,
                       label='Без кэша', color='#1f77b4')
        ax.bar(x + width / 2, times_cache, width,
                       label='С кэшем', color='#2ca02c')

        ax.set_xlabel('Тип графа')
        ax.set_ylabel('Время (с)')
        ax.set_title('Время выполнения')
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=11)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)

        ax = axes[1]
        speedups = [self.results[n]['speedup'] for n in names]
        coverage = [self.results[n]['coverage_ratio'] * 100 for n in names]

        ax.bar(x, speedups, width, color='#ff7f0e', label='Ускорение')
        ax.set_xlabel('Тип графа')
        ax.set_ylabel('Ускорение (раз)', color='#ff7f0e')

        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=11)
        ax.tick_params(axis='y', labelcolor='#ff7f0e')

        ax2 = ax.twinx()
        ax2.plot(x, coverage, 'o-', color='#d62728', linewidth=2,
                 markersize=8, label='Покрытие')
        ax2.set_ylabel('Покрытие (%)', color='#d62728')
        ax2.tick_params(axis='y', labelcolor='#d62728')

        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        ax.set_title('Эффективность алгоритма')
        ax.grid(True, axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig('test4_practical_results.png', dpi=150, bbox_inches='tight')

    def _create_compact_table(self):
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.axis('tight')
        ax.axis('off')

        headers = ['Граф', 'V', 'E', 'deg', 'D', '%', 't_1', 't_2', 'S']

        table_data = []
        for name in self.results.keys():
            r = self.results[name]
            table_data.append([
                name,
                f"{r['vertices']}",
                f"{r['edges']}",
                f"{r['avg_degree']:.1f}",
                f"{r['dominating_size']}",
                f"{r['coverage_ratio'] * 100:.1f}",
                f"{r['time_nocache']:.3f}",
                f"{r['time_cache']:.3f}",
                f"{r['speedup']:.1f}x"
            ])

        table = ax.table(cellText=table_data, colLabels=headers,
                         loc='center', cellLoc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 2.0)

        cell_width = 0.08
        for key, cell in table.get_celld().items():
            cell.set_width(cell_width)

        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#2E86AB')
            table[(0, i)].set_text_props(weight='bold', color='white', fontsize=13)

        explanation = (
            "V - вершины, E - рёбра, deg - средняя степень, D - размер доминирующего множества,\n"
            "% - покрытие, t_1 - время без кэша (с), t_2 - время с кэшем (с), S - ускорение (x)"
        )
        plt.figtext(0.5, 0.05, explanation, ha='center', fontsize=10,
                    style='italic', fontfamily='monospace')

        plt.subplots_adjust(bottom=0.2)
        plt.tight_layout()
        plt.savefig('test4_table.png', dpi=150, bbox_inches='tight',
                    pad_inches=0.5)

        self._create_vertical_table()

    def _create_vertical_table(self):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.axis('tight')
        ax.axis('off')

        headers = ['Параметр', 'Дороги', 'Соцсеть']

        table_data = [
            ['Вершины (V)',
             f"{self.results['Дороги']['vertices']}",
             f"{self.results['Соцсеть']['vertices']}"],
            ['Рёбра (E)',
             f"{self.results['Дороги']['edges']}",
             f"{self.results['Соцсеть']['edges']}"],
            ['Ср. степень',
             f"{self.results['Дороги']['avg_degree']:.1f}",
             f"{self.results['Соцсеть']['avg_degree']:.1f}"],
            ['|D|',
             f"{self.results['Дороги']['dominating_size']}",
             f"{self.results['Соцсеть']['dominating_size']}"],
            ['Покрытие (%)',
             f"{self.results['Дороги']['coverage_ratio'] * 100:.1f}",
             f"{self.results['Соцсеть']['coverage_ratio'] * 100:.1f}"],
            ['Время без кэша (с)',
             f"{self.results['Дороги']['time_nocache']:.3f}",
             f"{self.results['Соцсеть']['time_nocache']:.3f}"],
            ['Время с кэшем (с)',
             f"{self.results['Дороги']['time_cache']:.3f}",
             f"{self.results['Соцсеть']['time_cache']:.3f}"],
            ['Ускорение',
             f"{self.results['Дороги']['speedup']:.1f}x",
             f"{self.results['Соцсеть']['speedup']:.1f}x"],
        ]

        table = ax.table(cellText=table_data, colLabels=headers,
                         loc='center', cellLoc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 1.5)

        for i in range(len(headers)):
            table[(0, i)].set_facecolor('#2E86AB')
            table[(0, i)].set_text_props(weight='bold', color='white')

        for i in range(1, len(table_data) + 1):
            if i % 2 == 0:
                for j in range(len(headers)):
                    table[(i, j)].set_facecolor('#f0f0f0')

        plt.tight_layout()
        plt.savefig('test4_vertical_table.png', dpi=150, bbox_inches='tight')


def main():
    TestPracticalGraphs().run()


if __name__ == "__main__":
    main()