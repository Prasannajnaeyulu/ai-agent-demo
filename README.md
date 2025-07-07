# ai-agent-demo

This project responds to messages in a Slack channel by automatically fetching relevant context from GitHub issues or the repository's README. It leverages the Gemma 1B model running on Ollama for natural language understanding and response generation.

## Features

- Monitors a Slack channel for new messages.
- Retrieves and summarizes context from GitHub issues and the README file.
- Uses the Gemma 1B language model (served via Ollama) for AI-powered replies.

## How It Works

1. Listens for messages in a specified Slack channel.
2. Analyzes each message to determine if context is needed from GitHub.
3. Fetches relevant issue discussions or extracts information from the README.
4. Generates a response using the Gemma 1B model.

## Requirements

- Slack API credentials (for bot integration).
- Access to the GitHub repository you want to query.
- Ollama installed and configured to serve the Gemma 1B model.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/Prasannajnaeyulu/ai-agent-demo.git
    cd ai-agent-demo
    ```
2. Install dependencies:
    ```bash
    # Add your specific installation instructions here (e.g., npm install, pip install -r requirements.txt)
    ```
3. Set up your environment variables for Slack and GitHub API access.
4. Start Ollama and ensure the Gemma 1B model is running:
    ```bash
    ollama run gemma:1b
    ```
5. Run the application:
    ```bash
    # Provide your project-specific start command here
    ```

## Usage

- Add your bot to the desired Slack channel.
- Ask questions or mention GitHub issues in Slack.
- The bot will reply with contextually relevant answers, pulling information from GitHub as needed.
  
**Examples:**
#1 ![image](https://github.com/user-attachments/assets/8918364c-03bd-4736-9dc3-5626757270a3)
#2 <img width="1438" alt="image" src="https://github.com/user-attachments/assets/c2960e97-3579-4107-b85c-480767d4a6b8" />
#3 <img width="1396" alt="image" src="https://github.com/user-attachments/assets/0d6d422d-9bd0-45f2-ac4a-128501ab8dd1" />



## Technologies Used

- Slack API
- GitHub API
- Ollama (for LLM serving)
- Gemma 1B language model

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

[MIT](LICENSE)
