#!/usr/bin/env python3
"""Entry point for LocalAI Studio."""

import sys

from localai_studio.app import LocalAIStudioApp


def main() -> int:
    app = LocalAIStudioApp(sys.argv)
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
