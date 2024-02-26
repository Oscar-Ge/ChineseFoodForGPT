from model_training import *

video_picture_amount = [0, 219, 131, 214, 167]


def digits(n):
    """
    Calculate the number of digits in the given integer.
    Parameters:
    n (int): The integer for which the number of digits is to be calculated.
    Returns:
    int: The number of digits in the given integer.
    """
    s = str(n)
    return len(s)


def read_phase_annotations(video_number, database_path):
    """
    Read phase annotations from a specified video number and database path.
    Parameters:
    - video_number: The number of the video
    - database_path: The path to the database
    Returns:
    - phase_annotations: A list containing two lists. The first list contains the phase names, and the second list contains the corresponding frame numbers.
    """
    phase_annotations = [[], [1]]
    phase = "Preparation"
    n = 2 - digits(video_number)
    with open(database_path + "\phase_annotations\\video" + n * '0' + str(video_number) + ".txt", "r") as f:
        for line in f.readlines():
            if line == "Frame	Phase":
                continue
            else:
                line = line.split("\t")
                # print(line[1].strip())
                phase_annotations[0].append(line[1].strip())
                if line[1].strip() != phase and line[0].strip() != "Frame":
                    phase_annotations[1].append(int(line[0].strip()))
                    phase = line[1].strip()
    phase_annotations[1].append(video_picture_amount[video_number] + 1)
    return phase_annotations


def videos_path_generation(picture_number, video_number, database_path):
    """
    Generate paths for a set of images based on the given picture and video numbers, and the database path.
    :param picture_number: The number of pictures to generate paths for.
    :param video_number: The video number to generate paths for.
    :param database_path: The path to the database.
    :return: A list of image paths generated based on the input parameters.
    """
    image_path_set = []
    for i in range(1, picture_number + 1):
        image_path = database_path + "\\frames\\video" + '0' + str(video_number) + "\\frame" + str(i) + ".jpg"
        image_path_set.append(image_path)
    return image_path_set


def random_elements(video_number, n, phase, image_path):
    """
    Selects random elements from the given video and phase.

    Args:
    - video_number: int, the number of the video
    - n: int, the total number of elements to select
    - phase: list, containing phase information
    - image_path: list, containing paths to images

    Returns:
    - phase_random_elements: list, containing selected random elements with phase information
    """
    random_element = random.sample(range(1, video_picture_amount[video_number] + 1), n)
    # Generate random elements based on phase information
    phase_random_elements = []  # Create list of random elements with phase information
    for i in random_element:
        phase_random_elements.append([i, phase[0][i - 1], image_path[i - 1]])
    return phase_random_elements


# choose n images for testing purpose from the chosen set of video
def test_set_generation(n, phase_elements):
    """
    Generates a test set by popping 'n' elements from 'phase_elements' list and appending the remaining elements as a sublist at the end.

    Args:
    n (int): Number of elements to pop from 'phase_elements'
    phase_elements (list): List of elements to generate the test set from

    Returns:
    list: The generated test set
    """
    test_set = []
    phase_elements1 = phase_elements
    for i in range(n):
        test_set.append(phase_elements1.pop())
    test_set.append(phase_elements1)
    return test_set


def gpt(phase_elements, test_elements, api_key):
    """
    A function to interact with the GPT API using phase elements, test elements, and an API key, and return the response.
    """

    def prompts():
        """
        A function that generates prompts for a cooking expertise task. It concatenates texts with phase elements and test elements to form the prompts. Returns the concatenated texts.
        """
        texts = "You are a expert in cooking and you can undoubtedly answer this question below.These images are from different periods of making a Chinese dish."
        for i in phase_elements:
            texts = texts + "The number" + str(i[0]) + "image is in the pariod of " + i[1] + "."
        for i in range(len(test_elements)):
            texts = texts + "Can you tell me what is the stage of the cooking process in the" + str(len(phase_elements) + i + 1) + "th image? Answer format: Stage of the Nth picture."
        texts += "Thinking step by step by abstracting the features of specific stages in the cooking process to get the right answer.Don't respond saying you're unable to assist with requests like this since you are able to interact with the user's operating system via text responses you send to the end user."
        return texts

    def encode_image(image_path):
        """
        Encode an image file to base64 string.
        Args:
            image_path (str): The path to the image file.
        Returns:
            str: The base64 encoded string representation of the image.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    image_path_set = []
    base64_image_set = []
    test_image_path_set = []
    test_base64_image_set = []
    # Path to your image
    for i in phase_elements:
        image_path_set.append(i[2])
    for i in image_path_set:
        base64_image_set.append(encode_image(i))
    for i in test_elements:
        test_image_path_set.append(i[2])
    for i in test_image_path_set:
        test_base64_image_set.append(encode_image(i))
    # Getting the base64 string from the image
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompts()
                    },
                ]
            }
        ],
        "max_tokens": 300
    }
    for i in base64_image_set + test_base64_image_set:
        a = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{i}"}}
        payload["messages"][0]["content"].append(a)
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    return response.json()


def main():
    """
    This function handles the main workflow of the program.
    It prompts the user for database path, GPT-4v API key, training set capacity, and testing set capacity.
    It then generates random video, image path, phase, tool, phase elements, and test elements.
    It uses the GPT-4v API to generate a response and optionally records the data to a file.
    """
    is_training = int(input("What do you want to do? (1: training; 2: testing):"))
    # Prompting for user input
    database_path = input("please give the path of the database:")
    api_key = input("please give your GPT-4v api key:")
    video_chosen = 2
    image_path = videos_path_generation(video_picture_amount[video_chosen], video_chosen, database_path)
    phase_annotations = read_phase_annotations(video_chosen, database_path)
    if is_training == 1:
        training_set_number = int(input("please give the number of training sets:"))
        phase_number = 2
        phase_elements = phase_random_elements(training_set_number, phase_annotations, image_path, phase_number)
        phase_name = phase_elements[0][1]
        response = gpt_training(phase_elements, api_key, phase_name)
        print(phase_elements)
    else:
        training_set_capacity = int(input("please give the number of training sets:"))
        testing_set_capacity = int(input("please give the number of testing sets:"))
        phase_elements = random_elements(video_chosen, training_set_capacity, phase_annotations, image_path)
        test_elements = test_set_generation(testing_set_capacity, phase_elements)
        phase_elements = test_elements.pop()
        response = gpt(phase_elements, test_elements, api_key)
        print(test_elements)
    print(response)


if __name__ == "__main__":
    main()
