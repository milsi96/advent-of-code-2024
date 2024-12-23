from functools import partial
from itertools import combinations
import networkx as nx

from networkx import Graph

from advent_of_code.utils.file_utils import process_file


def get_graph(file_name: str) -> Graph:
    tuples = process_file(
        file_name=file_name,
        process=lambda line: ((pcs := line.replace("\n", "").split("-"))[0], pcs[1]),
    )

    graph = nx.Graph()
    for computer, link in tuples:
        graph.add_node(computer)
        graph.add_edge(computer, link)

    return graph


def solve_part_two(file_name: str) -> str:
    graph = get_graph(file_name=file_name)

    return ",".join(sorted(max(nx.find_cliques(G=graph), key=len)))


def solve_part_one(file_name: str) -> int:
    graph = get_graph(file_name=file_name)

    def startswith(letter: str, word: str) -> bool:
        return word.startswith(letter)

    startswith_t = partial(startswith, "t")

    triples = set(
        map(
            lambda triple: tuple(sorted(triple)),
            [
                triple
                for clique in nx.find_cliques(G=graph)
                for triple in combinations(clique, 3)
            ],
        )
    )
    triples_with_t = list(
        filter(lambda triple: any(startswith_t(c) for c in triple), triples)
    )

    return len(triples_with_t)


def main() -> None:
    file_name: str = "input/day23/input.txt"

    part_one = solve_part_one(file_name=file_name)
    print("Part one solution is", part_one)

    part_two = solve_part_two(file_name=file_name)
    print("Part two solution is", part_two)


if __name__ == "__main__":
    main()
