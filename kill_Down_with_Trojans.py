import numpy as np
import scipy


def load_input_file(file_name):
    with open(file_name, "r") as file:
        n, H = map(int, file.readline().split())
        tile_types = np.zeros((n, n), dtype=int)
        tile_values = np.zeros((n, n), dtype=int)

        for i in range(n * n):
            if i == 0:
                continue  # the initial tile is zero type with zero value
            x, y, t, v = map(int, file.readline().split())
            tile_types[x][y] = t
            tile_values[x][y] = v

    return n, H, tile_types, tile_values


def print_tile_data(tile_types, tile_values):
    print("Tile Types:")
    print(tile_types)
    print("\nTile Values:")
    print(tile_values)


def DP(n, H, tile_types, tile_values):
    if n == 0 or H <= 0:
        return False

    dp = [
        [{"health": -1, "protection": False, "multiplier": False} for _ in range(n)]
        for _ in range(n)
    ]
    dp[0][0]["health"] = H

    for i in range(n):
        for j in range(n):
            if i > 0:
                update_states(
                    dp[i - 1][j], dp[i][j], tile_types[i][j], tile_values[i][j]
                )
            if j > 0:
                update_states(
                    dp[i][j - 1], dp[i][j], tile_types[i][j], tile_values[i][j]
                )

    return dp[-1][-1]["health"] >= 0


def update_states(prev_state, curr_state, t, v):
    if prev_state["health"] < 0:
        return

    health = prev_state["health"]
    protection = prev_state["protection"]
    multiplier = prev_state["multiplier"]

    if t == 0:  # damage
        if protection:
            protection = False
        else:
            health -= v
    elif t == 1:  # healing
        health += v * (2 if multiplier else 1)
        multiplier = False
    elif t == 2:  # protection
        protection = True
    elif t == 3:  # multiplier
        multiplier = True

    if health > curr_state["health"]:
        curr_state["health"] = health
        curr_state["protection"] = protection
        curr_state["multiplier"] = multiplier


def write_output_file(output_file_name, result):
    with open(output_file_name, "w") as file:
        file.write(str(int(result)))


def main(input_file_name):
    n, H, tile_types, tile_values = load_input_file(input_file_name)
    print_tile_data(tile_types, tile_values)
    result = DP(n, H, tile_types, tile_values)
    print("Result: " + str(result))
    output_file_name = input_file_name.replace(".txt", "_out.txt")
    write_output_file(output_file_name, result)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python kill_Down_with_Trojans.py a_file_name.txt")
    else:
        main(sys.argv[1])
