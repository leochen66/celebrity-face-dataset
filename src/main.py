import argparse
import os

from src.list_generator.list_generator import list_generator
from src.image_generator.image_generator import image_generator


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    lists_dir = os.path.join(os.path.dirname(current_dir), "lists")
    images_dir = os.path.join(os.path.dirname(current_dir), "datasets")

    parser = argparse.ArgumentParser(
        description="Command line tool for generating lists or images."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Subcommands: 'list' or 'image'"
    )

    # Subcommand for 'list'
    list_parser = subparsers.add_parser("list", help="Generate a list")
    list_parser.add_argument(
        "-c", "--category", type=str, required=True, help="Specify the category"
    )
    list_parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=100,
        help="Specify the number of persons (default: 100)",
    )

    # Subcommand for 'image'
    image_parser = subparsers.add_parser("image", help="Generate images")
    image_parser.add_argument(
        "-c", "--category", type=str, required=True, help="Specify the category"
    )
    image_parser.add_argument(
        "-n",
        "--number",
        type=int,
        default=50,
        help="Specify the number of persons (default: 50)",
    )

    args = parser.parse_args()

    if args.command == "list":
        list_generator(args.category, args.number, lists_dir)
    elif args.command == "image":
        image_generator(args.category, args.number, lists_dir, images_dir)


if __name__ == "__main__":
    main()
