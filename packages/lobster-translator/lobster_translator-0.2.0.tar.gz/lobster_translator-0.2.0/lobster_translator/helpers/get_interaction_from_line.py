def get_interaction_from_line(line: str) -> str:
    interaction =  line.split(':')[1].split('->')[0] + line.split(':')[1].split('->')[1].split('(')[0]
    return interaction