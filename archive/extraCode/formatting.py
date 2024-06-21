import os

def rename(directory):

    for filename in os.listdir(directory):
        n = int(filename[1:filename.find('i')])
        i = int(filename[filename.find('i')+1:filename.find('e')])

        with open(f'{directory}/{filename}', 'r') as file:
            data = file.read()

        with open(
                f'{directory}/n{n}i{i}.txt', 'w+'
            ) as file:
                file.write(str(data))

rename('data/IonQHarmonySimulator')