# Contributing to MongoDB BSON Protocol Enumerator

Thank you for your interest in contributing! We welcome pull requests, ideas, and suggestions to improve this tool.

---

## Requirements

- Python 3.6+
- Basic understanding of MongoDB wire protocol and network sockets

---

## Setup

1. Clone the repository  
   git clone https://github.com/Arismr/MongoDB-BSON-Protocol-Enumerator.git
   cd MongoDB-BSON-Protocol-Enumerator
(Optional) Create a virtual environment

python3 -m venv venv
source venv/bin/activate
Install requirements
There are currently no external requirements.

Contribution Guidelines
1. Fork this repository
Click the "Fork" button in the top-right corner of the GitHub page to create your own copy of the project.

2. Create a new branch
git checkout -b your-feature-name
3. Make your changes
Keep code clean and readable

Include minimal but meaningful comments

Follow Python naming conventions (PEP8)

Keep the script portable and avoid unnecessary dependencies

4. Commit your changes
git add .
git commit -m "Descriptive message about what you changed"
5. Push and open a Pull Request
bash
Copy
Edit
git push origin your-feature-name
Then navigate to your fork on GitHub and click “Compare & Pull Request”.

Code Style
Use 4 spaces for indentation

Avoid large monolithic commits

If adding a new feature, update the README with usage or behavior changes

Respect existing naming and structure conventions in the script

## Adding New Features?
Test new functionality using a real MongoDB server (v3.6+)

Document changes or new capabilities in your pull request description

Update the ASCII banner or version string if applicable

Only add third-party libraries if absolutely necessary and justify their use

## Issues and Discussions
If you're not sure whether something should be added, changed, or fixed — open an issue first. Collaboration and discussion are welcome before diving into development.

## License
By contributing to this project, you agree that your contributions will be licensed under the MIT License — the same license used by the rest of the project.

Thank You
Your input — no matter how small — makes this project better.

Thanks again for helping improve MongoDB BSON Protocol Enumerator!

— Arismr
