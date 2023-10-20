def compute_elo(
    battles: list,
    ratings: dict[str, dict[str, float]],
    k: int = 4,
    scale: int = 400,
    base: int = 10,
    elo_key: str = "rating_1",
) -> dict[str, dict[str, float]]:
    """Compute elo ratings for a set of battles and ratings. Use elo_key to select which results to use"""
    # Ratings := {"model_name": {"rating_1": 1000, "rating_2": 1000}}
    # Compute elo ratings
    for model_a, model_b, winner, _judge in battles:
        ra = ratings[model_a][elo_key]
        rb = ratings[model_b][elo_key]

        ea = 1 / (1 + base ** ((rb - ra) / scale))
        eb = 1 / (1 + base ** ((ra - rb) / scale))

        if winner == 1:
            sa = 1.0
        elif winner == 2:
            sa = 0.0
        elif winner == 0:
            sa = 0.5
        else:
            raise Exception(f"unexpected vote {winner}")

        ra += k * (sa - ea)
        rb += k * (1 - sa - eb)

        ratings[model_a][elo_key] = ra
        ratings[model_b][elo_key] = rb

    return ratings
