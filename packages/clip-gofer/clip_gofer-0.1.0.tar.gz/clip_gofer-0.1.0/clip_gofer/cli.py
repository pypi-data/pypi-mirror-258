"""Console script for clip_gofer."""

import fire


def help() -> None:
    print("clip_gofer")
    print("=" * len("clip_gofer"))
    print("easily search through videos using natural language queries")


def main() -> None:
    fire.Fire({"help": help})


if __name__ == "__main__":
    main()  # pragma: no cover
