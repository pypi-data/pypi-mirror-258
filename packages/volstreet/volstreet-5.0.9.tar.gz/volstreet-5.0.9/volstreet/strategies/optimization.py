from scipy.optimize import minimize
import pandas as pd
from itertools import combinations
import numpy as np
import random
from volstreet import BackTester, UnderlyingInfo, add_greeks_to_dataframe


def optimize_leg(
    deltas: np.ndarray,
    gammas: np.ndarray,
    min_delta: float,
    max_delta: float,
):
    """
    Parameters:
    - deltas: np.ndarray, delta values for each strike.
    - gammas: np.ndarray, gamma values for each strike.
    - min_delta: float, minimum target delta.
    - max_delta: float, maximum target delta.

    Returns:
    - The optimized quantities and the objective value, ensuring the total delta is within the specified range.
    """

    def objective_v1(x):
        # Objective: maximize delta minus gamma
        total_delta = np.dot(x, deltas)
        total_gamma = np.dot(x, gammas)

        target = total_delta - total_gamma

        return target + 0

    def objective_v2(x, eps=1e-6):
        # Objective: maximize delta per unit of gamma
        total_delta = np.dot(x, deltas)  # Will be negative always as we are shorting
        total_gamma = np.dot(x, gammas)
        return -1 * (abs(total_delta) / (abs(total_gamma) + eps))

    # Constraints: total quantity is 1 and total delta equals target delta
    constraints = [
        # Total quantity should be zero - Hedged position
        {"type": "eq", "fun": lambda x: sum(x)},
        # Total delta should be within the specified range
        {
            "type": "ineq",
            "fun": lambda x: -np.dot(x, deltas) - min_delta,
        },  # Minimum delta
        {
            "type": "ineq",
            "fun": lambda x: np.dot(x, deltas) + max_delta,
        },  # Maximum delta
        # The absolute value of total positions should be less than 2
        {"type": "ineq", "fun": lambda x: 2 - sum(abs(x))},
        # The absolute value of total positions should be greater than 1.85
        {"type": "ineq", "fun": lambda x: sum(abs(x)) - 1.99},
        # The minimum quantity of each position should be ...
        {"type": "ineq", "fun": lambda x: min(abs(x)) - 0.02},
    ]

    # Initial guess zeros
    x0 = np.zeros(len(deltas))

    # Bounds: Each quantity should be between 0 and 1
    bounds = [(-1, 1) for _ in range(len(deltas))]

    result = minimize(
        objective_v1,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000},
    )
    return result


# %%
if __name__ == "__main__":
    mode = "sensibull"

    if mode == "historical":
        bt = BackTester()
        option_chain = bt.build_option_chain(
            UnderlyingInfo("NIFTY"),
            "2024-02-15 9:16",
            "2024-02-15 9:16",
            num_strikes=30,
            threshold_days_expiry=0,
        )
        oc_with_greeks = add_greeks_to_dataframe(option_chain)
        oc_with_greeks.sort_values("call_delta", inplace=True)
        oc_with_greeks[["call_gamma", "put_gamma"]] = (
            oc_with_greeks.filter(regex="gamma") * 40
        )

        call_data = oc_with_greeks.loc[
            oc_with_greeks["call_delta"] < 0.55, ["strike", "call_delta", "call_gamma"]
        ]
        call_data_array = call_data.values

        put_data = oc_with_greeks.loc[
            oc_with_greeks["put_delta"] > -0.55, ["strike", "put_delta", "put_gamma"]
        ]
        put_data_array = put_data.values

    elif mode == "sensibull":
        full_data = pd.read_csv("bnf_option_chain.csv")
        full_data.columns = full_data.columns.str.lower().map(
            lambda x: x.replace(" ", "_")
        )
        data = full_data.filter(regex="strike|delta|gamma|ltp")

        # if data is "--" then drop the row
        data = data.replace("--", np.nan).dropna()

        # convert the numeric columns to float, handling the strings with -signs for negative numbers
        data = data.applymap(float)

        call_data = data.loc[
            data["call_delta"] < 0.6, ["strike", "call_ltp", "call_delta", "call_gamma"]
        ]
        call_data_array = call_data.values

        put_data = data.loc[
            data["put_delta"] > -0.6, ["strike", "put_ltp", "put_delta", "put_gamma"]
        ]
        put_data_array = put_data.values

    ### Optimization

    # The target delta value specified
    call_result = optimize_leg(
        call_data_array[:, 2],
        call_data_array[:, 3] * 20,
        0.05,
        0.15,
    )
    put_result = optimize_leg(
        abs(put_data_array[:, 2]),
        put_data_array[:, 3] * 20,
        0.05,
        0.15,
    )
    # Adding the resault to the dataframe
    call_data["optimized_quantity"] = call_result.x
    put_data["optimized_quantity"] = put_result.x

    optimized_call_delta = np.dot(
        call_data["optimized_quantity"], call_data["call_delta"]
    )
    optimized_call_gamma = np.dot(
        call_data["optimized_quantity"], call_data["call_gamma"]
    )

    optimized_put_delta = np.dot(put_data["optimized_quantity"], put_data["put_delta"])
    optimized_put_gamma = np.dot(put_data["optimized_quantity"], put_data["put_gamma"])

    optimized_call_premium = np.dot(
        call_data["optimized_quantity"], call_data["call_ltp"]
    )
    optimized_put_premium = np.dot(put_data["optimized_quantity"], put_data["put_ltp"])

    optimized_portfolio_delta = optimized_call_delta + optimized_put_delta
    optimized_portfolio_gamma = optimized_call_gamma + optimized_put_gamma
    optimized_portfolio_premium = optimized_call_premium + optimized_put_premium
