from pathlib import Path
import re


ROOT = Path(".")


def find_matching_folders(root_path):
    pattern = r"^\d{2}-[a-zA-Z]+$"
    matching_folders = []

    for item in root_path.iterdir():
        if item.is_dir() and re.match(pattern, item.name):
            matching_folders.append(item)

    return matching_folders


def find_month_folders(path):
    """
    Find all the month folders in format of 2 digit numbers
    """
    pattern = r"^\d{2}$"
    month_folders = []

    for item in path.iterdir():
        if item.is_dir() and re.match(pattern, item.name):
            month_folders.append(item)

    return sorted(month_folders)


def find_day_folder(path):
    days = []
    for day in path.glob("*.md"):
        if day.stem != "README":
            days.append(day.stem)
    return days


matching_folders = find_matching_folders(ROOT)

for folder in matching_folders:
    year_path = ROOT / folder
    month_found = []
    for month_folder in find_month_folders(year_path):
        print(f"compile month: {month_folder}")
        month_number = month_folder.name
        month_found.append(f"Month [{month_number}]({month_number})")

        # Write the README for this year
    readme_path = year_path / "README.md"
    with open(readme_path, "w") as f:
        f.write(f"# {folder.name}\n\n")
        f.write("## Months\n\n")
        for month in month_found:
            f.write(f"- {month}\n")

    for month_path in find_month_folders(year_path):
        month = month_path.name
        month_readme = month_path / "README.md"
        with open(month_readme, "w") as f:
            print(f"Write month readme {folder} - {month}")
            f.write(f"# {folder} - {month}\n\n")
            for day in find_day_folder(month_path):
                f.write(f"* [{day}]({day})\n")

    print(f"README.md under {year_path}: {readme_path}")
