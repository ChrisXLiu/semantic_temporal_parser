Prerequisite: Retrieve and store OpenAI API KEY in `.env` file.

Program entry point: `semantic_parser.py`

Key Abstractions:
- `IParser`:
  `parse(today: str, utterance: str) -> str|None`
- `IStrategy`:
  `run(today: str, utterance: str, parsers: List<IParser>) -> str|None`
