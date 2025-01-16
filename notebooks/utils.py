import pandas as pd
import plotly.express as px


def get_best_worst_malls(data, metric):
    data.sort_values(by=metric, ascending=False, inplace=True)
    best_malls = data.copy().head(5)
    worst_malls = data.copy().tail(5)
    return best_malls, worst_malls


def plot_best_worst_malls_mix(
    store_data, best_malls_data, worst_malls_data, metric, title
):
    best_malls_sales_stores = store_data[
        store_data["mall_id"].isin(best_malls_data["mall_id"])
    ]
    worst_malls_stores = store_data[
        store_data["mall_id"].isin(worst_malls_data["mall_id"])
    ]

    best_malls_branch_count = (
        best_malls_sales_stores["store_branch_level_1"]
        .value_counts(normalize=True)
        .reset_index()
    )
    best_malls_branch_count.columns = ["store_branch_level_1", "count"]

    worst_malls_branch_count = (
        worst_malls_stores["store_branch_level_1"]
        .value_counts(normalize=True)
        .reset_index()
    )
    worst_malls_branch_count.columns = ["store_branch_level_1", "count"]

    best_malls_branch_count = best_malls_branch_count.head(4)
    worst_malls_branch_count = worst_malls_branch_count[
        worst_malls_branch_count["store_branch_level_1"].isin(
            best_malls_branch_count["store_branch_level_1"]
        )
    ]

    best_malls_branch_count["Category"] = "Best Malls"
    worst_malls_branch_count["Category"] = "Worst Malls"

    combined_branch_count = pd.concat(
        [best_malls_branch_count, worst_malls_branch_count]
    )

    fig = px.bar(
        combined_branch_count,
        x="store_branch_level_1",
        y="count",
        color="Category",
        barmode="group",
        title=title,
    )
    fig.update_layout(
        xaxis_title="Store category",
        yaxis_title="Fraction of stores",
        xaxis_tickangle=-45,
    )
    fig.update_layout(yaxis_tickformat=".0%")
    return fig
