from scipy.optimize import minimize, dual_annealing
import numpy as np
from volstreet import (
    BackTester,
    UnderlyingInfo,
    logger,
)
import pandas as pd
import numpy as np


def generate_constraints(
    deltas: np.ndarray, max_delta: float, min_delta: float = 0.05, full=True
):
    constraints = [
        {"type": "eq", "fun": lambda x: sum(x)},
        {"type": "ineq", "fun": lambda x: -np.dot(x, deltas) - min_delta},
        {"type": "ineq", "fun": lambda x: np.dot(x, deltas) + max_delta},
        {"type": "ineq", "fun": lambda x: 2 - sum(abs(x))},
        {"type": "ineq", "fun": lambda x: sum(abs(x)) - 1.99},
        {"type": "ineq", "fun": lambda x: min(abs(x)) - 0.01},
    ]
    return constraints if full else constraints[-1]


def generate_x0_and_bounds(n: int):
    x0 = np.zeros(n)
    bounds = [(-1, 1) for _ in range(n)]
    return x0, bounds


def calculate_penalty(deviation: float, weight: float = 1000):
    return (weight ** abs(deviation)) - 1


def normalize_array(arr):
    min_val = np.min(arr)
    max_val = np.max(arr)
    return (arr - min_val) / (max_val - min_val)


def scale_back_to_original(arr, original_arr):
    min_val = np.min(original_arr)
    max_val = np.max(original_arr)
    return arr * (max_val - min_val) + min_val


def basic_objective(x, deltas, gammas):
    # Objective: maximize delta minus gamma
    total_delta = np.dot(x, deltas)
    total_gamma = np.dot(x, gammas)
    return total_delta - total_gamma


def penalty_objective(
    x,
    deltas,
    gammas,
    target_delta,
    normalized=False,
    gamma_weight=10,
    original_deltas=None,
):
    # Objective: maximize delta minus gamma
    total_delta = np.dot(x, deltas)
    total_gamma = np.dot(x, gammas)

    # Penalty functions
    penalty = 0

    # Complete hedge penalty
    diff_from_zero = abs(sum(x))
    penalty += calculate_penalty(diff_from_zero)

    # Delta penalty
    _total_delta = np.dot(x, original_deltas) if normalized else total_delta
    diff_from_target = -_total_delta - target_delta
    penalty += calculate_penalty(diff_from_target)

    # Total quantity penalty
    diff_from_two = sum(abs(x)) - 2
    penalty += calculate_penalty(diff_from_two)

    return total_delta - (gamma_weight * total_gamma) + penalty


def optimize_leg_v1(
    deltas: np.ndarray,
    gammas: np.ndarray,
    min_delta: float,
    max_delta: float,
    gamma_scaler=1,
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

    deltas = abs(deltas)
    gammas = gammas * gamma_scaler

    def objective(x):
        return basic_objective(x, deltas, gammas)

    # Constraints: total quantity is 1 and total delta equals target delta
    constraints = generate_constraints(deltas, max_delta, min_delta)

    x0, bounds = generate_x0_and_bounds(len(deltas))

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000},
    )
    return result


def optimize_leg_v2(
    deltas: np.ndarray,
    gammas: np.ndarray,
    target_delta: float,
):
    """ "Using normalized values"""
    deltas = abs(deltas)

    normalized_deltas = normalize_array(deltas)
    normalized_gammas = normalize_array(gammas)

    def objective(x):
        return penalty_objective(
            x,
            normalized_deltas,
            normalized_gammas,
            target_delta,
            normalized=True,
            gamma_weight=1,
            original_deltas=deltas,
        )

    constraints = generate_constraints(deltas, target_delta, full=False)

    x0, bounds = generate_x0_and_bounds(len(deltas))

    result = minimize(
        objective,
        x0,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={"maxiter": 1000},
    )
    return result


def optimize_leg_global(
    deltas: np.ndarray,
    gammas: np.ndarray,
    target_delta: float,
):
    """
    Designed to be used with the global optimization algorithm. Since constraints are not supported,
    we will use a penalty function to enforce the constraints. The major constaints are that the total
    quantity should be 0 (complete hedge) and the delta should be very very close to the target delta.
    Lastly, the absolute total quantity should be less than very very close to 2.
    """
    deltas = abs(deltas)

    normalized_deltas = normalize_array(deltas)
    normalized_gammas = normalize_array(gammas)

    def objective(x):
        return penalty_objective(
            x,
            normalized_deltas,
            normalized_gammas,
            target_delta,
            normalized=True,
            gamma_weight=1,
            original_deltas=deltas,
        )

    x0, bounds = generate_x0_and_bounds(len(deltas))

    result = dual_annealing(
        objective,
        bounds=bounds,
        x0=x0,
        maxiter=15000,
        seed=42,
    )
    return result


