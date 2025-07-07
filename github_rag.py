def get_context_from_github(query: str) -> list:
    # Stub: you could use FAISS here with your indexed GitHub docs
    return [
        "To deploy the agent, use docker-compose up after pulling the latest model.",
        "Make sure the .env file contains your Slack token and GitHub PAT."
    ]
