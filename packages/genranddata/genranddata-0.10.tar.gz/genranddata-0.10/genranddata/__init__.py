import pickle
import random
import sys
from typing import Union


def create_random_data(
    fu: callable, data: Union[list, tuple], created_already: list, limit: int, **kwargs
) -> list:
    r"""
    Generate random data using a given function and input data, while ensuring uniqueness and handling exceptions.

    Parameters:
        fu (callable): The function used to generate new data.
        data (Union[list, tuple]): The input data to be used in the generation process.
        created_already (list): A list of data that has already been created.
        limit (int): The maximum number of new data to be generated.
        **kwargs: Additional keyword arguments to be passed to the function.

    Returns:
        list: A list of randomly generated data, with a length not exceeding the specified limit.
    """
    newdatafiltered = []
    ndata = list(map(str, data))
    while len(newdatafiltered) < limit:
        try:
            newdata = fu(ndata, **kwargs)
            if newdata not in created_already:
                created_already.append(newdata)
                newdatafiltered.append(newdata)
                if len(newdatafiltered) >= limit:
                    break
        except Exception as e:
            sys.stderr.write(f"{e}\n")
            sys.stderr.flush()
            continue
    return newdatafiltered


def save_data(data: list, filename: str) -> None:
    r"""
    Save data to a file using pickle.

    Args:
        data (list): The data to be saved.
        filename (str): The name of the file to save the data to.

    Returns:
        None
    """
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_data(filename: str) -> list:
    r"""
    Load data from the specified file using pickle and return the loaded data as a list.

    Parameters:
        filename (str): The name of the file to load data from.

    Returns:
        list: The loaded data as a list.
    """
    with open(filename, "rb") as f:
        data = f.read()
    return pickle.loads(data)


def get_random_not_repeating_values(l: list, howmany: int) -> list:
    r"""
    Generate a list of random non-repeating values from the given list.

    Args:
        l (list): The input list of values.
        howmany (int): The number of random non-repeating values to generate.

    Returns:
        list: A list of random non-repeating values.
    """
    resi = []
    resistr = []
    numbers = l
    numbersdi = {f"{repr(x)}{x}": x for x in numbers}
    if (h := len(numbersdi.keys())) < howmany:
        raise ValueError(f"choices: {howmany} / unique: {h}")
    while len(resi) <= howmany - 1:
        [
            (resi.append(numbersdi[g]), resistr.append(g))
            for x in range(len(numbers))
            if len(resi) <= howmany - 1
            and (g := random.choice(tuple(set(numbersdi.keys()) - set(resistr))))
            not in resistr
        ]
    return resi


def get_true_false_percent(percent_true: int = 60) -> bool:
    r"""
    Generate a boolean value based on the given percentage of True and False.

    :param percent_true: The percentage of True to be generated (default is 60).
    :type percent_true: int
    :return: A boolean value based on the given percentage.
    :rtype: bool
    """
    return random.choices([True, False], [percent_true, 100 - percent_true])[0]


def genfunction(
    data: list,
    min_: int = 1,
    max_: int = 3,
    camel_case_percentage: int = 0,
    uppercase_percentage: int = 0,
    lowercase_percentage: int = 0,
    join_values: Union[list, tuple] = ("x", "_"),
    random_number_percentage: int = 0,
    random_number_range: Union[list, tuple] = (0, 100),
) -> str:
    r"""
    Generates a string by randomly choosing values from the input data list and
    formatting them based on the provided percentages and options.

    Args:
        data (list): The list of values to choose from.
        min_ (int): The minimum number of values to choose.
        max_ (int): The maximum number of values to choose.
        camel_case_percentage (int): The percentage of values to format in camel case.
        uppercase_percentage (int): The percentage of values to format in uppercase.
        lowercase_percentage (int): The percentage of values to format in lowercase.
        join_values (Union[list, tuple]): The list or tuple of strings to choose from when joining the selected values.
        random_number_percentage (int): The percentage chance of adding a random number at the end of the generated string.
        random_number_range (Union[list, tuple]): The range of random numbers to choose from when adding a random number at the end.

    Returns:
        str: The generated string.
    """
    number_of_values = random.randint(min_, max_)
    chosen_vals = get_random_not_repeating_values(data, number_of_values)
    choose_format = []
    normal = 100 - camel_case_percentage - uppercase_percentage - lowercase_percentage
    if normal < 0:
        normal = 0
    choose_format_vals = [
        normal,
        camel_case_percentage,
        uppercase_percentage,
        lowercase_percentage,
    ]
    for ini, val in enumerate(choose_format_vals):
        for x in range(val):
            choose_format.append(ini)
    chosen_format = random.choice(choose_format)
    chosen_vals_formated = []
    for v in chosen_vals:
        if chosen_format == 1:
            chosen_vals_formated.append(v.lower().title())
        elif chosen_format == 2:
            chosen_vals_formated.append(v.upper())
        elif chosen_format == 3:
            chosen_vals_formated.append(v.lower())
        else:
            chosen_vals_formated.append(v)

    joinval = random.choice(join_values)
    joinedstring = joinval.join(chosen_vals_formated)
    if random_number_percentage > 0:
        if get_true_false_percent(percent_true=random_number_percentage):
            joinedstring = f"{joinedstring}{joinval}{random.randint(random_number_range[0],random_number_range[1])}"
    return joinedstring

