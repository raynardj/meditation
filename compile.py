from pathlib import Path
import re


ROOT = Path(".")


def find_year_folders(root_path):
    pattern = r"^\d{2}-[a-zA-Z]+$"
    matching_folders = []

    for item in root_path.iterdir():
        if item.is_dir() and re.match(pattern, item.name):
            matching_folders.append(item)

    return sorted(matching_folders)


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
    for day in sorted(list(path.glob("*.md"))):
        if day.stem != "README":
            days.append(day.stem)
    return days


matching_folders = find_year_folders(ROOT)

YEARS = {
    "01-jiachen": "2024 甲辰年",
}

# Year by year
years = []
for year_slug in matching_folders:
    year_name = YEARS[str(year_slug)]
    year_path = ROOT / year_slug
    print(f"year: {year_slug} {year_name}")
    years.append([year_name, year_slug])

    readme_path = year_path / "README.md"
    print(f"README.md under {year_path}: {readme_path}")
    with open(readme_path, "w") as f:
        f.write(f"# {year_slug} {year_name}\n\n")
        f.write("## Months\n\n")

        # Month by month
        for month_path in find_month_folders(year_path):
            f.write(f"- {month_path.name}\n")
            print(f"compile month: {month_path}")
            month_number = month_path.name
            f.write(f"🗓️ [{month_number}]({month_number})\n")

            month_name = month_path.name
            month_readme = month_path / "README.md"
            with open(month_readme, "w") as mf:
                print(f"Write month readme {year_slug} {year_name} - {month_name}")
                mf.write(f"# {year_slug} - {month_name}\n\n")

                # Day by day
                for day in find_day_folder(month_path):
                    mf.write(f"* [{day}]({day})\n")

year_readme_txt = (ROOT / "README.md").read_text()

with open(ROOT / "README.md", "w") as f:
    year_readmes = year_readme_txt.split("<hr>")
    year_readmes[1] = (
        "\n" + "\n".join(list(f"- [{year_name} {year_slug}]({year_slug})" for year_name, year_slug in years)) + "\n"
    )
    f.write("<hr>".join(year_readmes))
