class MinimumDominatingSetSolver:
    def __init__(self, graph, adjacency_matrix=False, cache=True):
        self.n = len(graph)

        self.dominating_set = []

        if adjacency_matrix:
            for v in range(self.n):
                mask = 1 << v
                for ind, neighbor in enumerate(graph[v]):
                    if neighbor:
                        mask |= 1 << ind
                self.dominating_set.append(mask)
        else:
            for v in range(self.n):
                mask = 1 << v
                for neighbor in graph[v]:
                    mask |= 1 << neighbor
                self.dominating_set.append(mask)

        self.use_cache = cache

        if cache:
            self._cache = {}
            self._solve_recursive = self._solve_recursive_cached
        else:
            self._solve_recursive = self._solve_recursive_impl

    def _solve_recursive_cached(self, U, available):
        key = (U, available)
        if key in self._cache:
            return self._cache[key]

        result = self._solve_recursive_impl(U, available)

        self._cache[key] = result
        return result

    def solve(self) -> list:
        if self.use_cache:
            self._cache.clear()

        U = (1 << self.n) - 1
        available = (1 << self.n) - 1
        return self._solve_recursive(U, available)

    def _solve_recursive_impl(self, U, available):
        if U == 0:
            return []

        # Первое правило редукции
        new_available = self._removal_of_nested_sets(U, available)

        if new_available != available:
            return self._solve_recursive(U, new_available)

        # Второе правило редукции
        unique_covering_set = self._search_for_the_unique_covering_set(U, available)
        if unique_covering_set != 0:
            list_removed = []
            while unique_covering_set:
                del_ind = (unique_covering_set & -unique_covering_set).bit_length() - 1
                unique_covering_set &= unique_covering_set - 1

                U = self._del(U, del_ind)
                list_removed.append(del_ind)
                available &= ~(1 << del_ind)

            return list_removed + self._solve_recursive(U, available)

        # Третье правило редукции
        ind_max = self._search_for_the_maximum_covering_set(U, available)

        first_branch = self._solve_recursive(U, available & ~(1 << ind_max))
        second_branch = ([ind_max] +
                         self._solve_recursive(self._del(U, ind_max),
                                               available & ~(1 << ind_max)))

        if len(first_branch) > len(second_branch):
            return first_branch
        else:
            return second_branch

    def _removal_of_nested_sets(self, U, available):
        temp_available = available
        removed = 0

        while temp_available:
            v = (temp_available & -temp_available).bit_length() - 1
            temp_available &= temp_available - 1

            mask_v = self.dominating_set[v] & U

            other_available = available & ~((1 << v) | removed)
            while other_available:
                u = (other_available & -other_available).bit_length() - 1
                other_available &= other_available - 1

                mask_u = self.dominating_set[u] & U

                if (mask_v & ~mask_u) == 0:
                    removed |= 1 << v
                    break

        return available & ~removed

    def _search_for_the_unique_covering_set(self, U, available):
        temp_available = available
        removed = 0

        while temp_available:
            v = (temp_available & -temp_available).bit_length() - 1
            temp_available &= temp_available - 1

            mask_v = self.dominating_set[v] & U

            other_available = available & ~((1 << v) | removed)
            while other_available:
                u = (other_available & -other_available).bit_length() - 1
                other_available &= other_available - 1

                mask_u = self.dominating_set[u] & U

                mask_v = (mask_v & ~mask_u)

                if mask_v == 0:
                    break

            if mask_v != 0:
                removed |= 1 << v

        return removed

    def _del(self, U, ind_del):
        return U & ~(self.dominating_set[ind_del])

    def _search_for_the_maximum_covering_set(self, U, available):
        temp_available = available

        max_elem, ind_max = 0, 0

        while temp_available:
            v = (temp_available & -temp_available).bit_length() - 1
            temp_available &= temp_available - 1

            mask_v = self.dominating_set[v] & U
            count_elem = mask_v.bit_count()

            if count_elem > max_elem:
                max_elem = count_elem
                ind_max = v

        return ind_max