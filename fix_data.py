import re

# muutetaan ensin pilkut hakasulkeiden sisältä jotta saadaan putsattu tiedosto joka voidaan
# jakaa kolumneihin pilkun mukaan

def fix_commas_inside_brackets(line):
    return re.sub(r"\[(.*?)\]", lambda m: m.group(0).replace(",", ";"), line)

with open(r"C:\Users\jasmi\Downloads\Labrat_tietokanta.csv", encoding="latin1") as f:
    fixed_lines = [fix_commas_inside_brackets(line) for line in f]

# luodaan uusi tiedosto fixed.csv
with open("fixed.csv", "w", encoding="utf-8") as f:
    f.writelines(fixed_lines)