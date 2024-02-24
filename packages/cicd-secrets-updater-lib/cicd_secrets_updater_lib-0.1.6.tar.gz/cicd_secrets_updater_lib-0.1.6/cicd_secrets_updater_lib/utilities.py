import re
import subprocess


def levenshtein_distance(a, b):
    """
    Calculate the Levenshtein distance between two strings
    :param a: The first string
    :param b: The second string
    :return: The Levenshtein distance between the two strings
    """

    if len(a) > len(b):
        a, b = b, a

    distances = range(len(a) + 1)
    for index2, char2 in enumerate(b):
        new_distances = [index2 + 1]

        for index1, char1 in enumerate(a):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))

        distances = new_distances

    return distances[-1]


def update_content_with_secrets(content, secrets):
    """
    Update content with the encrypted secrets, ensuring correct indentation.
    :param content: The content to update
    :param secrets: The secrets to update the content with
    """
    # Splitting the content into lines for easier manipulation
    lines = content.split('\n')
    updated_lines = []
    keys_found = set()

    # Process each line to check if it contains any of the secrets keys
    for line in lines:
        for key in secrets:
            if re.match(rf"\s*{key}:", line):
                # Update the line with the new value, maintaining original indentation
                indent = len(line) - len(line.lstrip())
                updated_lines.append(f"{' ' * indent}{key}: {secrets[key]}")
                keys_found.add(key)
                break
        else:
            # If no key is found to update, keep the line as is
            updated_lines.append(line)

    # Add any missing keys at the end under the correct section
    if len(keys_found) < len(secrets):
        # Assuming all keys belong under 'config:', find where to insert them
        config_index = -1
        for i, line in enumerate(updated_lines):
            if re.match(r"\s*config:", line):
                config_index = i
                break
        if config_index != -1:
            for key, value in secrets.items():
                if key not in keys_found:
                    # Add the missing key-value pairs with correct indentation (8 spaces)
                    updated_lines.insert(config_index + 1, f"        {key}: {value}")

    return '\n'.join(updated_lines)


def execute_command(command):
    subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
