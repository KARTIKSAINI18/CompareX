from app.services.query_planner import QueryPlanner


def main():
    planner = QueryPlanner()

    queries = [
        "Which smartphone has the largest battery?",
        "Which phone has the most RAM?",
        "Which phone has the highest rating?",
        "Which phone is the cheapest?",
        "Compare Samsung and OnePlus phones",
        "Recommend a phone with a good camera",
        "Show me smartphones with large batteries",
    ]

    for query in queries:
        result = planner.plan(query)

        print()
        print("=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)
        print(result.model_dump())


if __name__ == "__main__":
    main()