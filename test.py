import random
from datetime import datetime, timedelta
import json

def get_random_date(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date

def load_highscore(filename="highscore.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"highscore": float('inf'), "date": ""}

def save_highscore(highscore, filename="highscore.json"):
    with open(filename, "w") as file:
        json.dump(highscore, file)

def save_highscore_history(highscore_data, filename="highscore_history.json"):
    try:
        with open(filename, "r") as file:
            history = json.load(file)
    except FileNotFoundError:
        history = []
    history.append(highscore_data)
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)

def main():
    # Dictionary to map user input to full day names
    day_map = {
        "m": "Monday",
        "tu": "Tuesday",
        "w": "Wednesday",
        "th": "Thursday",
        "f": "Friday",
        "sa": "Saturday",
        "su": "Sunday"
    }

    year = 2024
    total_time = 0
    correct_answers = 0
    input("Press Enter to start the game...")

    for i in range(10):
        random_date = get_random_date(year)
        print(f"What day of the week was {random_date.strftime('%B %d, %Y')}?")

        start_time = datetime.now()
        user_input = input("Enter the day of the week (m, tu, w, th, f, sa, su): ").strip().lower()
        end_time = datetime.now()
        
        response_time = end_time - start_time
        total_time += response_time.total_seconds()

        correct_day = random_date.strftime('%A')
        user_day = day_map.get(user_input)

        if user_day and user_day.lower() == correct_day.lower():
            correct_answers += 1
            print("Correct!\n\n")
        else:
            print(f"Wrong! The correct answer is {correct_day}.")
            break  # Exit the loop if the answer is wrong
    
        print(f"Your response time for this round was {response_time.total_seconds()} seconds.")

    if correct_answers == 10:
        average_time = total_time / 10
        print(f"\nYour average response time was {average_time:.2f} seconds.")
        print(f"You got {correct_answers} out of 10 correct answers.")

        # Load the current highscore
        highscore_data = load_highscore()
        highscore = highscore_data["highscore"]

        # Check if the current average time is a new highscore
        if average_time < highscore:
            highscore_data = {
                "highscore": average_time,
                "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            save_highscore(highscore_data)
            save_highscore_history(highscore_data)
            print("Congratulations! You've set a new highscore!")
        else:
            print(f"The current highscore is {highscore:.2f} seconds, set on {highscore_data['date']}.")
    else:
        print("You did not answer all questions correctly. Try again to set a highscore.")

if __name__ == "__main__":
    main()