# %%
if __name__ == "__main__":
    delta_target = 0.1
    bt = BackTester()

    data_dump = {}
    start_dates = {
        "NIFTY": "2021-01-01",
        "BANKNIFTY": "2021-01-01",
        "FINNIFTY": "2023-01-01",
        "MIDCPNIFTY": "2023-10-01",
    }
    for index in ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"]:
        data_dump[index] = []
        ui = UnderlyingInfo(index)
        expiries = ui.expiry_dates
        start_date = start_dates[index]
        expiries = expiries[expiries < "2024-02-20"]
        expiries = expiries[expiries > start_date]

        times = ["9:17", "10:00" "11:00", "12:00", "13:00", "14:40"]

        for expiry in expiries:
            for time in times:
                timestamp = f"{pd.to_datetime(expiry).strftime('%Y-%m-%d')} {time}"

                try:
                    option_chain = bt.build_option_chain(
                        ui,
                        timestamp,
                        timestamp,
                        num_strikes=30,
                        threshold_days_expiry=0,
                        add_greeks=True,
                    )
                    call_data = option_chain.loc[
                        option_chain["call_delta"] < 0.58,
                        ["strike", "call_price", "call_delta", "call_gamma"],
                    ]
                    call_data_array = call_data.values

                    put_data = option_chain.loc[
                        option_chain["put_delta"] > -0.58,
                        ["strike", "put_price", "put_delta", "put_gamma"],
                    ]
                    put_data_array = put_data.values

                    for gamma_scaler in [1, 10, 20, 40, 60, 80, 100]:
                        call_result = optimize_leg_v1(
                            call_data_array[:, 2],
                            call_data_array[:, 3],
                            0.05,
                            delta_target,
                            80,
                        )

                        put_result = optimize_leg_v1(
                            put_data_array[:, 2],
                            put_data_array[:, 3],
                            0.05,
                            delta_target,
                            80,
                        )

                        # call_result = optimize_leg_v2(
                        #     call_data_array[:, 2], call_data_array[:, 3], delta_target
                        # )
                        #
                        # put_result = optimize_leg_v2(
                        #     put_data_array[:, 2], put_data_array[:, 3], delta_target
                        # )

                        # Adding the result to the dataframe
                        call_data["optimized_quantity"] = call_result.x
                        put_data["optimized_quantity"] = put_result.x

                        optimized_call_delta = np.dot(
                            call_data["optimized_quantity"], call_data["call_delta"]
                        )
                        optimized_call_gamma = np.dot(
                            call_data["optimized_quantity"], call_data["call_gamma"]
                        )
                        optimized_put_delta = np.dot(
                            put_data["optimized_quantity"], put_data["put_delta"]
                        )
                        optimized_put_gamma = np.dot(
                            put_data["optimized_quantity"], put_data["put_gamma"]
                        )
                        optimized_call_premium = np.dot(
                            call_data["optimized_quantity"], call_data["call_price"]
                        )
                        optimized_put_premium = np.dot(
                            put_data["optimized_quantity"], put_data["put_price"]
                        )

                        optimized_portfolio_delta = (
                            optimized_call_delta + optimized_put_delta
                        )
                        optimized_portfolio_gamma = (
                            optimized_call_gamma + optimized_put_gamma
                        )
                        optimized_portfolio_premium = (
                            optimized_call_premium + optimized_put_premium
                        )

                        data = {
                            "timestamp": timestamp,
                            "call_result": call_result,
                            "put_result": put_result,
                            "call_data": call_data,
                            "put_data": put_data,
                            "optimized_call_delta": optimized_call_delta,
                            "optimized_call_gamma": optimized_call_gamma,
                            "optimized_put_delta": optimized_put_delta,
                            "optimized_put_gamma": optimized_put_gamma,
                            "optimized_call_premium": optimized_call_premium,
                            "optimized_put_premium": optimized_put_premium,
                            "optimized_portfolio_delta": optimized_portfolio_delta,
                            "optimized_portfolio_gamma": optimized_portfolio_gamma,
                            "optimized_portfolio_premium": optimized_portfolio_premium,
                            "gamma_scaler": gamma_scaler,
                        }

                        data_dump[index].append(data)
                except Exception as e:
                    logger.error(f"Error for {index} and {timestamp}: {e}")
                    continue
