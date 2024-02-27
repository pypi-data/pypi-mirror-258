# SPDX-FileCopyrightText: 2024 PATHFINDER
#
# SPDX-License-Identifier: Unlicense

from argparse import ArgumentParser
from json import load
from icalendar import Calendar
from icalendar.cal import Todo
from importlib.metadata import version
from datetime import datetime
import os
import re


def main():
    # Constants
    SHORT_ID = "google-tasks-to-ical"
    LONG_ID = f"com.pathfinderdreams.{SHORT_ID}"
    VERSION = version(SHORT_ID)

    # Parse arguments
    parser = ArgumentParser(description="Converts Google Tasks JSON into iCal VTODO")
    parser.add_argument(
        "input_path", metavar="input", help="the input Google Tasks JSON file"
    )
    parser.add_argument(
        "output_path",
        metavar="output",
        nargs="?",
        help="the output folder",
        default="output",
    )
    parser.add_argument(
        "-t",
        "--tags",
        action="store_true",
        help="turn lists into tags (VTODO categories)",
    )
    parser.add_argument(
        "-s",
        "--single",
        action="store_true",
        help="merge all lists into a single iCal file",
    )
    parser.add_argument("-v", "--version", action="version", version=VERSION)
    args = parser.parse_args()

    # Load input file
    input_file = open(args.input_path, "r")
    input_json = load(input_file)

    # Create output folder
    if not os.path.exists(args.output_path):
        os.makedirs(args.output_path)

    # Create single output calendar
    if args.single:
        single_cal = Calendar()
        single_cal.add("prodid", LONG_ID)
        single_cal.add("version", VERSION)

    # For each list, use it as a tag or write it as separated files...
    for todo_list in input_json["items"]:
        todo_list_name = todo_list["title"]

        # If we're writing multiple files, create a new calendar for each list
        if not args.single:
            multi_cal = Calendar()
            multi_cal.add("prodid", LONG_ID)
            multi_cal.add("version", VERSION)

        # For each task in the list...
        for todo in todo_list["items"]:
            ical_todo = Todo()
            ical_todo.add("uid", todo["id"])
            ical_todo.add("summary", todo["title"])
            if args.tags:
                ical_todo.add("categories", todo_list_name)
            if "notes" in todo:
                ical_todo.add("description", todo["notes"])
            if "due" in todo:
                ical_todo.add("due", datetime.fromisoformat(todo["due"]))
            ical_todo.add("last-modified", datetime.fromisoformat(todo["updated"]))
            if "starred" in todo and todo["starred"] is True:
                # In etesync, priority 1 is HIGH while having no priority is
                # UNDEFINED, which is what we want instead of setting it as low
                # priority.
                # https://github.com/etesync/etesync-web/blob/840d95eebecc826fdf3424ff9516e80ca408016b/src/helpers.tsx#L112
                ical_todo.add("priority", 1)
            if "completed" in todo:
                ical_todo.add("completed", datetime.fromisoformat(todo["completed"]))
            ical_todo.add("status", todo["status"].upper())
            (single_cal if args.single else multi_cal).add_component(ical_todo)

        # If we're writing multiple files, write it to the output folder with the list name as the file name
        if not args.single:
            # Sanitise file name
            output_file_name = re.sub(r"[/|\\]", "_", todo_list_name)
            output_file = open(args.output_path + f"/{output_file_name}.ical", "wb")
            output_file.write(multi_cal.to_ical())

    # Create single output file
    if args.single:
        output_file = open(args.output_path + "/single.ical", "wb")
        output_file.write(single_cal.to_ical())


if __name__ == "__main__":
    main()
