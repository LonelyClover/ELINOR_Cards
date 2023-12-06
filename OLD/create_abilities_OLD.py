import csv, subprocess

with open("files/abilities.csv", "r", encoding="utf-8") as table:
    reader = csv.reader(table)

    levels = next(reader)

    for row in reader:
        for i, text in enumerate(row):
            if i == 0 or text == "" or text[0] == '#':
                continue

            lines = text.split('\n')
            
            ability_name = lines[0]
            ability_text = lines[1]
            ability_level = levels[i]

            with open("files/text.txt", "w", encoding="utf-8") as f:
                f.write(ability_name)
                f.write('\n')

                f.write("Навык")
                f.write('\n')

                f.write(ability_level)
                f.write('\n')

                f.write(ability_text)

            p1 = subprocess.Popen(["python", "create_card.py"],
                                 stdin=subprocess.PIPE)
            p1.communicate(b"2\n2\n")

